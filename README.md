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






