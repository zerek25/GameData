# coding:utf-8
from operator import itemgetter

import pymongo
from bson import json_util

from util import global_var_sr
import xlsx
from starrail import path

# 数据库设置
CLIENT = pymongo.MongoClient("mongodb://localhost:27017/")
DB = CLIENT["findie"]
ACHIEVEMENT_COL = DB["sr-achievement"]
SERIES_COL = DB["sr-series"]

RARITY_LIST = {
    "High": {
        "text": "金",
        "reward": 20
    },
    "Mid": {
        "text": "银",
        "reward": 10
    },
    "Low": {
        "text": "铜",
        "reward": 5
    },
}


# 写入成就至数据库
def write_achievement():
    for achievement in global_var_sr.get_sr_value("AchievementData").values():
        achievement_filter = {'id': achievement["id"]}
        achievement_set = {"$set": achievement}
        ACHIEVEMENT_COL.update_one(achievement_filter, achievement_set, upsert=True)

    for achievement in global_var_sr.get_sr_value("AchievementSeries").values():
        achievement_filter = {'id': achievement["id"]}
        achievement_set = {"$set": achievement}
        SERIES_COL.update_one(achievement_filter, achievement_set, upsert=True)


# 生成uniCloud导出文件
def export_unicloud_file():
    with open(path.get("AchievementCloudOutputPath"), 'a+', encoding='utf-8') as f:
        # 清空文件
        f.seek(0)
        f.truncate()
        for achievement in ACHIEVEMENT_COL.find():
            # 添加记录
            f.write(json_util.dumps(achievement, ensure_ascii=False, ) + "\n")
    with open(path.get("SeriesCloudOutputPath"), 'a+', encoding='utf-8') as f:
        # 清空文件
        f.seek(0)
        f.truncate()
        for goal in SERIES_COL.find():
            # 添加记录
            f.write(json_util.dumps(goal, ensure_ascii=False, ) + "\n")


# 生成成就excel文件
def export_achievement_excel():
    print("开始生成成就Excel")
    header = ["ID", "成就", "描述", "稀有度", "奖励", "合辑", "状态", "版本"]
    achievement_list = [header]
    series_dict = global_var_sr.get_sr_value("AchievementSeries")
    version_dict = {}

    for achievement in global_var_sr.get_sr_value("AchievementData").values():
        sid = str(achievement["sid"])
        version = achievement["version"]
        achievement_data = [achievement["id"], achievement["title"], achievement["desc"],
                            RARITY_LIST[achievement["rarity"]]["text"], RARITY_LIST[achievement["rarity"]]["reward"],
                            series_dict.get(sid)["title"],
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
    xlsx.generate_excel(excel_data, "全成就-单表", "starrail/output/xlsx", "starrail")

    print("生成合辑Excel")
    series_excel_data = []
    for series in sorted(series_dict.values(), key=itemgetter('order')):
        series_excel_data.append({
            "title": "合辑『" + series["title"] + "』成就",
            "sheet_name": series["title"],
            "list": series["list"]
        })
    xlsx.generate_excel(series_excel_data, "全成就-合辑分表", "starrail/output/xlsx", "starrail")

    print("生成版本Excel")
    version_excel_data = []
    for version in sorted(version_dict, reverse=False):
        version_excel_data.append({
            "title": "星穹铁道 " + version + " 版本成就",
            "sheet_name": version + "版本",
            "list": version_dict[version]
        })
    xlsx.generate_excel(version_excel_data, "全成就-版本分表", "starrail/output/xlsx", "starrail")


# 生成成就图片
def export_achievement_image():
    print("开始生成成就图片")
    header = ["ID", "成就", "描述", "稀有度", "奖励", "合辑", "状态", "版本"]
    achievement_list = [header]
    series_dict = global_var_sr.get_sr_value("AchievementSeries")
    version_dict = {}

    for achievement in global_var_sr.get_sr_value("AchievementData").values():
        sid = str(achievement["sid"])
        version = achievement["version"]
        achievement_data = [achievement["id"], achievement["title"], achievement["desc"],
                            RARITY_LIST[achievement["rarity"]]["text"], RARITY_LIST[achievement["rarity"]]["reward"],
                            series_dict.get(sid)["title"],
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

    print("生成全成就图片")
    excel_data = [{
        "title": "星穹铁道1.1版本全成就",
        "sheet_name": "全成就",
        "list": achievement_list,
    }]
    xlsx.generate_image(excel_data, "starrail/output/image", "starrail")

    print("生成合辑图片")
    series_excel_data = []
    for series in series_dict:
        series_excel_data.append({
            "title": "合辑『" + series_dict[series]["title"] + "』成就",
            "sheet_name": str(series_dict[series]["order"]) + " - " + series_dict[series]["title"],
            "list": series_dict[series]["list"]
        })
    xlsx.generate_image(series_excel_data, "starrail/output/image/series", "starrail")

    print("生成版本图片")
    version_excel_data = []
    for version in version_dict:
        version_excel_data.append({
            "title": "星穹铁道 " + version + " 版本成就",
            "sheet_name": version + "版本",
            "list": version_dict[version]
        })
    xlsx.generate_image(version_excel_data, "starrail/output/image/version", "starrail")
