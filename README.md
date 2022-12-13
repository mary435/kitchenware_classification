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

Script to training the final model and saving it.

To run this script in addition to the dataset saved at the same folder, you need the environment:
* Anaconda:
* Pipenv:

## Lambdda Function:
 * From tran.py choose the best mdel and save it as kitchenware-model.h5. Download and run this script [keras_to_tflite.py](keras_to_tflite.py) to save the model 'kitchenware-model.h5' to a lambda model file.     
 
 * Download this files:
     * lambda_function.py
     * dockerfile

 * Run this command: 
```docker build -t kitchenware-model .
docker build -t kitchenware-model . 
docker run -it --rm -p 8080:8080 kitchenware-model:latest
```
 * To try it locally download this file: 
       * [test.py](test.py) And run ```python test.py``` 


* [AWS Lambda configuration](AWS-Lambda-configuration.md)

* Video of the model running on AWS Lambda:
[![demo-video](images/demo-video.png)](https://youtu.be/ZKhc76kcJos) 

## Deploy on Kubernetes:

* Download the [model](kitchenware-model.h5)
* Convert the model:

> ipython
```
import tensorflow as tf
from tensorflow import keras
model = keras.models.load_model('kitchenware-model.h5')
tf.saved_model.save(model, 'kitchenware-model')
```
> exit ipython
```
saved_model_cli show --dir kitchenware-model --all
```
> Find and copy the second signature: signature_def to model-description.txt
```
signature_def['serving_default']:
  The given SavedModel SignatureDef contains the following input(s):
    inputs['input_45'] tensor_info:
        dtype: DT_FLOAT
        shape: (-1, 299, 299, 3)
        name: serving_default_input_45:0
  The given SavedModel SignatureDef contains the following output(s):
    outputs['dense_35'] tensor_info:
        dtype: DT_FLOAT
        shape: (-1, 6)
        name: StatefulPartitionedCall:0
  Method name is: tensorflow/serving/predict
```  
> Save this values:  
``` 
    serving_default
    input_45 - input
    dense_35 - output
```
> Run the model: 
```
docker run -it --rm -p 8500:8500 -v "$(pwd)/kitchenware-model:/models/kitchenware-model/1" -e MODEL_NAME="kitchenware-model" tensorflow/serving:2.7.0 
```
If it works ok, you will see a message like: "[evhttp_server.cc : 245] NET_LOG: Entering the event loop ..."

* tf-serving-connect: open [tf-serving-connect.ipynb](tf-serving-connect.ipynb) and run it to test the running model. 
* Run: ```jupiter nbconvert --tosript tf-serving-connect.ipynb``` and clear the file to run as script with: ```python tf-serving-connect.py```
* Convert this script to a Flask app: Add the flask configration to the tf-serving-connect.py and save it to gateway.py or download the following files already configured.   
          - [gateway.py](gateway.py).    
          - [test.py](test.py).     
          - [proto.py](proto.py).     
Test it running ```python gateway.py```. 
Now that gateway is running with flask, in another window: ```python test.py``` .
The model answers the most probable class.


### Docker compose:

* Prepare the environment with pipenv: 
```
pipenv --python 3.9
pipenv install grpcio ==1.42.0 flask gunicorn keras-image-helper tensorflow-protobuf==2.11.0
```  
* Or download from here: [pipfile]([pipfile) [pipfile.lock](pipfile.lock) And run ```pipenv install```

* Download the file: [image-model.dockerfile]([image-model.dockerfile). And run:     
```
docker build -t kitchenware-model:xception-v4-001 -f image-model.dockerfile .

docker run -it --rm -p 8500:8500 kitchenware-model:xception-v4-001
```
* For testing comment the line ```app.run(debug=True, host='0.0.0.0', port=9696)``` on gateway.py. And run ```pipenv run python gateway.py```.   

* Now uncomment the line ```app.run(debug=True, host='0.0.0.0', port=9696)``` on gateway.py. And comment the first tree:
``` 
url = 'https://raw.githubusercontent.com/mary435/kitchenware_classification/main/images/6172.jpg'  
response = predict(url)    
print(response)
```   
* Download the file: [image-gateway.dockerfile](image-gateway.dockerfile) 
```
docker build -t kitchenware-gateway:001 -f image-gateway.dockerfile .

docker run -it --rm -p 9696:9696 kitchenware-gateway:001
```
* Download docker compose file: [docker-compose.yaml](docker-compose.yaml)    
    * Run: ```docker-compose up```
    * Test: ```python test.py```
    * Option detached mode: ```docker-compose up -d``` And Off: ```docker-compose down```

### Kubernetes:

* Install kubectl: search on google "kubectl AWS" and install from the link instructions. Same for "kind" and follow the instructions for your OS.

* New folder: kube-config: Download the file [model-deployment.yaml](model-deployment.yaml)
```
kind load docker-image kitchenware-model:xception-v4-001
cd kube-config/
kubectl apply -f model-deployment.yaml
kubectl get pod
kubectl port-forward tf-serving-kitchenware-model-#add_here_the_id# 8500:8500
```
* Testing: comment the line ```app.run(debug=True, host='0.0.0.0', port=9696)``` on gateway.py, and uncomment the other tree lines. Run ```pipenv run python gateway.py```.   

* Download the file: [model-service.yaml](model-service.yaml) 
```
kubectl apply -f model-service.yaml
kubectl get service
kubectl port-forward service/tf-serving-kitchenware-model 8500:8500
```
* Test ```pipenv run python gateway.py```. 

* Download the file: [gateway-deployment.yaml](gateway-deployment.yaml) 
```
kind load docker-image kitchenware-gateway:001
kubectl get pod
kubectl apply -f gateway-deployment.yaml
kubectl get pod

kubectl port-forward gateway-#add_here_the_id# 9696:9696
```
* Test ```python test.py```

* Download the file: [gateway-service.yaml](gateway-service.yaml) 
```
kubectl apply -f gateway-service.yaml
kubectl get service
kubectl port-forward service/gateway 8080:80
```
* Test.py change the url to 8080 ```python test.py```

### Deploying to EKS:

* create cluster: download the file [eks-config.yaml](eks-config.yaml)
```
eksctl create cluster -f eks-config.yaml
aws ecr create-repository --repository-name kitchenware-images
```
* copy URI for example:
```
"repositoryUri": "894518756245.dkr.ecr.sa-east-1.amazonaws.com/kitchenware-images",
```
* And follow this isntructions for your accont and region:
```
ACCOUNT_ID=894518756245
REGION=sa-east-1
REGISTRY_NAME=kitchenware-images
PREFIX=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REGISTRY_NAME}

GATEWAY_LOCAL=kitchenware-gateway:001
GATEWAY_REMOTE=${PREFIX}:kitchenware-gateway-001
docker tag ${GATEWAY_LOCAL} ${GATEWAY_REMOTE}

MODEL_LOCAL=kitchenware-model:xception-v4-001
MODEL_REMOTE=${PREFIX}:kitchenware-model-xception-v4-001
docker tag ${MODEL_LOCAL} ${MODEL_REMOTE} 
```
* Login on AWS ECR and push
```
aws ecr get-login-password | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com

docker push ${MODEL_REMOTE}
docker push ${GATEWAY_REMOTE}
```
* Copy image URI from AWS ECR to gateway-deployment.yaml
```
echo ${GATEWAY_REMOTE}
894518756245.dkr.ecr.sa-east-1.amazonaws.com/kitchenware-images:kitchenware-gateway-001
``` 
Paste on file gateway-deployment.yaml line image and replace 
image: kitchenware-gateway:001 
for this: 
image: 894518756245.dkr.ecr.sa-east-1.amazonaws.com/kitchenware-images:kitchenware-gateway-001

* Copy image URI from AWS ECR to model-deployment.yaml
```
echo ${MODEL_REMOTE}
894518756245.dkr.ecr.sa-east-1.amazonaws.com/kitchenware-images:kitchenware-model-xception-v4-001
```
Paste on fle model-deployment.yaml line image and replace: 
image: kitchenware-model:xception-v4-001
for this: 
image: 894518756245.dkr.ecr.sa-east-1.amazonaws.com/kitchenware-images:kitchenware-model-xception-v4-001

* When cluster is ready:
```
kubectl get nodes
kubectl apply -f model-deployment.yaml
kubectl apply -f model-service.yaml
kubectl get pod
kubectl get service
kubectl port-forward service/tf-serving-kitchenware-model 8500:8500
```
* test: ```pipenv run python gateway.py```
* Now upload gateway files:
```
kubectl apply -f gateway-deployment.yaml
kubectl apply -f gateway-service.yaml
kubectl get pod
kubectl get service
```
* copy the EXTERNAL-IP for gateway and test the conection: 
```
kubectl port-forward service/gateway 8080:80
python test.py
```
EXTERNAL-IP = a913822c1cd1c46419c96a13dab473ab-1668504140.sa-east-1.elb.amazonaws.com
url = 'http://a913822c1cd1c46419c96a13dab473ab-1668504140.sa-east-1.elb.amazonaws.com/predict'
replace url on test.py and run ```python test.py```

Now its running on AWS.
video

* Delete servicies because cost money: 
```
eksctl delete cluster --name kitchenware-eks 
```
