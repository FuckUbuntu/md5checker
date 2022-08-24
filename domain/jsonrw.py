import os
import json


def json2dic():
    if (os.path.exists('md5.json')):   #检查一下有没有保存的json文件
        jsonfile = open('md5.json', 'r')
        jsvalue = jsonfile.read()
        dic = json.loads(jsvalue)    #转换成字典后赋值，return
        return dic
    else:
        print('当前路径下未找到md5.json文件，请检查。')
        return 0

def dic2json(dic):
    jsvalue = json.dumps(dic)     #把字典转换成json
    with open('md5.json', 'w') as json_file:
        json_file.write(jsvalue)