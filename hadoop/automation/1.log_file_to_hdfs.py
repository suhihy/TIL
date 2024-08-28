from hdfs import InsecureClient
import os

hdfs_client = InsecureClient('http://localhost:9870', user='ubunto')

local_logs_path = '/home/ubunto/dmf/automation/logs/'
hdfs_logs_path = 'input/logs/'

local_files = os.listdir(local_logs_path)

for file_name in local_files:
    local_file_path = local_logs_path + file_name
    hdfs_file_path = hdfs_logs_path + file_name

    if hdfs_client.content(hdfs_file_path, strict=False):
        print(f'이미 존재함 {file_name}')
    else:
        hdfs_client.upload(hdfs_file_path, local_file_path)
        print(f'업로드 완료 {file_name}')