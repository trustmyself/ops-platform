try:
    import boto3
    # import json
    import csv
    # from datetime import date, datetime
except ImportError:
    pass

ec2 = boto3.resource('ec2')


def main():
    for i in ec2.instances.all():
        if i.state["Name"] == "stopped":
            tag_list_all = []
            taglist = []
            taglist.append(i.id)
            taglist.append(i.private_ip_address)
            taglist.append(i.instance_type)
            '''
            for j in i.tags:
                taglist.append(j['Value'])
            '''
            for blockname, blockvalue in enumerate(i.block_device_mappings):
                ec2_volume_type = ec2_VolumeType(blockvalue['Ebs']['VolumeId'])
                ec2_volume_size = ec2_VolumeSize(blockvalue['Ebs']['VolumeId'])
                ec2_volume_price = ec2_VolumePrice(blockvalue['Ebs']['VolumeId'])
                taglist.append(blockvalue['DeviceName'])
                taglist.append(blockvalue['Ebs']['VolumeId'])
                taglist.append(ec2_volume_type)
                taglist.append(ec2_volume_size)
                taglist.append(ec2_volume_price)
            tag_list_all += taglist
            write_csv(csv_name, tag_list_all)


def ec2_VolumeType(volumeID):
    volume1 = ec2.Volume(volumeID)
    return volume1.volume_type


def ec2_VolumeSize(volumeID):
    volume2 = ec2.Volume(volumeID)
    return volume2.size


def ec2_VolumePrice(volumeID):
    ec2_type = ec2_VolumeType(volumeID)
    ec2_size = ec2_VolumeSize(volumeID)
    if ec2_type == "gp2":
        return str(ec2_size*0.1)
    elif ec2_type == "io1":
        return str(ec2_size*0.125)
    elif ec2_type == "st1":
        return str(ec2_size*0.045)
    elif ec2_type == "sc1":
        return str(ec2_size*0.025)
    else:
        return "None"


def write_csv(csvname, list):
    kika = open(csvname, 'a+')
    writer = csv.writer(kika)
    writer.writerow(list)
    kika.flush()
    kika.close()


def create_csv(name):
    kk = open(name, 'a+')
    writer = csv.writer(kk)
    # writer.writerow(['EC2InstanceID', 'Private_ip_address', 'Instance_type', 'TagName', 'TagGroup', 'TagProject', 'DeviceName', 'VolumeID', 'VolumeType', 'VolumeSize', 'VolumePrice'])
    writer.writerow(['EC2InstanceID', 'Private_ip_address', 'Instance_type', 'DeviceName', 'VolumeID', 'VolumeType', 'VolumeSize', 'VolumePrice'])
    kk.flush()
    kk.close()
    main()


if __name__ == '__main__':
    csv_name = "kika_aws_ec2_stopInstance_info.csv"
    create_csv(csv_name)
