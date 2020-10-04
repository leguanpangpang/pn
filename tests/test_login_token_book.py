'''第190节:【框架设计】API框架设计与案例实战(十六)'''
'''
判断请求参数，但是读取excel中的请求参数是字符串的数据类型，但是要的是json格式的字符串
Username，wuya，password，asd888都要带双引号，不然读取无法解析。
读取的是字符串，要的是字典，而且有的请求参数是空的，故请求参数的内容需要做判断。
请求头也需要做判断，也是key对应的value值。为空不处理，不为空，反序列化为字典。
如何处理请求参数：

'''


from common.public import *
from base.method import Requests
from utils.operationExcell import OperationExcell,ExcelVarles
import pytest
import json
import allure  #目的生成测试报告

excel=OperationExcell()
obj=Requests()

'''方法一'''
# @pytest.mark.parametrize('datas',excel.params())  #对list当中的所有数据进行循环取出，就是字典类型
# def test_login_book(datas):
# 	'''通过循环list获取可执行的用例,对请求参数做反序列化处理'''
# 	print(datas)  #通过调用excel.params()对请求参数为空的处理
# 	# print(type(datas))
# 	# print(datas[ExcelVarles.caseUrl])  #获取key对应的url地址
# 	# print(datas[ExcelVarles.params],type(datas[ExcelVarles.params]))  #excel中取出的参数为<class 'str'>
# 	# params=datas[ExcelVarles.params]  #从Excel中取出请求参数
# 	# print(excel.params())
# 	# for item in obj.params():
# 	# 	print(item)

