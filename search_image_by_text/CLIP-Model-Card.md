# Model Card: CLIP


## Model Details

CLIP is a multimodal model based on contrastive learning. Unlike some contrastive learning methods in CV such as moco and simclr, the training data of CLIP is a text-image pair: an image and its corresponding text description, here It is hoped that through contrastive learning, the model can learn the matching relationship between text-image pairs.
## How CLIP works


CLIP authors report that they assembled a dataset of 400 million (image, text) pairs from the Internet. The model will take an image as an input and predict text as an output.
![image](https://user-images.githubusercontent.com/105193758/208596230-178da618-adfe-44ae-8ff6-b16c8b18efce.png)

### Model Type

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
