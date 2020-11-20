import json, os
import requests
import fileoperate

def get_os(name):
    data = None
    r = requests.get('https://api.vultr.com/v1/os/list')
    if r.status_code == 200:
        data = json.loads(r.text)
    if data is not None:
        write_config(name, data)
    return data

def exist_os(name):
	'''
	判断是否存在os
	'''
	data = {}

	data = fileoperate.read_os_file(name)
	if len(data) > 0:
		return True
	return False

def write_config(name, data):
	'''
	写入数据
	'''
	fileoperate.write_os_file(name, data)

def read_config(name):
	'''
	读取数据
	'''
	return fileoperate.read_os_file(name)

def clear_config(name):
	'''
	清空配置
	'''
	data = {}
	return fileoperate.write_os_file(name, data)