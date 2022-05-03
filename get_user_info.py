import json
import os

import requests
import xlwt

import agent


def get_header():
    headers = {"User-Agent": agent.get_user_agents(),
               "Referer": "https://www.bilibili.com/"}
    return headers


def get_info(mid):
    user_url = "https://api.bilibili.com/x/space/acc/info"

    headers = get_header()

    user_info = requests.get(user_url,
                             params={
                                 "mid": mid,
                                 "jsonp": "jsonp"
                             }, headers=headers).json()

    with open("user_info.json", "w", encoding="utf-8") as f:
        # f.write(str(user_info))
        json.dump(user_info, f)


def all_gift_info():
    gift_url = "https://api.live.bilibili.com/xlive/web-room/v1/giftPanel/giftConfig"

    headers = get_header()

    gift_info = requests.get(gift_url,
                             params={
                                 # 'tab_id': 1,
                                 'room_id': 1184275,
                                 'area_id': 371,
                                 'area_parent_id': 9,
                                 'platform': 'pc',
                                 # 'source': 'live',
                                 # 'build': 1
                             }, headers=headers).json()

    # with open("gift_info.json", "w", encoding="utf-8") as f:
    #     json.dump(gift_info, f)

    gift_list = gift_info['data']['list']
    result_dict = {}
    for i in range(len(gift_list)):
        result_dict[gift_list[i]["id"]] = {
            "price": gift_list[i]["price"] / 100,
            "name": gift_list[i]["name"]
        }

    return result_dict


def room_gift_info(gift_dicts, settings):
    gift_url = "https://api.live.bilibili.com/xlive/web-room/v1/giftPanel/giftData"
    tab_gift_url = "https://api.live.bilibili.com/xlive/web-room/v1/giftPanel/tabRoomGiftList"
    headers = get_header()

    gift_info = requests.get(gift_url,
                             params={
                                 # 'tab_id': 1,
                                 'ruid': settings["ruid"],
                                 'room_id': settings["room_id"],
                                 'area_id': settings["area_id"],
                                 'area_parent_id': settings["area_parent_id"],
                                 'platform': 'pc',
                                 'source': 'live',
                                 # 'build': 1
                             }, headers=headers).json()

    tab_gift_all_list = []
    for tab_id in (2, 3):
        tab_gift_info = requests.get(tab_gift_url,
                                     params={
                                         'tab_id': tab_id,
                                         # 'ruid': 1485569,
                                         'room_id': settings["room_id"],
                                         'area_id': settings["area_id"],
                                         'area_parent_id': settings["area_parent_id"],
                                         'platform': 'pc',
                                         'source': 'live',
                                         'build': 1
                                     }, headers=headers).json()
        tab_gift_list = tab_gift_info['data']['list']
        tab_gift_all_list.append(tab_gift_list)

    # with open("gift_info.json", "w", encoding="utf-8") as f:
    #     json.dump(gift_info, f)

    gift_list = gift_info['data']['room_gift_list']['gold_list']
    # discount_gift_list = gift_info['data']['discount_gift_list']
    # if discount_gift_list is None:
    #     discount_gift_list = []
    # discount_gift_dict = {}
    #
    # for i in range(len(discount_gift_list)):
    #     discount_gift_dict[discount_gift_list[i]["gift_id"]] = discount_gift_list[i]["discount_price"]
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("礼物列表")
    sheet_head = ["id", "name", "price"]
    for i in range(len(sheet_head)):
        sheet.write(0, i, sheet_head[i])
    for i in range(1, len(gift_list) + 1):
        gift_id = gift_list[i - 1]["id"]
        sheet.write(i, 0, gift_id)
        sheet.write(i, 1, gift_dicts[gift_id]["name"])
        sheet.write(i, 2, gift_dicts[gift_id]["price"])
        # if gift_list[i]["id"] in discount_gift_dict:
        #     sheet.write(i, 3, discount_gift_dict[gift_id])
    sheet1 = wb.add_sheet("特权礼物")
    sheet1_head = ["id", "name", "price"]
    for i in range(len(sheet1_head)):
        sheet1.write(0, i, sheet1_head[i])
    for i in range(1, len(tab_gift_all_list[0]) + 1):
        gift_id = tab_gift_all_list[0][i - 1]["gift_id"]
        sheet1.write(i, 0, gift_id)
        sheet1.write(i, 1, gift_dicts[gift_id]["name"])
        sheet1.write(i, 2, gift_dicts[gift_id]["price"])

    sheet2 = wb.add_sheet("定制礼物")
    sheet2_head = ["id", "name", "price"]
    for i in range(len(sheet2_head)):
        sheet2.write(0, i, sheet2_head[i])
    for i in range(1, len(tab_gift_all_list[1]) + 1):
        gift_id = tab_gift_all_list[1][i - 1]["gift_id"]
        sheet2.write(i, 0, gift_id)
        sheet2.write(i, 1, gift_dicts[gift_id]["name"])
        sheet2.write(i, 2, gift_dicts[gift_id]["price"])

    wb.save("礼物列表.xls")


def get_setting():
    now_dir = os.getcwd()
    setting_file = os.path.join(now_dir, "setting.json")
    if os.path.exists(setting_file):
        with open(setting_file) as f:
            settings = json.load(f)
    else:
        settings = {
            "ruid": 1485569,
            "room_id": 1184275,
            "area_id": 371,
            "area_parent_id": 9
        }

    return settings


if __name__ == "__main__":
    # get_info(35192025)
    while True:
        now_dir = os.getcwd()
        create_file = os.path.join(now_dir, "礼物列表.xls")
        if os.path.exists(create_file):
            temp1 = input("当前列表存在“礼物列表.xls”，请输入“q”并回车确认覆盖：")
            if temp1 == "q":
                break
        else:
            break

    print("开始获取礼物列表")
    gift_dict = all_gift_info()
    setting = get_setting()
    room_gift_info(gift_dict, setting)
    print("已生成“礼物列表.xls”")
    input("获取完成，按回车结束程序")
