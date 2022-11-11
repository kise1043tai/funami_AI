import sys
import os
import datetime
import detect2 as detect
import glob
import csv

def creat_new_folder(path):
    if not os.path.exists(path):#ディレクトリがなかったら
        os.mkdir(path)#作成したいフォルダ名を作成

def AI_performance_evaluation():
    weights = glob.glob('test/weights/*.pt', recursive=True)
    labels = glob.glob('test/labels/*.txt', recursive=True)
    result_folder = 'test/result/'
    folder_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    folder_path = os.path.join(result_folder, folder_name) + '/'
    creat_new_folder(folder_path)

    img_ai_folder = os.path.join(folder_path)
    creat_new_folder(img_ai_folder)

    evaluation_record = []
    headder = ["label_name","tag"]
    for weight in weights:
         headder.append(os.path.splitext(weight)[0])

    evaluation_record.append(headder)
    for label in labels:
        record = []
        label_name = os.path.splitext(os.path.basename(label))[0]
        tag = ''
        with open(label, mode='r') as f:
            text = f.readlines()
            tag = text[0].split(' ')[0]
        record.append(label_name)
        record.append(tag)

        for weight in weights: 
            img_path = os.path.join('test/images/', label_name + '.jpg')
            img_name = label_name + "_" + os.path.splitext(os.path.basename(weight))[0] + '.jpg'
            res = detect.detect(img_path, img_name, img_ai_folder, weight)
            record.append(res)
        evaluation_record.append(record)
    with open(folder_path + 'result.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(evaluation_record)
        

if __name__ == "__main__":
    AI_performance_evaluation()