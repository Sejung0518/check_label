"""
레이블링 검수 코드
"""

import os
import shutil
import xml.etree.ElementTree as ET
from PIL import Image

# 클래스 이름
class_name = ["A", "B", "C0", "C1", "C2", "D0", "D1", "E", "Z"]

first_list = ["A", "C2", "E"]
second_list = ["B", "C0", "C1"]
third_list = ["D0", "D1"]
fourth_list = ["Z"]

for each_class in first_list:
    print("************", each_class, "************")
    # 원본 이미지, 라벨 파일의 폴더의 경로
    # 레이블링 이상하게 해놓고 저장한 폴더 만들기
    path_img = "C:/Users/rt_la/check_label_dataset/original/Class_" + each_class + "/images"
    path_lbl = "C:/Users/rt_la/check_label_dataset/original/Class_" + each_class + "/labels"
    files_img = os.listdir(path_img)
    if "desktop.ini" in files_img:
        files_img.remove("desktop.ini")
    files_lbl = os.listdir(path_lbl)
    if "desktop.ini" in files_lbl:
        files_lbl.remove("desktop.ini")
    print(len(files_img), len(files_lbl))

    # 잘못 레이블링된 파일 저장할 폴더
    new_label_path = "C:/Users/rt_la/check_label_dataset/wrong/labels"
    new_image_path = "C:/Users/rt_la/check_label_dataset/wrong/images"

    # 각 파일마다 검사
    for file in files_lbl:
        original_label_path = path_lbl + '/' + file
        file_name = os.path.splitext(file)[0]
        original_image_path = path_img + '/' + file_name + '.jpg'

        # 각 객체의 개수
        total_plate = 0  # 1개
        total_A = 0  # 1개
        total_N = 0  # 6개
        total_S = 0  # 1개

        # wrong으로 판정
        wrong_labeling = False

        # Plate, A, S, N의 정보 파싱
        tree = ET.parse(original_label_path, parser=ET.XMLParser(encoding='UTF-8'))
        root = tree.getroot()
        # width, height
        width = float(root.find("size").find("width").text)
        height = float(root.find("size").find("height").text)
        filename = os.path.splitext(file)[0]
        if width * height == 0:
            img = Image.open(path_img + '/' + filename + '.jpg')
            img_width, img_height = img.size
            width = img_width
            height = img_height

        # 각 객체의 좌표(xmin, ymin, xmax, ymax) 리스트
        result_plate = []
        result_A = []
        result_N = []
        result_S = []

        for obj in root.findall("object"):
            label = obj.find("name").text
            # Plate
            if label.startswith("P"):
                total_plate += 1
                result_plate = [int(x.text) for x in obj.find("bndbox")]  # "Plate"의 bound box 좌표
                # A_?
            elif label.startswith("A"):
                total_A += 1
                result_A = [int(x.text) for x in obj.find("bndbox")]  # "A?_?"의 bound box 좌표
                # N_?
            elif label.startswith("N"):
                total_N += 1
                n_bbox = [int(x.text) for x in obj.find("bndbox")]  # "N_?"의 bound box 좌표
                result_N.append(n_bbox)
                # S_?
            elif label.startswith("S"):
                total_S += 1
                result_S = [int(x.text) for x in obj.find("bndbox")]  # "S_?"의 bound box 좌표

        # print(total_plate, total_A, total_N, total_S)
        # print(len(result_plate), len(result_A), len(result_N), len(result_S))

        # 개수 확인
        # N
        result_N.sort(key=lambda x: x[1])  # result_N을 ymin 기준으로 정렬
        if len(result_N) == 5:  # N이 5개인 경우
            top_N = result_N[0]
            sorted_N = sorted(result_N[1:], key=lambda x: x[0])  # result_N의 나머지 4개를 xmin 기준으로 정렬
            if top_N[0] > sorted_N[0][2] and top_N[2] < sorted_N[3][0]:  # top_N의 x가 범위 안에 있는 경우
                for i in range(4):
                    if top_N[3] < sorted_N[i][1]:
                        # top_N의 y가 나머지 객체보다 위에 있으면 맞음
                        continue
                    else:
                        wrong_labeling = True
                        print("wrong labeling:", file)
                        break
            else:
                wrong_labeling = True
                print("wrong labeling:", file)
                break
        elif len(result_N) == 6:  # N이 6개인 경우
            sorted_top_N = sorted(result_N[:2], key=lambda x: x[0])  # result_N의 가장 위에 있는 두 객체를 xmin 기준으로 정렬
            sorted_bottom_N = sorted(result_N[2:], key=lambda x: x[0])  # result_N의 나머지 4개를 xmin 기준으로 정렬
            if sorted_top_N[0][0] > sorted_bottom_N[0][2] and sorted_top_N[1][2] < sorted_bottom_N[3][0]:  # sorted_top_N의 x가 범위 안에 있는 경우
                for i in range(4):
                    if sorted_top_N[0][3] < sorted_bottom_N[i][1] and sorted_top_N[i][3] < sorted_bottom_N[i][1]:
                        # sorted_top_N의 y가 나머지 객체보다 위에 있으면 맞음
                        continue
                    else:
                        wrong_labeling = True
                        print("wrong labeling:", file)
                        break
        # Plate, A, S
        if total_plate != 1 or total_A != 1 or total_S != 1:
            wrong_labeling = True
            print("wrong labeling:", file)
            break
        # 좌표 확인
        else:
            # print(result_plate)
            # print(result_N[:][0])
            for i in range(4):
                if i < 2:  # i = 0, 1 --> xmin, ymin 비교
                    if result_plate[i] > result_A[i]:
                        print("wrong A", file, i)
                        wrong_labeling = True
                        break
                else:  # i = 2, 3 --> xmax, ymax 비교
                    if result_plate[i] < result_A[i]:
                        print("wrong A", file, i)
                        wrong_labeling = True
                        break
            for i in range(len(result_N)):
                for j in range(4):
                    if j < 2:  # j = 0, 1 --> xmin, ymin 비교
                        if result_plate[j] > result_N[i][j]:
                            print("wrong N", file, i)
                            wrong_labeling = True
                            break
                    else:  # j = 2, 3 --> xmax, ymax 비교
                        if result_plate[j] < result_N[i][j]:
                            print("wrong N", file, i)
                            wrong_labeling = True
                            break
            for i in range(4):
                if i < 2:  # i = 0, 1 --> xmin, ymin 비교
                    if result_plate[i] > result_S[i]:
                        print("wrong S", file, i)
                        wrong_labeling = True
                        break
                else:  # i = 2, 3 --> xmax, ymax 비교
                    if result_plate[i] < result_S[i]:
                        print("wrong S", file, i)
                        wrong_labeling = True
                        break
        if wrong_labeling:
            shutil.copy(original_label_path, new_label_path)
            shutil.copy(original_image_path, new_image_path)
        else:
            print("correct labeling:", file)

