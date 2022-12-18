from __future__ import print_function, division

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch.backends.cudnn as cudnn
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import json
import time
import os
import argparse
import copy
import sys

cudnn.benchmark = True
plt.ion()   # interactive mode

import shutil
import glob
from PIL import Image

def classify(model,paths):
    torch.no_grad()
    imgfile = paths
    #print(len(imgfile), imgfile)
    model1 = torch.load(model)
    groups = {}
    transform = transforms.Compose([transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Lambda(lambda x: x.repeat(1,1,1)),
                                
                                            ]) 
    for i in imgfile:
        imgfile1 = i.replace("\\", "/")#统一路径
        img = Image.open(imgfile1)
        img = img.convert("RGB")
        #tran = []
        #tran.append(torchvision.transforms.ToTensor())
        #tran.append(torchvision.transforms.Lambda(lambda x:x.repeat(1, 1, 1,)))
        #img = img.reshape((*img.shape, -1))
        img = transform(img)
        new_dir=os.path.dirname(imgfile1)
 
        img = img.unsqueeze(0)
        outputs = model1(img)  # outputs，out1修改为你的网络的输出
        predicted, index  = torch.max(outputs, 1)
        degre = int(index[0])
        list = ['animal','building','food','plant','portrait','text','transportation','view']
        
        name=list[degre]
        if name not in groups:#添加新分类
            groups[name] = []
        groups[name].append(imgfile1)
        #output_dir=os.path.join(new_dir,list[degre])
        #shutil.copy(imgfile1, output_dir)
        #print(output_dir)
        #print(predicted, list[degre])
        #print(list[degre],imgfile1)
    return(groups)
        
    
    
'''    
def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('model', type=str,
                        help='Either a directory containing the meta_file and ckpt_file or a model protobuf (.pb) file')
    parser.add_argument('data_dir', type=str,
                        help='The directory containing the images to cluster into folders.')
   
   
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
'''