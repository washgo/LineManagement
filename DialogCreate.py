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
## Class DialogCreate
###########################################################################

class DialogCreate ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"创建线路", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"地区:            ", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer11.Add( self.m_staticText7, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		m_choiceRegionChoices = []
		self.m_choiceRegion = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 200,-1 ), m_choiceRegionChoices, 0 )
		self.m_choiceRegion.SetSelection( 0 )
		bSizer11.Add( self.m_choiceRegion, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer11, 1, wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"操作系统:     ", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer6.Add( self.m_staticText4, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		m_choiceOSChoices = []
		self.m_choiceOS = wx.Choice( self, wx.ID_ANY, wx.Point( -1,-1 ), wx.Size( 200,-1 ), m_choiceOSChoices, 0 )
		self.m_choiceOS.SetSelection( 0 )
		bSizer6.Add( self.m_choiceOS, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"配置信息:     ", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer12.Add( self.m_staticText8, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		m_choicePlanChoices = []
		self.m_choicePlan = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 200,-1 ), m_choicePlanChoices, 0 )
		self.m_choicePlan.SetSelection( 0 )
		bSizer12.Add( self.m_choicePlan, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer12, 1, wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"项目名称:     ", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer7.Add( self.m_staticText5, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_textCtrlProject = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer7.Add( self.m_textCtrlProject, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer7, 1, wx.EXPAND, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"数量:            ", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer9.Add( self.m_staticText6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_textCtrlNum = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer9.Add( self.m_textCtrlNum, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer9, 1, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_buttonCreate = wx.Button( self, wx.ID_OK, u"创建", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_buttonCreate, 0, wx.ALL, 5 )

		self.m_buttonCancel = wx.Button( self, wx.ID_CANCEL, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_buttonCancel, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer10, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer5 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_choiceRegion.Bind( wx.EVT_CHOICE, self.select_region )
		self.m_choiceOS.Bind( wx.EVT_CHOICE, self.select_os )
		self.m_choicePlan.Bind( wx.EVT_CHOICE, self.select_plan )
		self.m_buttonCreate.Bind( wx.EVT_BUTTON, self.create_line )
		self.m_buttonCancel.Bind( wx.EVT_BUTTON, self.cancel_line )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def select_region( self, event ):
		event.Skip()

	def select_os( self, event ):
		event.Skip()

	def select_plan( self, event ):
		event.Skip()

	def create_line( self, event ):
		event.Skip()

	def cancel_line( self, event ):
		event.Skip()


