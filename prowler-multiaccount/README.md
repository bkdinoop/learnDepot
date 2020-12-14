### Prowler multi account scanning

`Mainstack.yml` creates resources like lambda, iam role cloudwatch event rule ecs cluster task definition
ECR repo and docker build is not available here. 

Docker Image is build from `Dockerfile` present in this folder.

Lambda can be tested from console by giving a sample event like below

{
    "group" : "group4"
}

