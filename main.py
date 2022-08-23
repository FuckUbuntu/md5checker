import os
import hashlib
import json
import sys
import colorama
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

    dic2json('write',dic)
    print ('\033[1;32m ' + '全部文件MD5计算完毕，已自动保存为json文件' + ' \033[0m')

def checkmd5():
    cdir = r'./'
    filelist = list_files(cdir)
    json_md5_dic = dic2json('read','any')

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
    file_list = os.listdir(filedir)
    for list_leng in range(0,len(file_list)):
        path = os.path.join(filedir,file_list[list_leng])
        if os.path.isdir(path):#检查是否为文件夹，若所在目录下有文件夹，则报错。
            print("工作目录下存在文件夹，请排除。")
            return 0;
        if os.path.isfile(path):
            _files.append(path)
    _files.remove('./'+os.path.basename(__file__))#获取自己的文件名，把自己移出列表.
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
def dic2json(mode,value):
    if (mode=='write'):
        jsvalue = json.dumps(value)     #把字典转换成json
        with open('md5.json', 'w') as json_file:
            json_file.write(jsvalue)    #写入文件对象
        return True
    elif (mode=='read'):
        if (os.path.exists('md5.json')):   #检查一下有没有保存的json文件
            jsonfile = open('md5.json', 'r')
            jsvalue = jsonfile.read()
            dic = json.loads(jsvalue)    #转换成字典后赋值，return
            return dic
        else:
            print('当前路径下未找到md5.json文件，请检查。')
            return 0


main()