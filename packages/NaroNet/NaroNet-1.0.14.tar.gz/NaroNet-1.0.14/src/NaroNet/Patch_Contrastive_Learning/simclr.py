import logging
import os
import sys

import torch
import torch.nn.functional as F
from torch.cuda.amp import GradScaler, autocast
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from NaroNet.Patch_Contrastive_Learning.utils import save_config_file, accuracy, save_checkpoint
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.cluster import AgglomerativeClustering
import gc 
gc.set_threshold(0,0,0)

torch.manual_seed(0)

def visualize_using_clustering(name,features,image_size,patch_size,image):

    # Create patch Image
    Patch_im = np.zeros(image_size)                                
    division_rows = np.floor(Patch_im.shape[0]/patch_size)
    division_cols = np.floor(Patch_im.shape[1]/patch_size)
    lins = np.repeat(list(range(int(division_cols))), patch_size)
    lins = np.repeat(np.expand_dims(lins,axis=1), patch_size, axis=1)
    for row_indx, row in enumerate(range(int(division_rows))):
        Patch_im[row_indx*patch_size:(row_indx+1)*patch_size,:int(division_cols*patch_size)] = np.transpose(lins+int(row_indx*division_cols))    
    Patch_im = Patch_im.astype(int)

    # Cluster into distinct phenotypes
    clustering = AgglomerativeClustering(n_clusters=3).fit(features)
    Cluster_image = clustering.labels_[Patch_im]

    # Save patch Image
    imtosave = Image.fromarray(np.uint16(Patch_im))
    imtosave.save(name+'_PatchIm.png')                

    # Save cluster image
    imtosave = Image.fromarray(np.uint8(Cluster_image))
    imtosave.save(name+'_cluster.png') 

    # Save image    
    imtosave = Image.fromarray(np.uint16((image.squeeze()[:,:,6].numpy()/image.squeeze()[:,:,6].numpy().max())*65550))
    imtosave.save(name+'_image.png')                


