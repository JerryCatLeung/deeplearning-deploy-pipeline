FROM mcr.microsoft.com/azureml/onnxruntime-1.13-ubuntu20.04-py38-cpu-inference:20230824.v1

WORKDIR /workspace

# add java
RUN mkdir /workspace/software
ADD https://mirrors.huaweicloud.com/java/jdk/8u202-b08/jdk-8u202-linux-x64.tar.gz /workspace/software
RUN tar -zxvf /workspace/software/jdk-8u202-linux-x64.tar.gz -C /workspace/software

# set env
ENV JAVA_HOME=/workspace/software/jdk1.8.0_202
ENV PATH=$JAVA_HOME/bin:$PATH

# use root
USER root