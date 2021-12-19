# coding:utf8
# author: qux
'''
zip伪加密
'''

import re
import argparse


def process_zip(mode, the_path):
    # 读取原zip文件
    zipfile = open(the_path,'rb')
    zipfile_content = zipfile.read()
    zipfile.close()

    # 定位加密标志位并修改
    # Local file header
    global_enc_flag_re = rb'\x50\x4b\x03\x04[\x00-\xff]{4}'
    match_contents = re.findall(global_enc_flag_re, zipfile_content)
    if match_contents:
        print('[*] Modify local file header flag:')
        for match_content in match_contents:
            if mode == 'forge':
                tmp = match_content[6] | 0b00000001
            else:  # 'repair'
                tmp = match_content[6] & 0b11111110
            modified_content = match_content[:6] + bytes([tmp, match_content[7]])
            print('    -'+match_content.hex())
            print('    +'+modified_content.hex())
            zipfile_content = zipfile_content.replace(match_content, modified_content)
    
    # Central directory header
    file_enc_flag_re = rb'\x50\x4b\x01\x02[\x00-\xff]{6}'
    match_contents = re.findall(file_enc_flag_re, zipfile_content)
    if match_contents:
        print('[*] Modify central directory header flag:')
        for match_content in match_contents:
            if mode == 'forge':
                tmp = match_content[8] | 0b00000001
            else:  # 'repair'
                tmp = match_content[8] & 0b11111110
            modified_content = match_content[:8] + bytes([tmp, match_content[9]])
            print('    -'+match_content.hex())
            print('    +'+modified_content.hex())
            zipfile_content = zipfile_content.replace(match_content, modified_content)
    
    # 将处理后内容写入新文件
    new_path = the_path[:-4] + '_{}.zip'.format(mode)
    new_zipfile = open(new_path, 'wb')
    new_zipfile.write(zipfile_content)
    new_zipfile.close()
    print('[.] {} generated.'.format(new_path))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['forge', 'repair'])
    parser.add_argument('zip_path')
    args = parser.parse_args()

    process_zip(args.mode, args.zip_path)


if __name__ == '__main__':
    main()
