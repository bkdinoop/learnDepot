import boto3
import os
from botocore.exceptions import ClientError

ACC_EXCLUSION_LIST = ["111111111", "2222222"]
FARGATE_CLUSTER = os.environ['FARGATE_CLUSTER']
FARGATE_TASK_DEF_NAME = os.environ['FARGATE_TASK_DEF_NAME']
SUBNETS = [os.environ["SUBNET_ID_AZ1"], os.environ["SUBNET_ID_AZ1"]]
SG_ID = os.environ["SECURITY_GROUP"]
SEC_AUDIT_ROLE = os.environ["SECURITY_AUDIT_ROLE"]
AWS_REGION = os.environ["AWS_REGION"]
MASTER_ACC_ID = os.environ["MASTER_ACC_ID"]
MASTER_ROLE_NAME = os.environ["MASTER_ROLE_NAME"]
OU_ID = os.environ["OU_ID"]


def assume_role(service, accid, rolename, regionName):
    """
    Function Assumes the role name that is passed
    Return the boto3.client for service that is passed
    """
    try:
        Client = boto3.client('sts', region_name=regionName)
        roleArn = f"arn:aws:iam::{accid}:role/{rolename}"
        Response = Client.assume_role(
            RoleArn=roleArn,
            RoleSessionName='prowler-session')
        aws_access_key_id = Response['Credentials']['AccessKeyId']
        aws_secret_access_key = Response['Credentials']['SecretAccessKey']
        aws_session_token = Response['Credentials']['SessionToken']
        client = boto3.client(service, aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              aws_session_token=aws_session_token,
                              region_name=regionName)
        return client
    except ClientError as e:
        print(e.with_traceback)
        raise e


def getAcc():
    """
    Function return account list fetched from master account's 
    organization by passing ouId
    """
    try:
        orgClient = assume_role("organizations", MASTER_ACC_ID,
                                MASTER_ROLE_NAME, AWS_REGION)
        paginator = orgClient.get_paginator("list_accounts_for_parent")
        response_iterator = paginator.paginate(ParentId=ouID,)
        accList = []
        for resp in response_iterator:
            for acc in resp["Accounts"]:
                if acc["Id"] not in ACC_EXCLUSION_LIST:
                    accList.append(acc["Id"])
        return accList
    except ClientError as e:
        print(e.with_traceback)
        raise e


def run_prolwer_task():    
    ecsClient = boto3.client("ecs")
    resp = ecsClient.run_task(
        cluster=FARGATE_CLUSTER,
        launchType="FARGATE",
        taskDefinition=FARGATE_TASK_DEF_NAME,
        platformVersion='LATEST',
        overrides={
            'containerOverrides': [
                {
                    "command": ["-A", "111111111", "-R", SEC_AUDIT_ROLE, "-S", "-M", "json-asff", "-b", "-q","-g", "group4", "-f", AWS_REGION],
                    "name": "prowler-sechub-task",                    
                }
            ]
        },
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': SUBNETS,
                'assignPublicIp': "DISABLED",
                'securityGroups': [SG_ID],
            },
        }
    )


def handler(event, context):    
    # Prowler Scan  against all account id of an OU ID
    for acc in getAcc():
        run_prolwer_task(acc, event["group"])

    # Test with single accountID
    # run_prolwer_task("", event["group"])