for each_class in second_list:
    print("************", each_class, "************")
    # 원본 이미지, 라벨 파일의 폴더의 경로
    path_img = "C:/Users/rt_la/check_label_dataset/original/Class_" + each_class + "/images"
    path_lbl = "C:/Users/rt_la/check_label_dataset/original/Class_" + each_class + "/labels"
    files_img = os.listdir(path_img)
    if "desktop.ini" in files_img:
        files_img.remove("desktop.ini")
    files_lbl = os.listdir(path_lbl)
    if "desktop.ini" in files_lbl:
        files_lbl.remove("desktop.ini")
    print(len(files_img), len(files_lbl))

    # 잘못 레이블링된 파일 저장할 폴더
    new_label_path = "C:/Users/rt_la/check_label_dataset/wrong/labels"
    new_image_path = "C:/Users/rt_la/check_label_dataset/wrong/images"

    for file in files_lbl:
        original_label_path = path_lbl + '/' + file
        file_name = os.path.splitext(file)[0]
        original_image_path = path_img + '/' + file_name + '.jpg'
        # Plate, S, N의 정보 파싱
        total_plate = 0  # 1개
        total_N = 0  # 5, 6개
        total_S = 0  # 1개

        # wrong으로 판정
        wrong_labeling = False

        tree = ET.parse(original_label_path, parser=ET.XMLParser(encoding='UTF-8'))
        root = tree.getroot()

        # width, height
        width = float(root.find("size").find("width").text)
        height = float(root.find("size").find("height").text)
        filename = os.path.splitext(file)[0]
        if width * height == 0:
            img = Image.open(path_img + '/' + filename + '.jpg')
            img_width, img_height = img.size
            width = img_width
            height = img_height

        result_plate = []
        result_N = []
        result_S = []
        for obj in root.findall("object"):
            label = obj.find("name").text
            # Plate
            if label.startswith("P"):
                total_plate += 1
                result_plate = [int(x.text) for x in obj.find("bndbox")]  # "Plate"의 bound box 좌표
            # N_?
            elif label.startswith("N"):
                total_N += 1
                n_bbox = [int(x.text) for x in obj.find("bndbox")]  # "N_?"의 bound box 좌표
                result_N.append(n_bbox)
            # S_?
            elif label.startswith("S"):
                total_S += 1
                result_S = [int(x.text) for x in obj.find("bndbox")]  # "S_?"의 bound box 좌표

        print(total_plate, total_N, total_S)
        print(len(result_plate), len(result_N), len(result_S))

        # 개수 확인
        if total_plate != 1 or total_N != 6 or total_S != 1:  # or total_N != 5
            wrong_labeling = True
            print("wrong labeling:", file)

        # Plate 안에 N, S 있는 지 좌표로 확인
        else:
            # print(result_plate)
            # print(result_N[:][0])
            for i in range(len(result_N)):
                for j in range(4):
                    if j < 2:  # j = 0, 1 --> xmin, ymin 비교
                        if result_plate[j] > result_N[i][j]:
                            print("wrong N", file, i)
                            wrong_labeling = True
                            break
                    else:  # j = 2, 3 --> xmax, ymax 비교
                        if result_plate[j] < result_N[i][j]:
                            print("wrong N", file, i)
                            wrong_labeling = True
                            break
            for i in range(4):
                if i < 2:  # i = 0, 1 --> xmin, ymin 비교
                    if result_plate[i] > result_S[i]:
                        print("wrong S", file, i)
                        wrong_labeling = True
                        break
                else:  # i = 2, 3 --> xmax, ymax 비교
                    if result_plate[i] < result_S[i]:
                        print("wrong S", file, i)
                        wrong_labeling = True
                        break
        if wrong_labeling:
            shutil.copy(original_label_path, new_label_path)
            shutil.copy(original_image_path, new_image_path)
        else:
            print("correct labeling:", file)

