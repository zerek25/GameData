# coding:utf-8
import json
import os

from util import global_var_sr
import xlsx
from starrail import path, database, config


# 获取奖励
def _get_reward(reward_id):
    with open(path.get("RewardData"), encoding='utf-8') as load_f:
        reward_data = json.load(load_f)
    with open(path.get("ItemConfig"), encoding='utf-8') as load_f:
        item_config = json.load(load_f)
    with open(path.get("ItemConfigRelic"), encoding='utf-8') as load_f:
        item_config_relic = json.load(load_f)
    with open(path.get("ItemConfigAvatarRank"), encoding='utf-8') as load_f:
        item_config_avatar_rank = json.load(load_f)
    with open(path.get("ItemConfigEquipment"), encoding='utf-8') as load_f:
        item_config_equipment = json.load(load_f)
    with open(path.get("TextMapCN"), encoding='utf-8') as load_f:
        text_map_cn = json.load(load_f)
    reward_info = reward_data[reward_id]
    reward_list = {}
    if "Hcoin" in reward_info:
        reward_list["星琼"] = reward_info.get("Hcoin", 0)
    i = 1
    while True:
        item_id_str = "ItemID_" + str(i)
        count_str = "Count_" + str(i)
        if item_id_str in reward_info:
            item_id = reward_info.get(item_id_str)
            item_name_hash = item_config.get(str(item_id)) \
                             or item_config_relic.get(str(item_id)) \
                             or item_config_avatar_rank.get(str(item_id)) \
                             or item_config_equipment.get(str(item_id))
            item_name_hash = item_name_hash["ItemName"]["Hash"]
            item_name = text_map_cn.get(str(item_name_hash))
            count = reward_info.get(count_str)
            reward_list[item_name] = count
            i = i + 1
        else:
            break

    return reward_list


# 处理成就数据
def process_achievements():
    # 打开文件
    with open(path.get("AchievementData"), encoding='utf-8') as load_f:
        achievement_data = json.load(load_f)
    with open(path.get("AchievementSeries"), encoding='utf-8') as load_f:
        achievement_series = json.load(load_f)
    with open(path.get("TextMapCN"), encoding='utf-8') as load_f:
        text_map_cn = json.load(load_f)
    with open(os.path.join(path.get("Json"), "AchievementData.json"), encoding='utf-8') as load_f:
        achievement_data_local = json.load(load_f)

    # 加载配置
    branch_config = config.get("branch")

    # 处理成就合辑
    achievement_series_list = {}
    for key, series in achievement_series.items():
        achievement_series_list[key] = {
            "id": series["SeriesID"],
            "title": text_map_cn.get(str(series["SeriesTitle"]["Hash"])),
            "order": series["Priority"],
        }
    global_var_sr.set_sr_value("AchievementSeries", achievement_series_list)

    # 处理成就
    achievement_list = {}
    for key, achievement in achievement_data.items():
        # 获取本地数据
        achievement_local = achievement_data_local.get(key, {})
        # 处理描述
        desc = text_map_cn \
            .get(str(achievement["AchievementDesc"]["Hash"]), "") \
            .replace("<unbreak>", "") \
            .replace("</unbreak>", "")
        i = 1
        # 处理描述中的参数
        for param in achievement["ParamList"]:
            param_key = "#" + str(i) + "[i]"
            param_pos = desc.find(param_key) + len(param_key)
            if param_pos > len(desc):
                param_pos = 0
            last_char = desc[param_pos]
            if last_char == '%':
                desc = desc.replace(param_key, str(round(param["Value"] * 100)))
            else:
                desc = desc.replace(param_key, str(round(param["Value"])))
            i = i + 1
        # 处理标题
        title = text_map_cn.get(str(achievement["AchievementTitle"]["Hash"]), "") \
            .replace("<unbreak>", "") \
            .replace("</unbreak>", "")
        # 处理分支成就
        br = []
        tags = []
        for brs in branch_config:
            if int(achievement["AchievementID"]) in brs["list"]:
                br = brs["list"]
                tags.append("分支成就")

        achievement_list[key] = {
            "id": achievement["AchievementID"],
            "sid": achievement["SeriesID"],
            "series": achievement_series_list[str(achievement["SeriesID"])]["title"],
            "title": title,
            "desc": desc,
            "hideDesc": text_map_cn.get(str(achievement["HideAchievementDesc"]["Hash"]), ""),
            "order": achievement["Priority"],
            "rarity": achievement["Rarity"],
            "branch": br,
            "hide": achievement.get("ShowType", False) == "ShowAfterFinish",
            "version": achievement_local.get("version", path.VERSION),
            "detail": achievement_local.get("detail", ""),
            "ref": achievement_local.get("ref", ""),
            "tag": tags,
        }
        if achievement_list[key]["hideDesc"] != "":
            achievement_list[key]["desc"] = achievement_list[key]["hideDesc"]
            achievement_list[key]["hideDesc"] = desc
    global_var_sr.set_sr_value("AchievementData", achievement_list)

    # 写入数据库
    database.write_achievement()


