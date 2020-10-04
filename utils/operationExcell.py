
'''
第185节:【框架设计】API框架设计与案例实战(十五)
'''
import xlrd
from common.public import *
from utils.operationYamll import OperationYamll
import requests
import json

class ExcelVarles:
	'''分离excel列，放列封装到类ExcelVarles中'''
	caseID="测试用例ID"
	caseModel="模块"
	caseName="接口名称"
	caseUrl="请求地址"
	casePre="前置条件"
	method="请求方法"
	paramsType="请求参数类型"
	params="请求参数"
	expect="期望结果"
	isRun="是否运行"
	header="请求头"
	status_code="状态码"

	# @property
	# def getCaseID(self):
	# 	return self.caseID
	#
	# @property
	# def description(self):
	# 	return self.des
	#
	# @property
	# def getUrl(self):
	# 	return  self.url
	#
	# @property
	# def getMethod(self):
	# 	return self.method
	#
	# @property
	# def getData(self):
	# 	return self.data
	#
	# @property
	# def getExpect(self):
	# 	return self.expect


class OperationExcell(OperationYamll):
	def getSheet(self):
		'''获取sheet页'''
		# book=xlrd.open_workbook(filePath('data','books.xlsx'))
		book=xlrd.open_workbook(filePath('data','api.xlsx'))
		return book.sheet_by_index(0)

	# @property
	# def getRows(self):
	# 	'''获取总行数'''
	# 	return self.getSheet().nrows
	#
	# @property
	# def getCols(self):
	# 	'''获取总列数'''
	# 	return self.getSheet().ncols
	#
	# def getValue(self,row,col):
	# 	'''获取excel中行和列对应的具体值'''
	# 	return self.getSheet().cell_value(row,col)
	#
	# def getCaseID(self,row):
	# 	return self.getValue(row,col=ExcelVarles().getCaseID)
	#
	# def getUrl(self,row):
	# 	url=self.getValue(row=row,col=ExcelVarles().getUrl)
	# 	if '{bookID}' in url:
	# 		return str(url).replace('{bookID}', readContent())
	# 	else:
	# 		return url
	#
	# def getMethod(self,row):
	# 	'''读取excel中method'''
	# 	return self.getValue(row,col=ExcelVarles().getMethod)
	#
	# def getData(self,row):
	# 	'''读取excel中请求参数data'''
	# 	return self.getValue(row,col=ExcelVarles().getData)
	#
	# def getJson(self,row):
	# 	'''通过data读取的值映射book.yaml文件对应的内容'''
	# 	return self.dictYaml()[0][self.getData(row=row)]
	#
	# def getExpect(self,row):
	# 	return self.getValue(row,col=ExcelVarles().getExpect)

	@property
	def getExcelDatas(self):
		'''获取excel的sheet页的首行title'''
		datas=list()
		title=self.getSheet().row_values(0)
		# print(title)  #打印excel的首行title
		for row in range(1,self.getSheet().nrows):
			'''
			将所有的数据取出，放到Datas中
			for：对所有的循环取出
			zip：就是将两个值放到元组中，然后通过dict强制转化为dict
			'''
			row_values=self.getSheet().row_values(row)
			datas.append(dict(zip(title,row_values)))
		# print(datas)
		return datas

	def runs(self):
		'''获取到可执行的测试用例,y是可执行的测试用例'''
		run_list=[]
		for item in self.getExcelDatas:
			isRun=item[ExcelVarles.isRun]
			# print(isRun)
			if isRun=='y':run_list.append(item)
			else: pass
		return run_list

	def case_lists(self):
		'''获取excel中所有的测试点'''
		cases=list()
		'''list():传的是列表格式，用list()不是list[]标识'''
		for item in self.getExcelDatas:
			cases.append(item)
		return cases

	def params(self):
		'''对请求参数为空的处理'''
		params_list=[]
		for item in self.runs():
			# print(item)
			# print(type(item))  #从Excel中取出的记录为<class 'dict'>
			params=item[ExcelVarles.params] #从Excel中取出参数的key对应的value值
			# print(params,type(params))  #从Excel中取出的params为str
			if len(str(params).strip())==0:
				pass
			elif len(str(params).strip())>=0:
				params_list.append(json.loads(params))  #apppend追加的内容只能是字典类型
				# print(par)
				# print(params)
				# params
				# print(type(params))
		return  params_list # 从Excel中取出的params为str，反序列化为dict

	def case_prev(self,casePrev):
		'''
		依据前置测试条件找到关联的前置测试用例
		:param casePrev: 前置测试条件
		:return:
		'''
		# for item in self.runs():
		for item in self.case_lists():
			'''case_lists():涉及到关联，运行所有的测试用例，执行所有的测试用例'''
		# 	print(item)
			if casePrev in item.values(): #判断login 是否在value中
				# print(item)
				return item
		return None

	def prevHeaders(self,prevResult):
		'''
		替换被关联测试点的请求头变量的值
		:param preResult:
		:return:
		'''
		for item in self.runs():
			headers=item[ExcelVarles.header]
			'''从Excel中获取请求头的参数'''
			# print(header)
			# print(type(header))  #<class 'str'>
			if '{token}' in headers:
				'''验证{token}是否在header中，将登陆生成的token替换掉'''
				headers=str(headers).replace('{token}',prevResult) #prevResult替换Excel表请求头中token
				# print(header)
				return json.loads(headers)



if __name__=='__main__'	:
	obj=OperationExcell()
	# for item in obj.getExcelDatas():
		# print(item)
		# print(item[ExcelVarles.method])
		# print(item[ExcelVarles.caseUrl])
		# print(item[ExcelVarles.isRun])
	# print(obj.case_prev(ExcelVarles.casePre))

	# print(obj.runs())
	# for item in obj.runs():  #执行可执行的测试用例
	# 	print(item)
	# obj.params()
	# print(obj.params())
	# print(type(obj.params()))
	# for item in obj.params():
	# print(item)
	# print(type(obj.case_prev('login')))  #<class 'dict'>
	# print(obj.case_prev('login')[ExcelVarles.caseUrl])
	# print(obj.case_prev('login')[ExcelVarles.params])
	# print(type(obj.case_prev('login')[ExcelVarles.params])) #<class 'str'>
	# print(obj.prevHeaders(''))
	# print(obj.prevHeaders('aaa'))
	# for item in obj.case_lists():
	# 	'''循环取出Excel中的数据'''
	# 	print(item)
	# print(obj.case_prev('login'))