for each_class in third_list:
    print("************", each_class, "************")
    # 원본 이미지, 라벨 파일의 폴더의 경로
    path_img = "C:/Users/rt_la/check_label_dataset/original/Class_" + each_class + "/images"
    path_lbl = "C:/Users/rt_la/check_label_dataset/original/Class_" + each_class + "/labels"
    files_img = os.listdir(path_img)
    if "desktop.ini" in files_img:
        files_img.remove("desktop.ini")
    files_lbl = os.listdir(path_lbl)
    if "desktop.ini" in files_lbl:
        files_lbl.remove("desktop.ini")
    print(len(files_img), len(files_lbl))

    # 잘못 레이블링된 파일 저장할 폴더
    new_label_path = "C:/Users/rt_la/check_label_dataset/wrong/labels"
    new_image_path = "C:/Users/rt_la/check_label_dataset/wrong/images"

    for file in files_lbl:
        original_label_path = path_lbl + '/' + file
        file_name = os.path.splitext(file)[0]
        original_image_path = path_img + '/' + file_name + '.jpg'
        # Plate, S, N의 정보 파싱
        total_plate = 0  # 1개
        total_N = 0  # 7개
        total_S = 0  # 1개

        # wrong으로 판정
        wrong_labeling = False

        tree = ET.parse(original_label_path, parser=ET.XMLParser(encoding='UTF-8'))
        root = tree.getroot()

        # width, height
        width = float(root.find("size").find("width").text)
        height = float(root.find("size").find("height").text)
        filename = os.path.splitext(file)[0]
        if width * height == 0:
            img = Image.open(path_img + '/' + filename + '.jpg')
            img_width, img_height = img.size
            width = img_width
            height = img_height

        result_plate = []
        result_N = []
        result_S = []
        for obj in root.findall("object"):
            label = obj.find("name").text
            # Plate
            if label.startswith("P"):
                total_plate += 1
                result_plate = [int(x.text) for x in obj.find("bndbox")]  # "Plate"의 bound box 좌표
            # N_?
            elif label.startswith("N"):
                total_N += 1
                n_bbox = [int(x.text) for x in obj.find("bndbox")]  # "N_?"의 bound box 좌표
                result_N.append(n_bbox)
            # S_?
            elif label.startswith("S"):
                total_S += 1
                result_S = [int(x.text) for x in obj.find("bndbox")]  # "S_?"의 bound box 좌표

        print(total_plate, total_N, total_S)
        print(len(result_plate), len(result_N), len(result_S))

        # 개수 확인
        if total_plate != 1 or total_N != 7 or total_S != 1:
            wrong_labeling = True
            print("wrong labeling:", file)

        # Plate 안에 N, S 있는 지 좌표로 확인
        else:
            # print(result_plate)
            # print(result_N[:][0])
            for i in range(len(result_N)):
                for j in range(4):
                    if j < 2:  # j = 0, 1 --> xmin, ymin 비교
                        if result_plate[j] > result_N[i][j]:
                            print("wrong N", file, i)
                            wrong_labeling = True
                            break
                    else:  # j = 2, 3 --> xmax, ymax 비교
                        if result_plate[j] < result_N[i][j]:
                            print("wrong N", file, i)
                            wrong_labeling = True
                            break
            for i in range(4):
                if i < 2:  # i = 0, 1 --> xmin, ymin 비교
                    if result_plate[i] > result_S[i]:
                        print("wrong S", file, i)
                        wrong_labeling = True
                        break
                else:  # i = 2, 3 --> xmax, ymax 비교
                    if result_plate[i] < result_S[i]:
                        print("wrong S", file, i)
                        wrong_labeling = True
                        break
        if wrong_labeling:
            shutil.copy(original_label_path, new_label_path)
            shutil.copy(original_image_path, new_image_path)
        else:
            print("correct labeling:", file)

