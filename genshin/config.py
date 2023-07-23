#!/user/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

CONFIG_PATH = "genshin\\config"
CONFIG = {}


def __init():
    global CONFIG
    for path, dir_list, file_list in os.walk(CONFIG_PATH):
        for file in file_list:
            # 打开file并按文件名保存至CONFIG中
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                CONFIG[file.split(".")[0]] = json.load(f)


def get(key_word, def_value=None):
    try:
        return CONFIG[key_word]
    except KeyError:
        return def_value


def set_data(key, data):
    return


__init()
