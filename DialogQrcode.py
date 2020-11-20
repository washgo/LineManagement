# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DialogQrcode
###########################################################################

class DialogQrcode ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"二维码", pos = wx.DefaultPosition, size = wx.Size( 300,360 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.Size( -1,-1 ), wx.DefaultSize )

		bSizer27 = wx.BoxSizer( wx.VERTICAL )

		self.m_bitmapQrcode = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 300,300 ), 0 )
		self.m_bitmapQrcode.SetMinSize( wx.Size( 300,300 ) )

		bSizer27.Add( self.m_bitmapQrcode, 0, wx.ALL, 5 )

		self.m_buttonSave = wx.Button( self, wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.m_buttonSave, 0, wx.ALL, 5 )


		self.SetSizer( bSizer27 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


