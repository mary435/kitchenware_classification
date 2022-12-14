### Deploying to EKS:         


* create cluster: download the file [eks-config.yaml](kube-config/eks-config.yaml) And run:
```
eksctl create cluster -f eks-config.yaml
aws ecr create-repository --repository-name kitchenware-images
```
* copy URI for example:
```
"repositoryUri": "894518756245.dkr.ecr.sa-east-1.amazonaws.com/kitchenware-images",
```
* And follow this instructions for your accont and region:
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
Paste on file gateway-deployment.yaml line image and replace:      

image: kitchenware-gateway:001 

for this: 

image: 894518756245.dkr.ecr.sa-east-1.amazonaws.com/kitchenware-images:kitchenware-gateway-001

* Copy image URI from AWS ECR to model-deployment.yaml
```
echo ${MODEL_REMOTE}
894518756245.dkr.ecr.sa-east-1.amazonaws.com/kitchenware-images:kitchenware-model-xception-v4-001
```
Paste on file model-deployment.yaml line image and replace:      

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
* test: ```python3 gateway.py```
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
python3 test.py
```
EXTERNAL-IP = a913822c1cd1c46419c96a13dab473ab-1668504140.sa-east-1.elb.amazonaws.com     

url = 'http://a913822c1cd1c46419c96a13dab473ab-1668504140.sa-east-1.elb.amazonaws.com/predict'       

replace url on test.py and run ```python3 test.py```

* Run to delete servicies because cost money: 
```
eksctl delete cluster --name kitchenware-eks 
```
