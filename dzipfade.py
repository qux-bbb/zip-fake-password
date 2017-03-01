#! python3
# coding:utf8
# author: neo
'''
zip伪加密去除脚本
'''

import sys

def removefade(para1):
	# 读取原zip文件
	zipfile = open(para1,'rb')
	zipfile_content = zipfile.read().encode('hex')
	zipfile.close()

	zf_len = len(zipfile_content)

	# 查找加密标志位并处理
	for i in xrange(zf_len):
		comp_con = zipfile_content[i:i+8]
		if comp_con == '504b0102':
			zipfile_content = zipfile_content[:i+17] + '0' + zipfile_content[i+18:]
		if comp_con == '504b0304':
			zipfile_content = zipfile_content[:i+13] + '0' + zipfile_content[i+14:]


	# 将处理后内容写入新文件
	newzip = open(para1[:-4] + 'repair.zip','wb')
	newzip.write(zipfile_content.decode('hex'))
	newzip.close()
	print('Done')


if __name__ == '__main__':
	if(len(sys.argv) == 1):
		print('\nusage example:')
		print(' python dzipfade.py a.zip\n')
	else:
		para = sys.argv
		removefade(para[1])
