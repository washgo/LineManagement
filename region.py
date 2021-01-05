import requests
import json, os
import fileoperate

def get_regions(platform_name, name):
	regions = None
	r = requests.get('https://api.vultr.com/v1/regions/list')
	if r.status_code == 200:
		regions = json.loads(r.text)
	if regions is not None:
		for region_dcid in regions:
			region_item = regions[region_dcid]
			plan_id_list = get_available_by_region_dcid(int(region_dcid))
			region_item['available_plans'] = plan_id_list
		write_region_config(platform_name, name, regions)
	return regions

def get_available_by_region_dcid(region_dcid):
	plan_id_list = None
	r = requests.get('https://api.vultr.com/v1/regions/availability_vc2?DCID=%d'%region_dcid)
	if r.status_code == 200:
		plan_id_list = json.loads(r.text)
	return plan_id_list

def write_region_config(platform_name, name, data):
	'''
	保存region配置
	'''
	return fileoperate.write_region_file(platform_name, name, data)

def read_region_config(platform_name, name):
	'''
	读取region配置
	'''
	return fileoperate.read_region_file(platform_name, name)

def clear_config(platform_name, name):
	'''
	清空配置
	'''
	data = {}
	return fileoperate.write_region_file(platform_name, name, data)
