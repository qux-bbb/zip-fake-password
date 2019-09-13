# coding:utf8
# author: qux
'''
zip伪加密去除脚本
'''

import sys
import re

def removefade(para1):
	# 读取原zip文件
	zipfile = open(para1,'rb')
	zipfile_content = zipfile.read().encode('hex')
	zipfile.close()

	# 定位加密标志位并清零
	# Local file header
	about_global_enc_flag_re = r'504b0304.{8}'
	match_contents = re.findall(about_global_enc_flag_re, zipfile_content)
	if match_contents:
		print '[*] Modify local file header flag:'
		for match_content in match_contents:
			modified_content = match_content[:12] + hex(int(match_content[12:14], 16) & 0b11111110)[2:].zfill(2) + match_content[14:]
			print '    ' + match_content + ' --> ' + modified_content
			zipfile_content = zipfile_content.replace(match_content, modified_content)
	
	# Central directory header
	about_file_enc_flag_re = r'504b0102.{12}'
	match_contents = re.findall(about_file_enc_flag_re, zipfile_content)
	if match_contents:
		print '[*] Modify central directory header flag:'
		for match_content in match_contents:
			modified_content = match_content[:16] + hex(int(match_content[16:18], 16) & 0b11111110)[2:].zfill(2) + match_content[18:]
			print '    ' + match_content + ' --> ' + modified_content
			zipfile_content = zipfile_content.replace(match_content, modified_content)
	
	# 将处理后内容写入新文件
	newzip = open(para1[:-4] + '_repair.zip','wb')
	newzip.write(zipfile_content.decode('hex'))
	newzip.close()
	print('Done')


if __name__ == '__main__':
	if(len(sys.argv) != 2):
		print('\nusage example:')
		print(' python dzipfade.py a.zip\n')
	else:
		para = sys.argv
		removefade(para[1])
