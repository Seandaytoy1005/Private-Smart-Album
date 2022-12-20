# Model Card: CLIP


## Model Introduction

CLIP is a multimodal model based on contrastive learning. Unlike some contrastive learning methods in CV such as moco and simclr, the training data of CLIP is a text-image pair: an image and its corresponding text description, here It is hoped that through contrastive learning, the model can learn the matching relationship between text-image pairs.

## Model principle
### Pre-train
![image](https://user-images.githubusercontent.com/105193758/208637163-3826a2a7-c786-4576-88e6-7fc062cda6d5.png)

- The model architecture is divided into two parts, image encoder and text encoder.Here, the extracted text features and image features are compared and learned. For a training batch containing N text-image pairs, combining N text features and N image features in pairs, the CLIP model will predict the similarity of N^2 possible text-image pairs
- The similarity here directly calculates the cosine similarity of text features and image features. Note that the cosine similarity of text features and image features is calculated using text cls_token and image cls_token (cosine similarity)
The matrix shown above
- There are a total of N positive samples, that is, text and images that really belong to a pair (diagonal elements in the matrix), while the remaining N2-N** text-image pairs are negative samples
- The training goal of CLIP is to maximize the similarity of N positive samples while minimizing the similarity of the remaining negative samples.


### The corresponding pseudocode implementation is as follows:
     #image_encoder - ResNet or Vision Transformer
     #text_encoder - CBOW or Text Transformer
     #I[n, h, w, c] - minibatch of aligned images
     #T[n, l] - minibatch of aligned texts
     #W_i[d_i, d_e] - learned proj of image to embed
     #W_t[d_t, d_e] - learned proj of text to embed
     #t - learned temperature parameter

     #Extract image features and text features separately
     I_f = image_encoder(I) #[n, d_i]
     T_f = text_encoder(T) #[n, d_t]

     #Perform linear projection on two features to obtain features of the same dimension, and perform l2 normalization
     I_e = l2_normalize(np.dot(I_f, W_i), axis=1)
     T_e = l2_normalize(np.dot(T_f, W_t), axis=1)

     #Compute scaled cosine similarity: [n, n]
     logits = np.dot(I_e, T_e.T) * np.exp(t)

     #Symmetric contrastive learning loss: equivalent to cross_entropy_loss of N categories
     labels = np.arange(n) # labels for diagonal elements
     loss_i = cross_entropy_loss(logits, labels, axis=0)
     loss_t = cross_entropy_loss(logits, labels, axis=1)
     loss = (loss_i + loss_t)/2<br>





## Model Usege:
![image](https://user-images.githubusercontent.com/105193758/208666353-17d1f085-d007-4845-b50f-d3b85395e8ec.png)
- Construct the description text of each category according to the classification label of the task: A photo of {label}, and then send these texts to the Text Encoder to obtain the corresponding text features. If the number of categories is N, then N text features will be obtained;
- Send the image to be predicted to Image Encoder to obtain image features, and then calculate the scaled cosine similarity with N text features (consistent with the training process), and then select the category corresponding to the text with the largest similarity as the image classification prediction result, further, These similarities can be regarded as logits, and the predicted probability of each category can be obtained after being sent to softmax.

## Some examples show:
![image](https://user-images.githubusercontent.com/105193758/208669954-0fc4a326-9145-4716-8f8f-f2c36caee991.png)


## Limitations:

- While CLIP usually performs well on recognizing common objects, it struggles on more abstract or systematic tasks such as counting the number of objects in an image and on more complex tasks such as predicting how close the nearest car is in a photo. On these two datasets, zero-shot CLIP is only slightly better than random guessing. Zero-shot CLIP also struggles compared to task specific models on very fine-grained classification, such as telling the difference between car models, variants of aircraft, or flower species.
- CLIP also still has poor generalization to images not covered in its pre-training dataset. For instance, although CLIP learns a capable OCR system, when evaluated on handwritten digits from the MNIST dataset, zero-shot CLIP only achieves 88% accuracy, well below the 99.75% of humans on the dataset. Finally, we’ve observed that CLIP’s zero-shot classifiers can be sensitive to wording or phrasing and sometimes require trial and error “prompt engineering” to perform well.
## More information about clip
- https://github.com/openai/CLIP
- https://openai.com/blog/clip/
