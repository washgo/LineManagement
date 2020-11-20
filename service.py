import fileoperate

def create_service(name, subid, service_name, service_port, service_password):
    '''
    创建服务
    '''
    service_data = read_service_config(name)
    service_item = {}
    service_item['subid'] = subid
    service_item['service_port'] = service_port
    service_item['service_password'] = service_password
    service_item['service_list'] = service_name.upper()
    service_item['services'] = {}
    service_data[subid] = service_item
    write_service_config(name, service_data)
    return True

def read_service_config(name):
    '''
    读取service配置数据
    '''
    return fileoperate.read_server_service_file(name)

def write_service_config(name, data):
    '''
    写入service配置数据
    '''
    return fileoperate.write_server_service_file(name, data)