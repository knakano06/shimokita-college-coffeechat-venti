import random
import json

# import data (json files) from GCP


# """
#     ダミーデータを作る：20人ずつのグループを4つつくる
#     Return: それぞれのグループをリストに入れた nested list
# """
def init_student_groups():
    student_groups_dictionary = {}

    first_group_index = 20
    second_group_index = 40
    third_group_index = 60
    fourth_group_index = 80
    
    
    student_group1 = list(range(first_group_index))
    student_group2 = list(range(first_group_index, second_group_index))
    student_group3 = list(range(second_group_index, third_group_index))
    student_group4 = list(range(third_group_index, fourth_group_index))

    list_of_student_groups = [student_group1, student_group2, student_group3, student_group4]

    return list_of_student_groups


"""
Goal: ランダムに学生を選ぶ
Return: 学生
"""
def select_student(student_group):
    number_of_students = len(student_group)
    if number_of_students == 1:
        student = student_group[0]
    else:
        # print("lst_len in select_student: %d" % lst_len)
        index = random.randrange(0, number_of_students)
        student = student_group[index]
    return student


"""
Goal: 仮の venti をつくる（重複などのチェックをしない状態で）
Return: 仮のventi
"""
def create_tentative_venti(current_student_groups):
    venti = []
    # 4つのグループから、それぞれ学生を選ぶ
    for i in range(0, 4):
        # group 1, 2, 3, or 4
        student_group = current_student_groups[i]
        # ランダムに学生を選ぶ
        student = select_student(student_group)
        # 学生を venti に追加する
        venti.append(student)

    return venti


"""
Goal: Ventiをつくる
Return:
  ventiに選ばれた人たちを抜いた全体のグル―プと、ventiのグループのペア
"""
def create_venti(current_student_groups, past_venti_list):
    # これまで作成した venti と被らない venti ができるまで繰り返す
    notValid_venti = True
    while notValid_venti:
        # 仮の venti をつくる
        venti = create_tentative_venti(current_student_groups)

        # これまでの venti と被っていない場合
        if venti not in past_venti_list:
            notValid_venti = False 
            past_venti_list.append(venti)
            # venti に追加した学生をそれぞれの学生グループから取り除く
            for i in range(4):
                current_student_groups[i].remove(venti[i])
        
        # それ以外の場合は、再び while loop を繰り返す
                  
    # print("past venti list:\n")
    # print(past_venti_list)
    # print()
    return (venti, current_student_groups, past_venti_list)


"""
Goal: ID : Name のペアから、ID のみを抽出する
Return: ID のみのリスト
"""
def get_id_list(id_name_list):
    # ID : Name のリストから、ID だけのリストを作成
    id_list = []
    for id_name_pair in id_name_list:
        (id, _) = id_name_pair
        id_list.append(id)
    return id_list


def main():
  
    # 過去の venti を管理するリストを取得
    file_path_past_venti = r"C:\Users\karin\Projects\shimokitacollege_coffeechat_venti\build\src\past-venti.json"
    with open(file_path_past_venti, "r") as past_venti_file:
        try:
            past_venti_list = json.load(past_venti_file)
            # TODO: ID : Name になっているのを、ID だけにする
            past_venti_list_IDonly = get_id_list(past_venti_list)

            # initial student groups のファイルを open 
            file_path_initial_groups = r"C:\Users\karin\Projects\shimokitacollege_coffeechat_venti\build\src\venti-initial-student-groups.json"
            with open(file_path_initial_groups, "r") as initial_student_groups_file:
                # もとのグループを読み込む
                initial_student_groups = json.load(initial_student_groups_file)
            
        # past venti が空の場合
        except ValueError:
            print("in except case\n")
            past_venti_list = []
            # はじめて venti を作り始めるということなので、もとの student group のリストを作成
            initial_student_groups = init_student_groups()
            file_location = r"C:\Users\karin\Projects\shimokitacollege_coffeechat_venti\build\src\venti-initial-student-groups.json"
            with open(file_location, "w") as initial_student_groups_file:
                json.dump(initial_student_groups, initial_student_groups_file, indent=4)
    
  
    
    # 可能な組み合わせの数（各グループの人数を掛け合わせたもの）を計算する（可能な組み合わせを網羅したかどうか後で確認するため）
    number_of_combinations = 1
    # number of student_groups = 4
    for i in range(4):
        # group_name = "group" + str(i)
        # student_list = initial_student_groups.get(group_name)
        number_of_combinations * len(initial_student_groups[i])

    
    # すべての組み合わせを網羅していた場合
    if len(past_venti_list_IDonly) == number_of_combinations:
        print("すべての組み合わせを網羅しました。")
   
    # まだ可能な組み合わせが残っている場合`
    else: 
        # 前回までのグループのリストを読み込む（venti に一度は入った人が削除されているリスト）
        file_path_current_student = r"C:\Users\karin\Projects\shimokitacollege_coffeechat_venti\build\src\current-student-groups.json"
        with open(file_path_current_student, "r") as current_student_groups_file:
            try:
                current_student_groups = json.load(current_student_groups_file)    
                
                # TODO: ID : Name になっているのを、ID だけにする
                current_student_groups_IDonly = []
                for student_groups in current_student_groups:
                    student_group_IDonly = get_id_list(student_groups)
                    current_student_groups_IDonly.append(student_group_IDonly)

            except ValueError:
                # 空の場合は、空のリストにする 
                current_student_groups_IDonly = [[], [], [], []]



        # もし、グループリストに誰もいなくなっていたら、グループをリセット
        # （= 全員一度 venti のグループに入った）
        # group0_list = current_student_groups.get("group0")
        if len(current_student_groups_IDonly[0]) == 0:
            # 本来は再びもとのリストを取得
            current_student_groups = initial_student_groups

        # venti を作る！
        (venti1, current_student_groups, past_venti_list_IDonly) = create_venti(current_student_groups, past_venti_list_IDonly)
        print("Venti1:")
        print(venti1)
        print()
        (venti2, current_student_groups, past_venti_list_IDonly) = create_venti(current_student_groups, past_venti_list_IDonly)
        print("Venti2:")
        print(venti2)
        print()
        
        # アップデートされたリストを json file に書き込む
        # TODO: ID : Name に戻す
        with open(file_path_current_student, "w") as current_student_groups_file:
            json.dump(current_student_groups, current_student_groups_file, indent=4)
        with open(file_path_past_venti, "w") as past_venti_file:
            json.dump(past_venti_list, past_venti_file, indent=4)
         
    
    return

main()
