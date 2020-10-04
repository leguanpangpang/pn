#!/usr/bin/env python
#-*-coding:utf-8-*-
#Authon:芳芳

import  yaml
from common.public import filePath

class OperationYamll:
	def readYaml(self):
		with open(filePath(),'r',encoding='utf-8') as f:
			return list(yaml.safe_load_all(f))


	def dictYaml(self,fileDir='config',fileName='book.yaml'):
		with open(filePath(fileDir=fileDir,fileName=fileName),'r',encoding='utf-8') as f:
			return list(yaml.safe_load_all(f))

if __name__=='__main__':
	obj=OperationYamll()
	# print(obj.readYaml(),type(obj.readYaml()))  #结果：读取文件的内容是<class 'list'>
	# for item in obj.readYaml():  #将列表内容循环取出
	# 	print(item,type(item))  #结果：循环取出的内容是<class 'dict'>
	# print(obj.dictYaml(),type(obj.dictYaml()))
	# print(obj.dictYaml()[0]['book_002'])
	'''读取book.yaml文件的数据'''


