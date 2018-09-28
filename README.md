# translation
iOS 项目简体转换繁体

# 安装第三方依赖
pip3 install chardet
brew install opencc

# 使用
先進入到工程目錄，運行
path/translation.py --changeencode 1

等到把所有文件转换成utf-8后，查看git变动是否有变化。
如果无变化，证明没有内容变更，可以进行下一步简繁转换。
