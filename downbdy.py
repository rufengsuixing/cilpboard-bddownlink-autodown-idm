import os
import subprocess
import time
import win32clipboard
import win32con
# the download target folder
tar = 'C:/Users/yuan/Downloads/help'
# idm
idmpath = 'C:/app/IDM/IDMan.exe'
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
	/f   本地_文件_名 - 定义要保存的文件到本地的文件名
	/q - IDM 将在成功下载之后退出。这个参数只为第一个副本工作
	/h - IDM 将在成功下载之后挂起您的连接
	/n - 当不要 IDM 询问任何问题时启用安静模式
	/a - 添加一个指定的文件 用 /d 到下载队列，但是不能开始下载
	参数 /a, /h, /n, /q, /f 本地_文件_名,  /p 本地_路径工作只在您指定文件下载 /d URL
    '''
    param = '"' + idmpath + '"/a /n /d "' + url + '" /p ' + targetdir
    a = subprocess.Popen(param)
    a.wait()
    a.kill()

def main():
    global tar
    if tar[-1]=='/':
        tar=tar[:-1]
    downloaddir=tar
    cl_b = clipboard()
    while 1:
        cl_b_d = cl_b.getnew()
        if cl_b_d.find('全部文件') != -1:
            cl_b_d = cl_b_d.replace('...', '')
            dirli = cl_b_d.split('>')[1:]
            downloaddir = tar + '/' + '/'.join(dirli)
            if not os.path.isdir(downloaddir):
                os.makedirs(downloaddir)
            print(downloaddir)
        elif cl_b_d.find("www.baidupcs.com") != -1:
            cl_b_d = cl_b_d.replace('\r', '')
            downli = cl_b_d.split('\n')
            print('get ', len(downli), 'rar links')
            for a in downli:
                idm_down(a, targetdir=downloaddir)
        elif cl_b_d.find("d.pcs.baidu.com") != -1:
            cl_b_d = cl_b_d.replace('\r', '')
            downli = cl_b_d.split('\n')
            print('get ', len(downli), ' links')
            for a in downli:
                idm_down(a, targetdir=downloaddir)
if __name__ == "__main__":
    main()
