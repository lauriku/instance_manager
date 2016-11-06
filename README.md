# instance_manager

Python script to start/stop instances in AWS, meant to be run as a Lambda function.

Uses the python-lambda toolset [nficano/python-lambda](https://github.com/nficano/python-lambda) .

## Instructions

### Setup

To setup, create a virtualenv and run `pip install -r requirements.txt`

### AWS connection

To enable AWS connection you need to configure a default AWS profile in ~/.aws/credentials or provide keys in config.yaml.

### Test run

Once the AWS connection has been configured you can test instance_manager from the local workstation. The file event.json contains sample data for test purposes.

```
{
  "tags": {
    "Purpose": "lambda-testing",
    "Testing": "true"
  },
  "state": "stop"
}
```
Basically the tags given here are matched against the EC2 instance tags and when a match is found the instance state is moved to either `stop` or `start` which ever is defined here.

Define the tags and state as you want and run the test with command `lambda invoke -v`.

### Deploy instance_manager to AWS

To deploy instance_manager to AWS, just type `lambda deploy`. (make sure you're deploying to the correct account)
