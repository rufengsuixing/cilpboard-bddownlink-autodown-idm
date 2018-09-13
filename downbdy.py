import os
import subprocess
import time
import win32clipboard
import win32con
#复制百度云里面的路径如 全部文件>19政治>2019【徐涛】...>01 基础班
#可以一层一层复制，这样省略的路径会自动补全,但是层数太多仍然有bug
#然后用油猴脚本获取下载链接并复制到剪贴板，就会安排自动加入队列,并且自动开始队列下载
# the download target folder
tar = 'C:/Users/yuan/Downloads/help'
# idm
idmpath = 'C:/app/IDM/IDMan.exe'
downloadimmediately=True
class clipboard():
	def __init__(self):
		self.new = self.__get()
		print('clipboard success')

	def __get(self):
		win32clipboard.OpenClipboard()
		if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
			d = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
		else:
			d=''
		win32clipboard.CloseClipboard()
		return d
	def get(self):
		d = self.__get()
		self.new = d
		return d

	def getnew(self):
		while 1:
			d = self.__get()
			if d == self.new:
				time.sleep(1)
			else:
				self.new = d
				return d
class linkdata():
	def __init__(self):
		self.dic={}
	def add(self,path,li):
		try:
			self.dic[path]
		except:
			self.dic[path]=[]
		self.dic[path]+=li
	def downloadall(self):
		for path in self.dic:
			for link in self.dic[path]:
				idm_down(link, targetdir=path)
		self.dic={}

def idm_down(url, targetdir=tar, idmpath=idmpath):
	'''
	add the url into idm download list

	:Parameters:
		url : str
			The url of the file
		name : str
			The name of the download file you want
		targetdir : str
			The folder you want to put the file

	:return:`None`
	'''
	'''
	/d URL - 下载一个文件
		 例如： IDMan.exe /d "http://www.internetdownloadmanager.com/path/File Name.zip" 
	/s - 开始任务调度里的队列
	/p 本地_路径 - 定义要保存的文件放在哪个本地路径
	/f	 本地_文件_名 - 定义要保存的文件到本地的文件名
	/q - IDM 将在成功下载之后退出。这个参数只为第一个副本工作
	/h - IDM 将在成功下载之后挂起您的连接
	/n - 当不要 IDM 询问任何问题时启用安静模式
	/a - 添加一个指定的文件 用 /d 到下载队列，但是不能开始下载
	参数 /a, /h, /n, /q, /f 本地_文件_名,	/p 本地_路径工作只在您指定文件下载 /d URL
	'''
	param = '"' + idmpath + '"/a /n /d "' + url + '" /p "' + targetdir +'"'
	a = subprocess.Popen(param)
	a.wait()
	a.kill()
def idm_start(url, targetdir=tar, idmpath=idmpath):
	param = '"' + idmpath + '"/s'
	a = subprocess.Popen(param)
	a.wait()
	a.kill()

class fixpathdata():
	def __init__(self,downloadimmediately=True):
		self.data=[[]]
		self.d_i=downloadimmediately
		self.usedorder=[]	
	def fixpath(self,li):
		flag=True
		for a in range(len(li)):
			try:
				self.data[a]
			except:
				self.data+=[[]]
			ne=li[a]
			try:
				for c in range(len(self.usedorder)):
					if ne == self.data[a][self.usedorder[c][a]]:
						break
			except:
				pass
			for b in range(len(self.data[a])):
				da=self.data[a][b]
				if li[0]==da and flag:
					if b==0:
						flag=False
					else:
						flag=b
						print("debug 路径错位，可能下载错文件夹了，尝试修复")
						orderli=self.addused(li,fake=True)
						for c in range(len(self.usedorder)):
							if self.usedorder[c][flag:flag+2]==orderli[0:2]:
								for d in range(flag):
									li.insert(d,self.data[d][self.usedorder[c][d]])
								break
						return self.fixpath(li)
					# da=self.data[a][b+flag]
				if ne.find(da)!=-1:
					self.data[a][b]=ne
					break
				elif da.find(ne)!=-1:
					li[a]=da
					break
			else:
				self.data[a]+=[ne]
		return li
	def tryinputname(self,st):
		for a in range(len(self.data)):
			for b in range(len(self.data[a])):
				if st[:len(self.data[a][b])]==self.data[a][b]:
					self.data[a][b]=st
		return
	def addused(self,li,fake=False):
		order=[]
		for a in range(len(li)):
			try:
				order+=[self.data[a].index(li[a])]
			except:
				return None
		if order in self.usedorder:
			return True
		else:
			if not fake:
				self.usedorder+=order
			else:
				return order

def main():
	fixp=fixpathdata(downloadimmediately)
	if not downloadimmediately:
		dir_link=linkdata()
	global tar
	if tar[-1]=='/':
		tar=tar[:-1]
	downloaddir=tar
	cl_b = clipboard()
	while 1:
		cl_b_d = cl_b.getnew()
		if cl_b_d.find("d.pcs.baidu.com") != -1 or cl_b_d.find("www.baidupcs.com") != -1:
			cl_b_d = cl_b_d.replace('\r', '')
			downli = cl_b_d.split('\n')
			print('get ', len(downli), ' links')
			if not os.path.isdir(downloaddir):
				os.makedirs(downloaddir)
			if downloadimmediately:
				for a in downli:
					idm_down(a, targetdir=downloaddir)
				fixp.addused(li)
				idm_start()
			else:
				dir_link.add(downloaddir,downli)
		elif cl_b_d.find(">") != -1:
			cl_b_d = cl_b_d.replace('...', '')
			while cl_b_d[-1]==".":
				cl_b_d=cl_b_d[:-1]
			while cl_b_d[0]==".":
				cl_b_d=cl_b_d[1:]
			dirli = cl_b_d.split('>')[1:]
			li=fixp.fixpath(dirli)
			downloaddir = os.path.join(tar,*li)
			print(downloaddir)
		elif cl_b_d[:5]=="start":
			if not downloadimmediately:
				dir_link.downloadall()
				idm_start()
		else:
			fixp.tryinputname(cl_b_d)
			li=fixp.fixpath(dirli)
			
if __name__ == "__main__":
	main()
