import os
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client, get_tracker_conf
from django.conf import settings


class FDFSDstorage(Storage):
    """
    自定义文件存储类
    """
    def _open(self, name, mode='rb'):
        # 打开文件时使用
        pass

    def _save(self, name, content):
        # 保存文件时使用
        # name：选择上传文件的名称
        # content: 包含上传文件内容的File类的对象

        # 获取配置文件
        path = get_tracker_conf(settings.BASE_DIR + '/utils/fdfs/client.conf')
        
        # 创建一个Fdfs_client对象
        client = Fdfs_client(path)

        # 上传文件到fastdfs系统中
        res = client.upload_by_buffer(content.read())

        # 判断内容是否判断成功
        if res.get('Status') != "Upload successed.":
            # 上传失败
            raise Exception("上传文件到fast dfs失败")
        else:
            # 获取返回文件ID
            filename = res.get('Remote file_id')
        
        # 返回保存文件，这里返回的是什么，数据表里面就会保存什么内容,注意返回类型为bytes类型
        return filename.decode()

    def exists(self, name):
        # Django判断文件名是否可用
        return False