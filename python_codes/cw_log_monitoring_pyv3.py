# Ref : https://alexwlchan.net/2017/11/fetching-cloudwatch-logs/

# import time
import boto3
import argparse

def get_log_events(log_group, start_time=None, end_time=None):
    """
    List the first 10000 log events from a CloudWatch group.
    
    :param log_group  : Name of the CloudWatch log group
    :param start_time : Start time to fetch the 1st log
    :param end_time   : Start time of the last log
    
    """
    client = boto3.client('logs')
    kwargs = {'logGroupName': log_group, 
              'limit'       : 10000,}
    
    if start_time:
        kwargs['start_time'] = start_time
    if end_time:
        kwargs['end_time'] = end_time

    count = 0
    while count < 2:
        resp = client.filter_log_events(**kwargs)
        #print (json.dumps(resp['events']))
        yield from resp['events']
        try:
            kwargs['nextToken'] = resp['nextToken']
            count += 1
        except:
            break

if __name__ == '__main__':
    # Argparse Argments and variables defination
    parser = argparse.ArgumentParser(description='Downloading CloudWatch Logs Using Boto3')
    
    try : 
        parser.add_argument('-log_group'  ,action='store'  ,help='CW Log Group Path'      ,dest='log_group'  )
        parser.add_argument('-start_time' ,action='store'  ,help='Initial Log Start Time' ,dest='start_time' )
        parser.add_argument('-end_time'   ,action='store'  ,help='Last Log End Time'      ,dest='end_time'   )
        # arguments = parser.parse_args()
        arguments = parser.parse_args(['-log_group', '/aws/rds/instance/test-instance/postgresql'])
    except:
        parser.print_help()
        exit(1)
    
    log_group     = arguments.log_group
    start_time    = arguments.start_time
    end_time      = arguments.end_time

    # start_time = (int(time.time()) - 10800) * 1000

    # logs = get_log_events(log_group=log_group, start_time=start_time, end_time=end_time)
    for event in get_log_events(log_group=log_group, start_time=start_time, end_time=end_time):
        print(event['message'].strip())