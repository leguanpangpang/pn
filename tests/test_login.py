#!/usr/bin/env python
#-*-coding:utf-8-*-
#Authon:芳芳
'''
为什么@pytest.markparametrize(‘data’,objYaml.readYaml())中data参数化的只有一个参数，
这就是单个API强大的地方，是参数化所在，在参数化的价值观或者意义同样的操作步骤，
写一个用例就能实现所有测试点的测试，对,objYaml.readYaml()：就是将yaml文件中所有数据放在列表中，
通过传值（data）循环执行列表中数据。


@pytest.mark.parametrize:pytest的参数化对列表的元素进行循环处理
'''
''' @pytest.mark.parametrize的实例'''
# import  pytest

# def add(a,b):
# 	return a+b
#
# @pytest.mark.parametrize('a,b,result',[
# 	(1,2,3),
# 	(2,2,4)
# ])
#
# def test_add(a,b,result):
# 	assert add(a,b)==result

# if __name__=='__main__':
# 	pytest.main(["-v","test_login.py"])

'''第184节:【框架设计】API框架设计与案例实战(十)'''

'''
pytest.main(["-s","-s","test_login.py"])中-s：输出打印的信息，即调试信息，-v：输出详细信息
'''
'''调式一'''
# import pytest
# from base.method import  Requests
# from utils.operationYaml import OperationYaml
#
# obj=Requests()
# objYaml=OperationYaml()
#
# @pytest.mark.parametrize('data',objYaml.readYaml())
# def test_login(data):
# 	# print(type(data)) #结果：<class 'dict'>
# 	# print(data['data'])  #取出字典data的内容
# 	print(type(data['data'])) #
# if __name__=='__main__':
# 	pytest.main(["-s","-s","test_login.py"])





'''调式二'''
'''
针对单个的API的，将全部测试点放在yaml文件中，然后通过pytest.mark.parametrize当中的参数化可以很轻松的实现测试用例，实现所有的测试点。
pytest.mark.parametrize：就是将yaml文件中的测试点放在列表中，通过循环列表，把对应的值赋值进去。就是一行代码实现所有测试点的操作。
是全链路的也可以用这种方法，业务场景：就是增加角色不同的用户，例如：20个角色，40个权限，常规写60条不同的用例，但是60条用例的代码都是一样的，
不同的是传的参数不同，可以通过pytest的参数化，用一行代码将60条用例搞定了。
至于20个用户40个权限可以放到list中，将对应的值传进去，进行循环操作。这就是pytest参数化结合yaml文件，结合框架当中的一些处理，
就能够很轻松的实现针对相同的步骤，相同的业务逻辑通过一行代码实现很多点的测试内容。

'''
'''
函数式的编程思想
'''

import pytest
from base.method import  Requests
from utils.operationYaml import OperationYaml
import json

obj=Requests()
objYaml=OperationYaml()

@pytest.mark.parametrize('datas',objYaml.readYaml())
def test_login(datas):
	# print(datas['expect'],type(datas['expect']))  #<class 'dict'>
	# print(datas['expect']['username'], type(datas['expect']['username']))  #<class 'str'>
	# print(type(datas)) #结果：<class 'dict'>
	# print(datas['data'])  #取出字典data的内容
	# print(type(datas['data'])) #结果：<class 'dict'>
	# print(type(json.dumps(datas['data'])))  #结果：<class 'str'>
	# print(datas['url'])
	r=obj.post(url=datas['url'],
	           # data=datas['data'],
	           json=datas['data']
	           )
	# print(json.dumps(r.json()))  #打印为乱码
	# print(r.text)  ##打印为乱码
	# print(type(json.dumps(r.json(),ensure_ascii=False)))  #结果为<class 'str'>
	# print(json.dumps(r.json(),ensure_ascii=False))
	# assert datas['expect']['username'] in json.dumps(r.json(),ensure_ascii=False)
	assert datas['expect'] in json.dumps(r.json(), ensure_ascii=False)
	'''设置断言'''

if __name__=='__main__':
	pytest.main(["-s","-v","test_login.py"])


