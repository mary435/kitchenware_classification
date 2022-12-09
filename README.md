# Kitchenware Classification

This project corresponds to a Kaggle image classification contest organized by [DataTalks.Club](https://www.kaggle.com/competitions/kitchenware-classification/overview).

In this competition we need to classify images of different kitchenware items into 6 classes:

* cups
* glasses
* plates
* spoons
* forks
* knives

## Data: 
 * Download from [Kaggle contest](https://www.kaggle.com/competitions/kitchenware-classification/data).
 * API from Kaggle:  ```kaggle competitions download -c kitchenware-classification```
 
## [Notebook](notebook.):
The notebook was created with this anaconda environment: cardio_project_env.yaml

Download it and import it to your anaconda, option environments, import.

Next, open the jupyter Notebook file and run it to view the EDA analyzes, training of differents models, selection process and parameter tuning.

## [Train.py](train.py):

Script to training the final model and saving it model or download from here: [model](kitchenware-model.h5)

To run this script in addition to the dataset saved at the same folder, you need the environment:
* Anaconda:
* Pipenv:

## Lambdda Function:
Firsth download and run this script [keras_to_tflite.py](keras_to_tflite.py) to save the model the to a lambda model file or download the [model](kitchenware-model.tflite)

Download this files:
* lambda_function.py
* dockerfile
```.```
Run this command: ```docker build -t kitchenware-model .```
Mac M1 ```docker build -t kitchenware-model . --platform linux/amd64```
```docker run -it --rm -p 8080:8080 kitchenware-model:latest```
To try it locally use this file: 
* [test.py](test.py) And run ```python test.py```
```.```

## AWS 
* Create repository
```pip install awscli
aws ecr create-repository --repository-name kitchenware-tflite-images
```
* Copy URI

```"repositoryUri": "894518756245.dkr.ecr.sa-east-1.amazonaws.com/kitchenware-tflite-images",```

* Login docker to aws:
```aws ecr get-login --no-include-email | sed 's/[0-9a-zA-Z=]\{20,\}PASSWORD/g'

$(aws ecr get-login --no-include-email)
```
* Tag and push the image:
```
ACCOUNT=894518756245
REGION=sa-east-1
REGISTRY=kitchenware-tflite-images
PREFIX=${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/${REGISTRY}

TAG=kitchenware-model-v1
REMOTE_URI=${PREFIX}:${TAG}

docker tag kitchenware-model:latest ${REMOTE_URI}
docker push ${REMOTE_URI}

```
* AWS Console:
> AWS > Lambda > Functions > Create Function > Container Image
Name: kitchenware-classification
Browse, select the image and create
> When function is created.
Test > Name: Plate 
Json to test it:
```{
  "url": "https://raw.githubusercontent.com/mary435/kitchenware_classification/main/images/6172.jpg"
}
```
Response: 
```{
  "cup": -3.761310577392578,
  "fork": -10.92747974395752,
  "glass": -3.0994043350219727,
  "knife": -9.020426750183105,
  "plate": 5.195217609405518,
  "spoon": -8.06590747833252
}
```
> AWS > API Gateway > Opcion Rest API > Build
> Options: Rest, New Api, Name: kitchenware-classification, Create.
> Inside API > Create resourse > Name:predict (usually a Noun) > Create Resourse.
> Create Method > POST > Create > Lambda function: kitchenware-classification > Save

>Test > Request:
```{
  "url": "https://raw.githubusercontent.com/mary435/kitchenware_classification/main/images/6172.jpg"
}
```
Same result as before.

>Deploy API > New Stage > Test > Deploy
>Copy the URL: https://oe6aug0jqj.execute-api.sa-east-1.amazonaws.com/Test/predict
To test.py
And try running python test.py.

Video?

## Kubernets:
* Download the [model](kitchenware-model.h5)
* Convert the model:
```
iphython
import tensorflow
from tensorflow import keras
model = keras.models.load_model('kitchenware-model.h5')
tf.saved_mdoel.save(model, kitchenware-model)
saved_model_cli show --dir kitchenware-model --all
```
> Copy signature_def to model descrption.txt
```
docker run -it --rm -p 8500:8500 -v "$(pwd)/kitchenware-model:/models/kitchenware-model/1 -e MODEL_NAME="kitchenware-model" tensorflow/serving:2.7.0" 

pip install grpcio==1.42.0 tensorflow-serving-api==2.7.0
```
* tf-serving-connect:
Run: ```jupiter nbconvert --tosript tf-serving-connect.ipynb``` and clear the file or download the file [tf-serving-connect.ipynb](tf-serving-connect.ipynb).
* Test the mdoel:
```
docker run -it --rm -p 8500:8500 -v "$(pwd)/kitchenware-model:/models/kitchenware-model/1 -e MODEL_NAME="kitchenware-model" tensorflow/serving:2.7.0" 
```
* Download the files: 
   * [gateway.py](gateway.py)
   * [test.py](test.py)
  
```
python3 gateway.py
python3 test.py
```
* Download the file: [image-model.dockerfile]([image-model.dockerfile) 
```
docker build -t kitchenware-model:xception-v4-001 -f image-model.dockerfile .

docker run -it --rm -p 8500:8500 kitchenware-model:xception-v4-001
```
* Create the environment with pipenv or download from here: [pipfile]([pipfile)

```
pipenv install grpcio ==1.42.0 flask gunicorn keras-image-helper tensorflow-protobuf==2.11.0

```


```
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
grpcio = "==1.42.0"
flask = "*"
gunicorn = "*"
keras-image-helper = "*"
tensorflow-protobuf = "==2.11.0"

[dev-packages]

[requires]
python_version = "3.9"
```
* Download the file: [image-gateway.dockerfile](image-gateway.dockerfile) 
```
docker build -t kitchenware-gateway:001 -f image-gateway.dockerfile .

docker run -it --rm -p 9696:9696 kitchenware-gateway:001
```

* Docker Compose: download the file: [docker-compose.yaml](docker-compose.yaml) 
Run: ```docker-compose up```
Detached mode: ```docker-compose up -d```
Off: ```docker-compose down```

* Kubectl: Google > kubercrl AWS and copy the link
```brew install kind```
* New folder: kube-config > Download the file [model-deployment.yaml](model-deployment.yaml)
```kind load docker-image kitchenware-model:xception-v4-001
cd kube-config/
kuclt apply -f model-deployment.yaml
kubeclt get pod
kubectl port-forward tf-serving-kitchenware-model 8500:8500
puthon gateway.py
```
* Download the file: [model-service.yaml](model-service.yaml) 
```
kubectl apply -f model-service.yaml
kubeclt get service
kubectl port-forward service/tf-serving-kitchenware-model 8500:8500
```
* Test ```python3 gateway.py```
* Download the file: [gateway-deployment.yaml](gateway-deployment.yaml) 
```
kind load docekr-image kitchenware-gateway:002
kubectl get pod
kubeclt exec -it ping-deployment- --bash
apt install curl
apt update
curl localhost:9696/ping response PONG
apt install telnet
telnet tf-serving-kitchenware-model.default.svc.cluster.local 8500
kubectl apply -f gateway-deployment.yaml
kubectl get pod
kubectl port forward ping-deployment 9696:9696
kubectl logs
kubectl port forward gateway- 9696:9696
```
* Test ```python3 test.py```

* Download the file: [gateway-service.yaml](gateway-service.yaml) 
```
kubectl apply -f gateway-service.yaml
kubectl get service
kubectl port forward service/gateway 8080:80
```
* Test.py URL:8080 ```python3 test.py```

##Deploying to EKS

```brew install ... see comannds on aws```
* create cluster: download the file [eks-config.yaml](eks-config.yaml)
```eksctl create cluster -f eks-config.yaml
aws ecr create-repository --repository-name kitchenware-images
```
* copy URI
* ver archvio config.txt ???
```kuctl get nodes
kubectl aaply -f model-deployment.yaml
.
.
.

```
* test: ```python3 gateway.py```
* copy URL to test file ```python3 test.py```

video?















