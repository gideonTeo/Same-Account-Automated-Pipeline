import json
import boto3
import botocore
from time import gmtime, strftime

def lambda_handler(event, context):
    print("event:", event)
    print("context:", context)
    
    # get the model_data_uri
    sagemaker = boto3.client("sagemaker")
    
    # we get the latest approved model from pipeline model package
    latest_approved_model = sagemaker.list_model_packages(
                                    ModelApprovalStatus="Approved",
                                    ModelPackageGroupName="AbaloneModelPackageGroupName", # edit Model Package Group Name
                                    SortBy='CreationTime',
                                    SortOrder='Descending'
                                )

    latest_approved_model = latest_approved_model["ModelPackageSummaryList"][0]["ModelPackageArn"]
    # print(latest_approved_model)
    model_data_uri = sagemaker.describe_model_package(
                                ModelPackageName=latest_approved_model
                            )

    model_data_uri = model_data_uri["InferenceSpecification"]["Containers"][0]["ModelDataUrl"] # model.tar.gz path
    
    # create model
    model_name = "trained-model" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    res = sagemaker.create_model(
        ModelName=model_name, # edit model name
        Containers=[
        {
            'ModelPackageName': latest_approved_model,
            },
        ],
        ExecutionRoleArn="arn:aws:iam::507708461453:role/service-role/AmazonSageMaker-ExecutionRole-20230110T134193", # edit execution role 
        EnableNetworkIsolation=False
    )
    
    # Once model is approved and created, we update Batch Transform Pipeline definition
    pipeline_def_json = json.loads(sagemaker.describe_pipeline(PipelineName='<Pipeline_Name>')["PipelineDefinition"]) # edit PipelineName
  
    # overwrite Batch Transform Pipeline definition with the latest model 
    pipeline_def_json["Steps"][0]["Arguments"]["ModelName"] = model_name
  
    # convert Batch Transform Pipeline definition back to string
    pipeline_def_str = json.dumps(pipeline_def_json)
    
    # update Batch Transform pipeline (think upsert)
    sagemaker.update_pipeline(
        PipelineName='<Pipeline_Name>',
        PipelineDefinition=pipeline_def_str,
        RoleArn='<Execution_Role>'
        )
  
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
