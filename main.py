import wx, wx._adv, wx._html
from MainWindow import MainWindow

if __name__=='__main__':
	app = wx.App()
	mainWindow = MainWindow()
	mainWindow.Show()
	app.MainLoop()