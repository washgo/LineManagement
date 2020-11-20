import json, sys, platform, os

def read_apikeyname_file():
    '''
    读取api-名称设置文件
    '''
    data = {}
    data = _read_json_file('', 'apiname.json')
    return data

def read_services_file():
    '''
    读取services.json文件
    '''
    data = {}
    data = _read_json_file('', 'services.json')
    return data

def read_api_file(name):
    '''
    读取配置文件
    '''
    data = _read_json_file(name, 'apikey.json')
    api_key = ''
    if 'API-Key' in data.keys():
        api_key = data['API-Key']
    return api_key
 
def write_api_file(name, api_key):
    '''
    写入配置文件
    '''
    apiname_data = _read_json_file('', 'apiname.json')
    if api_key in apiname_data.keys():
        apiname_data[api_key] = name
    else:
        apiname_data[api_key] = name
    _write_json_file('', 'apiname.json', apiname_data)
    
    data = { "API-Key":api_key }
    return _write_json_file(name, 'apikey.json', data)

def read_plan_file(name):
    '''
    读取plan数据
    '''
    return _read_json_file(name, 'plan.json')

def write_plan_file(name, data):
    '''
    写入plan数据
    '''
    return _write_json_file(name, 'plan.json', data)

def read_region_file(name):
    '''
    读取region数据
    '''
    return _read_json_file(name, 'region.json')

def write_region_file(name, data):
    '''
    写入region数据
    '''
    return _write_json_file(name, 'region.json', data)

def read_os_file(name):
    '''
    读取os数据
    '''
    return _read_json_file(name, 'os.json')

def write_os_file(name, data):
    '''
    写入os数据
    '''
    return _write_json_file(name, 'os.json', data)

def read_server_file(name):
    '''
    读取os数据
    '''
    return _read_json_file(name, 'server.json')

def write_server_file(name, data):
    '''
    写入os数据
    '''
    return _write_json_file(name, 'server.json', data)

def read_server_service_file(name):
    '''
    读取ss数据
    '''
    return _read_json_file(name, 'server_service.json')

def write_server_service_file(name, data):
    '''
    写入ss数据
    '''
    return _write_json_file(name, 'server_service.json', data)

def _read_json_file(name, file_name):
    '''
    读取json文件
    '''
    data = {}
    try:
        # file_path = file_name
        file_path = create_config_directory(name) + os.sep + file_name
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        pass
    return data

def _write_json_file(name, file_name, data):
    '''
    写入json文件
    '''
    try:
        # file_path = file_name
        # if platform.system() == 'Darwin':
        file_path = create_config_directory(name) + os.sep + file_name
        with open(file_path, 'w+') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        pass
    return False

def write_file(name, file_name, data):
    '''
    写入文件
    '''
    try:
        # file_path = file_name
        file_path = create_config_directory(name) + os.sep + file_name
        with open(file_path, 'a+') as f:
            f.write(data)
    except Exception as e:
        print('write file:%s'%(str(e)))

def create_config_directory(name):
    '''
    创建配置文件目录
    '''
    config_directory = ''
    try:
        config_directory = get_config_directory(name)
        if not os.path.exists(config_directory):
            os.mkdir(config_directory)
    except Exception as e:
        pass
    return config_directory

def get_config_directory(name):
    '''
    获取配置文件目录
    '''
    home = ''
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        home = os.environ['HOME'] + os.sep + '.HaLineManagement' + os.sep + name
    elif platform.system() == 'Windows':
        home = os.getcwd() + os.sep + 'config' + os.sep + name
        # print(home)
    return home