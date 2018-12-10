try:
    import boto3
    # from datetime import datetime, timedelta
    # import time
    # import json
except ImportError:
    pass


client = boto3.client('athena')


def GetQueryExecutionTime():
    response_id = client.list_query_executions(
        MaxResults=100
    )
    for id in response_id['QueryExecutionIds']:
        response = client.get_query_execution(
            QueryExecutionId=id
        )
        Submissiondatetime = response['QueryExecution']['Status']['SubmissionDateTime']
        DatascannedInBytes = response['QueryExecution']['Statistics']['DataScannedInBytes']
        submit_time_local = Submissiondatetime.strftime("%Y-%m-%d %H:%M:%S")
        real_size = convert_bytes(DatascannedInBytes)
        # return id, submit_time_local, real_size
        print(id, submit_time_local, real_size)


def convert_bytes(bytes):
    if bytes < 1024:  # 比特
        bytes = str(round(bytes, 2)) + ' B'  # 字节
    elif bytes >= 1024 and bytes < 1024 * 1024:
        bytes = str(round(bytes / 1024, 2)) + ' KB'  # 千字节
    elif bytes >= 1024 * 1024 and bytes < 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024, 2)) + ' MB'  # 兆字节
    elif bytes >= 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024, 2)) + ' GB'  # 千兆字节
    elif bytes >= 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024, 2)) + ' TB'  # 太字节
    elif bytes >= 1024 * 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024 / 1024, 2)) + ' PB'  # 拍字节
    elif bytes >= 1024 * 1024 * 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024 / 1024 /1024, 2)) + ' EB'  # 艾字节
    return bytes


def main():
    # get athena id
    # query_id = GetAllQueryExecutionID()
    # query_exe_id, submit_time, data_scan_size = GetQueryExecutionTime()
    # print(query_exe_id, submit_time, data_scan_size)
    GetQueryExecutionTime()


if __name__ == '__main__':
    main()
