import requests
import config, fileoperate, service
import json, socket
import paramiko, asyncio, time

def get_servers(name):
    servers = None
    # local_servers = read_config()
    api_key = config.get_apikey(name)
    headers = {
        'API-Key':api_key
    }
    r = requests.get('https://api.vultr.com/v1/server/list',headers=headers)
    if r.status_code == 200:
        servers = json.loads(r.text)
    if servers is not None:
        write_config(name, servers)
    return servers

def get_server_by_subid(name, subid):
    '''
    根据subid获取对应的server的信息
    '''
    api_key = config.get_apikey(name)
    headers = {
        'API-Key':api_key
    }
    r = requests.get('https://api.vultr.com/v1/server/list?SUBID=%s'%subid,headers=headers)
    if r.status_code == 200:
        local_servers = read_config(name)
        server_item = json.loads(r.text)
        local_servers[subid] = server_item
        write_config(name, local_servers)
        return server_item
    return None

def create_server(name, region_dcid, plan_id, osid, project_name, server_num):
    api_key = config.get_apikey(name)
    headers = {
        'API-Key':api_key
    }
    data = {
        'DCID':region_dcid,
        'VPSPLANID':plan_id,
        'OSID':osid,
        'tag':project_name,
        'label':server_num
    }
    r = requests.post('https://api.vultr.com/v1/server/create',headers=headers, data=data)
    if r.status_code == 200:
        new_server = json.loads(r.text)
        subid = new_server['SUBID']
        server_item = get_server_by_subid(name, subid)
        return subid
    return None

def delete_server(name, subid):
    '''
    删除server
    '''
    api_key = config.get_apikey(name)
    headers = {
        'API-Key':api_key
    }
    data = {
        'SUBID':subid
    }
    r = requests.post('https://api.vultr.com/v1/server/destroy',headers=headers, data=data)
    if r.status_code == 200:
        data = read_config(name)
        data.pop(subid)
        write_config(name, data)
        ss_data = service.read_service_config(name)
        if subid in ss_data.keys():
            ss_data.pop(subid)
            service.write_service_config(name, ss_data)
        return True
    return False

def start_server(name, subid):
    '''
    开启server
    成功返回True，失败返回False
    '''
    return execute_server(name, subid, 'start')

def stop_server(name, subid):
    '''
    关闭server
    成功返回True，失败返回False
    '''
    return execute_server(name, subid, 'halt')

def reboot_server(name, subid):
    '''
    重启server
    成功返回True，失败返回False
    '''
    return execute_server(name, subid, 'reboot')

def execute_server(name, subid, action):
    '''
    执行server
    成功返回True，失败返回False
    '''
    api_key = config.get_apikey(name)
    headers = {
        'API-Key':api_key
    }
    data = {
        'SUBID':subid
    }
    r = requests.post('https://api.vultr.com/v1/server/%s'%action,headers=headers, data=data)
    if r.status_code == 200:
        server_data = read_config(name)
        if action == 'halt':
            server_data[subid]['power_status'] = 'stopped'
        elif action == 'reboot' or action == 'start':
            server_data[subid]['power_status'] = 'running'
        write_config(name, server_data)
        return True
    return False

def write_config(name, data):
    '''
    写入数据
    '''
    return fileoperate.write_server_file(name, data)

def insert_service(name, subid, service_name, service_generation):
    '''
    插入service
    '''
    data = service.read_service_config(name)
    server_item = data[subid]
    server_item_services = {}
    if 'services' in server_item.keys():
        server_item_services = server_item['services']
    
    if service_name not in server_item_services.keys():
        server_item_services[service_name] = {}
    server_item_services[service_name]['generation'] = service_generation
    service_list = ''
    if 'service_list' not in server_item.keys():
        server_item['service_list'] = ''
    else:
        service_list = server_item['service_list']
    if service_list == '':
        server_item['service_list'] = service_name
    else:
        service_name = service_name.upper()
        if service_name not in service_list:
            server_item['service_list'] = service_list + ',' + service_name
    service.write_service_config(name, data)

def update_service_list(name, subid, service_name):
    '''
    更新service列表
    '''
    data = service.read_service_config(name)
    server_item = data[subid]
    service_list = ''
    if 'service_list' not in server_item.keys():
        server_item['service_list'] = ''
    else:
        service_list = server_item['service_list']
    if service_list == '':
        server_item['service_list'] = service_name
    else:
        service_name = service_name.upper()
        if service_name not in service_list:
            server_item['service_list'] = service_list + ',' + service_name
    service.write_service_config(name, data)

def read_config(name):
    '''
    读取数据
    '''
    return fileoperate.read_server_file(name)

def clear_config():
    '''
    清空配置
    '''
    data = {}
    return fileoperate.write_server_file(data)