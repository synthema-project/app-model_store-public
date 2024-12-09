# MLFlow REST API (app-model-store)

## Description
This project hosts the code for a REST API that provides an interface to use an existing MLFlow Tracking Server via HTTP protocol. The RESTAPI is built with FastAPI and contains endpoints to manage models, runs and experiments.

The FastAPI app is configured with an installation of "mlflow" python library to interact with a Mlflow Tracking Server.

### Structure
The component is structured 
- The folder src contains the FastAPI definition and endpoints declaration, with a folder routers containing the different endpoints (Fastapi routers) and a config.py file setting the connection with the mlflow tracking server
- The folder k8s includes the kubernetes resources
- The folder jenkins includes the jenkins resources
- The folder tests contains different sets of tests
- The folder assets contains testing scripts and pickle files for testing the existing model upload endpoint

## Contributing
Pull requests are welcome. Please make sure to update tests as appropriate.

### Prerequisites
Extending the code requires a set of tools to be present in your environment:

1. Docker (recommended) or FastAPI, mlflow and other dependencies installed (see src/requirements.txt)
1. A running instance of mlflow-server (see model-experiment-registry GitHub repository).

### Setting up the environment

1. Clone the repository
1. Copy the .env from the templates folder with `cp templates/dotenv_standalone .env`. You will require to fill the .env file with the port for the API to listen (PORT) and the Mlflow Tracking Server url (TRACKING_URI) Then sync it with your deployment service (IDE or "--env-file .env" in docker run command).


### Running tests and code checks
The main entrypoint for testing purposes is the folder tests 

### Bulding the images
To build image, navigate to the root of the project where Dockerfile is located and run:
docker build -t <image-name>:<image-tag> . 



### Deploying app

#### Docker deployment
You can deploy the API in docker as follows.

1. To deploy the Mlflow API in docker (the standalone or stack version will be defined by the ".env" selected previously) run the command:  docker run -p 5000:5000 --env-file .env ghcr.io/mlflow/mlflow:v2.16.2 mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri postgresql://<postgres-user>:<postgres-password>@<postgres-container-name>/<mlflow-db-name> --artifacts-destination s3://<buccket-name> --serve-artifacts
1. Go to "localhost:<port>/docs" in the browser  to access the Swagger Ui or use the REST communication to perform requests.

#### Kubernetes deployment
You can deploy the apps in kubernetes by using the "manifest.yaml" provided under the folder k8s

### Running a federated learning job


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

This project extends and usage the following Open Software, which are compatible with MIT License:
- FastAPI (MIT License)
- python-multipart (MIT License)
- pytest (MIT License)
- Uvicorn (MIT License)
- httpx (MIT License)
- MLFlow (Apache 2.0 License)
- Numpy (BSD License)
- boto3 (Apache 2.0 License)