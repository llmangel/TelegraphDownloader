import concurrent.futures
import os
import re
import requests
import sys
import TelegramDownloaderGui

from PyQt5 import QtWidgets
from qt_material import apply_stylesheet

floderTitleName = ''


def getFileName(url) -> list:
    global floderTitleName
    resp = requests.get(url=url).text
    fileNameList = re.findall(r'<img src="/file/(.*?).jpg">', resp)
    floderTitle = re.findall(r'<title>(.*?)</title>', resp)
    floderTitleName = floderTitle[0]

    # floderTitle = re.findall(r'<title>(.*?)</title>', mystr.test_str)
    # floderTitleName = floderTitle[0]
    fileNameList = re.findall(r'<img src="/file/(.*?).jpg">', resp)
    r = []
    for i in fileNameList:
        r.append('https://telegra.ph/file/{}.jpg'.format(i))
    print(r)
    return r


class Downloader(TelegramDownloaderGui.Ui_TgInterface, QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.cwd = os.getcwd()
        self.downloadCwd = self.cwd
        # self.tgurl = imageDownload("")

    def chooseDir(self):
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件夹", self.cwd)
        self.FileLine.setText(dirName)
        if dirName == "":
            self.FileLine.setText(self.cwd)
        self.downloadCwd = dirName

    def dirCreate(self):

        # print("floadername", floderTitleName)
        print(r'{}\{}'.format(self.downloadCwd, floderTitleName))
        if not os.path.exists(r'{}\{}'.format(self.downloadCwd, floderTitleName)):
            os.mkdir(r'{}\{}'.format(self.downloadCwd, floderTitleName))
            print('*' * 50)
        else:
            print("文件夹存在，开始下载")

    def signalImgDownload(self, url):
        image = requests.get(url=url).content
        with open(r'{}\{}\{}.jpg'.format(self.downloadCwd, floderTitleName, url.split('/')[-1]), 'wb') as f:
            f.write(image)

    def startDownload(self):
        imglist = getFileName(url=self.urlLine.text())
        print(len(imglist))
        print(floderTitleName)
        self.dirCreate()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            pool.map(self.signalImgDownload, imglist)
        self.urlLine.setText("下载完成")
        # 创建以title命名的文件夹


# 다운로드

def show_loginWindow():
    app = QtWidgets.QApplication(sys.argv)  # 实例化 QApplication 类，作为 GUI 主
    MainWindow = QtWidgets.QMainWindow()  # 创建 MainWindow
    ui = Downloader()  # 实例化 UI 类
    ui.setupUi(MainWindow)
    ui.FileLine.setText(os.getcwd())
    # *************************************
    ui.PathButton.clicked.connect(ui.chooseDir)
    ui.DownloadButton.clicked.connect(ui.startDownload)
    # *************************************
    apply_stylesheet(app, theme='dark_teal.xml')
    MainWindow.show()  # 显示窗体
    sys.exit(app.exec_())




if __name__ == '__main__':
    show_loginWindow()
