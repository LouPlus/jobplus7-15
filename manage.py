#!/usr/bin/python3
# -*- coding: <encoding name> -*-

from jobplus.app import create_app

app = create_app('') #环境模式选择，此处暂未选择

if __name__ == '__main__':
    app.run
