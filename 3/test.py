import os

N = 10  # Число тестов
task_number = 3  # Номер задания

# Вспомогательная функция: преобразовать строку, содержащую список, в множество
def get_set_from_str_list(str_list, split_with):
    str_list = str_list[1:len(str_list) - 1]
    str_list = str_list.split(split_with)
    return set(str_list)  # set

# Вспомогательная функция: найти нужный список в тексте ответа
def get_list_from_answer(answer, code_name):
    return answer[answer.find("[", answer.find(code_name)):answer.find("\n", answer.find("[", answer.find(code_name))):]

# Вспомогательная функция: отформатировать список в соответствии с его видом
def format__str(str, list_type):
    if list_type == "bridge":
        str = str[1:len(str) - 1]
        str = str.replace("), (", "G", 999)
        str = str.replace("(", "G", 999)
        str = str.replace(")", "G", 999)
    return str

# Сравнить два ответа по выданным числам
def compare_anwers(correct_ans, my_ans):

    correct_bridges = get_list_from_answer(correct_ans, "Bridges")
    correct_bridges = format__str(correct_bridges, "bridge")
    correct_bridges = get_set_from_str_list(correct_bridges, "G")

    my_bridges = my_ans[my_ans.find("["):my_ans.find("]", my_ans.find("["))+1:]
    my_bridges = format__str(my_bridges, "bridge")
    my_bridges = get_set_from_str_list(my_bridges, "G")

    correct_points = correct_ans[correct_ans.find("[", correct_ans.find("]")):correct_ans.rfind("]")+1:]
    correct_points = get_set_from_str_list(correct_points, ", ")

    my_points = my_ans[my_ans.find("[", my_ans.find("]")):my_ans.rfind("]")+1:]
    my_points = get_set_from_str_list(my_points, ", ")

    return correct_bridges == my_bridges and correct_points == my_points

# Счетчик номера теста:
for test_number in range(1, N + 1):

    # В 4-ом тесте неправильный ответ, в 6-ом тесте неправильные файлы исходных данных:
    if test_number == 4:
        print("Тест №", test_number, " - этот тест некорректный! Неверный ответ!")
        continue

    if test_number == 6:
        print("Тест №", test_number, " - этот тест некорректный! Неверные исходные данные (разные при разных ключах)!")
        continue

    # По формулам собираем имена файлов исходных и выходных данных для теста:

    if test_number < 10:
        str_test_number = "00" + str(test_number)
    else:
        str_test_number = "0" + str(test_number)

    e = "task" + str(task_number) + "/list_of_edges_t" + str(task_number) + "_" + str_test_number + ".txt"
    m = "task" + str(task_number) + "/matrix_t" + str(task_number) + "_" + str_test_number + ".txt"
    l = "task" + str(task_number) + "/list_of_adjacency_t" + str(task_number) + "_" + str_test_number + ".txt"

    input_files = {"e": e, "m": m, "l": l}

    ans = "task" + str(task_number) + "/ans_t" + str(task_number) + "_" + str_test_number + ".txt"

    # Запускаем программу с соответствующими ключами и получаем ответ, который требует проверки:

    ans_e = os.popen("python main.py -e " + e).read()
    ans_m = os.popen("python main.py -m " + m).read()
    ans_l = os.popen("python main.py -l " + l).read()

    my_answers = {"e": ans_e, "m": ans_m, "l": ans_l}

    # Считываем правильный ответ на тест из файла с ответом:

    f = open(ans, "r")
    correct_ans = f.read()

    # Сверяем наш ответ с правильным, если они не совпадают, выдаем ошибку:
    for key in ["e", "m", "l"]:

        if correct_ans != my_answers[key]:
            if not compare_anwers(correct_ans, my_answers[key]):

                print("-----------------------------\n" +
                      "Ошибка в тесте №" + str(test_number) + ".\n" +
                      "Указан ключ: -" + key + ".\n" +
                      "-----------------------------")

                print("ИСХОДНЫЕ ДАННЫЕ\n" +
                      "-----------------------------")

                f = open(input_files[key], "r")
                print(f.read() +
                      "-----------------------------")

                print("ПОЛУЧЕННЫЙ ОТВЕТ\n" +
                      "-----------------------------\n" +
                      my_answers[key] +
                      "-----------------------------")

                print("ПРАВИЛЬНЫЙ ОТВЕТ\n" +
                      "-----------------------------\n" +
                      correct_ans +
                      "-----------------------------")

                exit()
            else:
                print("Тест №", test_number, key, " пройден, просто числа записаны в другом порядке.")
        else:
            print("Тест №", test_number, key, " пройден на все 100%")

print("Все тесты пройдены!")
