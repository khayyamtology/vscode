# Aqua-sidecar Docker Setup

This repository contains the Dockerfile for setting up the Aqua-sidecar. The setup includes downloading the updated microenforcer file from Nexus, and incorporating it into the Docker image.

## Prerequisites

- Docker installed on your system.
- Access to the Nexus repository hosting the aqua-sidecar microenforcer binary.
- AWS access to the Alpine image in Elastic Container Registry (ECR).
- Nexus credentials (or a token) to download the microenforcer.20022.4.460 file from Nexus (optional).

## Dockerfile Explanation

### Base Image

We are using the Alpine base image, which is fetched from AWS Elastic Container Registry (ECR):

```dockerfile
FROM 328519145923.dkr.ecr.us-east-1.amazonaws.com/alpine:3.11
```

## Downloading and Copying the microenforcer File
You have two options to download the updated Aqua microenforcer file (microenforcer.20022.4.460).

### Manually Download from Nexus and Copy to Docker Context

#### Log in to Nexus: 
Open your web browser and log in to your Nexus repository using your Nexus credentials.

#### Download the microenforcer File: 
Navigate to the repository where the microenforcer binary (microenforcer.20022.4.460) is stored. Manually download the file to your local machine.

#### Copy the File to the Docker Context: 
Once the microenforcer.20022.4.460 file is downloaded, manually move or copy it to the directory where your Dockerfile is located (Docker context folder). This will ensure the file can be included in the Docker image.

#### Copying microenforcer into Docker Image
Once downloaded, the microenforcer.20022.4.460 file is copied into the Docker image:
```
COPY microenforcer.20022.4.460 /bin/microenforcer
RUN chmod +x /bin/microenforcer
```
This makes the microenforcer executable inside the container.

## Aqua microenforcer Initialization
The Aqua microenforcer is initialized during the Docker image build process with the following command:

```
RUN /bin/microenforcer aqua-init
```
This prepares the Aqua microenforcer for runtime protection.

## Directory Setup and Permissions
We create a directory /.aquasec/bin to store the microenforcer file and set the necessary permissions:

```
RUN mkdir -p /.aquasec/bin && \
    cp /bin/microenforcer /.aquasec/bin/microenforcer && \
    chmod +x /.aquasec/bin/microenforcer
```
This ensures the microenforcer file is in the correct location with executable permissions.

## User and Group Setup
We add a new group and user (aqua) with specific IDs.

```
RUN add group -g 11433 -S aqua && \
adduser -h /home/aqua -g "aqua user" -s /sbin/nologin -G aqua -S -u 11431 aqua

USER aqua
```
This avoids errors during the build if the user or group already exists.

## Environment Variables
The necessary environment variables for the Aqua-sidecar are set as follows:

```
ENV LD_PRELOAD=/.aquasec/bin/$PLATFORM/slklib.so \
    AQUA_microenforcer="1" \
    AQUA_DEBUG_TYPE=STDOUT
```
These variables enable specific runtime protection features.

## Metadata
The Docker image includes metadata about the Aqua-sidecar using Docker LABEL commands:

```
LABEL name="Aqua microenforcer" \
    vendor="Aqua Security Software Ltd." \
    summary="Aqua Security microenforcer" \
    description="The Aqua Security microenforcer provides runtime protection." \
    com.aquasec.component=microenforcer \
    com.aquasec.baseimage=alpine \
    product=aqua \
    maintainer="admin@aqua.com"
```

## Volume Declaration
A volume is declared to store data used by the aqua-sidecar:

```
VOLUME ["/.aquase"]
```
This ensures persistence for the .aquase directory across container runs.

## Steps to Build and Test the Docker Image

### Manually Download from Nexus and Copy to Docker Context

Log in to Nexus and manually download the microenforcer.20022.4.262 file.
Copy the file to your Docker context folder (same directory as your Dockerfile).

## 2. Build the Docker Image
Once you have the Dockerfile and the microenforcer.20022.4.460 file, build the Docker image:

```
docker build -t aqua-sidecar:latest .
```

## Pushing the Image to AWS ECR

To push the aqua-sidecar:latest image to AWS Elastic Container Registry (ECR), follow these steps:

### 1. Authenticate Docker with AWS ECR
Run the following command to log in to ECR. Replace <aws_account_id> with your actual AWS account ID and <region> with your ECR region (e.g., us-east-1).

```
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
```

### 2. Tag the Docker Image
Tag the aqua-sidecar:latest image with your ECR repository:

```
docker tag aqua-sidecar:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/aqua-sidecar:latest
```

### 3. Push the Docker Image to ECR
Push the tagged image to your ECR repository:

```
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/aqua-sidecar:latest
```

### 4. Verify the Image in ECR
You can log in to the AWS Management Console and verify that the image has been successfully pushed to your ECR repository.

