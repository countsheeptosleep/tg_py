import os

N = 15  # Число тестов
task_number = 1  # Номер задания

# Счетчик номера теста:
for test_number in range(1, N + 1):

    # По формулам собираем имена файлов исходных и выходных данных для теста:

    if test_number < 10:
        str_test_number = "00" + str(test_number)
    else:
        str_test_number = "0" + str(test_number)

    e = "task" + str(task_number) + "/list_of_edges_t" + str(task_number) + "_" + str_test_number + ".txt"
    m = "task" + str(task_number) + "/matrix_t" + str(task_number) + "_" + str_test_number + ".txt"
    l = "task" + str(task_number) + "/list_of_adjacency_t" + str(task_number) + "_" + str_test_number + ".txt"

    input_files = {"e" : e, "m" : m, "l" : l}

    ans = "task" + str(task_number) + "/ans_t" + str(task_number) + "_" + str_test_number + ".txt"

    # Запускаем программу с соответствующими ключами и получаем ответ, который требует проверки:

    ans_e = os.popen("python main.py -e " + e).read()
    ans_m = os.popen("python main.py -m " + m).read()

    if test_number >= 13:
        ans_l = os.popen("python main.py -l " + l).read()
    else:
        ans_l = None

    my_answers = {"e" : ans_e, "m" : ans_m, "l" : ans_l}

    # Считываем правильный ответ на тест из файла с ответом:

    f = open(ans, "r")
    correct_ans = f.read()

    # Сверяем наш ответ с правильным, если они не совпадают, выдаем ошибку:

    for key in ["e", "m", "l"]:

        if correct_ans != my_answers[key] and not (key == "l" and test_number < 13):

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

print("Все тесты пройдены!")
