#!/usr/bin/env python
#-*-coding:utf-8-*-
#Authon:芳芳

'''写入的文件是str类型'''

import  os
import datetime
'''对地址的封装'''
# print(os.path.dirname(os.path.dirname(__file__)))

# base_url=os.path.dirname(os.path.dirname(__file__))
# print(os.path.join(base_url,'data','login.yaml'))

def filePath(fileDir='datass',fileName='login.yaml'):
	'''
	当前目录切换到要读取文件的目录
	:param fileDir:目录
	:param fileName: 文件的名称
	:return:
	'''
	return os.path.join(os.path.dirname(os.path.dirname(__file__)),fileDir,fileName)

def basePath():
	return os.path.dirname(os.path.dirname(__file__))

def writeContent(content):
	print('写的时间：',datetime.datetime.now())
	with open(filePath(fileDir='data',fileName='bookID'),'w') as f:
		f.write(str(content))
		'''写入的文件是str类型'''

def readContent():
	print('读的时间：', datetime.datetime.now())
	with open(filePath(fileDir='data',fileName='bookID'),'r') as f:
		return f.read()

# print(basePath())
# # print(filePath('base','method'))
# print(filePath())
# print(filePath('config','book.yaml'))
writeContent('1')
# print(readContent())


