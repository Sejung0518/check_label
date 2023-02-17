"""
레이블링 검수 코드
"""

import os
import shutil
import xml.etree.ElementTree as ET
from PIL import Image

# 클래스 이름
# class_name = ["A", "B", "C0", "C1", "C2", "D0", "D1", "E", "Z"]

for loop in range(1):
    # print("************", each_class, "************")
    # 원본 이미지, 라벨 파일의 폴더의 경로
    # 레이블링 이상하게 해놓고 저장한 폴더 만들기
    path_img = "C:/Users/rt_la/check_label_dataset/images/src"
    path_lbl = "C:/Users/rt_la/check_label_dataset/labels/src"
    files_img = os.listdir(path_img)
    if "desktop.ini" in files_img:
        files_img.remove("desktop.ini")
    files_lbl = os.listdir(path_lbl)
    if "desktop.ini" in files_lbl:
        files_lbl.remove("desktop.ini")
    print(len(files_img), len(files_lbl))

    # 잘못 레이블링된 파일 저장할 폴더
    wrong_label_path = "C:/Users/rt_la/check_label_dataset/Class_E_check_label/labels"
    wrong_image_path = "C:/Users/rt_la/check_label_dataset/Class_E_check_label/images"

    for file in files_lbl:
        original_label_path = path_lbl + '/' + file
        file_name = os.path.splitext(file)[0]
        original_image_path = path_img + '/' + file_name + '.jpg'

        # 각 객체의 개수
        total_plate = 0  # 1개
        total_A = 0  # 0, 1개
        total_N = 0  # 4, 5, 6, 7개
        total_S = 0  # 0, 1개
        total_City = 0  # 0, 1개
        total_B = 0  # 0, 1개
        total_Char = 0  # 0, 1개

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
        result_City = []
        result_B = []
        result_Char = []

        # 각 객체의 좌표 알아내기
        for obj in root.findall("object"):
            label = obj.find("name").text
            # Plate
            if label.startswith("P"):
                total_plate += 1
                result_plate = [int(x.text) for x in obj.find("bndbox")]  # "Plate"의 bound box 좌표
                # 이미지의 사이즈 벗어나는지 체크
                for i in range(len(result_plate)):
                    if i % 2 == 0:  # xmin, xmax
                        if 0 <= result_plate[i] <= width:
                            continue
                        else:
                            print("82 plate xmin, xmax out of range", file)
                            wrong_labeling = True
                            break
                    else:  # ymin, ymax
                        if 0 <= result_plate[i] <= height:
                            continue
                        else:
                            print("87 plate ymin, ymax out of range", file)
                            wrong_labeling = True
                            break
            # A?_?
            elif label.startswith("A"):
                total_A += 1
                result_A = [int(x.text) for x in obj.find("bndbox")]  # "A?_?"의 bound box 좌표
                for i in range(len(result_A)):
                    if i % 2 == 0:  # xmin, xmax
                        if 0 <= result_A[i] <= width:
                            continue
                        else:
                            print("101 A xmin, xmax out of range", file)
                            wrong_labeling = True
                            break
                    else:  # ymin, ymax
                        if 0 <= result_A[i] <= height:
                            continue
                        else:
                            print("108 A ymin, ymax out of range", file)
                            wrong_labeling = True
                            break
            # N_?
            elif label.startswith("N"):
                total_N += 1
                n_bbox = [int(x.text) for x in obj.find("bndbox")]  # "N_?"의 bound box 좌표
                for i in range(len(n_bbox)):
                    if i % 2 == 0:  # xmin, xmax
                        if 0 <= n_bbox[i] <= width:
                            continue
                        else:
                            print("120 N xmin, xmax out of range", file)
                            wrong_labeling = True
                            break
                    else:  # ymin, ymax
                        if 0 <= n_bbox[i] <= height:
                            continue
                        else:
                            print("127 N ymin, ymax out of range", file)
                            wrong_labeling = True
                            break
                result_N.append(n_bbox)
            # S_?
            elif label.startswith("S"):
                total_S += 1
                result_S = [int(x.text) for x in obj.find("bndbox")]  # "S_?"의 bound box 좌표
                for i in range(len(result_S)):
                    if i % 2 == 0:  # xmin, xmax
                        if 0 <= result_S[i] <= width:
                            continue
                        else:
                            print("140 S xmin, xmax out of range", file)
                            wrong_labeling = True
                            break
                    else:  # ymin, ymax
                        if 0 <= result_S[i] <= height:
                            continue
                        else:
                            print("140 S ymin, ymax out of range", file)
                            wrong_labeling = True
                            break
            # City
            elif label.startswith("City"):
                total_City += 1
                result_City = [int(x.text) for x in obj.find("bndbox")]  # "City"의 bound box 좌표
                for i in range(len(result_S)):
                    if i % 2 == 0:  # xmin, xmax
                        if 0 <= result_City[i] <= width:
                            continue
                        else:
                            print("159 City xmin, xmax out of range", file)
                            wrong_labeling = True
                            break
                    else:  # ymin, ymax
                        if 0 <= result_City[i] <= height:
                            continue
                        else:
                            print("166 City ymin, ymax out of range", file)
                            wrong_labeling = True
                            break
            # B
            elif label.startswith("B"):
                total_B += 1
                result_B = [int(x.text) for x in obj.find("bndbox")]  # "B"의 bound box 좌표
                for i in range(len(result_B)):
                    if i % 2 == 0:  # xmin, xmax
                        if 0 <= result_B[i] <= width:
                            continue
                        else:
                            print("178 B xmin, xmax out of range", file)
                            wrong_labeling = True
                            break
                    else:  # ymin, ymax
                        if 0 <= result_B[i] <= height:
                            continue
                        else:
                            print("178 B ymin, ymax out of range", file)
                            wrong_labeling = True
                            break
            # Char
            elif label.startswith("Char"):
                total_Char += 1
                result_Char = [int(x.text) for x in obj.find("bndbox")]  # "Char"의 bound box 좌표
                for i in range(len(result_Char)):
                    if i % 2 == 0:  # xmin, xmax
                        if 0 <= result_Char[i] <= width:
                            continue
                        else:
                            print("197 Char xmin, xmax out of range", file)
                            wrong_labeling = True
                            break
                    else:  # ymin, ymax
                        if 0 <= result_Char[i] <= height:
                            continue
                        else:
                            print("197 Char ymin, ymax out of range", file)
                            wrong_labeling = True
                            break
        # 각 객체의 개수 확인
        # Plate
        if total_plate != 1:
            wrong_labeling = True
            print("110 wrong plate number:", file)
        else:
            # result_A의 y 중간점
            result_A_middle = result_A[1] + (result_A[3] - result_A[1]) / 2
            # result_S의 y 중간점
            result_S_middle = result_S[1] + (result_S[3] - result_S[1]) / 2

            # N
            # N이 4개인 경우
            if len(result_N) == 4:
                # print(total_A, total_S)
                if total_A != 0 or total_S != 0:
                    wrong_labeling = True
                    print("117 wrong number of A or S or something else:", file)
                else:
                    if total_City != 1 or total_B != 1 or total_Char != 1:
                        wrong_labeling = True
                        print("121 wrong number of City or B or Char or something else:", file)
                    else:
                        # Plate 안에 객체들이 있는지 확인
                        # City
                        for i in range(4):
                            if i < 2:
                                if result_plate[i] > result_City[i]:
                                    wrong_labeling = True
                                    print("129 wrong City location:", file)
                                    break
                            else:
                                if result_plate[i] < result_City[i]:
                                    wrong_labeling = True
                                    print("134 wrong City location:", file)
                                    break
                        # B
                        for i in range(4):
                            if i < 2:
                                if result_plate[i] > result_B[i]:
                                    wrong_labeling = True
                                    print("wrong B location:", file)
                                    break
                            else:
                                if result_plate[i] < result_B[i]:
                                    wrong_labeling = True
                                    print("wrong B location:", file)
                                    break
                        # Char
                        for i in range(4):
                            if i < 2:
                                if result_plate[i] > result_Char[i]:
                                    wrong_labeling = True
                                    print("wrong Char location:", file)
                                    break
                            else:
                                if result_plate[i] < result_Char[i]:
                                    wrong_labeling = True
                                    print("wrong Char location:", file)
                                    break
                        # N
                        for i in range(len(result_N)):
                            for j in range(4):
                                if j < 2:  # j = 0, 1 --> xmin, ymin 비교
                                    if result_plate[j] > result_N[i][j]:
                                        wrong_labeling = True
                                        print("wrong N location", file, i)
                                        break
                                else:  # j = 2, 3 --> xmax, ymax 비교
                                    if result_plate[j] < result_N[i][j]:
                                        wrong_labeling = True
                                        print("wrong N location", file, i)
                                        break
                        # 상대적인 위치 확인
                        # City, B가 일렬로
                        if result_City[2] > result_B[0]:  # City의 xmax가 B의 xmin보다 작아야 함
                            wrong_labeling = True
                            print("City, B not aligned", file)
                        result_City_middle = result_City[1] + (result_City[3] - result_City[1]) / 2
                        result_B_middle = result_B[1] + (result_B[3] - result_B[1]) / 2
                        if result_B[1] < result_City_middle < result_B[3]:  # City의 중간점이 B의 ymin, ymax 사이에 있어야 함
                            if result_City[1] < result_B_middle < result_City[3]:  # B의 중간점이 City의 ymin, ymax 사이에 있어야 함
                                pass
                            else:
                                wrong_labeling = True
                                print("City, B not aligned", file)
                        else:
                            wrong_labeling = True
                            print("City, B not aligned", file)
                        # Char, N이 일렬로
                        result_Char_N = result_N.copy()
                        result_Char_N.append(result_Char)
                        result_Char_N.sort(key=lambda x: x[0])
                        for i in range(len(result_Char_N) - 1):
                            if result_Char_N[i][2] < result_Char_N[i + 1][0]:
                                continue
                            else:
                                wrong_labeling = True
                                print("Char, N not aligned", file)
                                break
                        for i in range(len(result_Char_N)):
                            result_Char_N_middle = result_Char_N[i][1] + (result_Char_N[i][3] - result_Char_N[i][1]) / 2
                            for j in range(len(result_Char_N)):
                                if i == j:
                                    continue
                                else:
                                    if result_Char_N[j][1] < result_Char_N_middle < result_Char_N[j][3]:
                                        continue
                                    else:
                                        wrong_labeling = True
                                        print("Char, N, not aligned", file)
                                        break

            # N이 5개인 경우
            elif len(result_N) == 5:
                if total_A != 1 or total_S != 1:
                    wrong_labeling = True
                    print("wrong number of A or S:", file)
                else:
                    if total_City != 0 or total_B != 0 or total_Char != 0:
                        wrong_labeling = True
                        print("wrong number of City or B or Char:", file)
                    else:
                        # Plate 안에 객체들이 있는지 확인
                        # A
                        # xmin, xmax
                        if result_plate[0] <= result_A[0] and result_A[2] <= result_plate[2]:
                            pass
                        else:
                            print("233 xmin, xmax", file)
                            wrong_labeling = True
                        # ymin, ymax
                        if result_plate[1] <= result_A[1] and result_A_middle <= result_plate[3]:
                            pass
                        else:
                            print("238 ymin, ymax", file)
                            wrong_labeling = True
                        # N
                        for i in range(len(result_N)):
                            result_N_middle = result_N[i][1] + (result_N[i][3] - result_N[i][1]) / 2
                            # xmin, xmax
                            if result_plate[0] <= result_N[i][0] and result_N[i][2] <= result_plate[2]:
                                pass
                            else:
                                print("249 xmin xmax", file)
                                wrong_labeling = True
                                break
                            # ymin, ymax
                            if result_plate[1] <= result_N[i][1] and result_N_middle <= result_plate[3]:
                                pass
                            else:
                                print("256 ymin ymax", file)
                                wrong_labeling = True
                                break
                        # S
                        # xmin, xmax
                        if result_plate[0] <= result_S[0] and result_S[2] <= result_plate[2]:
                            pass
                        else:
                            print("264 xmin, xmax", file)
                            wrong_labeling = True
                        # ymin, ymax
                        if result_plate[1] <= result_S[1] and result_S_middle <= result_plate[3]:
                            pass
                        else:
                            print("271 ymin, ymax", file)
                            wrong_labeling = True

                # 위치 확인
                # A, N 일렬
                result_N.sort(key=lambda x: x[1])  # result_N을 ymin 기준으로 정렬
                top_N = result_N[0]
                if result_A[2] > top_N[0]:  # A의 xmax가 N의 xmin보다 작아야 함
                    wrong_labeling = True
                    print("266 A, N not aligned", file)
                result_A_middle = result_A[1] + (result_A[3] - result_A[1]) / 2
                top_N_middle = top_N[1] + (top_N[3] - top_N[1]) / 2
                if top_N[1] < result_A_middle < top_N[3] and result_A[1] < top_N_middle < result_A[3]:
                    pass
                else:
                    wrong_labeling = True
                    print("273 A, N not aligned", file)
                # S, N 일렬
                sorted_N = sorted(result_N[1:].copy(), key=lambda x: x[0])  # result_N의 나머지 4개를 xmin 기준으로 정렬
                result_S_N = sorted_N.copy()
                result_S_N.append(result_S)
                result_S_N.sort(key=lambda x: x[0])
                for i in range(len(result_S_N) - 1):
                    if result_S_N[i][3] < result_S_N[i + 1][0]:
                        continue
                    else:
                        wrong_labeling = True
                        print("S, N not aligned", file)
                        break
                for i in range(len(result_S_N)):
                    result_S_N_middle = result_S_N[i][1] + (result_S_N[i][3] - result_S_N[i][1]) / 2
                    for j in range(len(result_S_N)):
                        if i == j:
                            continue
                        else:
                            if result_S_N[j][1] < result_S_N_middle < result_S_N[j][3]:
                                continue
                            else:
                                wrong_labeling = True
                                print("S, N not aligned", file)
                                break
                # N의 좌표로 검수
                if top_N[0] > sorted_N[0][2] and top_N[2] < sorted_N[3][2]:  # top_N의 x가 범위 안에 있는 경우
                    for i in range(4):
                        if top_N[1] < sorted_N[i][1]:
                            # top_N의 y가 나머지 객체보다 위에 있으면 맞음
                            continue
                        else:
                            wrong_labeling = True
                            print("wrong N y-point:", file)
                            break
                else:
                    wrong_labeling = True
                    print("wrong N x-point:", file)

            # N이 6개인 경우
            elif len(result_N) == 6:
                if total_S != 1:
                    wrong_labeling = True
                    print("wrong number of S:", file)
                else:
                    if total_A != 1 and total_A != 0:
                        wrong_labeling = True
                        print("wrong number of A:", file, total_A)
                    # A가 있는 경우
                    elif total_A == 1:
                        # Plate 안에 객체 있는지 확인
                        # A
                        # xmin, xmax
                        if result_plate[0] <= result_A[0] and result_A[2] <= result_plate[2]:
                            pass
                        else:
                            print("344 xmin, xmax", file)
                            wrong_labeling = True
                        # ymin, ymax
                        if result_plate[1] <= result_A_middle and result_A[1] <= result_plate[3]:
                            pass
                        else:
                            print("351 ymin, ymax", file)
                            wrong_labeling = True
                        # N
                        for i in range(len(result_N)):
                            result_N_middle = result_N[i][1] + (result_N[i][3] - result_N[i][1]) / 2
                            # xmin, xmax
                            if result_plate[0] <= result_N[i][0] and result_N[i][2] <= result_plate[2]:
                                pass
                            else:
                                print("361 xmin xmax", file)
                                wrong_labeling = True
                                break
                            # ymin, ymax
                            if result_plate[1] <= result_N[i][1] and result_N_middle <= result_plate[3]:
                                pass
                            else:
                                print("368 ymin ymax", file)
                                wrong_labeling = True
                                break
                        # S
                        # xmin, xmax
                        if result_plate[0] <= result_S[0] and result_S[2] <= result_plate[2]:
                            pass
                        else:
                            print("376 xmin, xmax", file)
                            wrong_labeling = True
                        # ymin, ymax
                        if result_plate[1] <= result_S[1] and result_S_middle <= result_plate[3]:
                            pass
                        else:
                            print("383 ymin, ymax", file)
                            wrong_labeling = True

                        result_N.sort(key=lambda x: x[1])
                        sorted_top_N = sorted(result_N[:2].copy(), key=lambda x: x[0])  # result_N의 가장 위에 있는 두 객체를 xmin 기준으로 정렬
                        sorted_bottom_N = sorted(result_N[2:].copy(), key=lambda x: x[0])  # result_N의 나머지 4개를 xmin 기준으로 정렬
                        # A가 위에 있는 경우
                        # if result_A[3] < result_S[1]:
                        if result_A_middle < result_S[1]:
                            # N 2개가 위에 있는 경우
                            if sorted_top_N[0][3] < result_S[1] and sorted_top_N[1][3] < result_S[1]:
                                # Class A
                                sorted_bottom_N_S = sorted_bottom_N.copy()
                                sorted_bottom_N_S.append(result_S)
                                sorted_bottom_N_S.sort(key=lambda x: x[0])
                                for i in range(len(sorted_bottom_N_S)):
                                    sorted_bottom_N_S_middle = sorted_bottom_N_S[i][1] + (sorted_bottom_N_S[i][3] - sorted_bottom_N_S[i][1]) / 2
                                    for j in range(len(sorted_bottom_N_S)):
                                        if i == j:
                                            continue
                                        else:
                                            if sorted_bottom_N_S[j][1] < sorted_bottom_N_S_middle < sorted_bottom_N_S[j][3]:
                                                pass
                                            else:
                                                print("382", file)
                                                wrong_labeling = True
                                                break
                            else:
                                # Class E
                                result_N_S = result_N.copy()
                                result_N_S.append(result_S)
                                # print("result_N_S:", result_N_S)
                                result_N_S.sort(key=lambda x: x[0])
                                # print("sorted result_N_S:", result_N_S)
                                for i in range(len(result_N_S)):
                                    result_N_S_middle = result_N_S[i][1] + (result_N_S[i][3] - result_N_S[i][1]) / 2
                                    if i == 0:
                                        if result_N_S[i + 1][1] <= result_N_S_middle <= result_N_S[i + 1][3]:
                                            continue
                                        else:
                                            print("402", file)
                                            wrong_labeling = True
                                            break
                                    elif i == (len(result_N_S) - 1):
                                        if result_N_S[i - 1][1] <= result_N_S_middle <= result_N_S[i - 1][3]:
                                            continue
                                        else:
                                            print("409", file)
                                            wrong_labeling = True
                                            break
                                    else:
                                        if (result_N_S[i - 1][1] <= result_N_S_middle <= result_N_S[i - 1][3]) and (result_N_S[i + 1][1] <= result_N_S_middle <= result_N_S[i + 1][3]):
                                            continue
                                        else:
                                            print("416", file)
                                            wrong_labeling = True
                                            break
                        else:
                            # Class C2
                            result_A_N_S = result_N.copy()
                            result_A_N_S.append(result_A)
                            result_A_N_S.append(result_S)
                            result_A_N_S.sort(key=lambda x: x[0])
                            for i in range(len(result_A_N_S)):
                                result_A_N_S_middle = result_A_N_S[i][1] + (result_A_N_S[i][3] - result_A_N_S[i][1]) / 2
                                for j in range(len(result_A_N_S)):
                                    if i == j:
                                        continue
                                    else:
                                        if result_A_N_S[j][1] < result_A_N_S_middle < result_A_N_S[j][3]:
                                            pass
                                        else:
                                            print("432", file)
                                            wrong_labeling = True
                                            break

                    # A가 없는 경우(class B, C0, C1)
                    elif total_A == 0:
                        # Plate 안에 객체 있는지 확인
                        # N
                        for i in range(len(result_N)):
                            result_N_middle = result_N[i][1] + (result_N[i][3] - result_N[i][1]) / 2
                            # xmin, xmax
                            if result_plate[0] < result_N[i][0] and result_N[i][2] < result_plate[2]:
                                pass
                            else:
                                print("470 xmin xmax", file)
                                wrong_labeling = True
                                break
                            # ymin, ymax
                            if result_plate[1] <= result_N[i][1] and result_N_middle <= result_plate[3]:
                                pass
                            else:
                                print("477 ymin ymax", file)
                                wrong_labeling = True
                                break
                        # S
                        # xmin, xmax
                        if result_plate[0] <= result_S[0] and result_S[2] <= result_plate[2]:
                            pass
                        else:
                            print("481 xmin, xmax", file)
                            wrong_labeling = True
                        # ymin, ymax
                        if result_plate[1] <= result_S[1] and result_S_middle <= result_plate[3]:
                            pass
                        else:
                            print("488 ymin, ymax", file)
                            wrong_labeling = True
                        # N 2개, S가 위에 있는 경우(class B)
                        result_N.sort(key=lambda x: x[1])  # ymin 기준으로 정렬
                        sorted_top_N = sorted(result_N[:2].copy(), key=lambda x: x[0])  # 위에 있는 N 2개
                        sorted_bottom_N = sorted(result_N[2:].copy(), key=lambda x: x[0])  # 밑에 있는 N 4개
                        x_sorted_N = sorted(result_N.copy(), key=lambda x: x[0])
                        # print("x_sorted_N:", x_sorted_N)
                        # print("result_S:", result_S)
                        # print("result_S[3], sorted_bottom_N[0][1]:", result_S[3], sorted_bottom_N[0][1])
                        if result_S[3] <= sorted_bottom_N[0][1]:  # S의 ymax가 아래 N의 ymin보다 작으면
                            # S, N 일렬
                            result_N_S = sorted_top_N.copy()
                            result_N_S.append(result_S)
                            result_N_S.sort(key=lambda x: x[0])
                            for i in range(len(result_N_S)):
                                result_N_S_middle = result_N_S[i][1] + (result_N_S[i][3] - result_N_S[i][1]) / 2
                                for j in range(len(result_N_S)):
                                    if result_N_S[j][1] < result_N_S_middle < result_N_S[j][3]:
                                        continue
                                    else:
                                        wrong_labeling = True
                                        print("N, S not aligned", file, i)
                                        break
                            # sorted_bottom_N 일렬
                            for i in range(len(sorted_bottom_N)):
                                sorted_bottom_N_middle = sorted_bottom_N[i][1] + (sorted_bottom_N[i][3] - sorted_bottom_N[i][1]) / 2
                                for j in range(len(sorted_bottom_N)):
                                    if i == j:
                                        continue
                                    else:
                                        if sorted_bottom_N[j][1] < sorted_bottom_N_middle < sorted_bottom_N[j][3]:
                                            continue
                                        else:
                                            wrong_labeling = True
                                            print("N not aligned", file, i)
                                            break
                        # S, N 모두 일렬인 경우
                        elif x_sorted_N[1][2] < result_S[0] and result_S[2] < x_sorted_N[2][0]:  # S가 x_sorted_N의 두번째, 세번째 N 사이에 있으면
                            result_N_S = x_sorted_N.copy()
                            result_N_S.append(result_S)
                            result_N_S.sort(key=lambda x: x[0])
                            for i in range(len(result_N_S)):
                                result_N_S_middle = result_N_S[i][1] + (result_N_S[i][3] - result_N_S[i][1]) / 2
                                for j in range(len(result_N_S)):
                                    if result_N_S[j][1] < result_N_S_middle < result_N_S[j][3]:
                                        continue
                                    else:
                                        wrong_labeling = True
                                        print("502 N, S not aligned", file)
                                        break
                        else:
                            wrong_labeling = True
                            print("506 something else wrong", file)
                    else:
                        wrong_labeling = True
                        print("510 wrong A location", file)

            # N이 7개인 경우(class D0, D1)
            elif len(result_N) == 7:
                if total_S != 1:
                    wrong_labeling = True
                    print("wrong number of S", file)
                else:
                    # Plate 안에 객체 있는지 확인
                    # N
                    for i in range(len(result_N)):
                        result_N_middle = result_N[i][1] + (result_N[i][3] - result_N[i][1]) / 2
                        # xmin, xmax
                        if result_plate[0] <= result_N[i][0] and result_N[i][2] <= result_plate[2]:
                            pass
                        else:
                            print("565 xmin xmax", file)
                            wrong_labeling = True
                            break
                        # ymin, ymax
                        if result_plate[1] <= result_N[i][1] and result_N_middle <= result_plate[3]:
                            pass
                        else:
                            print("572 ymin ymax", file)
                            wrong_labeling = True
                            break
                    # S
                    # xmin, xmax
                    if result_plate[0] <= result_S[0] and result_S[2] <= result_plate[2]:
                        pass
                    else:
                        print("481 xmin, xmax", file)
                        wrong_labeling = True
                    # ymin, ymax
                    if result_plate[1] <= result_S[1] and result_S_middle <= result_plate[3]:
                        pass
                    else:
                        print("488 ymin, ymax", file)
                        wrong_labeling = True
                    # N, S가 일렬로 있는지
                    # S가 N 사이에 있는지
                    result_N_S = result_N.copy()
                    result_N_S.append(result_S)
                    result_N_S.sort(key=lambda x: x[0])
                    for i in range(len(result_N_S)):
                        result_N_S_middle = result_N_S[i][1] + (result_N_S[i][3] - result_N_S[i][1]) / 2
                        for j in range(len(result_N_S)):
                            if result_N_S[j][1] < result_N_S_middle < result_N_S[j][3]:
                                continue
                            else:
                                wrong_labeling = True
                                print("556 N, S not aligned", file, i)
                                break
            else:
                wrong_labeling = True
                print("wrong number of N", file)

        # wrong_labeling일 경우 wrong 폴더로 파일 복사
        if wrong_labeling:
            print("-------", file, "copied", "-------")
            shutil.copy(original_image_path, wrong_image_path)
            shutil.copy(original_label_path, wrong_label_path)
        else:
            print("-------", file, "correct", "-------")
