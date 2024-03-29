###
## Assumptions
1. Docker is installed, localstack is already installed and localstack s3 service is running
1. You have a python virtual env already setup python(optional)


## Setup
Check if s3 service is running in localstack, the output should be `running`
```
localstack status services -f json | jq '.s3'

docker ps | grep -i "localstack" ##docker container named localstack should be running/healthy  
```

We need to create a aws profile `localstack`, you can set the `AWS Access Key ID=test`,  `AWS Secret Access Key=test`, `region=us-east-1`
```
aws configure --profile localstack
```

Create a s3 bucket called `deployments`
```
AWS_PROFILE=localstack aws s3 mb s3://deployments --endpoint-url http://localhost:4566ck 
```


## Create fake data `deployments` s3 buckets

**On your terminal, cd into the git repository, run the following command**

`pip install -r requirements.txt`


`python -m createFakeData`

```
The output should something like this 
Uploaded file 'deployhash112/index.html' successfully.
Uploaded file 'deployhash112/css/font.css' successfully.
Uploaded file 'deployhash112/images/hey.png' successfully.
Uploaded file 'dsfsfsl9074/root.html' successfully.
Uploaded file 'dsfsfsl9074/styles/font.css' successfully.
Uploaded file 'dsfsfsl9074/img/hey.png' successfully.
Uploaded file 'delkjlkploy3/base.html' successfully.
Uploaded file 'delkjlkploy3/fonts/font.css' successfully.
Uploaded file 'delkjlkploy3/png/hey.png' successfully.
Uploaded file 'klljkjkl123/index.html' successfully.
Uploaded file 'klljkjkl123/css/font.css' successfully.
Uploaded file 'klljkjkl123/images/hey.png' successfully.
Uploaded file 'dsfff1234321/root.html' successfully.
Uploaded file 'dsfff1234321/styles/font.css' successfully.
Uploaded file 'dsfff1234321/img/hey.png' successfully.
```

Use the following command to check data in s3
```
AWS_PROFILE=localstack aws s3 ls s3://deployments --endpoint-url http://localhost:4566 --recursive
```


## Next run the `cleanDeployments.py` script, `keep-x-deployments` => is the # of deployment to keep, default is `1`

`python -m cleanupDeploys --keep-x-deployments 2`

```
2024-03-29 01:44:15,265 - INFO - There are total of 5 deployments we are keeping 2 deployments
2024-03-29 01:44:15,265 - INFO - These deployments will be deleted ['delkjlkploy3', 'dsfsfsl9074', 'deployhash112']
2024-03-29 01:44:15,319 - INFO - Deleted deployment: delkjlkploy3
2024-03-29 01:44:15,343 - INFO - Deleted deployment: dsfsfsl9074
2024-03-29 01:44:15,365 - INFO - Deleted deployment: deployhash112
```
