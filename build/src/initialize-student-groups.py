import json

"""
    ダミーデータを作る：20人ずつのグループを4つつくる
    Return: それぞれのグループをリストに入れた nested list
"""
def init_student_groups():
    first_group_index = 20
    second_group_index = 40
    third_group_index = 60
    fourth_group_index = 80
    student_group1 = list(range(first_group_index))
    student_group2 = list(range(first_group_index, second_group_index))
    student_group3 = list(range(second_group_index, third_group_index))
    student_group4 = list(range(third_group_index, fourth_group_index))

    list_of_student_groups = [student_group1, student_group2, student_group3, student_group4]
    # student_groups_dictionary = {}
    # student_groups_dictionary.update({"group1" : student_group1})
    # student_groups_dictionary.update({"group2" : student_group2})
    # student_groups_dictionary.update({"group3" : student_group3})
    # student_groups_dictionary.update({"group4" : student_group4})
    #
    return list_of_student_groups
    # return student_groups_dictionary


def main():
    # student_groups_dictionary = {}
    list_of_student_groups = init_student_groups()
    # for i in range(4):
        # group_name = "group" + str(i)
        # student_groups_dictionary.update({group_name : list_of_student_groups[i]})

    file_location = r"C:\Users\karin\Projects\shimokitacollege_coffeechat_venti\build\src\venti-initial-student-groups.json"
    with open(file_location, "w") as initial_student_groups:
        json.dump(list_of_student_groups, initial_student_groups, indent=4)

    return

main()
