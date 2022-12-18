from pathlib import Path
import clip
import torch
from PIL import Image
import math
import numpy as np
import pandas as pd
import os, glob
import shutil


def compute_features(device,model,preprocess,photos_batch):
    # Load all the photos from the files
#     print('3.1')
    photos = [Image.open(photo_file) for photo_file in photos_batch]
#     print("3.2")
    # Preprocess all photos
    photos_preprocessed = torch.stack([preprocess(photo) for photo in photos]).to(device)
#     print("3.3")

    with torch.no_grad():
        # Encode the photos batch to compute the feature vectors and normalize them
#         print("3.4")
        photos_features = model.encode_image(photos_preprocessed)#对图片进行编码
#         print("3.5")
        photos_features /= photos_features.norm(dim=-1, keepdim=True)
#         print("3.6")

    # Transfer the feature vectors back to the CPU and convert to numpy
#     print("3.7")
    return photos_features.cpu().numpy()

def compute_clip_features(model,device,preprocess,data_path):
        
        #device = "cuda" if torch.cuda.is_available() else "cpu"
        #model, preprocess = clip.load("ViT-B/32", device=device)
        batch_size = 16
        photos_path=data_path
        features_path=data_path/"features"
        if(os.path.exists(features_path)==0):
            os.mkdir(features_path)
        
        photos_files = list(photos_path.glob("*.jpg"))
#         print(photos_files)
        batches = math.ceil(len(photos_files) / batch_size)
        # Process each batch
        for i in range(batches):
            #print(f"Processing batch {i+1}/{batches}")

            batch_ids_path = features_path / f"{i:010d}.csv"
            batch_features_path = features_path / f"{i:010d}.npy"

            # Only do the processing if the batch wasn't processed yet
            if not batch_features_path.exists():
                try:
                    # Select the photos for the current batch
#                     print('1')
                    batch_files = photos_files[i*batch_size : (i+1)*batch_size]
#                     print('2')
#                     print(batch_files)

                    # Compute the features and save to a numpy file
                    batch_features = compute_features(device,model,preprocess,batch_files)
#                     print('3')
                    np.save(batch_features_path, batch_features)
#                     print("4")

                    # Save the photo IDs to a CSV file
                    photo_ids = [photo_file.name.split(".")[0] for photo_file in batch_files]
                    photo_ids_data = pd.DataFrame(photo_ids, columns=['photo_id'])
                    photo_ids_data.to_csv(batch_ids_path, index=False)
                except:
                    # Catch problems with the processing to make the process more robust
                    print(f'Problem with batch {i}')
        merge(features_path,data_path)
        delefeature(features_path)
        #return photo_ids

    
def merge(features_path,data_path):
    # Load all numpy files
    featuresall_path=data_path/"featuresall"
    if(os.path.exists(featuresall_path)==0):
            os.mkdir(featuresall_path)
    features_list = [np.load(features_file) for features_file in sorted(features_path.glob("*.npy"))]
    
    # Concatenate the features and store in a merged file
    features = np.concatenate(features_list)
    np.save(featuresall_path/"features.npy", features)

    # Load all the photo IDs
    photo_ids = pd.concat([pd.read_csv(ids_file) for ids_file in sorted(features_path.glob("*.csv"))])
    photo_ids.to_csv(featuresall_path/ "photo_ids.csv", index=False)

def delefeature(features_path):
    #Loop Through the folder projects all files and deleting them one by one
    shutil.rmtree(features_path)
    #os.rmdir(features_path)
def text_encode(device,search_query,model):
    with torch.no_grad():
        # Encode and normalize the description using CLIP
            # model.encode_text(text)    # 将文本进行编码
        text_encoded = model.encode_text(clip.tokenize(search_query).to(device))
        text_encoded /= text_encoded.norm(dim=-1, keepdim=True)
    return text_encoded   
def similarity(data_path,device,search_query,model,preprocess):
    compute_clip_features(model,device,preprocess,data_path)
    # Load the features and the corresponding IDs
    photo_features = np.load(data_path/"featuresall" / "features.npy")
    photo_ids = pd.read_csv(data_path/"featuresall" / "photo_ids.csv")
    photo_ids = list(photo_ids['photo_id'])
    text_encoded=text_encode(device,search_query,model)
    # Retrieve the description vector and the photo vectors
    text_features = text_encoded.cpu().numpy()

    # Compute the similarity between the descrption and each photo using the Cosine similarity
    similarities = list((text_features @ photo_features.T).squeeze(0))

    # Sort the photos by their similarity score
    best_photos = sorted(zip(similarities, range(photo_features.shape[0])), key=lambda x: x[0], reverse=True)
    return best_photos,photo_ids
def search_images_by_text(data_path,search_query):
#     print(type(data_path))
#     print(type(search_query))
#     print(data_path)
#     print(search_query)
    data_path=Path(data_path)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    best_photos,photo_ids=similarity(data_path,device,search_query,model,preprocess)
    results=[]
    for i in range(10):
        # Retrieve the photo ID
        idx = best_photos[i][1]
        photo_id = photo_ids[idx]
        result=(photo_id+'.jpg')
        results.append(result)
    search_results=[results]    
#     print(results)
    return search_results

        
#  #输入data的目录       
# data_path='C:/Users/Lenovo/Desktop/smart/data/database'
# search_query = "family with dog"
# print(type(data_path))
# print(type(search_query))
# search_images_by_text(data_path,search_query)