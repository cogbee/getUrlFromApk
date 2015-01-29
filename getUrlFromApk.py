#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
author:jaffer tsao
time:2015-1-29
function:getUrlFromApk


apk反编译---->逐一文件读取---->匹配规则---->存入结果文件中
'''

import os
import sys
import re
import pdb
pdb.set_trace()
#设置递归深度
sys.setrecursionlimit(1000000)

'''
该类主要是来反编译apk，生成一个目录，里面是反编译之后的内容。
参数：
apk_path：这是一个路径，里面有很多apk。 目前先做一个，apk_path目前也加上了name
返回值：
暂无，可以设置一个是否反编译成功的指示值。目前不做处理，默认反编译成功。
'''
class decompile_apk(object):
	def __init__(self,apk_path):
		self.apk_path = apk_path

	def decompile_apk(self):
		os.system('apktool.jar d '+self.apk_path)

	#def getApkName(self):
'''
path 是目录，每一个apk反编译之后都有一个目录
'''
class getUrl(object):
	def __init__(self,path,save_dir):
		self.path = path
		self.urllist = []
		self.save_dir = save_dir
		self.count = 0

	def getUrlFromfile(self,filepath):
		fp = open(filepath)
		# 其余的一些url匹配模式暂时就不写
		match1 = r'http://[a-zA-Z0-9./*#:?%*&=!@\\]+'
		for line in fp.readlines():
			y = re.findall(match1,line)
			if y:
				#y 也是一个list 下面一个循环是去重
				for each in y:
					if self.urllist.count(each) == 0:
						self.urllist.append(each)
	
	#walk这个函数已经递归了。所以不需要再一次递归
	def walk_file(self,path):
		#判断是否是路径(目录)
		if not os.path.isdir(self.path):
			return
		#root遍历路径，dirs当前遍历路径下的目录，list当前遍历目录下的文件名  
		for root,dirs,files in os.walk(self.path):
			for i in files:
				#将分离的部分组成一个路径名
				file_path = os.path.join(root,i)
				self.count = self.count + 1
				self.getUrlFromfile(file_path)

	def save(self):
		#最后目录是以\结尾要去掉
		if self.path[-1] == '\\':
			self.path = self.path[0:-1]
		save_name = os.path.split(self.path)[1]
		sp = open(self.save_dir+'\\'+save_name,'w+')
		sp.write(save_name+':\n')
		for each in self.urllist:
			sp.write(each+'\n')
		sp.close()
		print 'count :' + str(self.count)


if __name__=='__main__':
	#得到脚本目录
	baseloc = sys.path[0]
	#暂时以一个名字，以后可以修改自己寻找apk后缀的，以处理多个apk情况
	apk=baseloc + '\\123.apk'
	os.mkdir('result')
	save_dir = baseloc + '\\result'
	de = decompile_apk(apk)
	de.decompile_apk()
	path = baseloc + '\\123'
	get = getUrl(path,save_dir)
	get.walk_file(path)
	get.save()
	raw_input('OK\n')

