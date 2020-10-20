#coding=utf-8
import urllib
import urllib2
import re
import csv
import codecs

with open("centadata.csv","wt") as csvfile:
	#csvfile.write(codecs.BOM_UTF8)
	writer = csv.writer(csvfile)
	writer.writerow(['Name','Address','Type','Property Age','No. of units', 'Transactions in last 180 days', 'Latest transaction unit price'])
	class Tool:
		removeqst = re.compile('\?')

		def replace(self,x):
			x = re.sub(self.removeqst, u'邨', x)
			return x.strip()
	class Centadata:

		def __init__(self, baseurl, region):
			self.baseurl = baseurl
			self.region = '?type=district17&code='+str(region)
			self.tool = Tool()

		def getpage(self, pagenum):
			try:
				url = self.baseurl + self.region + '&info=&code2=lord:~lordtype:~tabIdx:0&page=' + str(pagenum)
				request = urllib2.Request(url)
				response = urllib2.urlopen(request, context = ctx)
				return response
			except urllib2.URLError, e:
				if hasattr(e, "reason"):
					print u"连接失败，错误原因：", e.reason
					return None
		def getdata(self):
			page = self.getpage(0).read().decode('big5')
			pattern1 = re.compile(u'共(.*?)頁',re.S)
			result = re.search(pattern1,page)
			if result is None:
				m=1
			else:
				m=int(result.group(1))+1
			for i in range(0, m):
				page1 = self.getpage(i).read().decode('big5')
				pattern2 = re.compile('<span style="text-decoration:underline">(.*?)</span>.*?;</td><td class="tdscp1addr">(.*?)&nbsp;&nbsp;</td><td class="tdscp1type">(.*?)&nbsp;&nbsp;</td><td class="tdscp1bldgage">(.*?)&nbsp;&nbsp;</td><td class="tdscp1unitcnt">(.*?)&nbsp;&nbsp;</td><td class="tdscp1vol">(.*?)&nbsp;&nbsp;</td><td class="tdscp1Suprice">(.*?)(&|<).*?</td>', re.S)
				items = re.findall(pattern2, page1)
				for item in items:
					#writer.writerow([item[0].encode('utf-8')])
					#print item[0], " ", item[1], " ",item[2], " ",item[3], " ",item[4], " ",item[5], " ",item[6], " ", "\n"
					writer.writerow([item[0].encode('utf-8')])
					#,item[1].encode('utf-8'),item[2].encode('utf-8'),item[3],item[4],item[5],item[6]
	baseURL = 'http://www1.centadata.com/paddresssearch1.aspx'
#print u'香港', '\n'
	for n in range(101, 118):
		if n =='103':
			continue
		cdt = Centadata(baseURL, n)
		cdt.getdata()
#print u'九龍', '\n'
	for n in range(201, 221):
		cdt = Centadata(baseURL, n)
		cdt.getdata()
#print u'新界東', '\n'
	for n in range(301, 309):
		if n =='305':
			continue
		cdt = Centadata(baseURL, n)
		cdt.getdata()
#print u'新界西和大嶼山', '\n'
	for n in range(401, 410):
		cdt = Centadata(baseURL, n)
		cdt.getdata()
	cdt = Centadata(baseURL, 309)
	cdt.getdata()
	cdt = Centadata(baseURL, 103)
	cdt.getdata()

