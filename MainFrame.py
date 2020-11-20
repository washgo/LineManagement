# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"线路管理", pos = wx.DefaultPosition, size = wx.Size( 800,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 800,700 ), wx.Size( 800,700 ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticTextVps = wx.StaticText( self, wx.ID_ANY, u"平台:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextVps.Wrap( -1 )

		bSizer26.Add( self.m_staticTextVps, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		m_choiceVPSChoices = [ u"Vultr" ]
		self.m_choiceVPS = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 90,-1 ), m_choiceVPSChoices, 0 )
		self.m_choiceVPS.SetSelection( 0 )
		bSizer26.Add( self.m_choiceVPS, 0, wx.ALL, 5 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"API-Key:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer26.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_textCtrlAPIKey = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 320,-1 ), 0 )
		bSizer26.Add( self.m_textCtrlAPIKey, 0, wx.ALL, 5 )

		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"名称:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		bSizer26.Add( self.m_staticText16, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_textCtrlName = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.m_textCtrlName, 0, wx.ALL, 5 )

		self.m_buttonSetAPIKey = wx.Button( self, wx.ID_ANY, u"设置API-Key", wx.DefaultPosition, wx.Size( -1,23 ), 0 )
		bSizer26.Add( self.m_buttonSetAPIKey, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer26, 1, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer34 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"API :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		bSizer34.Add( self.m_staticText18, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		m_choiceNameChoices = []
		self.m_choiceName = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 90,-1 ), m_choiceNameChoices, 0 )
		self.m_choiceName.SetSelection( 0 )
		bSizer34.Add( self.m_choiceName, 0, wx.ALL, 5 )

		self.m_buttonUpdate = wx.Button( self, wx.ID_ANY, u"更新数据", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer34.Add( self.m_buttonUpdate, 0, wx.ALL, 5 )

		self.m_buttonStopUpdate = wx.Button( self, wx.ID_ANY, u"停止更新", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer34.Add( self.m_buttonStopUpdate, 0, wx.ALL, 5 )


		bSizer2.Add( bSizer34, 1, wx.EXPAND, 5 )

		bSizer35 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_buttonCreate = wx.Button( self, wx.ID_ANY, u"创建线路", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer35.Add( self.m_buttonCreate, 0, wx.ALL, 5 )

		self.m_buttonDelete = wx.Button( self, wx.ID_ANY, u"删除线路", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer35.Add( self.m_buttonDelete, 0, wx.ALL, 5 )

		self.m_buttonStart = wx.Button( self, wx.ID_ANY, u"开启线路", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer35.Add( self.m_buttonStart, 0, wx.ALL, 5 )

		self.m_buttonStop = wx.Button( self, wx.ID_ANY, u"停止线路", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer35.Add( self.m_buttonStop, 0, wx.ALL, 5 )

		self.m_buttonRestart = wx.Button( self, wx.ID_ANY, u"重启线路", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer35.Add( self.m_buttonRestart, 0, wx.ALL, 5 )


		bSizer2.Add( bSizer35, 1, wx.EXPAND, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer29 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"服务:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		bSizer29.Add( self.m_staticText19, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		m_choiceServiceChoices = []
		self.m_choiceService = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 90,-1 ), m_choiceServiceChoices, 0 )
		self.m_choiceService.SetSelection( 0 )
		bSizer29.Add( self.m_choiceService, 0, wx.ALL, 5 )

		self.m_buttonBuildService = wx.Button( self, wx.ID_ANY, u"安装服务", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer29.Add( self.m_buttonBuildService, 0, wx.ALL, 5 )

		self.m_buttonStartService = wx.Button( self, wx.ID_ANY, u"启动服务", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer29.Add( self.m_buttonStartService, 0, wx.ALL, 5 )

		self.m_buttonStopService = wx.Button( self, wx.ID_ANY, u"停止服务", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer29.Add( self.m_buttonStopService, 0, wx.ALL, 5 )


		bSizer18.Add( bSizer29, 1, wx.EXPAND, 5 )

		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_gaugeProgress = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 280,-1 ), wx.GA_HORIZONTAL )
		self.m_gaugeProgress.SetValue( 0 )
		bSizer19.Add( self.m_gaugeProgress, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticTextUpdateStatus = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticTextUpdateStatus.Wrap( -1 )

		bSizer19.Add( self.m_staticTextUpdateStatus, 0, wx.ALIGN_CENTER|wx.ALIGN_RIGHT|wx.ALL, 5 )


		bSizer18.Add( bSizer19, 1, wx.EXPAND, 5 )


		bSizer1.Add( bSizer18, 1, wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer23 = wx.BoxSizer( wx.VERTICAL )

		self.m_gridLine = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 800,250 ), 0 )

		# Grid
		self.m_gridLine.CreateGrid( 0, 13 )
		self.m_gridLine.EnableEditing( False )
		self.m_gridLine.EnableGridLines( True )
		self.m_gridLine.EnableDragGridSize( False )
		self.m_gridLine.SetMargins( 0, 0 )

		# Columns
		self.m_gridLine.SetColSize( 0, 0 )
		self.m_gridLine.SetColSize( 1, 100 )
		self.m_gridLine.SetColSize( 2, 120 )
		self.m_gridLine.SetColSize( 3, 120 )
		self.m_gridLine.SetColSize( 4, 100 )
		self.m_gridLine.SetColSize( 5, 120 )
		self.m_gridLine.SetColSize( 6, 70 )
		self.m_gridLine.SetColSize( 7, 70 )
		self.m_gridLine.SetColSize( 8, 70 )
		self.m_gridLine.SetColSize( 9, 0 )
		self.m_gridLine.SetColSize( 10, 0 )
		self.m_gridLine.SetColSize( 11, 0 )
		self.m_gridLine.SetColSize( 12, 0 )
		self.m_gridLine.EnableDragColMove( False )
		self.m_gridLine.EnableDragColSize( True )
		self.m_gridLine.SetColLabelSize( 30 )
		self.m_gridLine.SetColLabelValue( 0, u"id" )
		self.m_gridLine.SetColLabelValue( 1, u"名称" )
		self.m_gridLine.SetColLabelValue( 2, u"IP" )
		self.m_gridLine.SetColLabelValue( 3, u"操作系统" )
		self.m_gridLine.SetColLabelValue( 4, u"地区" )
		self.m_gridLine.SetColLabelValue( 5, u"项目名称" )
		self.m_gridLine.SetColLabelValue( 6, u"服务器状态" )
		self.m_gridLine.SetColLabelValue( 7, u"电源状态" )
		self.m_gridLine.SetColLabelValue( 8, u"服务列表" )
		self.m_gridLine.SetColLabelValue( 9, u"密码" )
		self.m_gridLine.SetColLabelValue( 10, u"服务端口" )
		self.m_gridLine.SetColLabelValue( 11, u"服务密码" )
		self.m_gridLine.SetColLabelValue( 12, u"generation" )
		self.m_gridLine.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_gridLine.EnableDragRowSize( True )
		self.m_gridLine.SetRowLabelSize( 80 )
		self.m_gridLine.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_gridLine.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer23.Add( self.m_gridLine, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer4.Add( bSizer23, 1, wx.EXPAND, 5 )


		bSizer1.Add( bSizer4, 1, 0, 5 )

		bSizer191 = wx.BoxSizer( wx.VERTICAL )

		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_textCtrlCommand = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,-1 ), 0 )
		bSizer20.Add( self.m_textCtrlCommand, 0, wx.ALL, 5 )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_buttonInteractive = wx.Button( self, wx.ID_ANY, u"连接", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer22.Add( self.m_buttonInteractive, 0, wx.ALL, 5 )

		self.m_buttonCommand = wx.Button( self, wx.ID_ANY, u"执行", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer22.Add( self.m_buttonCommand, 0, wx.ALL, 5 )

		self.m_buttonClear = wx.Button( self, wx.ID_ANY, u"清除", wx.DefaultPosition, wx.Size( 70,23 ), 0 )
		bSizer22.Add( self.m_buttonClear, 0, wx.ALL, 5 )


		bSizer20.Add( bSizer22, 1, 0, 5 )


		bSizer191.Add( bSizer20, 1, 0, 5 )

		bSizer21 = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrlReseponse = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,400 ), wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.VSCROLL )
		bSizer21.Add( self.m_textCtrlReseponse, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer191.Add( bSizer21, 1, wx.EXPAND, 5 )


		bSizer1.Add( bSizer191, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_timerGrid = wx.Timer()
		self.m_timerGrid.SetOwner( self, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_buttonSetAPIKey.Bind( wx.EVT_BUTTON, self.set_api_key )
		self.m_choiceName.Bind( wx.EVT_CHOICE, self.choice_name )
		self.m_buttonUpdate.Bind( wx.EVT_BUTTON, self.button_update_data )
		self.m_buttonStopUpdate.Bind( wx.EVT_BUTTON, self.button_stop_update )
		self.m_buttonCreate.Bind( wx.EVT_BUTTON, self.create_line )
		self.m_buttonDelete.Bind( wx.EVT_BUTTON, self.delete_line )
		self.m_buttonStart.Bind( wx.EVT_BUTTON, self.start_server )
		self.m_buttonStop.Bind( wx.EVT_BUTTON, self.stop_server )
		self.m_buttonRestart.Bind( wx.EVT_BUTTON, self.restart_server )
		self.m_buttonBuildService.Bind( wx.EVT_BUTTON, self.build_service )
		self.m_buttonStartService.Bind( wx.EVT_BUTTON, self.start_service )
		self.m_buttonStopService.Bind( wx.EVT_BUTTON, self.stop_service )
		self.m_gridLine.Bind( wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.grid_context )
		self.m_gridLine.Bind( wx.grid.EVT_GRID_SELECT_CELL, self.grid_select_cell )
		self.m_buttonInteractive.Bind( wx.EVT_BUTTON, self.interactive_server )
		self.m_buttonCommand.Bind( wx.EVT_BUTTON, self.command_execute )
		self.m_buttonClear.Bind( wx.EVT_BUTTON, self.command_clear )
		self.Bind( wx.EVT_TIMER, self.timer_update, id=wx.ID_ANY )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def set_api_key( self, event ):
		event.Skip()

	def choice_name( self, event ):
		event.Skip()

	def button_update_data( self, event ):
		event.Skip()

	def button_stop_update( self, event ):
		event.Skip()

	def create_line( self, event ):
		event.Skip()

	def delete_line( self, event ):
		event.Skip()

	def start_server( self, event ):
		event.Skip()

	def stop_server( self, event ):
		event.Skip()

	def restart_server( self, event ):
		event.Skip()

	def build_service( self, event ):
		event.Skip()

	def start_service( self, event ):
		event.Skip()

	def stop_service( self, event ):
		event.Skip()

	def grid_context( self, event ):
		event.Skip()

	def grid_select_cell( self, event ):
		event.Skip()

	def interactive_server( self, event ):
		event.Skip()

	def command_execute( self, event ):
		event.Skip()

	def command_clear( self, event ):
		event.Skip()

	def timer_update( self, event ):
		event.Skip()


