#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
translation
~~~~~~~~~~~~~~~~~

简体转换成繁体

Usage:
    1. 修改translation.py file_types。更改进行简体转换台湾繁体的文件的后缀，默认iOS
    2. 打開終端.
    3. brew install opencc enca
    4. 切換到需要簡體轉換繁體的目錄.
    5. 運行 'path/translation.py'.
       'path' is the path from project's root to this script file.
"""

file_types = ['m','h','swift','storyboard','plist','pch','c','mm','cpp'] # iOS
#file_types = ['java','kt','html','json','xml'] # Android


import os
import re
import opencc
from argparse import ArgumentParser
from utils import console
from utils import file_assistant
import subprocess

def get_file_encoding(filename):
    filename = re.sub(' ', '\ ',filename)
    file_encode_type = subprocess.Popen("enca -L zh -i {}".format(filename), shell=True, stdout=subprocess.PIPE).stdout.read()
    file_encode_type = str(file_encode_type.decode('utf-8'))
    file_encode_type = re.sub('-', '_',file_encode_type)
    return file_encode_type.lower()


def main():
    current_path = os.getcwd()
    print('Current directory: ' + current_path)

    assets_paths = file_assistant.get_paths(
        current_path,
        types=file_types,
        exclusive_paths=['Pods','framework']
        )

    if not assets_paths:
        console.print_fail('没有找到任何文件')
        exit(1)

    pattern = re.compile(r'[\u4E00-\u9FA5]+[^"]*?')
    for assets_path in assets_paths:
        file_encoding = get_file_encoding(assets_path)
        #print(file_encoding)
        #print(assets_path)
        try:
            with open(assets_path, 'r',encoding = file_encoding) as read_source_file:
                text = read_source_file.read()
                
                result = pattern.findall(text)
                for chineseString in result:
                    converter = opencc.OpenCC(config='s2twp.json', opencc_path='/usr/local/bin/opencc')
                    didConverString = converter.convert(chineseString)
                    if len(didConverString) < 1:
                        console.print_fail('转换失败了，请撤销改动')
                        exit(1)
                    text = re.sub(chineseString, didConverString, text)
                    print(chineseString + "\tconver to\t" + didConverString)
            
                with open(assets_path, 'w',encoding =file_encoding) as write_source_file:
                    write_source_file.write(text)
        except Exception as error:
            console.print_fail("error: {}".format(error))

    console.print_green('简体转换繁体完成')

if __name__ == "__main__":
    main()