for each_class in fourth_list:
    print("************", each_class, "************")
    # 원본 이미지, 라벨 파일의 폴더의 경로
    path_img = "C:/Users/rt_la/check_label_dataset/original/Class_" + each_class + "/images"
    path_lbl = "C:/Users/rt_la/check_label_dataset/original/Class_" + each_class + "/labels"
    files_img = os.listdir(path_img)
    if "desktop.ini" in files_img:
        files_img.remove("desktop.ini")
    files_lbl = os.listdir(path_lbl)
    if "desktop.ini" in files_lbl:
        files_lbl.remove("desktop.ini")
    print(len(files_img), len(files_lbl))

    # 잘못 레이블링된 파일 저장할 폴더
    new_label_path = "C:/Users/rt_la/check_label_dataset/wrong/labels"
    new_image_path = "C:/Users/rt_la/check_label_dataset/wrong/images"

    for file in files_lbl:
        original_label_path = path_lbl + '/' + file
        file_name = os.path.splitext(file)[0]
        original_image_path = path_img + '/' + file_name + '.jpg'
        # Plate, City, B, Char, N의 정보 파싱
        total_plate = 0  # 1개
        total_City = 0  # 1개
        total_B = 0  # 1개
        total_Char = 0  # 1개
        total_N = 0  # 4개

        # wrong으로 판정
        wrong_labeling = False

        tree = ET.parse(original_label_path, parser=ET.XMLParser(encoding='UTF-8'))
        root = tree.getroot()

        # width, height
        width = float(root.find("size").find("width").text)
        height = float(root.find("size").find("height").text)
        filename = os.path.splitext(file)[0]
        if width * height == 0:
            img = Image.open(path_img + '/' + filename + '.jpg')
            img_width, img_height = img.size
            width = img_width
            height = img_height

        result_plate = []
        result_City = []
        result_B = []
        result_Char = []
        result_N = []
        for obj in root.findall("object"):
            label = obj.find("name").text
            # Plate
            if label.startswith("P"):
                total_plate += 1
                result_plate = [int(x.text) for x in obj.find("bndbox")]  # "Plate"의 bound box 좌표
            # City
            elif label.startswith("City"):
                total_City += 1
                result_City = [int(x.text) for x in obj.find("bndbox")]  # "City"의 bound box 좌표
            # B
            elif label.startswith("B"):
                total_B += 1
                result_B = [int(x.text) for x in obj.find("bndbox")]  # "B"의 bound box 좌표
            # Char
            elif label.startswith("Char"):
                total_Char += 1
                result_Char = [int(x.text) for x in obj.find("bndbox")]  # "Char"의 bound box 좌표
            # N_?
            elif label.startswith("N"):
                total_N += 1
                n_bbox = [int(x.text) for x in obj.find("bndbox")]  # "N_?"의 bound box 좌표
                result_N.append(n_bbox)

        print(total_plate, total_City, total_B, total_Char, total_N)
        print(len(result_plate), len(result_City), len(result_B), len(result_Char), len(result_N))

        # 개수 확인
        if total_plate != 1 or total_City != 1 or total_B != 1 or total_Char != 1 or total_N != 4:
            wrong_labeling = True
            print("wrong labeling:", file)

        # Plate 안에 City, B, Char, N 있는 지 좌표로 확인
        else:
            # print(result_plate)
            # print(result_N[:][0])
            # City
            for i in range(4):
                if i < 2:
                    if result_plate[i] > result_City[i]:
                        print("wrong City", file, i)
                        wrong_labeling = True
                        break
                else:
                    if result_plate[i] < result_City[i]:
                        print("wrong City", file, i)
                        wrong_labeling = True
                        break
            # B
            for i in range(4):
                if i < 2:
                    if result_plate[i] > result_B[i]:
                        print("wrong B", file, i)
                        wrong_labeling = True
                        break
                else:
                    if result_plate[i] < result_B[i]:
                        print("wrong B", file, i)
                        wrong_labeling = True
                        break
            # Char
            for i in range(4):
                if i < 2:
                    if result_plate[i] > result_Char[i]:
                        print("wrong Char", file, i)
                        wrong_labeling = True
                        break
                else:
                    if result_plate[i] < result_Char[i]:
                        print("wrong Char", file, i)
                        wrong_labeling = True
                        break
            # N
            for i in range(len(result_N)):
                for j in range(4):
                    if j < 2:  # j = 0, 1 --> xmin, ymin 비교
                        if result_plate[j] > result_N[i][j]:
                            print("wrong N", file, i)
                            wrong_labeling = True
                            break
                    else:  # j = 2, 3 --> xmax, ymax 비교
                        if result_plate[j] < result_N[i][j]:
                            print("wrong N", file, i)
                            wrong_labeling = True
                            break
        if wrong_labeling:
            shutil.copy(original_label_path, new_label_path)
            shutil.copy(original_image_path, new_image_path)
        else:
            print("correct labeling:", file)
