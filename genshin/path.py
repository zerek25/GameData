# coding:utf-8
import os

DATA_PATH = "genshin\\data"
OUTPUT_PATH = "genshin\\output"
FILE_PATH = {}
VERSION = u'1.0'


def __init():
    global VERSION
    for path, dir_list, file_list in os.walk(DATA_PATH):
        path_list = path.split("\\")
        if len(path_list) == 3:
            VERSION = path_list[-1]
            for file in file_list:
                file_name = file.split(".")[0]
                FILE_PATH[file_name] = os.path.join(path, file)

    FILE_PATH["AchievementCloudOutputPath"] = os.path.join(OUTPUT_PATH, "cloud\\AchievementCloud.json")
    FILE_PATH["SeriesCloudOutputPath"] = os.path.join(OUTPUT_PATH, "cloud\\SeriesCloud.json")

    FILE_PATH["Json"] = os.path.join(OUTPUT_PATH, "json")


def get(key_word, def_value=None):
    try:
        return FILE_PATH[key_word]
    except KeyError:
        return def_value


__init()
