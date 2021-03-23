from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client


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
    
        # 创建一个Fdfs_client对象
        client = Fdfs_client('./utils/fdfs/cloent.conf')

        # 上传文件到fastdfs系统中
        res = client.upload_by_buffer(content.read())

        # 判断内容是否判断成功
        if res.get('Status') != "Upload successed.":
            # 上传失败
            raise Exception("上传文件到fast dfs失败")
        else:
            # 获取返回文件ID
            filename = res.get('Remote file_id')
        
        # 返回保存文件，这里返回的是什么，数据表里面就会保存什么内容
        return filename

    def exists(self, name):
        # Django判断文件名是否可用
        return False