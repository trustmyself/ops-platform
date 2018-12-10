import argparse
import boto3
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--days', type=int, default=1)
args = parser.parse_args()


now = datetime.datetime.utcnow()
start = (now - datetime.timedelta(days=args.days)).strftime('%Y-%m-%d')
end = now.strftime('%Y-%m-%d')

cd = boto3.client('ce', region_name='us-east-1', aws_access_key_id='', aws_secret_access_key='')

def CostUsage():
    results = []
    token = None
    while True:
        if token:
            kwargs = {'NextPageToken': token}
        else:
            kwargs = {}
        data = cd.get_cost_and_usage(
            TimePeriod={'Start': start, 'End':  end}, 
            Granularity='DAILY', 
            Metrics=['UnblendedCost'], 
            GroupBy=[
                    {
                        'Type': 'DIMENSION', 
                        'Key': 'LINKED_ACCOUNT'
                    }, 
                    {
                        'Type': 'DIMENSION', 
                        'Key': 'SERVICE'
                    }
                ], 
            **kwargs)
        
        results += data['ResultsByTime']
        token = data.get('NextPageToken')
        if not token:
            break

    for result_by_time in results:
        all_amount = 0
        for group in result_by_time['Groups']:
            amount = group['Metrics']['UnblendedCost']['Amount']
            unit = group['Metrics']['UnblendedCost']['Unit']
            all_amount += int(float(amount))
        # print(all_amount)
        return all_amount


def Result():
    daily_money = CostUsage()
    # print(daily_money)
    if daily_money > 700:
        return 1
    else:
        return 0


if __name__ == "__main__":
    Result()