'''方法二'''
@pytest.mark.parametrize('datas',excel.runs())  #对list当中的所有数据进行循环取出，就是字典类型
def test_login_book(datas):
	'''通过循环list获取可执行的用例,对请求参数做反序列化处理'''
	# print(datas)
	# # print(type(datas))
	# print(datas[ExcelVarles.caseUrl])  #获取key对应的url地址
	# # print(datas[ExcelVarles.params],type(datas[ExcelVarles.params]))  #excel中取出的参数为<class 'str'>
	params = datas[ExcelVarles.params]  # 从Excel中取出请求参数
	if len(str(params).strip())==0:
		pass
	elif len(str(params).strip())>=0:
		params=json.loads(params)
		# print(params)


	'''对请求头做反序列化的处理'''
	header=datas[ExcelVarles.header]
	# print(headers)
	# print(type(headers))
	if len(str(header).strip())==0:
		pass
	elif len(str(header).strip())>=0:
		header=json.loads(header)  #结果：<class 'dict'> 切记：请求头必须是dict类型
		# print(header,type(header))

	'''
	1、先获取到所有前置测试点的测试用例
	2、执行前置测试点
	3、获取它的结果信息
	4、拿他的结果信息替换对应测试点的变量
	'''
	'''执行前置条件关联的测试点'''

	# print(datas[ExcelVarles.casePre])  #从Excel中读取casePre="前置条件"的内容
	# print(excel.case_prev(datas[ExcelVarles.casePre]))  #执行所有测试用例

	r=obj.post(
		url=excel.case_prev(datas[ExcelVarles.casePre])[ExcelVarles.caseUrl],
		# url=excel.case_prev('login')[ExcelVarles.caseUrl],
		json=json.loads(excel.case_prev(datas[ExcelVarles.casePre])[ExcelVarles.params])
		# json = json.loads(excel.case_prev('login')[ExcelVarles.params])
	)
	# print(r.text)
	# print(r.json())  #响应结果是token
	# print(type(r.json()))  #结果：<class 'dict'>
	prevResult = r.json()['access_token'] #生成token值
	# print(prevResult)


	'''替换被关联测试点中请求头信息的变量'''
	header = excel.prevHeaders(prevResult)
	# print(header)  #获取请求头参数
	# print(type(header)) #<class 'dict'>

	'''状态码'''
	status_code=int(datas[ExcelVarles.status_code]) #Excel中取出的数据是字符串，要转化为整形
	# print(status_code)
	# print(type(status_code))

	def case_assert_result(r):
		'''断言的封装'''
		assert r.status_code==status_code
		assert datas[ExcelVarles.expect] in json.dumps(r.json(), ensure_ascii=False)

	def getUrl():
		'''分离url'''
		return str(datas[ExcelVarles.caseUrl]).replace('{bookID}', readContent())


	# if datas[ExcelVarles.method]=='get':
	# 	'''获取所有书籍'''
	# 	r=obj.get(
	# 		url=datas[ExcelVarles.caseUrl],
	# 		headers=header
	# 	)
	# 	print(type(json.dumps(r.json(),ensure_ascii=False)))
	# 	# print(json.dumps(r.json(),ensure_ascii=False))
	# 	# print(r.json()['datas'][0]['name']) #响应数据中文乱码
	# 	# assert datas[ExcelVarles.expect] in json.dumps(r.json()['datas'][0]['name'], ensure_ascii=False)
	# 	# assert datas[ExcelVarles.expect] in json.dumps(r.json(), ensure_ascii=False)
	# 	case_assert_result(r=r)
	# 	print('get请求:',r.url)

	if datas[ExcelVarles.method]=='get':
		'''获取所有书籍'''
		if '/books' in datas[ExcelVarles.caseUrl]:
			r = obj.get(
				url=datas[ExcelVarles.caseUrl],
				headers=header
			)
			# print(type(json.dumps(r.json(), ensure_ascii=False)))
			# print(json.dumps(r.json(),ensure_ascii=False))
			# print(r.json()['datas'][0]['name']) #响应数据中文乱码
			# assert datas[ExcelVarles.expect] in json.dumps(r.json()['datas'][0]['name'], ensure_ascii=False)
			# assert datas[ExcelVarles.expect] in json.dumps(r.json(), ensure_ascii=False)
			case_assert_result(r=r)
			# print('获取所有书籍的get请求:', r.url)
		else:
			# url=str(datas[ExcelVarles.caseUrl]).replace('{bookID}',readContent())
			r=obj.get(url=getUrl(),headers=header)
			# print('查看书籍信息的get请求:',r.url)
			# print(json.dumps(r.json(), ensure_ascii=False))
			case_assert_result(r=r)

	elif datas[ExcelVarles.method]=='post':
		'''添加书籍'''
		r=obj.post(
			url=datas[ExcelVarles.caseUrl],
			json=params,
			headers=header
		)
		# print('@@@@@@: ',params)
		# print(r.json())
		# print(type(r.json()))  #<class 'list'>
		# print(json.dumps(r.json(),ensure_ascii=False))
		# print(r.text)  #响应数据中文乱码
		# status_code=int(datas[ExcelVarles.expect])
		# assert r.status_code==status_code
		# assert datas[ExcelVarles.expect] in json.dumps(r.json(),ensure_ascii=False)
		case_assert_result(r=r)  #通过函数写断言
		# print(r.json()[0]['datas']['id'])  #获取id
		writeContent(content=str(r.json()[0]['datas']['id']))  #int类型不能写入文件中，必须是str数据类型可以写入文件中
		# print('添加post请求:',r.url)

	elif datas[ExcelVarles.method]=='put':
		# url=str(datas[ExcelVarles.caseUrl]).replace('{bookID}',readContent())
		# print(url)
		r=obj.put(url=getUrl(), json=params, headers=header)
		# print(header)
		# print(type(header))  #<class 'dict'>
		# print('更新put请求:', r.url)
		# print(params)
		# # print(type(params))
		# print(r.json())
		case_assert_result(r=r)  #断言
		# print(datas[ExcelVarles.expect] )
		# assert datas[ExcelVarles.expect] in json.dumps(r.json()['msg'], ensure_ascii=False)  #断言




	elif datas[ExcelVarles.method]=='delete':
		# url=str(datas[ExcelVarles.caseUrl]).replace('{bookID}',readContent())
		# print(url)
		r=obj.delete(url=getUrl(),headers=header)
		# print(r.json())
		case_assert_result(r=r)
		# assert datas[ExcelVarles.expect] in json.dumps(r.json(), ensure_ascii=False)
		# print('delete请求:',r.url)


allure.title("API测试报告")





if __name__=='__main__':
	pytest.main(["-s","-v","test_login_token_book.py","--alluredir","./report/result"])
	import subprocess
	subprocess.call('allure generate report/result/ -o report/html --clean',shell=True)
	subprocess.call('allure open -h 127.0.0.1 -p 8088 ./report/html',shell=True)  #127.0.0.1，只能本地可以访问
	subprocess.call('allure open -h 0.0.0.0 -p 8088 ./report/html', shell=True)  #IP写成 0.0.0.0 ，外网可以访问




