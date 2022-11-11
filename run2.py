import sys
import os
import shutil
import requests
from requests.auth import HTTPDigestAuth
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import base64
import time
import datetime
import sql_query
import detect3 as detect

INTERVAL_SECONDS = 10
#URL = f'http://192.168.1.200/jpg/image.jpg'
WIDTH = 512
HEIGHT = 480

def get_image(img_binary):
    img_bin = BytesIO(img_binary)
    img =  Image.open(img_bin)
    return img

def expand2square(pil_img, size=640, background_color=(0, 0, 0)):
    width, height = pil_img.size
    if width == height:
        return pil_img.resize((size,size))
    elif width > height:
        rh = int(height * size / width)
        pil_img = pil_img.resize((size, rh))
        result = Image.new(pil_img.mode, (size, size), background_color)
        result.paste(pil_img, (0, (size - rh) // 2))
        return result
    else:
        rw = int(width * size / height)
        pil_img = pil_img.resize((rw, size))
        result = Image.new(pil_img.mode, (size, size), background_color)
        result.paste(pil_img, ((size - rw) // 2, 0))
        return result

def NdarrayToBase64(img):
    buffered = BytesIO()
    img.save(buffered, format="png")
    img_base64 = base64.b64encode(buffered.getvalue())

    return img_base64.decode('utf-8')
 
def creat_new_folder(path):
    if not os.path.exists(path):#ディレクトリがなかったら
        os.mkdir(path)#作成したいフォルダ名を作成

def cal_aspect_ratio(ox,oy):
      x, y = ox, oy
      while y:
        x, y = y, x % y
      return (ox/x, oy/x)

def analys(url, path, id):
    dba = sql_query.DbAccess()
    data = None
    if('image.jpg' in url):
        data = requests.get(url ,auth=HTTPDigestAuth('root', 'password'))
    else:
        data = requests.get(url)
    
    img_orgin = get_image(data.content)
    aspect_ratio = cal_aspect_ratio(img_orgin.width,img_orgin.height)
    origin_size = WIDTH / aspect_ratio[0]
    reseize_height = int(origin_size * aspect_ratio[1])
    img_resize = img_orgin.resize((WIDTH, reseize_height))
    img = expand2square(img_resize)
    now = datetime.datetime.now()
    img_name = str('image_' + now.strftime('%Y-%m-%d_%Hz%Mz%S') + '.jpg')
    img_folder = path + 'img/' + now.strftime('%Y-%m-%d') + '/'
    creat_new_folder(img_folder) 
    img_path = img_folder + img_name
    img_resize.save(img_path)

    img_ai_folder = path + 'img_ai/' + now.strftime('%Y-%m-%d') + '/'
    creat_new_folder(img_ai_folder)
    result, cx1, cy1, cx2, cy2 = detect.detect(img_path, img_name, img_ai_folder)
    if(result == -1):
        isThere = False
    else:
        isThere = True
    img_base64 = 'data:image/png;base64,' + NdarrayToBase64(img_resize)
    where = f'id={id}'
    d = {'latest_status': isThere, 'latest_update':now, 'image_src':img_base64}
    dba.db_update('funamiAI_result_of_analysis',where=where,**d)
    d = {'id': id,'is_there': isThere, 'status': result, 'insert_date':now, 'image_path':img_path.replace("/", "\\")}
    dba.db_insert('funamiAI_results',**d)
    return d

def judge_track():      
    isThere = True
    print('Running')
    beyond = 0

    while True:
        try:
            strat = time.time()
            now = datetime.datetime.now()
            folder = '//ts-funami2/share/iot/funami/clustering/' + now.strftime('%Y-%m-%d') + '/'
            creat_new_folder(folder)

            #data = requests.get('http://192.168.2.191/jpg/image.jpg' ,auth=HTTPDigestAuth('guest', 'tozan1234'))
            d1 = analys('http://root:password@192.168.2.150/jpg/image.jpg', '//ts-funami2/share/iot/funami/1/', 1)
            d2 = analys('http://root:password@192.168.2.151/jpg/image.jpg', '//ts-funami2/share/iot/funami/2/', 2)
            d3 = analys('http://root:password@192.168.2.152/jpg/image.jpg', '//ts-funami2/share/iot/funami/3/', 3)
            d4 = analys('http://root:password@192.168.2.153/jpg/image.jpg', '//ts-funami2/share/iot/funami/4/', 4)
            d5 = analys('http://root:password@192.168.2.154/jpg/image.jpg', '//ts-funami2/share/iot/funami/5/', 5)
            d6 = analys('http://root:password@192.168.2.155/jpg/image.jpg', '//ts-funami2/share/iot/funami/6/', 6)
            d7 = analys('http://root:password@192.168.2.156/jpg/image.jpg', '//ts-funami2/share/iot/funami/7/', 7)
            d8 = analys('http://root:password@192.168.2.157/jpg/image.jpg', '//ts-funami2/share/iot/funami/8/', 8)
            d9 = analys('http://root:password@192.168.2.158/jpg/image.jpg', '//ts-funami2/share/iot/funami/9/', 9)
            d10 = analys('http://root:password@192.168.2.159/jpg/image.jpg', '//ts-funami2/share/iot/funami/10/', 10)
            #d3 = analys('http://guest:tozan1234@192.168.7.30/jpg/image.jpg', '//ts-nawa/share/iot/nawa/99/', 3)

            if d1["is_there"]:
                folder += str(d1["status"])
            else:
                folder += "none"            
            creat_new_folder(folder)

            shutil.copy(d1["image_path"], folder)
            end = time.time() - strat + beyond
            if end < INTERVAL_SECONDS:
                wait = INTERVAL_SECONDS - (end)
                beyond = 0
                time.sleep(wait)
            else:
                beyond = end - INTERVAL_SECONDS
        except:
            print('error!')
            
        

if __name__ == "__main__":
    judge_track()