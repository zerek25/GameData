#!/user/bin/env python3
# -*- coding: utf-8 -*-
# 数据库设置
from operator import itemgetter

import pymongo

import xlsx
from util import global_var_gi

CLIENT = pymongo.MongoClient("mongodb://localhost:27017/")
DB = CLIENT["gwh"]
ACHIEVEMENT_COL = DB["gwh-achievement"]
SERIES_COL = DB["gwh-series"]


# 写入数据库
def write_achievement():
    for achievement in global_var_gi.get_gi_value("AchievementData").values():
        achievement_filter = {'id': achievement["id"]}
        achievement_set = {"$set": achievement}
        ACHIEVEMENT_COL.update_one(achievement_filter, achievement_set, upsert=True)

    for achievement in global_var_gi.get_gi_value("AchievementSeries").values():
        achievement_filter = {'id': achievement["id"]}
        achievement_set = {"$set": achievement}
        SERIES_COL.update_one(achievement_filter, achievement_set, upsert=True)


# 生成成就excel文件
def export_achievement_excel():
    print("开始生成成就Excel")
    header = ["ID", "成就", "描述", "合辑", "奖励", "状态", "版本"]
    achievement_list = [header]
    series_dict = global_var_gi.get_gi_value("AchievementGoalExcelConfigData")
    version_dict = {}

    for achievement in global_var_gi.get_gi_value("AchievementExcelConfigData").values():
        sid = achievement["sid"]
        version = achievement["version"]
        achievement_data = [achievement["id"], achievement["title"], achievement["desc"],
                            series_dict.get(sid)["title"], achievement["reward"],
                            "隐藏" if achievement["hide"] else "公开", version + "\t"]

        # 全成就
        achievement_list.append(achievement_data)

        # 合辑分表
        if "list" not in series_dict[sid]:
            series_dict[sid]["list"] = [header]
        series_dict[sid]["list"].append(achievement_data)

        # 版本分表
        if version not in version_dict:
            version_dict[version] = [header]
        version_dict[version].append(achievement_data)

    print("生成全成就Excel")
    excel_data = [{
        "title": "星穹铁道1.1版本全成就",
        "sheet_name": "全成就",
        "list": achievement_list,
    }]
    xlsx.generate_excel(excel_data, "全成就-单表", "genshin/output/xlsx", "genshin")

    print("生成合辑Excel")
    series_excel_data = []
    for series in sorted(series_dict.values(), key=itemgetter('order')):
        series_excel_data.append({
            "title": "合辑『" + series["title"] + "』成就",
            "sheet_name": series["title"],
            "list": series["list"]
        })
    xlsx.generate_excel(series_excel_data, "全成就-合辑分表", "genshin/output/xlsx", "genshin")

    print("生成版本Excel")
    version_excel_data = []
    for version in sorted(version_dict, reverse=False):
        version_excel_data.append({
            "title": "星穹铁道 " + version + " 版本成就",
            "sheet_name": version + "版本",
            "list": version_dict[version]
        })
    xlsx.generate_excel(version_excel_data, "全成就-版本分表", "genshin/output/xlsx", "genshin")


# 生成成就图片
def export_achievement_image():
    print("开始生成成就图片")
    header = ["ID", "成就", "描述", "合辑", "奖励", "状态", "版本"]
    achievement_list = [header]
    series_dict = global_var_gi.get_gi_value("AchievementGoalExcelConfigData")
    version_dict = {}

    for achievement in global_var_gi.get_gi_value("AchievementExcelConfigData").values():
        sid = achievement["sid"]
        version = achievement["version"]
        achievement_data = [achievement["id"], achievement["title"], achievement["desc"],
                            series_dict.get(sid)["title"], achievement["reward"],
                            "隐藏" if achievement["hide"] else "公开", version + "\t"]

        # 全成就
        achievement_list.append(achievement_data)

        # 合辑分表
        if "list" not in series_dict[sid]:
            series_dict[sid]["list"] = [header]
        series_dict[sid]["list"].append(achievement_data)

        # 版本分表
        if version not in version_dict:
            version_dict[version] = [header]
        version_dict[version].append(achievement_data)

    # print("生成全成就图片")
    # excel_data = [{
    #     "title": "原神4.0版本全成就",
    #     "sheet_name": "全成就",
    #     "list": achievement_list,
    # }]
    # xlsx.generate_image(excel_data, "genshin/output/image", "genshin")

    print("生成合辑图片")
    series_excel_data = []
    for series in series_dict:
        series_excel_data.append({
            "title": "合辑『" + series_dict[series]["title"] + "』成就",
            "sheet_name": str(series_dict[series]["order"]) + " - " + series_dict[series]["title"],
            "list": series_dict[series]["list"]
        })
    xlsx.generate_image(series_excel_data, "genshin/output/image/series", "genshin")

    print("生成版本图片")
    version_excel_data = []
    for version in version_dict:
        version_excel_data.append({
            "title": "原神 " + version + " 版本成就",
            "sheet_name": version + "版本",
            "list": version_dict[version]
        })
    xlsx.generate_image(version_excel_data, "genshin/output/image/version", "genshin")
