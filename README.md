# WestpacNZ-Pipeline-Poc
Proof of Concept for automating a Pipeline using EventBridge and Lambda function
![Pipeline Diagram]([https://github.com/gidteo/WestpacNZ-Pipeline-Poc/blob/main/Images/EventB1.png](https://github.com/gidteo/WestpacNZ-Pipeline-Poc/blob/main/Images/WestpacNZ%20Pipeline.png))

## EventBridge
#### See below for step-by-step guidance on how to create EventBridge that will triggered by Model Package Approval in Pipeline
### Step 1 - Define Rule Detail:
![Step 1](https://github.com/gidteo/WestpacNZ-Pipeline-Poc/blob/main/Images/EventB1.png)

### Step 2 - Go to "Event Pattern" Section and insert code (Sample code can be found [here](https://github.com/gidteo/WestpacNZ-Pipeline-Poc/blob/main/EventBridge_Pattern.json)):
![Step 2](https://github.com/gidteo/WestpacNZ-Pipeline-Poc/blob/main/Images/EventB2.png)

### Step 3 - Select Targets (Target should be pointing to the Lambda Function that will be triggered after `Approved Model` action):
![Step 3](https://github.com/gidteo/WestpacNZ-Pipeline-Poc/blob/main/Images/EventB3.png)

## Lambda Code
#### Sample Lambda code can be found [here](https://github.com/gidteo/WestpacNZ-Pipeline-Poc/blob/main/lambda_handler.py)

Below are the workflow implemented in the lambda function:

1. List the model packages filter by `Approved` status; 
2. Fetch the model data URL from most recent approved model package;
3. Create the most up-to-date `Approved` SageMaker model;
4. Sync the new model created in step 3 to the batch transform pipeline;


### Author: 
Gideon Teo and Jeff Shi
