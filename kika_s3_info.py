try:
    import boto3
    import json
    import csv
    from datetime import date, datetime
except ImportError:
    pass

client = boto3.client('s3')


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def main():
    bucket_all = client.list_buckets()
    dict2 = {}
    dict2 = bucket_all["Buckets"]

    for element in dict2:
        tag_list_all = []
        # tag_list = []
        if element['Name'] == 'kika-share':
            continue
        else:
            bucket_location_region = client.get_bucket_location(
                Bucket=element['Name']
            )
            try:
                bucket_tagging = client.get_bucket_tagging(
                    Bucket=element['Name']
                )
                for ele in bucket_tagging['TagSet']:
                    tag_list = []
                    tag_list.append(ele['Value'])
                    tag_list_all += tag_list
            except Exception:
                tag_list_all.append('None')
            info_list = []
            info_list.insert(0, element['Name'])
            info_list.insert(1, bucket_location_region['LocationConstraint'])
            info_list.insert(2, tag_list_all)
            # print(info_list)
            write_csv(csv_name, info_list)


def write_csv(csvname, list):
    kika = open(csvname, 'a+')
    writer = csv.writer(kika)
    # writer.writerow(['BucketName', 'Region', 'Tag'])
    writer.writerow(list)
    kika.flush()
    kika.close()


def create_csv(name):
    kk = open(name, 'a+')
    writer = csv.writer(kk)
    writer.writerow(['BucketName', 'Region', 'Tag'])
    kk.flush()
    kk.close()
    main()


if __name__ == '__main__':
    csv_name = "kika_aws_s3_info7.csv"
    create_csv(csv_name)
