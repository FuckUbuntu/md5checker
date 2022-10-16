import hashlib
import imp
import os
import sys

#计算md5方法
#增加进度条输出


def get_file_md5(fname): 
    md = hashlib.md5()
    filesize = os.path.getsize(fname)#获取文件大小
    fullparts = parts(filesize,4096)#获取总共的分块数量，这里是以4096为单位
    finishedpart = 0
    with open(fname,'rb') as fobj:  #打开文件fname，以rb，即只读二进制方式读取
        while True:
            data = fobj.read(4096)
            if not data:
                print('|finished')
                break
            finishedpart += 1
            progress = (finishedpart*100) // fullparts
            print ('\r'+'progressing |' + '█' * (progress // 2) + '-'*(50-(progress // 2)) + '|' , end ='')
            md.update(data)#更新对象内容
    return md.hexdigest()  #返回完整对象的MD5

def parts(size,leng):
    if size < leng:
        npart =1
        return npart
    npart = size // leng
    if (size % leng != 0):
        npart += 1
    return npart