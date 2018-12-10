try:
    import boto3
    # import json
    import csv
    # from datetime import date, datetime
except ImportError:
    pass


def main():
    client = boto3.client('ec2')
    response = client.describe_snapshots(
        Filters=[
            {
                'Name': 'status',
                'Values': [
                    'completed',
                ],
            },
        ],
    )
    list1 = response['Snapshots']
    # listall = []
    for i in list1:
        if i['OwnerId'] == "011383927026":
            ssid = i['SnapshotId']
            sssize = i['VolumeSize']
            sstime = i['StartTime']
            ssdis = i['Description']
            snapshot_price = CostAccounting(sssize)
            list2 = []
            list2.append(ssid)
            list2.append(sssize)
            list2.append(sstime)
            list2.append(ssdis)
            list2.append(snapshot_price)
            # listall += list2
            write_csv(csv_name, list2)


def CostAccounting(size):
    cost = size*0.05
    return cost


def write_csv(csvname, list):
    kika = open(csvname, 'a+')
    writer = csv.writer(kika)
    writer.writerow(list)
    kika.flush()
    kika.close()


def create_csv(name):
    kk = open(name, 'a+')
    writer = csv.writer(kk)
    writer.writerow(['SnapShotID', 'SnapShotSize/G', 'SnapShotStarttime', 'SnapShotDescription', 'SnapShotPrice/$/Month'])
    kk.flush()
    kk.close()
    main()


if __name__ == '__main__':
    csv_name = "kika_aws_ec2_snapshot_info.csv"
    create_csv(csv_name)
