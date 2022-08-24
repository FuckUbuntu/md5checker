import os
import sys
import colorama
from domain.jsonrw import *
from domain.get_md5 import *


colorama.init(autoreset=True)

def main():
    print("m : MD5校验，对目录下的所有文件计算MD5并保存\nc : CheckMD5，对保存的MD5验证，确保文件完整性。")
    todo = input("请输入(m/c，默认c):")
    if ((todo == 'c') | (len(todo) == 0)): #用len判断输入是否为空，如果为空就默认执行校验。
        print("开始校验MD5")
        checkmd5()
    elif (todo == 'm'):
        print("开始计算并保存MD5")
        computemd5()
    else:
        main()
    
    def choose():
        print('r:重新选择\nl:退出程序')
        nexttodo=input("请输入(r/l):")
        if (nexttodo == 'l'):
            return 0
        elif(nexttodo == 'r'):
            main()
        else:
            choose()

    choose()


#计算并写入MD5---m
def computemd5(): 
    cdir = r'./'    #查找范围为自身所在的路径
    filelist = list_files(cdir)
    nfile = 0
    dic = {}
    if(filelist==0):
        return 0

    for thefile in filelist:   #遍历list下的所有文件
        nfile = nfile + 1
        print('\033[1;33m ' + '正在计算第' + str(nfile) + '个文件：' + thefile + '的MD5' + ' \033[0m')
        filemd5 = get_file_md5(thefile)#调用上面的函数，计算出MD5值。
        print ('\033[1;32m ' + '第' + str(nfile) + '个文件:' + thefile + ',MD5计算完成：' + filemd5 + ' \033[0m')
        dic[thefile] = filemd5

    dic2json(dic)
    print ('\033[1;32m ' + '全部文件MD5计算完毕，已自动保存为json文件' + ' \033[0m')

def checkmd5():
    cdir = r'./'
    filelist = list_files(cdir)
    json_md5_dic = json2dic()

    if (filelist==0):
        return 0


    nfile = 0
    checkfailed = list()
    if (json_md5_dic == 0):
        print('\033[1;31m ' + '错误：未找到md5.json文件，请检查' +' \033[0m')
        return 0
    for jsonfilename , jsonmd5 in json_md5_dic.items():
        nfile += 1
        print ('正在验证第' + str(nfile) + '个文件：' + jsonfilename)
        filemd5 = get_file_md5(jsonfilename)
        if (filemd5 == jsonmd5):
            print('\033[1;32m ' + '文件' + jsonfilename + '的MD5验证通过：' + jsonmd5 + ' \033[0m')
        else:
            print('\033[1;31m ' + '文件' + jsonfilename + '的MD5校验失败，\n记录值为：' + jsonmd5 + ',实际值为' + filemd5 + ',请检查文件完整性' +' \033[0m')
            checkfailed.append(jsonfilename)
        filelist.remove(jsonfilename)
    print('校验完毕,结果如下：')
    print('MD5异常的文件：')#把校验未通过的文件列出
    for temp in checkfailed:
        print('\033[1;31m ' + temp + '\033[0m')
    print('未记录的文件：')
    for temp in filelist:
        print('\033[1;34m ' + temp + '\033[0m')

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