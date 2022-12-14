## AWS Lambda configuration

* Create repository
```pip install awscli
aws ecr create-repository --repository-name kitchenware-tflite-images
```
* Copy URI for example:
```"repositoryUri": "894518756245.dkr.ecr.sa-east-1.amazonaws.com/kitchenware-tflite-images",```


* Login docker to aws:
```
aws ecr get-login --no-include-email | sed 's/[0-9a-zA-Z=]\{20,\}PASSWORD/g'

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

>Browse, select the image and create

> When function is created.
Test > Name: Plate 

>Json to test it:
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

> Create Method > POST

> Create > Lambda function: kitchenware-classification > Save

>Test > Request:
```{
  "url": "https://raw.githubusercontent.com/mary435/kitchenware_classification/main/images/6172.jpg"
}
```
> Same result as before.

> Deploy API > New Stage > Test > Deploy

>Copy the URL for example: https://oe6aug0jqj.execute-api.sa-east-1.amazonaws.com/Test/predict

>Paste to test.py.   
>Test: running python test.py. Same result as before.
