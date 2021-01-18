from MainFrame import MainFrame
from DialogCreateWindow import DialogCreateWindow
import wx, wx._adv, wx._html
import threading, json, os, uuid
import config, server, region, operatingsystem, plan, log, service, WorkThread
import paramiko
import qrcode, base64

class MainWindow(MainFrame):
    def __init__(self):
        super().__init__(None)

        self._initialize()

    def _initialize(self):
        '''
        初始化
        '''
        self._apikeynames = {}
        self._projects = ['']
        self._servers = {}
        self._services = {}
        self._plans = {}
        self._regions = {}
        self._oss = {}
        # 正在更新状态的server的索引字典
        self._updating_server_indexs = {}
        # 进度条值
        self._gauge_value = 0
        # Grid
        self.m_gridLine.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        # popup menu
        self._popup_items = {}
        # 所有交互的ssh
        self._sshs = {}

        self._initialize_services()
        self._initialize_context_menu()
        self._initialize_api_key_name()
        self._initialize_servers()
        self._initialize_plans()
        self._initialize_regions()
        self._initialize_oss()

    def _initialize_context_menu(self):
        #设置弹出菜单
        self.grid_menu = wx.Menu()
        self.grid_menu.Append(1,"复制IP")
        self.grid_menu.Append(2, "复制密码")
        i = 3
        for service_name in self._services.keys():
            self._popup_items[i] = "生成%s配置文件"%service_name
            self.grid_menu.Append(i, "生成%s配置文件"%service_name)
            i += 1
            self._popup_items[i] = "生成%s二维码"%service_name
            self.grid_menu.Append(i, "生成%s二维码"%service_name)
            i += 1
        self.grid_menu.Bind(wx.EVT_MENU, self.popup_context, id=1, id2=7)
        # self.m_gridLine.Bind(wx.EVT_CONTEXT_MENU, self.grid_context)

    def grid_context(self, event):
        '''
        grid控件 右键事件
        '''
        # 先选择当前行
        self.m_gridLine.SelectRow(event.Row)
        services = self.get_current_grid_services()
        for key in self._popup_items.keys():
            self.grid_menu.FindItemById(key).Enable(enable=False)
            popup_name = self._popup_items[key]
            if services == '':
                continue
            for service_name in services.keys():
                if service_name in popup_name:
                    self.grid_menu.FindItemById(key).Enable(enable=True)
        # 弹出菜单
        pos = event.GetPosition()
        pos.x = pos.x + 25
        pos.y = pos.y + 110
        self.PopupMenu(self.grid_menu, pos)

    def copy_value(self, value):
        text_obj = wx.TextDataObject()
        text_obj.SetText(value)
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_obj)
            wx.TheClipboard.Close()

    def popup_context(self, event):
        '''
        选择popup menu项目
        '''
        if event.Id == 1:
            ip = self.get_current_grid_ip()
            self.copy_value(ip)
        elif event.Id == 2:
            password = self.get_current_grid_password()
            self.copy_value(password)
        elif event.Id > 2:
            for service_name in self._services.keys():
                services = self.get_current_grid_services()
                service_name_generation = ''
                if services == '':
                    wx.MessageBox('配置内容为空','警告',wx.OK|wx.ICON_INFORMATION)
                else:
                    if service_name in services.keys():
                        service_name_config = services[service_name]
                        # print(service_name_config)
                        service_name_generation = service_name_config['generation']
                    if service_name_generation != '':
                        if '配置文件' in self._popup_items[event.Id]:
                            # current_service = self.get_current_selection_service()
                            service_generation_configcontent = ''
                            if 'ConfigContent' in service_name_generation.keys():
                                service_generation_configcontent = service_name_generation['ConfigContent']
                            if service_generation_configcontent == '':
                                wx.MessageBox('配置内容为空','警告',wx.OK|wx.ICON_INFORMATION)
                            else:
                                if config.create_service_config(service_generation_configcontent):
                                    wx.MessageBox('生成配置文件成功','警告',wx.OK|wx.ICON_INFORMATION)
                                else:
                                    wx.MessageBox('生成配置文件失败','警告',wx.OK|wx.ICON_INFORMATION)
                        elif '二维码' in self._popup_items[event.Id]:
                            service_generation_sharelink = ''
                            service_generation_sharelink_prefix = ''
                            service_generation_sharelink_content = ''
                            if 'ShareLink' in service_name_generation.keys():
                                service_generation_sharelink = service_name_generation['ShareLink']
                                if 'Prefix' in service_generation_sharelink.keys():
                                    service_generation_sharelink_prefix = service_generation_sharelink['Prefix']
                                if 'Content' in service_generation_sharelink.keys():
                                    service_generation_sharelink_content = service_generation_sharelink['Content']
                            if service_generation_sharelink_content == '':
                                wx.MessageBox('%s分享链接为空'%current_service,'警告',wx.OK|wx.ICON_INFORMATION)
                            else:
                                qrcode_str_base64 = '%s%s'%(service_generation_sharelink_prefix,str(base64.b64encode(service_generation_sharelink_content.encode('utf-8')), 'utf-8'))
                                img = qrcode.make(qrcode_str_base64)
                                img.show()

    def _initialize_api_key_name(self):
        '''
        初始化api-key name
        '''
        # 清除数据
        self.m_choiceName.Clear()
        self._apikeynames.clear()

        platform_name = self.get_select_platform_name()
        apikeyname_data = config.get_apikeynames(platform_name)
        for apikey in apikeyname_data.keys():
            self._apikeynames[apikey] = apikeyname_data[apikey]
        # print(list(self._apikeynames.values()))
        self.m_choiceName.SetItems(list(self._apikeynames.values()))

    def _initialize_services(self):
        '''
        初始化service
        '''
        platform_name = self.get_select_platform_name()
        services = config.get_services()
        for service_key in services.keys():
            self._services[service_key] = services[service_key]
        self.m_choiceService.SetItems(list(services.keys()))

    def get_select_apikey_name(self):
        '''
        获取当前选择的apikey_name
        '''
        selection_index = self.m_choiceName.GetSelection()
        name = ''
        if selection_index >= 0:
            name = self.m_choiceName.GetString(selection_index).strip()
        return name

    def get_select_platform_name(self):
        '''
        获取当前选择的平台
        '''
        selection_index = self.m_choicePlatform.GetSelection()
        name = ''
        if selection_index >= 0:
            name = self.m_choicePlatform.GetString(selection_index).strip()
        return name

    def get_servers(self):
        '''
        获取所有server列表
        '''
        platform_name = self.get_select_platform_name()
        name = self.get_select_apikey_name()
        self._servers = server.read_config(platform_name, name)
        server_services = service.read_service_config(platform_name, name)
        projects = ['']
        if self._servers is not None:
            self.m_gridLine.InsertRows(0, len(self._servers))
            i = 0
            for server_subid in self._servers:
                server_item = self._servers[server_subid]
                if server_subid in server_services.keys():
                    server_service_item = server_services[server_subid]
                    server_item['service_port'] = server_service_item['service_port']
                    server_item['service_password'] = server_service_item['service_password']
                    if 'service_list' not in server_service_item.keys():
                        server_item['service_list'] = ''
                    else:
                        server_item['service_list'] = server_service_item['service_list']
                    server_item['services'] = json.dumps(server_service_item['services'])
                wx.CallAfter(self.callback_update_server, i, server_item)
                i += 1

    def get_server_by_subid(self, platform_name, name, subid):
        '''
        获取某个server的信息
        '''
        server_item = server.get_server_by_subid(platform_name, name, subid)
        self._servers[subid] = server_item
        if server_item is not None:
            i = self._updating_server_indexs[subid]
            wx.CallAfter(self.callback_update_server, i, server_item)

    def callback_update_server(self, i, server_item):
        project = server_item['tag']
        subid = server_item['SUBID']
        self.m_gridLine.SetCellValue(i, 0, subid)
        self.m_gridLine.SetCellValue(i, 1, server_item['label'])
        ip = server_item['main_ip']
        self.m_gridLine.SetCellValue(i, 2, ip)
        self.m_gridLine.SetCellValue(i, 3, server_item['os'])
        self.m_gridLine.SetCellValue(i, 4, server_item['location'])
        self.m_gridLine.SetCellValue(i, 5, project)
        server_status = server_item['status']
        power_status = server_item['power_status']
        if server_status not in 'active':
            self._updating_server_indexs[subid] = i
        else:
            if subid in self._updating_server_indexs.keys() and self.m_timerGrid.IsRunning() \
                and power_status == 'running':
                self.m_timerGrid.Stop()
                self.m_gaugeProgress.Value = 100
                self.Unbind(wx.EVT_IDLE)
                self.callback_update_status('新线路已更新')
        self.m_gridLine.SetCellValue(i, 6, server_status)
        self.m_gridLine.SetCellValue(i, 7, power_status)
        service_list = ''
        if 'service_list' in server_item.keys():
            service_list = server_item['service_list']
        self.m_gridLine.SetCellValue(i, 8, service_list)
        password = server_item['default_password']
        self.m_gridLine.SetCellValue(i, 9, password)
        service_port = ''
        if 'service_port' in server_item.keys():
            service_port = server_item['service_port']
        self.m_gridLine.SetCellValue(i, 10, service_port)
        service_password = ''
        if 'service_password' in server_item.keys():
            service_password = server_item['service_password']
        self.m_gridLine.SetCellValue(i, 11, service_password)
        services = ''
        if 'services' in server_item.keys():
            services = server_item['services']
        self.m_gridLine.SetCellValue(i, 12, services)
        self.m_gridLine.ForceRefresh()
        if project not in self._projects:
            self._projects.append(project)

    def _initialize_servers(self):
        '''
        初始化servers
        '''
        rows = self.m_gridLine.GetNumberRows()
        if rows > 0:
            self.m_gridLine.DeleteRows(pos=0, numRows=rows)

        thread = threading.Thread(target=self.get_servers)
        thread.start()

    def _initialize_plans(self):
        '''
        初始化plans
        '''
        platform_name = self.get_select_platform_name()
        name = self.get_select_apikey_name()
        self._plans = plan.read_config(platform_name, name)

    def _initialize_regions(self):
        '''
        初始化regions
        '''
        platform_name = self.get_select_platform_name()
        name = self.get_select_apikey_name()
        self._regions = region.read_region_config(platform_name, name)

    def _initialize_oss(self):
        '''
        初始化oss
        '''
        platform_name = self.get_select_platform_name()
        name = self.get_select_apikey_name()
        self._oss = operatingsystem.read_config(platform_name, name)

    def _clear_configuration_data(self, platform_name, name):
        '''
        清除配置数据
        '''
        region.clear_config(platform_name, name)
        plan.clear_config(platform_name, name)
        # os.clear_config()

    def set_api_key(self, event):
        '''
        设置API-Key
        '''
        api_key = self.m_textCtrlAPIKey.Value
        if api_key == '' or api_key == None:
            wx.MessageBox('请设置API-Key','警告',wx.OK|wx.ICON_INFORMATION)
            return

        name = self.m_textCtrlName.Value
        if name == '' or name == None:
            wx.MessageBox('请设置名称','警告',wx.OK|wx.ICON_INFORMATION)
            return

        platform_name = self.get_select_platform_name()
        if config.modify_apikey(platform_name, name, api_key):
            self._clear_configuration_data(platform_name, name)
            self._initialize()

    def gauge_progress_update(self,event): 
        if self._gauge_value < 100: 
            self._gauge_value += 1
            self.m_gaugeProgress.SetValue(self._gauge_value)
        else:
            self._gauge_value = 0

    def button_update_data(self, event):
        '''
        更新数据事件方法
        '''
        platform_name = self.get_select_platform_name()
        name = self.get_select_apikey_name()
        if not config.exist_apikey(platform_name, name):
            wx.MessageBox('请先选择API','警告',wx.OK|wx.ICON_INFORMATION)
            return
        # thread = threading.Thread(target=self.update_data)
        # thread.start()
        self.thread = WorkThread.WorkThread(target=self.update_data, args=(platform_name,))
        self.thread.start()
        # 进度条
        self._gauge_value = 0
        self.Bind(wx.EVT_IDLE, self.gauge_progress_update)

    def button_stop_update( self, event ):
        '''
        停止更新数据
        '''
        self.thread.stop()

        self.callback_update_status('停止更新')
        self.update_progress_task_end()

    def update_data(self, platform_name):
        '''
        更新数据
        '''
        name = self.get_select_apikey_name()
        # 获取server数据
        wx.CallAfter(self.callback_update_status, '获取更新包1')
        self._servers = server.get_servers(platform_name, name)
        # 更新服务状态
        wx.CallAfter(self.callback_update_status, '更新服务状态')
        # 获取plan数据
        wx.CallAfter(self.callback_update_status, '获取更新包2')
        self._plans = plan.get_plans(platform_name, name)
        # 获取region数据
        wx.CallAfter(self.callback_update_status, '获取更新包3')
        self._regions = region.get_regions(platform_name, name)
        # 获取os数据
        wx.CallAfter(self.callback_update_status, '获取更新包4')
        self._oss = operatingsystem.get_os(platform_name, name)
        wx.CallAfter(self.callback_update_data)
        wx.CallAfter(self.callback_update_status, '更新完成')

    def callback_update_service_list(self, platform_name, subid, service):
        '''
        回调更新服务列表
        '''
        name = self.get_select_apikey_name()
        server.update_service_list(platform_name, name, subid, service)

    def callback_insert_service(self, platform_name, subid, service_name):
        '''
        回调初始化Service
        '''
        name = self.get_select_apikey_name()
        service_item = self._services[service_name]
        service_item_install_generation = {}
        if 'Install' in service_item.keys():
            service_item_install = service_item['Install']
            if 'Generation' in service_item_install.keys():
                service_item_install_generation = service_item_install['Generation']
        server.insert_service(platform_name, name, subid, service_name, service_item_install_generation)
    
    def callback_update_status(self, status_message):
        '''
        更新状态数据
        '''
        self.m_staticTextUpdateStatus.Label = status_message

    def update_server_data_by_create(self):
        '''
        更新server数据
        '''
        # self._servers = server.get_servers()
        wx.CallAfter(self.callback_update_server_data_by_create)

    def update_progress_task_end(self):
        '''
        任务结束更新进度条
        '''
        self.m_gaugeProgress.Value = 100
        self.Unbind(wx.EVT_IDLE)

    def callback_update_server_data_by_create(self):
        '''
        回调方法，新建线路时更新server数据
        '''
        self._initialize_servers()
        self.m_timerGrid.Start(milliseconds=5000)

    def callback_update_data(self):
        '''
        回调方法，更新数据
        '''
        self._initialize_servers()
        self.update_progress_task_end()

    def is_updated_data(self):
        '''
        是否已经更新数据
        '''
        is_updated_data = True
        if len(self._plans) == 0 or len(self._regions) == 0 or len(self._oss) == 0:
            is_updated_data = False
        return is_updated_data

    def choice_platform( self, event ):
        '''
        选择平台
        '''
        select_platform = self.m_choicePlatform.GetString(self.m_choicePlatform.GetSelection()).strip()
        self._initialize_api_key_name()

    def choice_name(self, event):
        '''
        选择apikey名称
        '''
        select_name = self.m_choiceName.GetString(self.m_choiceName.GetSelection()).strip()
        self._initialize_servers()
        self._initialize_plans()
        self._initialize_regions()
        self._initialize_oss()

    def get_current_grid_subid(self):
        '''
        获取当前选择的server的subid
        '''
        currentRow = self.m_gridLine.GetGridCursorRow()
        server_subid = ''
        try:
            server_subid = self.m_gridLine.GetCellValue(currentRow, 0)
        except Exception as e:
            server_subid = ''
        return server_subid

    def get_current_grid_ip(self):
        '''
        获取当前选择的server的ip
        '''
        currentRow = self.m_gridLine.GetGridCursorRow()
        server_ip = ''
        try:
            server_ip = self.m_gridLine.GetCellValue(currentRow, 2)
        except Exception as e:
            server_ip = ''
        return server_ip

    def get_current_grid_password(self):
        '''
        获取当前选择的server的password
        '''
        currentRow = self.m_gridLine.GetGridCursorRow()
        server_password = self.m_gridLine.GetCellValue(currentRow, 9)
        return server_password

    def get_current_grid_OS(self):
        '''
        获取当前选择的server的os
        '''
        currentRow = self.m_gridLine.GetGridCursorRow()
        server_os = self.m_gridLine.GetCellValue(currentRow, 3)
        return server_os

    def get_current_grid_services(self):
        '''
        获取当前选择的server的services
        '''
        currentRow = self.m_gridLine.GetGridCursorRow()
        services = self.m_gridLine.GetCellValue(currentRow, 12)
        if services == '':
            return ''
        return json.loads(services)

    def get_current_selection_service(self):
        '''
        获取当前选择的服务
        '''
        select_service = self.m_choiceService.GetString(self.m_choiceService.GetSelection()).strip()
        return select_service

    def create_line(self, event ):
        '''
        创建线路
        '''
        platform_name = self.get_select_platform_name()
        name = self.get_select_apikey_name()
        if not config.exist_apikey(platform_name, name):
            wx.MessageBox('请先设置API-Key','警告',wx.OK|wx.ICON_INFORMATION)
            return

        # 判断是否已经更新数据
        if not self.is_updated_data():
            wx.MessageBox('请先更新数据','警告',wx.OK|wx.ICON_INFORMATION)
            return

        dialogCreateWindow = DialogCreateWindow(self, platform_name)
        if dialogCreateWindow.ShowModal() == wx.ID_OK:
            self._gauge_value = 0
            self.Bind(wx.EVT_IDLE, self.gauge_progress_update)
            self.callback_update_status('更新新线路')

    def delete_line(self, event):
        '''
        删除线路
        '''
        platform_name = self.get_select_platform_name()
        name = self.get_select_apikey_name()
        server_subid = self.get_current_grid_subid()
        if server.delete_server(platform_name, name, server_subid):
            self._servers.pop(server_subid)
            self.m_gridLine.DeleteRows(self.m_gridLine.GetGridCursorRow())
            self.m_gridLine.ForceRefresh()
            wx.MessageBox('删除线路成功','警告',wx.OK|wx.ICON_INFORMATION)
        else:
            wx.MessageBox('删除线路失败','警告',wx.OK|wx.ICON_INFORMATION)

    def execute_server(self, action):
        '''
        执行server操作
        '''
        platform_name = self.get_select_platform_name()
        server_subid = self.get_current_grid_subid()
        currentRow = self.m_gridLine.GetGridCursorRow()
        thread = threading.Thread(target=self.execute_server_backend, args=(platform_name, server_subid, action, currentRow, ))
        thread.start()

        # 进度条
        self._gauge_value = 0
        self.Bind(wx.EVT_IDLE, self.gauge_progress_update)

    def execute_server_backend(self, platform_name, subid, action, row):
        '''
        后台执行server操作
        '''
        operation_result = False
        name = self.get_select_apikey_name()
        if action == 'start':
            operation_result = server.start_server(platform_name, name, subid)
        elif action == 'stop':
            operation_result = server.stop_server(platform_name, name, subid)
        elif action == 'restart':
            operation_result = server.reboot_server(platform_name, name, subid)
        wx.CallAfter(self.callback_execute_server, action, operation_result, row)
        
    def callback_execute_server(self, action, operation_result, row):
        '''
        回调，后台执行server操作
        '''
        if operation_result:
            if action == 'start':
                self.m_gridLine.SetCellValue(row, 7, 'running')
                wx.MessageBox('开启服务成功','警告',wx.OK|wx.ICON_INFORMATION)
            elif action == 'stop':
                self.m_gridLine.SetCellValue(row, 7, 'stopped')
                wx.MessageBox('停止服务成功','警告',wx.OK|wx.ICON_INFORMATION)
            elif action == 'restart':
                wx.MessageBox('重启服务成功','警告',wx.OK|wx.ICON_INFORMATION)
        else:
            if action == 'start':
                wx.MessageBox('开启服务失败','警告',wx.OK|wx.ICON_INFORMATION)
            elif action == 'stop':
                wx.MessageBox('停止服务失败','警告',wx.OK|wx.ICON_INFORMATION)
            elif action == 'restart':
                wx.MessageBox('重启服务失败','警告',wx.OK|wx.ICON_INFORMATION)
        self.m_gridLine.ForceRefresh()
        self.update_progress_task_end()

    def start_server(self, event):
        '''
        开启服务
        '''
        self.execute_server('start')

    def stop_server(self, event):
        '''
        停止服务
        '''
        self.execute_server('stop')

    def restart_server(self, event):
        '''
        重启服务
        '''
        self.execute_server('restart')

    def show_message(self, message):
        self.m_textCtrlReseponse.AppendText('%s%s'%(message,os.linesep))

    def callback_update_message(self, message):
        '''
        回调更新消息
        '''
        self.show_message(message)
        self.m_gaugeProgress.Value = 100
        self.Unbind(wx.EVT_IDLE)

    def execute_connect(self, ssh, host, port, user, password):
        '''
        执行连接
        '''
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, user, password)
            wx.CallAfter(self.callback_update_message, 'ssh登录%s成功!'%host)
        except Exception as e:
            wx.CallAfter(self.callback_update_message, 'ssh登录%s失败，请重试!'%host)
            print(str(e))

    def exec_cmd(self, ssh, command):
        '''
        执行server服务器上命令
        '''
        try:
            # 先打印一行命令
            wx.CallAfter(self.callback_update_message, "root@vps:# " + command)

            stdin, stdout, stderr = ssh.exec_command(command)
            err = ''.join(stderr.readlines()).strip()
            
            if "" != err:
                wx.CallAfter(self.callback_update_message, err)
                # self.show_message(out)
            else:
                for line in stdout.readlines():
                    wx.CallAfter(self.callback_update_message, line)
                # 最后也打印一行，无错误，也无输出的情况，可以分辨
                wx.CallAfter(self.callback_update_message, "root@vps:# ")
        except Exception as e:
            wx.CallAfter(self.callback_update_message, str(e))

    def interactive_server(self, event):
        '''
        与server交互
        '''
        host = self.get_current_grid_ip()
        if host == '' or host is None:
            wx.MessageBox('未选择线路','警告',wx.OK|wx.ICON_INFORMATION)
            return
        port = 22
        username = 'root'
        password = self.get_current_grid_password()
        ssh = None
        if host not in self._sshs.keys():
            ssh = paramiko.SSHClient()
            self._sshs[host] = ssh
        else:
            ssh = self._sshs[host]

        thread = threading.Thread(target=self.execute_connect, args=(ssh, host, port, username, password))
        thread.start()
        self._gauge_value = 0
        self.Bind(wx.EVT_IDLE, self.gauge_progress_update)
        self.callback_update_status('连接主机')

    def command_execute(self, event):
        '''
        交互执行命令
        '''
        host = self.get_current_grid_ip()
        if host == '' or host is None:
            wx.MessageBox('未选择线路','警告',wx.OK|wx.ICON_INFORMATION)
            return
        if host not in self._sshs.keys():
            wx.MessageBox('请先连接','警告',wx.OK|wx.ICON_INFORMATION)
            return
        ssh = self._sshs[host]
        command_text = self.m_textCtrlCommand.Value
        if '' == command_text:
            wx.MessageBox('请输入命令','警告',wx.OK|wx.ICON_INFORMATION)
            return
        thread = threading.Thread(target=self.exec_cmd, args=(ssh, command_text,))
        thread.start()

        self._gauge_value = 0
        self.Bind(wx.EVT_IDLE, self.gauge_progress_update)
        self.callback_update_status('执行命令')

    def command_clear(self, event):
        self.m_textCtrlReseponse.Clear()

    def timer_update( self, event ):
        '''
        定时器，定时更新
        '''
        # self._initialize_servers()
        platform_name = self.get_select_platform_name()
        name = self.get_select_apikey_name()
        for subid in self._updating_server_indexs.keys():
            thread = threading.Thread(target=self.get_server_by_subid, args=(platform_name, name, subid,))
            thread.start()

    def get_available_err(self, errors):
        '''
        获取可用的错误信息
        '''
        err = ''
        for line_err in errors:
            if 'DEPRECATION' in line_err:
                continue
            elif 'upgrading' in line_err:
                continue
            elif 'pip version' in line_err:
                continue
            else:
                err += line_err
        return err

    def write_log(self, platform_name, content):
        '''
        日志
        '''
        name = self.get_select_apikey_name()
        log.write_log(platform_name, name, content)

    def build_service_thread(self, platform_name, subid, host, port, username, password, installer='apt'):
        try:
            self._gauge_value = 0
            self.Bind(wx.EVT_IDLE, self.gauge_progress_update)
            wx.CallAfter(self.callback_update_status, '开始连接主机')
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)

            # 开始安装
            current_service = self.get_current_selection_service()
            service_item = self._services[current_service]
            if 'Install' not in service_item.keys():
                wx.CallAfter(self.callback_update_status, '服务配置错误')
                return
            else:
                service_item_install = service_item['Install']
                self.write_log(platform_name, '%s install start.'%current_service)
                wx.CallAfter(self.callback_update_status, '%s开始安装'%current_service)
                service_item_start = ''
                service_port = 34001
                service_password = 'gogoline'
                service_config_file = ''
                config_content = ''
                if 'Config' in service_item_install.keys():
                    install_item_config = service_item_install['Config']
                    host_server = ''
                    if 'Host' in install_item_config.keys():
                        host_server = install_item_config['Host']
                    if 'Content' in install_item_config.keys():
                        config_content = install_item_config['Content']
                        service_port = config_content['server_port']
                        service_password = config_content['password']
                        if host_server == 'server':
                            config_content['server'] = host
                    if 'File' in install_item_config.keys():
                        service_config_file = install_item_config['File']
                name = self.get_select_apikey_name()
                if service.create_service(platform_name, name, subid, current_service ,service_port, service_password):
                    if 'Command' in service_item_install.keys():
                        install_command = service_item_install['Command']
                        for install_item in install_command:
                            stdin, stdout, stderr = ssh.exec_command(install_item)
                            wx.CallAfter(self.callback_update_message, ''.join(stdout.readlines()))
                            wx.CallAfter(self.callback_update_message, ''.join(stderr.readlines()))
                            err = self.get_available_err(stderr.readlines())
                            if '' != err:
                                self.write_log(platform_name, err)
                                wx.CallAfter(self.callback_update_status, '%s创建失败'%current_service)
                            else:
                                self.write_log(platform_name, ''.join(stdout.readlines()))
                                self.write_log(platform_name, '%s install end.'%current_service)
                                wx.CallAfter(self.callback_update_status, '%s创建成功'%current_service)
                                wx.CallAfter(self.callback_insert_service, platform_name, subid, current_service)
                    if service_config_file != '' and config_content != '':
                        stdin, stdout, stderr = ssh.exec_command('echo %s > %s'%(config_content, service_config_file))
                        wx.CallAfter(self.callback_update_message, ''.join(stdout.readlines()))
                        wx.CallAfter(self.callback_update_message, ''.join(stderr.readlines()))
                        err = self.get_available_err(stderr.readlines())
                        if '' != err:
                            self.write_log(platform_name, err)
                            wx.CallAfter(self.callback_update_status, '%s配置失败'%current_service)
                        else:
                            self.write_log(platform_name, ''.join(stdout.readlines()))
                            self.write_log(platform_name, '%s 配置成功 .'%current_service)
                            wx.CallAfter(self.callback_update_status, '%s配置成功'%current_service)
                            wx.CallAfter(self.callback_insert_service, platform_name, subid, current_service)
                else:
                    wx.CallAfter(self.callback_update_message, '%s创建失败'%current_service)
        except Exception as e:
            self.write_log(platform_name, '%s,%s'%(host,str(e)))
            wx.CallAfter(self.callback_update_status, '连接失败')
            wx.CallAfter(self.callback_update_message, str(e))
        wx.CallAfter(self.callback_update_data)

    def start_service_thread(self, platform_name, subid, host, port, username, password):
        '''
        启动服务
        '''
        try:
            self._gauge_value = 0
            self.Bind(wx.EVT_IDLE, self.gauge_progress_update)
            wx.CallAfter(self.callback_update_status, '开始连接主机')
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)

            current_service = self.get_current_selection_service()
            service_item = self._services[current_service]
            if 'Start' in service_item.keys():
                service_item_start = service_item['Start']
                if service_item_start != '':
                    if 'Command' not in service_item_start.keys():
                        wx.CallAfter(self.callback_update_status, '服务配置错误')
                        return
                    else:
                        for command_string in service_item_start['Command']:
                            self.write_log(platform_name, '%s install start.'%current_service)
                            wx.CallAfter(self.callback_update_status, '%s开始启动'%current_service)
                            stdin, stdout, stderr = ssh.exec_command(command_string)
                            wx.CallAfter(self.callback_update_message, ''.join(stdout.readlines()))
                            wx.CallAfter(self.callback_update_message, ''.join(stderr.readlines()))
                            err = self.get_available_err(stderr.readlines())
                            if '' != err:
                                self.write_log(platform_name, err)
                                wx.CallAfter(self.callback_update_status, '%s启动失败'%current_service)
                            else:
                                self.write_log(platform_name, ''.join(stdout.readlines()))
                                self.write_log(platform_name, '%s install end.'%current_service)
                                wx.CallAfter(self.callback_update_status, '%s已启动'%current_service)
                                wx.CallAfter(self.callback_update_service_list, platform_name, subid, current_service)
        except Exception as e:
            self.write_log(platform_name, '%s,%s'%(host,str(e)))
            wx.CallAfter(self.callback_update_status, '连接失败')
            wx.CallAfter(self.callback_update_message, str(e))
        wx.CallAfter(self.callback_update_data)

    def stop_service_thread(self, subid, host, port, username, password):
        '''
        停止服务
        '''
        try:
            self._gauge_value = 0
            self.Bind(wx.EVT_IDLE, self.gauge_progress_update)
            wx.CallAfter(self.callback_update_status, '开始连接主机')
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)

            current_service = self.get_current_selection_service()
            service_item = self._services[current_service]
            if 'Stop' in service_item.keys():
                for command_string in service_item['Stop']:
                    self.write_log(platform_name, '%s install start.'%current_service)
                    wx.CallAfter(self.callback_update_status, '%s开始停止'%current_service)
                    stdin, stdout, stderr = ssh.exec_command(command_string)
                    err = ''.join(stderr.readlines())
                    wx.CallAfter(self.callback_update_message, ''.join(stdout.readlines()))
                    wx.CallAfter(self.callback_update_message, ''.join(stderr.readlines()))
                    if '' != err:
                        self.write_log(platform_name, err)
                        wx.CallAfter(self.callback_update_status, '%s停止失败'%current_service)
                    else:
                        self.write_log(platform_name, ''.join(stdout.readlines()))
                        wx.CallAfter(self.callback_update_status, '%s已停止'%current_service)
                        wx.CallAfter(self.callback_update_service_list, platform_name, subid, current_service)
        except Exception as e:
            print('%s,%s'%(host,str(e)))
            wx.CallAfter(self.callback_update_status, '连接失败')
        wx.CallAfter(self.callback_update_data)

    def build_service(self, event):
        '''
        安装服务
        '''
        platform_name = self.get_select_platform_name()
        subid = self.get_current_grid_subid()
        host = self.get_current_grid_ip()
        if host == '':
            wx.MessageBox('未选择主机','警告',wx.OK|wx.ICON_INFORMATION)
            return
        current_service = self.get_current_selection_service()
        if current_service == '':
            wx.MessageBox('未选择服务','警告',wx.OK|wx.ICON_INFORMATION)
            return
        port = 22
        username = 'root'
        password = self.get_current_grid_password()
        os = self.get_current_grid_OS()
        installer = 'apt'
        if 'CentOS' in os:
            installer = 'yum'
        thread = threading.Thread(target=self.build_service_thread,args=(platform_name, subid, host, port, username, password, installer,))
        thread.start()

    def start_service(self, event):
        '''
        启动服务
        '''
        subid = self.get_current_grid_subid()
        host = self.get_current_grid_ip()
        platform_name = self.get_select_platform_name()
        port = 22
        username = 'root'
        password = self.get_current_grid_password()
        thread = threading.Thread(target=self.start_service_thread, 
                                args=(platform_name, subid, host, port, username, password))
        thread.start()

    def stop_service(self, event):
        '''
        停止服务
        '''
        subid = self.get_current_grid_subid()
        host = self.get_current_grid_ip()
        port = 22
        username = 'root'
        password = self.get_current_grid_password()
        thread = threading.Thread(target=self.stop_service_thread,args=(subid, host, port, username, password,))
        thread.start()

    def grid_select_cell(self, event):
        '''
        选择一个cell
        '''
        currentRow = event.Row