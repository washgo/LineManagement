from DialogCreate import DialogCreate
import plan, operatingsystem, server, region
import wx
import threading

class DialogCreateWindow(DialogCreate):
	def __init__(self, parent):
		super().__init__(parent)

		self.name = parent.get_select_apikey_name()
		self._initialize_data()
		self._initialize_ui()

	def _initialize_data(self):
		self._regions = {}
		self._oss = {}
		self._plans = {}

		self._initialize_region_data()
		self._initialize_os_data()
		self._initialize_plan_data()

	def _initialize_region_data(self):
		'''
		初始化region的数据
		'''
		self._regions = region.read_region_config(self.name)

	def _initialize_os_data(self):
		'''
		初始化os的数据
		'''
		self._oss = operatingsystem.read_config(self.name)

	def _initialize_plan_data(self):
		'''
		初始化plan的数据
		'''
		self._plans = plan.read_config(self.name)

	def _get_region_list(self):
		'''
		获取region的列表
		'''
		region_list = []
		for region_dcid in self._regions:
			region_item = self._regions[region_dcid]
			region_list.append('%s - %s'%(region_dcid,region_item['name']))
		return region_list

	def _get_os_list(self):
		'''
		获取os的列表
		'''
		os_list = []
		for item_osid in self._oss:
			item = self._oss[item_osid]
			os_list.append('%s - %s'%(item_osid,item['name']))
		return os_list

	def _get_plan_list(self):
		# available_plans = self._regions[region_dcid]['available_plans']
		plan_list = []
		for plan_id in self._plans:
			plan_id = str(plan_id)
			if plan_id in self._plans.keys():
				plan_item = self._plans[plan_id]
				plan_list.append('%s - %s'%(plan_id,plan_item['name']))
		return plan_list

	def _initialize_ui(self):
		self._initialize_region_ui()
		self._initialize_os_ui()

	def _initialize_region_ui(self):
		'''
		初始化region的ui
		'''
		region_list = self._get_region_list()
		if len(region_list) > 0:
			self.m_choiceRegion.SetItems(region_list)

		# 刚初始化时，手动触发一次选择
		region_dcid = self.get_current_region_dcid()
		self._initialize_plan_ui(region_dcid)

	def _initialize_os_ui(self):
		'''
		初始化os的ui
		'''
		os_list = self._get_os_list()
		if len(os_list) > 0:
			self.m_choiceOS.SetItems(os_list)

	def _initialize_plan_ui(self, region_dcid):
		'''
		初始化plan的ui
		'''
		plan_list = self._get_plan_list()
		if len(plan_list) > 0:
			self.m_choicePlan.SetItems(plan_list)

	def select_region( self, event ):
		'''
		选择region事件
		'''
		region_dcid = self.get_current_region_dcid()
		self.set_choice_plans_by_region_dcid(region_dcid)

	def get_current_region_dcid(self):
		'''
		获取当前选择的region的dcid
		'''
		region_dcid = ''
		selectedRow = self.m_choiceRegion.GetSelection()
		if selectedRow > 0:
			select_region_value = self.m_choiceRegion.GetString(selectedRow)
			region_dcid = select_region_value.split('-')[0].strip()
		return region_dcid

	def set_choice_plans_by_region_dcid(self, region_dcid):
		'''
		设置plan的choice
		'''
		if region_dcid == '':
			return
		available_plans = self._regions[region_dcid]['available_plans']
		plan_list = []
		for plan_id in available_plans:
			plan_id = str(plan_id)
			if plan_id in self._plans.keys():
				plan_item = self._plans[plan_id]
				plan_list.append('%s - %s'%(plan_id,plan_item['name']))
		self.m_choicePlan.SetItems(plan_list)
	
	def create_line( self, event ):
		'''
		创建线路
		'''
		select_region = self.m_choiceRegion.GetString(self.m_choiceRegion.GetSelection())
		region_dcid = select_region.split('-')[0].strip()
		
		select_os = self.m_choiceOS.GetString(self.m_choiceOS.GetSelection())
		osid = select_os.split('-')[0].strip()

		if self.m_choicePlan.GetCurrentSelection() < 0:
			wx.MessageBox('配置信息为空','警告',wx.OK|wx.ICON_INFORMATION)
			return
		select_plan = self.m_choicePlan.GetString(self.m_choicePlan.GetSelection())
		plan_id = select_plan.split('-')[0].strip()

		project_name = self.m_textCtrlProject.GetValue()

		server_num = self.m_textCtrlNum.GetValue()
		if server_num == None or server_num == '':
			wx.MessageBox('未设置创建服务器数量','警告',wx.OK|wx.ICON_INFORMATION)
			return

		thread = threading.Thread(target=self.create_server, 
									args=(region_dcid, plan_id, osid, project_name, server_num))
		thread.start()

		self.EndModal(wx.ID_OK)

	def create_server(self, region_dcid, plan_id, osid, project_name, server_num):
		'''
		创建服务器
		'''
		for i in range(int(server_num)):
			server.create_server(self.name, region_dcid, plan_id, osid, project_name, project_name)
		wx.CallAfter(self.callback_update)

	def callback_update(self):
		'''
		回调更新
		'''
		thread = threading.Thread(target=self.Parent.update_server_data_by_create)
		thread.start()

	def cancel_line( self, event ):
		'''
		取消
		'''
		self.EndModal(wx.ID_CANCEL)