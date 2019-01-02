#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
translation
~~~~~~~~~~~~~~~~~

简体转换成繁体

Usage:
    1. 打開終端.
    2. 切換到需要簡體轉換繁體的目錄.
    3. 運行 'path/translation.py --changeencode 1'.
       'path' is the path from project's root to this script file.
    4. 最好先把文件編碼轉換成 utf-8下，內容無變化再直接運行腳本 'path/translation.py'
"""

import os
import re
import chardet
import opencc
from argparse import ArgumentParser
from utils import console
from utils import file_assistant

def convert_encoding(filename, target_encoding):
    # Backup the origin file.

    # convert file from the source encoding to target encoding
    with open(filename, 'rb') as source_file:
        content = source_file.read()
        source_encoding = chardet.detect(content)['encoding']
        language = chardet.detect(content)['language']
        if source_encoding == 'Windows-1254' :
            # 項目中個別個文件，utf-8識別成Windows-1254，暫時這樣修復處理
            source_encoding='utf-8'
        print(source_encoding, filename, chardet.detect(content))
        if source_encoding != target_encoding:
            content = content.decode(source_encoding) #.encode(source_encoding)
            if content == None:
                print('the file no text')
                exit()
            with open(filename, 'wb+') as source_file_utf8:
                content = content.encode(target_encoding)
                source_file_utf8.write(content)

def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--changeencode",
        help="change encode",
        type=int)
    args = parser.parse_args()
    changeencode = 0
    if args.changeencode == 1:
        changeencode = 1

    current_path = os.getcwd()
    print('Current directory: ' + current_path)

    assets_paths = file_assistant.get_paths(
        current_path,
        types=['m','h','swift','storyboard','plist','pch','c','mm','cpp'],
        exclusive_paths=['Pods','framework']
        )

    if not assets_paths:
        console.print_fail('没有找到文件')
        exit(1)

    pattern = re.compile(r'[\u4E00-\u9FA5]+[^"]*?')
    if changeencode == 1:
        print("轉換文件編碼為utf-8")

    for assets_path in assets_paths:
        print(assets_path)
        try:
            os.chmod(assets_path, "777")
            convert_encoding(assets_path, 'utf-8')
            with open(assets_path, 'r',encoding ='utf-8') as read_source_file:
                text = read_source_file.read()
                text = re.sub(r'å¹´', "年", text)
                text = re.sub(r'Â©', "©", text)
                text = re.sub(r'â€™', "’", text)

                result = pattern.findall(text)
                if changeencode != 1:
                    for chineseString in result:
                        converter = opencc.OpenCC(config='s2twp.json', opencc_path='/usr/local/bin/opencc')
                        didConverString = converter.convert(chineseString)
                        if len(didConverString) < 1:
                            console.print_fail('转换失败了，请撤销改动')
                            exit(1)
                        text = re.sub(chineseString, didConverString, text)
                        print(chineseString + "\tconver to\t" + didConverString)

                with open(assets_path, 'w',encoding ='utf-8') as write_source_file:
                    write_source_file.write(text)
        except:
                pass
    if changeencode == 1:
        console.print_green('文件编码改utf-8完成')
    else:
        console.print_green('简体转换繁体完成')

if __name__ == "__main__":
    main()
