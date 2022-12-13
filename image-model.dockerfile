FROM tensorflow/serving:2.7.0

COPY kitchenware-model /models/kitchenware-model/1
ENV MODEL_NAME="kitchenware-model"
