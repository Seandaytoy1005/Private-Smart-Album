# Model Card: CLIP


## Model Introduction

CLIP is a multimodal model based on contrastive learning. Unlike some contrastive learning methods in CV such as moco and simclr, the training data of CLIP is a text-image pair: an image and its corresponding text description, here It is hoped that through contrastive learning, the model can learn the matching relationship between text-image pairs.
## How CLIP works

CLIP authors report that they assembled a dataset of 400 million (image, text) pairs from the Internet. The model will take an image as an input and predict text as an output.
![image](https://user-images.githubusercontent.com/105193758/208596230-178da618-adfe-44ae-8ff6-b16c8b18efce.png)
## Model principle
### Pre-train
![image](https://user-images.githubusercontent.com/105193758/208637163-3826a2a7-c786-4576-88e6-7fc062cda6d5.png)

The model architecture is divided into two parts, image encoder and text encoder.Here, the extracted text features and image features are compared and learned. For a training batch containing N text-image pairs, combining N text features and N image features in pairs, the CLIP model will predict the similarity of N^2 possible text-image pairs

### The corresponding pseudocode implementation is as follows:
     #image_encoder - ResNet or Vision Transformer
     #text_encoder - CBOW or Text Transformer
     #I[n, h, w, c] - minibatch of aligned images
     #T[n, l] - minibatch of aligned texts
     #W_i[d_i, d_e] - learned proj of image to embed
     #W_t[d_t, d_e] - learned proj of text to embed
     #t - learned temperature parameter

     #分别提取图像特征和文本特征
     I_f = image_encoder(I) #[n, d_i]
     T_f = text_encoder(T) #[n, d_t]

     #对两个特征进行线性投射，得到相同维度的特征，并进行l2归一化
     I_e = l2_normalize(np.dot(I_f, W_i), axis=1)
     T_e = l2_normalize(np.dot(T_f, W_t), axis=1)

     #计算缩放的余弦相似度：[n, n]
     logits = np.dot(I_e, T_e.T) * np.exp(t)

     #对称的对比学习损失：等价于N个类别的cross_entropy_loss
     labels = np.arange(n) # 对角线元素的labels
     loss_i = cross_entropy_loss(logits, labels, axis=0)
     loss_t = cross_entropy_loss(logits, labels, axis=1)
     loss = (loss_i + loss_t)/2<br>


Please see the paper linked below for further details about their specification.

#### Documents

- [Blog Post](https://openai.com/blog/clip/)
- [CLIP Paper](https://arxiv.org/abs/2103.00020)



## Model Use

### Intended Use

The model is intended as a research output for research communities. We hope that this model will enable researchers to better understand and explore zero-shot, arbitrary image classification. We also hope it can be used for interdisciplinary studies of the potential impact of such models - the CLIP paper includes a discussion of potential downstream impacts to provide an example for this sort of analysis.

#### Primary intended uses

The primary intended users of these models are AI researchers.

We primarily imagine the model will be used by researchers to better understand robustness, generalization, and other capabilities, biases, and constraints of computer vision models.


## Data

The model was trained on publicly available image-caption data. This was done through a combination of crawling a handful of websites and using commonly-used pre-existing image datasets such as [YFCC100M](http://projects.dfki.uni-kl.de/yfcc100m/). A large portion of the data comes from our crawling of the internet. This means that the data is more representative of people and societies most connected to the internet which tend to skew towards more developed nations, and younger, male users.



## Performance and Limitations

### Performance

We have evaluated the performance of CLIP on a wide range of benchmarks across a variety of computer vision datasets such as OCR to texture recognition to fine-grained classification. The paper describes model performance on the following datasets:

- Food101
- CIFAR10   
- CIFAR100   
- Birdsnap
- SUN397
- Stanford Cars
- FGVC Aircraft
- VOC2007
- DTD
- Oxford-IIIT Pet dataset
- Caltech101
- Flowers102
- MNIST   
- SVHN 
- IIIT5K   
- Hateful Memes   
- SST-2
- UCF101
- Kinetics700
- Country211
- CLEVR Counting
- KITTI Distance
- STL-10
- RareAct
- Flickr30
- MSCOCO
- ImageNet
- ImageNet-A
- ImageNet-R
- ImageNet Sketch
- ObjectNet (ImageNet Overlap)
- Youtube-BB
- ImageNet-Vid

## Limitations

CLIP and our analysis of it have a number of limitations.
CLIP currently struggles with respect to certain tasks such as fine grained classification and counting objects.
 Additionally, our approach to testing CLIP also has an important limitation- in many cases use linear probes to evaluate the performance of CLIP and there is evidence suggesting that linear probes can underestimate model performance.
