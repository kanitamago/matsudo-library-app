"""
foliumで地図上にプロットし、ファイル化する
"""
from app.scripts import libraryData
#import libraryData
import folium
import random
from time import sleep
from datetime import datetime
import os

#緯度(lat): 35.805649 経度(lon): 139.945003

matsudo = folium.Map(location=[35.805649, 139.945003], zoom_start=13)

library_data = libraryData.results

def default_position():
    position = libraryData.get_library_position(library_data)
    for lat, lon, name in position:
        folium.Marker([lat, lon], popup=name, icon=folium.Icon(color="blue", icon="book")).add_to(matsudo)
    print("CREATE DEFAULT POSITION.")

def put_library_position(circle_dic, circle_keywords):
    default_position()
    position = libraryData.get_library_position(library_data)
    color_str_lists = circle_color(circle_keywords)
    keyword_list = []
    color_list = []
    for lat, lon, name in position:
        for circle_items, color in zip(circle_dic.items(), color_str_lists):
            for keyword in [circle_items[0]]:
                keyword_list.append(keyword)
                color_list.append(color)
                for items in [circle_items[1]]:
                    for item in items:
                        if item.library_name in name:
                            circle_val = item.exist_num
                            circle_val = weight_val(circle_val)
                            folium.CircleMarker([lat, lon], radius=circle_val, color=color, fill_color=color).add_to(matsudo)
                        else:
                            continue
    keyword_set = sorted(set(keyword_list), key=keyword_list.index)
    color_set = sorted(set(color_list), key=color_list.index)
    keyword_color = {}
    if len(keyword_set) == len(color_set):
        for keyword, color in zip(keyword_set, color_set):
            keyword_color[keyword] = color
    return (True, keyword_color)

def weight_val(circle_val):
    WEIGHT = 10
    if circle_val > 500:
        circle_val = 600
    if circle_val <= 500 and circle_val > 400:
        circle_val = 550
    if circle_val <= 400 and circle_val > 300:
        circle_val = 500
    if circle_val <= 300 and circle_val > 200:
        circle_val = 450
    if circle_val <= 200 and circle_val > 100:
        circle_val = 400
    if circle_val <= 100 and circle_val > 50:
        circle_val = 350
    if circle_val <= 50 and circle_val > 25:
        circle_val = 300
    if circle_val <= 25 and circle_val >= 1:
        circle_val *= WEIGHT
    if circle_val == 0:
        circle_val = 5;
    return circle_val

def circle_color(circle_keywords):
    create_color_num = len(circle_keywords)
    color_num = list(range(0, 256))
    while True:
        color_lists = []
        color_str_lists = []
        for _ in range(create_color_num):
            color_list = random.sample(color_num, 3)
            color_lists.append(color_list)
        for color_list in color_lists:
            color_str = "rgb({}, {}, {})".format(color_list[0], color_list[1], color_list[2])
            color_str_lists.append(color_str)
        if len(set(color_str_lists)) == create_color_num:
            break
    return color_str_lists

def create_library_file(checker):
    if checker:
        folder = os.listdir("app/mapfile")
        if folder:
            filename = "app/mapfile/"+folder[0]
            os.remove(filename)
            sleep(2)
        matsudo.save("app/mapfile/library-map.html")
        print(" Create now.")
    else:
        return "Can not create file."
    return "Success create file."
