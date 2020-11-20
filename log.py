import fileoperate

def write_log(name, content):
	'''
	写入日志
	'''
	fileoperate.write_file(name, 'log.txt', '%s\n'%content)