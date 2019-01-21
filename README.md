# Smack-it
Distributed System for large scale data management

## Architecture

[automation/](automation) : Bash scripts to automatize the deployment of the infrastructure and the application

[config/](config) : Kubernetes and AWS configuration files

[src/](src) : Source code of our application
  - [app/](src/app) : Code source of the web application and Dockerfile associated
  - [aws/](src/aws) : Code source of the aws manager (perform actions on AWS)
  - [cassandra/](src/cassandra) : Creator of the database and Dockerfile associated
  - [kafka/](src/kafka) : Code source of the kafka producer to generate tweets and Dockerfile associated to kafka
  - [utils/](src/utils) : Config manager for project's variables

## Getting started

### Run the solution

In order to automatically run the solution, please follow these steps :

1. Configure your credentials AWS :

Follow this guide to have at least the `~/.aws/credentials` and `~/.aws/config` (at least with the region) files : https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

2. Install the packages (python3)

`pip3 install -r requirements.txt` (You could use virtualenv to isolate this project from your other projects : https://virtualenv.pypa.io/en/latest/)

3. Configure your deployment (Optional)

You could configure the deployment using the [config/instances.ini](config/instances.ini) file

4. Go to the automation folder

 `cd automation`

 5. Launch the deployment script and wait during the creation time

 `./deploy.sh`

### Connect to the master and control the Kubernetes cluster (Optional)

 In order to automatically run the solution, please follow these steps :

1. Go back to the root folder

`cd ..`

2. Get back the master's public ip address

`./manage.py read type get-master-public-ip`

3. Connect by ssh to the master

`ssh -i ssh/Smackey ubuntu@MASTER_PUBLIC_IP`

4. You could use `kubectl` commands for example to play with the cluster

`kubectl get pods`

> Some pods at the startup will have the status 'Error' : the cluster just need some time to attain a global coherency

### See the application running

1. Get back a worker's ip address

`./manage.py read type get-workers-public-ip`

2. Open a browser to the address below

`http://ONE_WORKER_PUBLIC_IP:32222`

## Contributing

All contributions are well appreciated.

Please read **CONTRIBUTING.md** before starting to contribute on this project.
