import random

# import data (json files) from GCP

# global variables
# group_lst = []
# dic = {}
# flag = False

"""
    ダミーデータを作る：20人ずつのグループを4つつくる
    Return: それぞれのグループをリストに入れた nested list
"""
def init_groups(group_lst):
    # first_group_length = 20
    # second_group_length = 40
    # third_group_length = 60
    # fourth_group_length = 80
    # group1 = range(first_group_length, 1)
    # group2 = range(second_group_length,21)
    group1 = []
    group2 = []
    group3 = []
    group4 = []
    group_lst = [group1, group2, group3, group4]

    for i in range(1, 81):
        if i < 21:
            group1.append(i)
        elif 20 < i < 41:
            group2.append(i)
        elif 40 < i < 61:
            group3.append(i)
        else:
            group4.append(i)



    # print(group1)
    # print()
    # print(group2)
    # print()
    # print(group3)
    # print()
    # print(group4)
    # print()
    #
    # print(group_lst)
    return group_lst


"""
    すでに同じグループになった人を管理する dictionary　をつくる
    dic = {カレッジ生 : [すでにマッチしたカレッジ生のリスト]}
    Return: 空の dictionary
"""
def init_dictionary(group_lst):
    # group1 = group_lst[0]
    group2 = group_lst[1]
    group3 = group_lst[2]
    group4 = group_lst[3]

    dic = {}
    for i in range(0, 20):
        # dic.update({group1[i] : []})
        dic.update({group2[i] : []})
        dic.update({group3[i] : []})
        dic.update({group4[i] : []})

    # print(dic)
    return dic


"""
    すでにマッチした学生とマッチしないように確認する
    Return: Ventiグループに追加してよい学生
"""
def check_overlap(student, venti, group, dic):

    # 可能なグループをすべて網羅したことの確認方法を確立する！！
    all_combination = False
    matched_for_lst = dic.get(80)
    # matched_lst に他のグループにいる学生全員が入っていたら、
    # 可能なグループをすべて網羅したことになる
    if len(matched_for_lst) == 60:
        # print("length of matched == 60")
        all_combination = True


    else:
        # print("len does not match 60")
        matched_lst = dic.get(student)

        if len(venti) > 0:
            # venti にすでにいる学生とこれまでマッチしたかみる
            valid = False
            while not valid:
                for s in venti:
                    if s in matched_lst:
                        # print("len matched list: %d" % len(matched_lst))
                        student = select_student(group)
                        matched_lst = dic.get(student)
                    else:
                        valid = True

    return (all_combination, student)


"""
Goal: ランダムに学生を選ぶ
Return: 学生
"""
def select_student(group):
    lst_len = len(group)
    if lst_len == 1:
        student = group[0]
    else:
        # print("lst_len in select_student: %d" % lst_len)
        index = random.randrange(0, lst_len)
        student = group[index]
    return student


"""
Goal: Ventiのグループをつくる
Return:
  ventiに選ばれた人たちを抜いた全体のグル―プと、ventiのグループのペア
"""
def create_groups(group_lst, dic):
    venti = []
    for i in range(0, 4):
        # group 1, 2, 3, or 4
        group = group_lst[i]
        # ランダムに学生を選ぶ
        student = select_student(group)
        # venti グループにいる人とすでにマッチしていないか確認
        (flag, checked_student) = check_overlap(student, venti, group, dic)
        if flag == True:
            print("すべての組み合わせを網羅しました。")
        else:
            # 追加する学生の dictionary list に venti メンバーを追加する
            #（
            #   毎回 group1、group2、という順番でグループから学生を追加していくので
            #   すでにいる学生の dictionary はアップデートしなくてよい
            # ）
            for s in venti:
                dic[checked_student].append(s)
            # 学生を venti に追加する
            venti.append(checked_student)
            # venti に一度配属された人は、リストから排除
            group.remove(checked_student)

    return (venti, group_lst)

def main():
    # 本来は json file を読み込んで、各グループのリストを取得
    # ダミーグループをつくる
    group_lst = init_groups([])
    dic = init_dictionary(group_lst)
    # print(group_lst)
    # print(dic)

    # グループが作れなくなるまで Venti 作成を繰り返す
    # 実際は venti1 と venti2 ができたら終わり

    # while ((len(dic.get(80))) < 60):
    # もし、グループリストに誰もいなくなっていたら、グループをリセット
    # （= 全員一度 venti のグループに入った）
    if len(group_lst[0]) == 0:
        # print("in if case in main")
        print()
        # 本来は再びもとのリストを取得
        group_lst = init_groups([])
        print(dic)

    (venti1, group_lst) = create_groups(group_lst, dic)
    print("Venti1:")
    print(venti1)
    print()
    (venti2, group_lst) = create_groups(group_lst, dic)
    print("Venti2:")
    print(venti2)
    print()

    return

main()