# 处理开拓等级数据
def process_player_level():
    # 打开文件
    with open(path.get("PlayerLevelConfig"), encoding='utf-8') as load_f:
        player_level_config = json.load(load_f)

    # 计算等级
    player_level_data = {}
    total_exp = 0
    for level, level_info in player_level_config.items():
        player_level_data[level] = [level, level_info.get("PlayerExp", 0), 0]
        if "PlayerExp" in level_info:
            player_level_data[str(int(level) - 1)][2] = level_info["PlayerExp"] - total_exp
            total_exp = level_info.get("PlayerExp", 0)
        if "LevelRewardID" in level_info:
            player_level_data[level].append(_get_reward(str(level_info["LevelRewardID"])))
        else:
            player_level_data[level].append({})
    res = []
    excel_data = [["等级", "累计", "下一级", "增加值", "增长", "奖励"]]
    last_exp = 0
    for data in player_level_data.values():
        res.append({
            "level": data[0],
            "total": data[1],
            "next": data[2],
            "reward": data[3],
        })
        reward_str = ""
        for key, value in data[3].items():
            reward_str = reward_str + key + " x " + str(value) + "\n"
        reward_str = reward_str[:-1]
        if last_exp == 0 or data[2] == 0:
            exp = ""
            exp_percent = ""
        else:
            exp = data[2] - last_exp
            exp_percent = str(int((exp / last_exp) * 10000) / 100) + "%"
        last_exp = data[2]
        excel_data.append([data[0], data[1], data[2], exp, exp_percent, reward_str])
    global_var_sr.set_sr_value("PlayerLevelConfig", res)

    # 生成图片
    level_excel_data = [
        {
            "title": "开拓等级表",
            "sheet_name": "开拓等级表",
            "list": excel_data
        }
    ]
    xlsx.generate_image(level_excel_data, "starrail/output/image", "starrail")
    xlsx.generate_excel(level_excel_data, "开拓等级表", "starrail/output/xlsx", "starrail")

    print("开拓等级数据处理完毕")


# 每日实训
def process_daily_reward():
    # 打开文件
    with open(path.get("DailyActiveConfig"), encoding='utf-8') as load_f:
        daily_active_config = json.load(load_f)
    daily_active_reward = []
    for world_level, daily_active in daily_active_config.items():
        reward_list_res = []
        for reward in daily_active.values():
            reward_id = str(reward["DailyActiveReward"])
            reward_list = _get_reward(reward_id)
            reward_list_res.append(reward_list)
        daily_active_reward.append({
            "worldLevel": world_level,
            "reward": reward_list_res
        })

    global_var_sr.set_sr_value("DailyActiveConfig", daily_active_reward)

    # 遍历daily_active_reward获取总和的奖励
    daily_active_reward_total = [['均衡等级', '星琼', '里程', '信用点', '遗失碎金', '冒险记录']]
    for daily_active in daily_active_reward:
        reward_total = {}
        for reward in daily_active["reward"]:
            for key, value in reward.items():
                reward_total[key] = reward_total.get(key, 0) + value
        # 数组合并
        reward_total_list = [daily_active["worldLevel"]]
        for value in reward_total.values():
            reward_total_list.append(value)
        daily_active_reward_total.append(reward_total_list)

    # 生成图片
    daily_excel_data = [
        {
            "title": "每日实训奖励表",
            "sheet_name": "每日实训奖励表",
            "list": daily_active_reward_total
        }
    ]
    xlsx.generate_image(daily_excel_data, "starrail/output/image", "starrail")
    xlsx.generate_excel(daily_excel_data, "每日实训奖励表", "starrail/output/xlsx", "starrail")

    print("每日实训数据处理完毕")


# 处理个人签名
def process_message_contact():
    # 打开文件
    with open(path.get("MessageContactsConfig"), encoding='utf-8') as load_f:
        message_contacts_config = json.load(load_f)
    with open(path.get("TextMapCN"), encoding='utf-8') as load_f:
        text_map_cn = json.load(load_f)

    signature_list = {}
    for message in message_contacts_config.values():

        name_hash = str(message["Name"]["Hash"])
        signature_hash = str(message["SignatureText"]["Hash"])
        if text_map_cn.get(signature_hash, "") == "":
            continue
        name = text_map_cn.get(name_hash)
        signature = text_map_cn.get(signature_hash)
        signature_list[name] = signature

    global_var_sr.set_sr_value("MessageContactsConfig", signature_list)
    print("个人签名数据处理完毕")
