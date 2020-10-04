#!/usr/bin/env python
#-*-coding:utf-8-*-
#Authon:芳芳

'''
执行模块中某一条测试用例的写法：
pytest.main(["-s","-v","test_book.py::TestBook::test_book_002"])
test_book.py：模块
TestBook：是类
test_book_002：测试用例
'''

'''
添加书籍的目的就是获取id，后面才可以查看这本书籍的信息，删除这本书的信息，
这就涉及到参数的关联。处理的思路：将ID写到文件中，然后将它读取出来，然后传进去。
就涉及到url的处理
'''
from base.method import Requests
from utils.operationYaml import OperationYaml
from utils.operationExcel import  OperationExcel
from common.public import *
import pytest
import json


obj=Requests()
objYaml=OperationYaml()



class TestBook:
	excel=OperationExcel()
	obj=Requests()

	def result(self,r,row):
		'''将期望结果和协议状态码封装到一个函数'''
		assert r.status_code==200
		assert self.excel.getExpect(row=row) in json.dumps(r.json(), ensure_ascii=False)

	def test_book_001(self):
		'''获取所有书籍的信息'''
		r=self.obj.get(url=self.excel.getUrl(row=1))
		# print(r.json())
		# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
		# print(self.excel.getExpect(row=2))
		# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
		assert self.excel.getExpect(row=1) in json.dumps(r.json(),ensure_ascii=False)
		self.result(r=r,row=1)
	#
	def test_book_002(self):
		'''添加书籍'''
		r=self.obj.post(
			url=self.excel.getUrl(row=2),
			json=self.excel.getJson(row=2)
		)
		# print(r.text)
		# print(type(json.dumps(r.json(), ensure_ascii=False)))  #结果：<class 'str'>
		# print(json.dumps(r.json(),ensure_ascii=False))
		# print(type(r.json()))  #<class 'dict'>
		# print(r.json())
		# print(type(r.json()[0]['datas']['id']))  #获取id  结果： <class 'int'>
		print(r.json()[0]['datas']['id'])  #获取id
		bookID=r.json()[0]['datas']['id']
		writeContent(content=bookID)  #将ID写入到bookID中
		# self.result(r=r,row=2)  #断言封装为函数，调用函数报错
		self.excel.getExpect(row=2) in json.dumps(r.json(), ensure_ascii=False)  #断言

	def test_book_003(self):
		'''查看书籍'''
		r=self.obj.get(url=self.excel.getUrl(row=3))
		print(r.url)  #获取响应的url
		print(r.json())
		print(r.json()['datas'][0]['id'])
		self.result(r=r,row=3)
		# self.excel.getExpect(row=2) in json.dumps(r.json(),ensure_ascii=False)

	def test_book_004(self):
		'''编辑书籍信息'''
		r=self.obj.put(
			url=self.excel.getUrl(row=4),
			json=self.excel.getJson(row=4)
		)
		self.result(r=r, row=4)

	def test_book_005(self):
		'''删除一条记录'''
		r=self.obj.delete(
			url=self.excel.getUrl(row=5)
		)
		# print(r.json)
		self.result(r=r,row=5)


if __name__=='__main__':
	pytest.main(["-s", "-v", "test_book.py"])
	# pytest.main(["-s","-v","test_book.py::TestBook::test_book_002"])
	'''执行模块中某一条测试用例的写法'''

