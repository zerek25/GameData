#!/user/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

from util import global_var_gi
from genshin import path, config


# 处理成就
def process_achievements():
    # 打开文件

    with open(path.get("AchievementExcelConfigData"), encoding='utf-8') as load_f:
        achievement_excel_config_data = json.load(load_f)
    with open(path.get("AchievementGoalExcelConfigData"), encoding='utf-8') as load_f:
        achievement_goal_excel_config_data = json.load(load_f)
    with open(path.get("RewardExcelConfigData"), encoding='utf-8') as load_f:
        reward_excel_config_data = json.load(load_f)
    with open(path.get("TextMapCHS"), encoding='utf-8') as load_f:
        text_map_chs = json.load(load_f)
    with open(os.path.join(path.get("Json"), "AchievementExcelConfigData.json"), encoding='utf-8') as load_f:
        achievement_data_local = json.load(load_f)

    # 成就黑名单
    black_list = [84517]

    # 遍历合辑
    goal_list = {}
    for goal in achievement_goal_excel_config_data:
        goal_list[goal.get("id", 10001)] = {
            "id": goal.get("id", 10001),
            "title": text_map_chs.get(str(goal.get("nameTextMapHash"))),
            "order": goal.get("orderId"),
        }
    global_var_gi.set_gi_value("AchievementGoalExcelConfigData", goal_list)

    # 遍历成就
    achievement_list = {}
    config_daily = config.get("daily-task-achievement")
    config_trigger = config.get("trigger")
    config_tag = config.get("tag")

    # 未使用tag合辑
    unused_tag = set()

    for achievement in achievement_excel_config_data:
        # 可获取数据
        achievement_id = achievement.get("id")
        if (achievement_id in black_list) or achievement.get("isDisuse"):
            continue
        achievement_title = text_map_chs.get(str(achievement.get("titleTextMapHash")))
        achievement_desc = text_map_chs.get(str(achievement.get("descTextMapHash")))
        achievement_desc = achievement_desc.replace("{param0}", str(achievement.get("progress")))
        achievement_sid = achievement.get("goalId", 10001)
        achievement_series = goal_list.get(achievement_sid).get("title")
        achievement_reward = next(
            reward["rewardItemList"][0]["itemCount"] for reward in reward_excel_config_data if
            reward["rewardId"] == achievement["finishRewardId"])
        achievement_order = achievement.get("orderId")
        achievement_hide = "isShow" in achievement and achievement["isShow"] == "SHOWTYPE_HIDE"
        achievement_progress = achievement.get("progress")
        achievement_trigger = achievement["triggerConfig"]["triggerType"]
        achievement_pre = achievement.get("preStageAchievementId", 0)

        # 自定义数据
        achievement_local = achievement_data_local.get(str(achievement_id), {})
        achievement_version = achievement_local.get("version", path.VERSION)
        achievement_detail = achievement_local.get("detail", "")
        achievement_reference = achievement_local.get("reference", "")
        achievement_mission = achievement_local.get("mission", "")
        achievement_video = achievement_local.get("video", "")
        achievement_article = achievement_local.get("article", "")

        # 多来源数据
        if achievement_trigger not in config_trigger:
            config_trigger[achievement_trigger] = {
                "triggerType": achievement_trigger,
                "triggerDesc": achievement_trigger,
                "triggerTags": []
            }
        achievement_t_desc = config_trigger[achievement_trigger].get("triggerDesc")

        achievement_tag_temp = achievement_local.get("tag", [])
        achievement_tag_temp.extend(config_trigger[achievement_trigger].get("triggerTags"))
        if achievement_title in config_daily["achievement"]:
            achievement_tag_temp.append("委托任务")
        achievement_tag_temp = list(set(achievement_tag_temp))

        achievement_tag = []
        for tag in config_tag:
            tag_list = config_tag[tag].get("list", [])
            count = 0
            for item in tag_list:
                if item in achievement_tag_temp:
                    achievement_tag.append(item)
                    achievement_tag_temp.remove(item)
                    count += 1
            if tag in achievement_tag_temp:
                achievement_tag_temp.remove(tag)
            if config_tag[tag].get("showMain", False) and count > 0:
                achievement_tag.append(tag)
        unused_tag.update(achievement_tag_temp)

        achievement_list[achievement_id] = {
            "id": achievement_id,
            "order": achievement_order,
            "title": achievement_title,
            "desc": achievement_desc,
            "sid": achievement_sid,
            "series": achievement_series,
            "reward": achievement_reward,
            "progress": achievement_progress,
            "hide": achievement_hide,
            "pre": achievement_pre,
            "trigger": achievement_trigger,
            "version": achievement_version,
            "detail": achievement_detail,
            "reference": achievement_reference,
            "mission": achievement_mission,
            "video": achievement_video,
            "article": achievement_article,
            "tDesc": achievement_t_desc,
            "tag": achievement_tag,
        }

    if len(unused_tag) > 0:
        print("未标记的tag:", list(unused_tag))
    config.set_data("trigger", config_trigger)
    global_var_gi.set_gi_value("AchievementExcelConfigData", achievement_list)