class SimCLR(object):

    def __init__(self, *args, **kwargs):
        self.args = kwargs['args']
        self.model = kwargs['model'].to(self.args['PCL_GPU_INDEX'])
        self.optimizer = kwargs['optimizer']
        self.scheduler = kwargs['scheduler']            
        self.model_dir = self.args['path']+'Patch_Contrastive_Learning/Model/'        
        self.writer = SummaryWriter(log_dir=self.model_dir)    
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)  
        logging.basicConfig(filename=os.path.join(self.model_dir, 'training.log'), level=logging.DEBUG)
        self.criterion = torch.nn.CrossEntropyLoss().to(self.args['PCL_GPU_INDEX'])

    def info_nce_loss(self, features):

        labels = torch.cat([torch.arange(features.shape[0]/2) for i in range(2)], dim=0)
        labels = (labels.unsqueeze(0) == labels.unsqueeze(1)).float()
        labels = labels.to(self.args['PCL_GPU_INDEX'])

        features = F.normalize(features, dim=1)

        similarity_matrix = torch.matmul(features, features.T)

        # discard the main diagonal from both: labels and similarities matrix
        mask = torch.eye(labels.shape[0], dtype=torch.bool).to(self.args['PCL_GPU_INDEX'])
        labels = labels[~mask].view(labels.shape[0], -1)
        similarity_matrix = similarity_matrix[~mask].view(similarity_matrix.shape[0], -1)

        # select and combine multiple positives
        positives = similarity_matrix[labels.bool()].view(labels.shape[0], -1)

        # select only the negatives the negatives
        negatives = similarity_matrix[~labels.bool()].view(similarity_matrix.shape[0], -1)

        logits = torch.cat([positives, negatives], dim=1)
        labels = torch.zeros(logits.shape[0], dtype=torch.long).to(self.args['PCL_GPU_INDEX'])

        logits = logits / self.args['PCL_Temperature']
        return logits, labels

    def train(self, train_loader):

        scaler = GradScaler(enabled=True)

        # save config file
        save_config_file(self.writer.log_dir, self.args)

        n_iter = 0
        logging.info(f"Start SimCLR training for {self.args['PCL_Epochs']} epochs.")        

        for epoch_counter in tqdm(range(self.args['PCL_Epochs'])):
            for images in train_loader:
                images[0] = torch.cat(torch.tensor_split(images[0], images[0].shape[0]),1).squeeze()
                images[1] = torch.cat(torch.tensor_split(images[1], images[1].shape[0]),1).squeeze()

                images = torch.cat((images[0],images[1]),dim=0)

                images = images.to(torch.float32)

                images = images.to(self.args['PCL_GPU_INDEX'])

                images = torch.moveaxis(images, 3, 1)

                with autocast(enabled=True):
                    features = self.model(images)
                    logits, labels = self.info_nce_loss(features)
                    loss = self.criterion(logits, labels)
                
                self.optimizer.zero_grad()

                scaler.scale(loss).backward()

                scaler.step(self.optimizer)
                scaler.update()

                # Log info
                top1, top5 = accuracy(logits, labels, topk=(1, 5))
                self.writer.add_scalar('loss', loss, global_step=n_iter)
                self.writer.add_scalar('acc/top1', top1[0], global_step=n_iter)
                self.writer.add_scalar('acc/top5', top5[0], global_step=n_iter)
                self.writer.add_scalar('learning_rate', self.scheduler.get_lr()[0], global_step=n_iter)

                n_iter += 1                
                
                del images, features
                gc.collect(0)
                gc.collect(1)
                gc.collect(2)
                logging.debug(f"Epoch: {epoch_counter}\tLoss: {loss}\tTop1 accuracy: {top1[0]}\tTop5 accuracy: {top5[0]}")

            # warmup for the first 10 epochs
            if epoch_counter >= 6*(self.args['PCL_Epochs']/10):
                self.scheduler.step()
            
            # save model checkpoints
            if epoch_counter % int(self.args['PCL_Epochs']/10) == 0:
                checkpoint_name = 'checkpoint_{:04d}.pth.tar'.format(epoch_counter)
                torch.save(self.model.state_dict(), os.path.join(self.model_dir, checkpoint_name))        
                logging.info(f"Model checkpoint and metadata has been saved at {self.model_dir}.")

        logging.info("Training has finished.")
        

    def infer(self,infer_loader, out_dir):
        
        # Open last saved model checkpoint          
        text_files = [f for f in os.listdir(self.model_dir) if f.endswith('.tar')]
        text_files.sort()
        self.model.load_state_dict(torch.load(os.path.join(self.model_dir, text_files[-1])))
        del self.model.backbone.fc._modules['4']
        del self.model.backbone.fc._modules['3']
        self.model.eval()       

        self.folder = out_dir 

        # Order Images 
        infer_loader.dataset.image_list.sort()

        # Extract patches and save it into a graph
        for patches, patch_pos, filename in tqdm(infer_loader):                                    
            
            # Locate model to device.
            self.model = self.model.to(self.args['PCL_GPU_INDEX'])
            
            # Minibatch to extract features
            step = 400
            features = []
            for p in range(0,len(patches),step):                
                features.append(self.model(torch.moveaxis(torch.squeeze(torch.tensor(np.stack(patches[p:p+step],0),device=self.args['PCL_GPU_INDEX'])),3,1).to(torch.float32)).to('cpu').detach().numpy())
                gc.collect(0)
                gc.collect(1)      
                gc.collect(2)      
            features = np.concatenate(features,axis=0)

            # Save features
            features = np.concatenate((np.squeeze(patch_pos),features),axis=1)    

            # Join several images to one numpy structure
            patient_to_image = [i for i in os.listdir(self.args['path']+'Raw_Data/Experiment_Information/') if 'Patient_to_Image.xlsx'==i]
            if len(patient_to_image)>0:
                
                # Find subject name and subject file
                patient_to_image_excel = pd.read_excel(self.args['path']+'Raw_Data/Experiment_Information/'+patient_to_image[0])
                index = list(patient_to_image_excel['Image_Name']).index(filename[0])
                NPYname = self.folder+patient_to_image_excel['Subject_Name'][index]+'.npy'
                
                # if already exists...                 
                if os.path.isfile(NPYname):
                    
                    # Load previous concatenate with actual data and save it.
                    prevFeats = np.load(NPYname)
                    features[:,:2] = features[:,:2] + prevFeats[:,:2].max() + self.args['PCL_Patch_Size']*10 
                    np.save(NPYname,np.concatenate((prevFeats,features),axis=0))      
                    del prevFeats           

                else:

                    # Create new file
                    np.save(NPYname,features)    
                
            # Save one image is one subject
            else:
                np.save(self.folder+filename[0],features)    
                # tifffile.imsave(self.folder+filename[0]+'##.tiff',np.stack([np.reshape(features[:,i],(289,240)) for i in range(features.shape[1])]))


            # Eliminate data from garbage collector
            del patches, patch_pos, filename, features 
            gc.collect(0)
            gc.collect(1)      
            gc.collect(2)      
            
            
            # visualize_using_clustering(folder+filename[0],features,[1200,1200],patches.shape[2],image)
            
            
            

        return 
