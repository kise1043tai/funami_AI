import sys
import os
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
import detect2 as detect

INTERVAL_SECONDS = 10
HOST_IP = '192.168.2.188'
HOST_PORT = '8000'
URL = f'http://' + HOST_IP + ':' + HOST_PORT
#URL = f'http://192.168.1.200/jpg/image.jpg'
WIDTH = 640
HEIGHT = 480

IMAGE_FOLDER = f'//ts-funami2/share/iot/funami/1/'
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

def analys(url, path, id):
    dba = sql_query.DbAccess()
    data = None
    if('image.jpg' in url):
        data = requests.get(url ,auth=HTTPDigestAuth('guest', 'tozan1234'))
    else:
        data = requests.get(url)
    
    img_orgin = get_image(data.content)
    img_resize = img_orgin.resize((WIDTH, HEIGHT))
    img = expand2square(img_orgin)
    now = datetime.datetime.now()
    img_name = str('image_' + now.strftime('%Y-%m-%d_%Hz%Mz%S') + '.jpg')
    img_path = path + 'img/' + img_name
    img_resize.save(img_path)

    result = detect.detect(img_path, img_name, path + 'img_ai/')
    if(result == -1):
        isThere = False
    else:
        isThere = True
    img_base64 = 'data:image/png;base64,' + NdarrayToBase64(img_orgin)
    where = f'id={id}'
    d = {'latest_status': isThere, 'latest_update':now, 'image_src':img_base64}
    dba.db_update('funamiAI_result_of_analysis',where=where,**d)
    d = {'id': id,'is_there': isThere, 'status': result, 'insert_date':now, 'image_path':img_path.replace("/", "\\")}
    dba.db_insert('funamiAI_results',**d)

def judge_track():      
    isThere = True
    print('Running')
    beyond = 0

    while True:
        try:
            strat = time.time()
            #data = requests.get('http://192.168.2.191/jpg/image.jpg' ,auth=HTTPDigestAuth('guest', 'tozan1234'))
            analys('http://192.168.2.188:8000', '//ts-funami2/share/iot/funami/1/', 1)
            analys('http://guest:tozan1234@192.168.2.191/jpg/image.jpg', '//ts-funami2/share/iot/funami/99/', 2)

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