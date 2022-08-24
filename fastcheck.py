import os
import sys
import colorama
from domain.jsonrw import json2dic
from domain.get_md5 import *

colorama.init(autoreset=True)



def main():
    checkmd5()

    next=input('确认并退出：')


def checkmd5():
    cdir = r'./'
    filelist = list_files(cdir)
    json_md5_dic = json2dic()

    if (filelist==0):
        return 0

    nfile = 0
    checkfailed = list()
    lostfile = []
    if (json_md5_dic == 0):
        print('\033[1;31m ' + '错误：未找到md5.json文件，请检查' +' \033[0m')
        return 0
    for jsonfilename , jsonmd5 in json_md5_dic.items():
        if(jsonfilename in filelist):
            nfile += 1
            print ('正在验证第' + str(nfile) + '个文件：' + jsonfilename)
            filemd5 = get_file_md5(jsonfilename)
            if (filemd5 == jsonmd5):
                print('\033[1;32m ' + '文件' + jsonfilename + '的MD5验证通过：' + jsonmd5 + ' \033[0m')
            else:
                print('\033[1;31m ' + '文件' + jsonfilename + '的MD5校验失败，\n记录值为：' + jsonmd5 + ',实际值为' + filemd5 + ',请检查文件完整性' +' \033[0m')
                checkfailed.append(jsonfilename)
            filelist.remove(jsonfilename)
        else:
            print('\033[1;31m ' + '遇到错误，未找到文件'+ jsonfilename +' \033[0m')
            lostfile.append(jsonfilename)

    if (len(checkfailed)!=0)|(len(filelist)!=0)|(len(lostfile)!=0):
        print('校验完毕,结果如下：')
        
        print('未记录的文件：')
        for temp in filelist:
            print('\033[1;34m ' + temp + '\033[0m')
        print('MD5异常的文件：')#把校验未通过的文件列出
        for temp in checkfailed:
            print('\033[1;31m ' + temp + '\033[0m')
        print('丢失的文件：')
        for temp in lostfile:
            print('\033[1;31m ' + temp + '\033[0m')

    else:
        print('\033[1;32m ' + '验证完毕，所有文件完整' + ' \033[0m')

#列出目录下的所有文件
def list_files(filedir): 
    _files = []
    for par ,dirn, filen in os.walk(filedir):
        for filename in filen:
            _files.append(os.path.join(par,filename))
    _files.remove('./'+os.path.basename(sys.argv[0]))#获取自己的文件名，把自己移出列表.
    if './md5.json' in _files:
        _files.remove('./md5.json')               #如果存在md5.json文件，则一并排除
    if (len(_files)!=0):
        return _files
    else:
        print('\033[1;31m ' + '错误：路径下未找到需要计算的文件，请检查。程序不会计算自身和md5.json文件的md5' +' \033[0m')
        return 0

main()