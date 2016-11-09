# -*- coding: utf-8 -*-
import boto3
import sys
import calendar
import datetime

from botocore.exceptions import ClientError

def start_instances(instance_ids):
  ec2_conn = boto3.client('ec2')
  try:
    starting = ec2_conn.start_instances(InstanceIds=instance_ids)
    waiter = ec2_conn.get_waiter('instance_running')
    waiter.wait(InstanceIds=instance_ids)
    print("Started instances: %s" % ", ".join(instance_ids))
  except ClientError as e:
    print("Error while starting instances: %s" % e)
    raise
  except:
    print("Unknown error occured while starting instances: %s " % sys.exc_info()[0])
    raise

def stop_instances(instance_ids):
  ec2_conn = boto3.client('ec2')
  try:
    stopping = ec2_conn.stop_instances(InstanceIds=instance_ids)
    waiter = ec2_conn.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=instance_ids)
    print("Stopped instances: %s" % ", ".join(instance_ids))
  except ClientError as e:
    print("Error while stopping instances: %s" % e)
    raise
  except:
    print("Unknown error occured while stopping instances: %s " % sys.exc_info()[0])
    raise

def get_instances(args):
  """
  event:
  {
    "tags": {
      "Purpose": "lambda-testing",
      "Powersave": "true"
    },
    "state": "stop"
  }  
  """
  ec2_conn = boto3.client('ec2')

  if 'instance_id' in args.keys():
    instances = ec2_conn.describe_instances(InstanceIds=[args['instance_id']])

  if 'tags' in args.keys():
    filters = []
    for key, value in args['tags'].items():
        filters.append(
          {
            'Name': 'tag:' + key,
            'Values': [
              value
          ]})
    instances = ec2_conn.describe_instances(Filters=filters)

  return instances

def get_instance_ids(instances):
  instanceids_list = []
  for reservation in instances['Reservations']:
    for inst in reservation['Instances']:
      instanceids_list.append(inst['InstanceId'])
  return instanceids_list

def is_first_monday_of_month():
  # check whether today is the first monday of the running month
  today = datetime.date.today()
  current_month_days = calendar.monthrange(today.year, today.month)
  delta = (calendar.MONDAY - current_month_days[0]) % 7
  if today.weekday() == delta:
    return True
  else:
    return False

def handler(event, context):
  instances = get_instances(event)
  instanceids = []
  if len(instances) > 0:
    instanceids = get_instance_ids(instances)

  if event.get('custom_schedule') == 'first-monday-of-month':
    if is_first_monday_of_month():
      print("First monday of month, continuing run.")
    else:
      print("Custom schedule not matched, exiting.")
      sys.exit(0)

  if event.get('state') == 'start' and len(instanceids) > 0:
    print("Starting instances: %s" % ", ".join(instanceids))
    start_instances(instanceids)
    return "Ok!"
  elif event.get('state') == 'stop' and len(instanceids) > 0:
    print("Stopping instances: %s" % ", ".join(instanceids))
    stop_instances(instanceids)
    return "Ok!"
  else:
    return "No instances found"
   
