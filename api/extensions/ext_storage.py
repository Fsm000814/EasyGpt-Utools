import os
import shutil
from contextlib import closing
from typing import Union, Generator

import boto3
from botocore.exceptions import ClientError
from flask import Flask

class Storage:
    def __init__(self):
        self.storage_type = None
        self.bucket_name = None
        self.client = None
        self.folder = None

    def init_app(self, app: Flask):
        # 初始化应用程序配置
        self.storage_type = app.config.get('STORAGE_TYPE')
        if self.storage_type == 's3':
            # 使用S3存储
            self.bucket_name = app.config.get('S3_BUCKET_NAME')
            self.client = boto3.client(
                's3',
                aws_secret_access_key=app.config.get('S3_SECRET_KEY'),
                aws_access_key_id=app.config.get('S3_ACCESS_KEY'),
                endpoint_url=app.config.get('S3_ENDPOINT'),
                region_name=app.config.get('S3_REGION')
            )
        else:
            # 使用本地存储
            self.folder = app.config.get('STORAGE_LOCAL_PATH')
            if not os.path.isabs(self.folder):
                self.folder = os.path.join(app.root_path, self.folder)

    def save(self, filename, data):
        if self.storage_type == 's3':
            # 将数据保存到S3存储桶中
            self.client.put_object(Bucket=self.bucket_name, Key=filename, Body=data)
        else:
            # 将数据保存到本地文件系统中
            if not self.folder or self.folder.endswith('/'):
                filename = self.folder + filename
            else:
                filename = self.folder + '/' + filename

            folder = os.path.dirname(filename)
            os.makedirs(folder, exist_ok=True)

            with open(os.path.join(os.getcwd(), filename), "wb") as f:
                f.write(data)

    def load(self, filename: str, stream: bool = False) -> Union[bytes, Generator]:
        if stream:
            return self.load_stream(filename)
        else:
            return self.load_once(filename)

    def load_once(self, filename: str) -> bytes:
        if self.storage_type == 's3':
            try:
                with closing(self.client) as client:
                    # 从S3存储桶中加载数据
                    data = client.get_object(Bucket=self.bucket_name, Key=filename)['Body'].read()
            except ClientError as ex:
                if ex.response['Error']['Code'] == 'NoSuchKey':
                    # 文件不存在
                    raise FileNotFoundError("文件未找到")
                else:
                    raise
        else:
            if not self.folder or self.folder.endswith('/'):
                filename = self.folder + filename
            else:
                filename = self.folder + '/' + filename

            if not os.path.exists(filename):
                # 文件不存在
                raise FileNotFoundError("文件未找到")

            with open(filename, "rb") as f:
                data = f.read()

        return data

    def load_stream(self, filename: str) -> Generator:
        def generate(filename: str = filename) -> Generator:
            if self.storage_type == 's3':
                try:
                    with closing(self.client) as client:
                        # 从S3存储桶中以流式方式加载数据
                        response = client.get_object(Bucket=self.bucket_name, Key=filename)
                        for chunk in response['Body'].iter_chunks():
                            yield chunk
                except ClientError as ex:
                    if ex.response['Error']['Code'] == 'NoSuchKey':
                        # 文件不存在
                        raise FileNotFoundError("文件未找到")
                    else:
                        raise
            else:
                if not self.folder or self.folder.endswith('/'):
                    filename = self.folder + filename
                else:
                    filename = self.folder + '/' + filename

                if not os.path.exists(filename):
                    # 文件不存在
                    raise FileNotFoundError("文件未找到")

                with open(filename, "rb") as f:
                    while chunk := f.read(4096):  # 以4KB的块读取数据
                        yield chunk

        return generate()

    def download(self, filename, target_filepath):
        if self.storage_type == 's3':
            # 将文件从S3存储桶中下载到目标文件路径
            with closing(self.client) as client:
                client.download_file(self.bucket_name, filename, target_filepath)
        else:
            if not self.folder or self.folder.endswith('/'):
                filename = self.folder + filename
            else:
                filename = self.folder + '/' + filename

            if not os.path.exists(filename):
                # 文件不存在
                raise FileNotFoundError("文件未找到")

            shutil.copyfile(filename, target_filepath)

    def exists(self, filename):
        if self.storage_type == 's3':
            with closing(self.client) as client:
                try:
                    # 检查S3存储桶中是否存在文件
                    client.head_object(Bucket=self.bucket_name, Key=filename)
                    return True
                except:
                    return False
        else:
            if not self.folder or self.folder.endswith('/'):
                filename = self.folder + filename
            else:
                filename = self.folder + '/' + filename

            return os.path.exists(filename)

storage = Storage()

def init_app(app: Flask):
    storage.init_app(app)