import json, os
import requests
import fileoperate

def get_plans(platform_name, name):
    data = None
    r = requests.get('https://api.vultr.com/v1/plans/list_vc2')
    if r.status_code == 200:
        data = json.loads(r.text)
    if data is not None:
        write_config(platform_name, name, data)
    return data

def exist_plans(platform_name, name):
	'''
	判断是否存在plan
	'''
	data = {}

	data = fileoperate.read_plan_file(platform_name, name)
	if len(data) > 0:
		return True
	return False

def write_config(platform_name, name, data):
	'''
	写入数据
	'''
	return fileoperate.write_plan_file(platform_name, name, data)

def read_config(platform_name, name):
	'''
	读取数据
	'''
	return fileoperate.read_plan_file(platform_name, name)

def clear_config(platform_name, name):
	'''
	清空配置
	'''
	data = {}
	return fileoperate.write_plan_file(platform_name, name, data)