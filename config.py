import json, sys
import log, fileoperate

def exist_apikey(name):
    '''
    判断是否存在api_key
    '''
    api_key = fileoperate.read_api_file(name)
    if api_key not in '':
        return True
    return False

def modify_apikey(name, api_key):
    '''
    修改api_key
    '''
    return fileoperate.write_api_file(name, api_key)

def get_apikeynames():
    '''
    获取api_key对应的name
    '''
    return fileoperate.read_apikeyname_file()

def get_services():
    '''
    获取service
    '''
    return fileoperate.read_services_file()

def get_apikey(name):
    '''
    获取api_key
    '''
    return fileoperate.read_api_file(name)

def create_service_config(config_data):
    '''
    创建服务配置文件
    '''
    data = config_data
    try:
        with open('service_config.json', 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        pass
    return True