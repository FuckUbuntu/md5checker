import os
import hashlib
import json
import sys
import colorama


colorama.init(autoreset=True)


def main():
    checkmd5()

    next=input('确认并退出：')

#计算md5方法
def get_file_md5(fname):
    md = hashlib.md5()
    with open(fname,'rb') as fobj:  #打开文件fname，以rb，即只读二进制方式读取
        while True:
            data = fobj.read(4096)
            if not data:
                break
            md.update(data)#更新对象内容
    return md.hexdigest()  #返回完整的对象

def checkmd5():
    cdir = r'./'
    filelist = list_files(cdir)
    json_md5_dic = dic2json()

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
    file_list = os.listdir(filedir)
    for list_leng in range(0,len(file_list)):
        path = os.path.join(filedir,file_list[list_leng])
        if os.path.isdir(path):#检查是否为文件夹，若所在目录下有文件夹，则报错。
            print("工作目录下存在文件夹，请排除。")
            return 0;
        if os.path.isfile(path):
            _files.append(path)
    _files.remove('./'+os.path.basename(sys.argv[0]))#获取自己的文件名，把自己移出列表.
    if './md5.json' in _files:
        _files.remove('./md5.json')               #如果存在md5.json文件，则一并排除
    if (len(_files)!=0):
        return _files
    else:
        print('\033[1;31m ' + '错误：路径下未找到需要计算的文件，请检查。程序不会计算自身和md5.json文件的md5' +' \033[0m')
        return 0



#创建json读取和写入的方法,分read和write，分别对应读取json到字典和把字典内容写入json。/*其实弄成def只是看得舒服而已*/
#读取的返回值是字典，写入的返回值是bool
#读取时value不调用，随便写。
def dic2json():
    if (os.path.exists('md5.json')):   #检查一下有没有保存的json文件
        jsonfile = open('md5.json', 'r')
        jsvalue = jsonfile.read()
        dic = json.loads(jsvalue)    #转换成字典后赋值，return
        return dic
    else:
        print('当前路径下未找到md5.json文件，请检查。')
        return 0


main()