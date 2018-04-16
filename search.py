#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,shutil
import re

from selenium import webdriver  
import time  
import urllib 

OUTPUT_DIR = '/Users/liyu20/Documents/运动'

SEARCH_KEY_WORDS = ['羽毛球','羽毛球拍','篮球','足球','乒乓球拍','网球拍','台球桌','弓箭','跑步机','动感单车']

PAGE_NUM = 15

repeateNum = 0
preLen = 0

def getSearchUrl(keyWord):
	if(isEn(keyWord)):
		return 'https://www.google.com.hk/search?q=' + keyWord + '&safe=strict&source=lnms&tbm=isch'
	else:
		return 'https://www.google.com.hk/search?q=' + keyWord + '&safe=strict&hl=zh-CN&source=lnms&tbm=isch'

def isEn(keyWord):  
	return all(ord(c) < 128 for c in keyWord)

# 启动Firefox浏览器  
driver = webdriver.Firefox()

if os.path.exists(OUTPUT_DIR) == False:
	os.makedirs(OUTPUT_DIR)

def output(SEARCH_KEY_WORD):
	global repeateNum
	global preLen

	print('搜索' + SEARCH_KEY_WORD + '图片中，请稍后...')

	# 爬取页面地址  
	url = getSearchUrl(SEARCH_KEY_WORD);
	#'http://pic.sogou.com/pics?query=%CA%D6%BB%FA&w=05009900&p=40030500&_asf=pic.sogou.com&_ast=1422627003&sc=index&sut=1376&sst0=1422627002578'  
	  
	# 目标元素的xpath  
	xpath = '//div[@id="rg"]/div/div/a/img'
	#'//div[@id="imgid"]/ul/li/a/img'  

	# 浏览器打开爬取页面  
	driver.get(url)  

	outputFile = OUTPUT_DIR + '/' + SEARCH_KEY_WORD + '.txt'
	outputSet = set()

	# 模拟滚动窗口以浏览下载更多图片  
	pos = 0  
	m = 0 # 图片编号  
	for i in range(PAGE_NUM):  
		pos += i*600 # 每次下滚600  
		js = "document.documentElement.scrollTop=%d" % pos  
		driver.execute_script(js)  
		time.sleep(1)
		for element in driver.find_elements_by_xpath(xpath):
			img_url = element.get_attribute('src')
			if img_url is not None and img_url.startswith('http'):
				outputSet.add(img_url)
		if preLen == len(outputSet):
			if repeateNum == 2:
				repeateNum = 0
				preLen = 0
				break
			else:
				repeateNum = repeateNum + 1
		else:
			repeateNum = 0
			preLen = len(outputSet)

	print('写入' + SEARCH_KEY_WORD + '图片中，请稍后...')
	file = open(outputFile, 'wr')
	for val in outputSet:
		file.write(val + '\n')
	file.close()

	print(SEARCH_KEY_WORD+'图片搜索写入完毕')
	print(len(outputSet))

for val in SEARCH_KEY_WORDS:
	output(val)

driver.close()

