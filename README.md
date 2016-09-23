Python script to start/stop instances in AWS, meant to be run as a Lambda function.

Uses the python-lambda toolset https://github.com/nficano/python-lambda .

To test, configure a default AWS profile in ~/.aws/credentials or provide keys in config.yaml.

event.json contains test data to test the script with, test by running lambda -v invoke.

To deploy to AWS, just type lambda deploy. (make sure you're deploying to the correct account)

To setup, create a virtualenv and run pip install -f requirements.txt