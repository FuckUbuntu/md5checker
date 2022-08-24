import hashlib

#计算md5方法

def get_file_md5(fname):
    md = hashlib.md5()
    with open(fname,'rb') as fobj:  #打开文件fname，以rb，即只读二进制方式读取
        while True:
            data = fobj.read(4096)
            if not data:
                break
            md.update(data)#更新对象内容
    return md.hexdigest()  #返回完整对象的MD5