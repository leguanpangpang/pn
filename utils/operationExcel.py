
'''
第185节:【框架设计】API框架设计与案例实战(十一)
'''
import xlrd
from common.public import *
from utils.operationYaml import OperationYaml
import requests


class ExcelVarles:
	'''分离excel列，放列封装到类ExcelVarles中'''
	caseID=0
	des=1
	url=2
	method=3
	data=4
	expect=5

	@property
	def getCaseID(self):
		return self.caseID

	@property
	def description(self):
		return self.des

	@property
	def getUrl(self):
		return  self.url

	@property
	def getMethod(self):
		return self.method

	@property
	def getData(self):
		return self.data

	@property
	def getExpect(self):
		return self.expect


class OperationExcel(OperationYaml):
	def getSheet(self):
		'''获取sheet页'''
		# book=xlrd.open_workbook(filePath('data','books.xlsx'))
		book=xlrd.open_workbook(filePath('data','api.xlsx'))
		return book.sheet_by_index(0)
	@property
	def getRows(self):
		'''获取总行数'''
		return self.getSheet().nrows

	@property
	def getCols(self):
		'''获取总列数'''
		return self.getSheet().ncols

	def getValue(self,row,col):
		'''获取excel中行和列对应的具体值'''
		return self.getSheet().cell_value(row,col)

	def getCaseID(self,row):
		return self.getValue(row,col=ExcelVarles().getCaseID)

	def getUrl(self,row):
		url=self.getValue(row=row,col=ExcelVarles().getUrl)
		if '{bookID}' in url:
			return str(url).replace('{bookID}', readContent())
		else:
			return url

	def getMethod(self,row):
		'''读取excel中method'''
		return self.getValue(row,col=ExcelVarles().getMethod)

	def getData(self,row):
		'''读取excel中请求参数data'''
		return self.getValue(row,col=ExcelVarles().getData)

	def getJson(self,row):
		'''通过data读取的值映射book.yaml文件对应的内容'''
		return self.dictYaml()[0][self.getData(row=row)]

	def getExpect(self,row):
		return self.getValue(row,col=ExcelVarles().getExpect)

	def getExcelDatas(self):
		'''获取excel的sheet页的首行title'''
		datas=list()
		title=self.getSheet().row_values(0)
		print(title)  #打印excel的首行title
		for row in range(1,self.getSheet().nrows):
			'''
			将所有的数据取出，放到Datas中
			for：对所有的循环取出
			zip：就是将两个值放到元组中，然后通过dict强制转化为dict
			'''
			row_values=self.getSheet().row_values(row)
			datas.append(dict(zip(title,row_values)))
		return datas




if __name__=='__main__'	:
	obj=OperationExcel()
	# print(obj.getCols)
	# print(obj.getRows)
	# print(obj.getValue(2,1))
	# print(obj.getValue(2,ExcelVarles().description()))
	# print(obj.getCaseID(row=2))
	# print(obj.getUrl(row=3))
	# print(obj.getMethod(row=2))
	# print(obj.getExpect(row=2))
	# print(obj.getData(row=5))
	# print(obj.getJson(row=2),type(obj.getJson(row=2)))  #结果为：<class 'dict'>
	# print(obj.getExcelDatas())

	for item in obj.getExcelDatas():
		print(item)



