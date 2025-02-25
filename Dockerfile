FROM bitnami/spark:3.4.0

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        libopenmpi-dev \
        openmpi-bin \
        python3-dev \
        libpng-dev \
        libfreetype6-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --upgrade pip && \
    pip3 install tensorflow==2.12.0 matplotlib tensorflowonspark && \
    HOROVOD_WITH_TENSORFLOW=1 HOROVOD_WITH_GLOO=1 pip3 install --no-cache-dir horovod[tensorflow]

USER 1001

EXPOSE 4040 7077 8080 18080
CMD ["/opt/bitnami/spark/bin/spark-class", "org.apache.spark.deploy.master.Master"]