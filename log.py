import fileoperate

def write_log(platform_name, name, content):
	'''
	写入日志
	'''
	fileoperate.write_file(platform_name, name, 'log.txt', '%s\n'%content)