# coding:utf-8
import json
import os.path

from genshin import path as gi_path
from starrail import path as sr_path


global _gi_dict
global _sr_dict


def __init():  # 初始化
    global _gi_dict
    global _sr_dict
    _gi_dict = {}
    _sr_dict = {}


def set_sr_value(key, value):
    _sr_dict[key] = value
    json_path = os.path.join(sr_path.get("Json"), key + ".json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, separators=(',', ':'))


def get_sr_value(key, def_value=None):
    try:
        return _sr_dict[key]
    except KeyError:
        return def_value


def set_gi_value(key, value):
    _gi_dict[key] = value
    json_path = os.path.join(gi_path.get("Json"), key + ".json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, separators=(',', ':'))


def get_gi_value(key, def_value=None):
    try:
        return _gi_dict[key]
    except KeyError:
        return def_value


def export_file():
    for k, v in _sr_dict.items():
        json_path = os.path.join(sr_path.get("Json"), k + ".json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(v, f, ensure_ascii=False, indent=2, separators=(',', ':'))

    for k, v in _gi_dict.items():
        json_path = os.path.join(gi_path.get("Json"), k + ".json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(v, f, ensure_ascii=False, indent=2, separators=(',', ':'))


__init()
