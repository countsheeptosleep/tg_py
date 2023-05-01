import sys
import os

'''
----- СПРАВКА К КОДУ -----

Задача: 3
Автор: Б Виталий
Группа: М3О-211Б-21
Ключи:
    -e "edges_list_file_path"
    -m "adjacency_matrix_file_path"
    -l "adjacency_list_file_path"
    -o "output_file_path"
    -h Справка

----- УСЛОВИЕ ЗАДАЧИ 3 -----

Программа, находящая мосты и шарниры в графе. Для орграфа находятся
мосты и шарниры в соотнесённом графе.
Входные данные для работы программы задаются следующими ключами
с параметрами:
-e "edges_list_file_path"
-m "adjacency_matrix_file_path"
-l "adjacency_list_file_path"
Одновременно может указываться только один из этих ключей. Если
указано более одного – выдать сообщение об ошибке.
Результаты работы выводятся на экран, либо в файл при указании
следующего ключа:
-o "output_file_path"
Также должна быть доступна справка, в которой указывается: автор
работы, группа, список ключей с кратким описанием. Справка вызывается
при помощи ключа -h. При этом, если указаны остальные ключи, они
игнорируются

'''

INF = 9999999  # Бесконечность.


# Класс "Граф":
class Graph:

    # Конструктор класса "Граф".
    # Принимает: путь к файлу исходных данных и тип файла исходных данных.
    def __init__(self,
                 input_file_path,  # - путь к файлу входных данных.
                 input_file_type):  # - тип файла входных данных.

        # Открытие файла исходных данных:

        try:  # Пробуем открыть файл исходных данных.

            input_file = open(input_file_path, "r")

        except IOError:  # Если не удается открыть файл исходных данных, выдаем ошибку и завершаем выполнение программы.

            print("Ошибка: Не удалось открыть файл исходных данных.\n"
                      " Нажмите любую клавишу чтобы выйти...")
            exit()

        # Непосредственное чтение файла исходных данных одним из трех способов, в зависимости от типа файла:

        if input_file_type == "-e":  # В файле дан список ребер.

            # Определяем размер графа:

            self.__N = 0  # По началу считаем равным 0.

            for input_file_line in input_file:  # Перебираем все строчки файла

                # В каждой строчке файла 0-ое и 1-ое числа - это номера вершин графа.
                # Поэтому выбрав максимальное из 0-ых и 1-ых чисел среди всех строчек файла,
                # получим максимальный номер вершины, т. е. размер графа.
                if input_file_line == "\n":
                    continue
                self.__N = max(self.__N, int(input_file_line.split()[0]), int(input_file_line.split()[1]))

            input_file.seek(0)  # Сделаем возврат позиции чтения к началу файла.

            # Строим заготовку матрицы смежности (пустую матрицу):

            self.__adjacency_matrix = []  # По началу пустая.

            for vertex_number in range(self.__N):  # Заполним матрицу смежности N списками, содержащими N нулей.
                self.__adjacency_matrix.append([0] * self.__N)

            # Определяем, указана ли в файле исходных данных длина ребер (или ее следует принять равной 1):

            if len(input_file.readline().split()) == 3:  # Если в первой строке файла 3 элемента (v1, v2, длина ребра).

                is_edge_length_defined_in_input_file = True  # Длина ребра задана в файле исходных данных.

            else:

                is_edge_length_defined_in_input_file = False  # Длина ребра задана в файле исходных данных.

            input_file.seek(0)  # Сделаем возврат позиции чтения к началу файла.

            # Непосредственная запись ребер графа в матрицу смежности из файла исходных данных:

            if is_edge_length_defined_in_input_file:  # В случае, когда в файле исходных данных задана длина ребер.

                for input_file_line in input_file:  # Перебираем строки в файле исходных данных.

                    # Пропускаем пустые строки:
                    if input_file_line == "\n":
                        continue

                    # Считывание данных из очередной строки файла:
                    v1, v2, edge_length = [int(n) for n in input_file_line.split()]

                    # Запись ребра в матрицу смежности графа:
                    self.__adjacency_matrix[v1 - 1][v2 - 1] = edge_length

            else:  # В случае, когда в файле исходных данных не задана длина ребер

                for input_file_line in input_file:  # Перебираем строки в файле исходных данных.

                    # Пропускаем пустые строки:
                    if input_file_line == "\n":
                        continue

                    # Считывание данных из очередной строки файла:
                    v1, v2 = [int(n) for n in input_file_line.split()]

                    # Запись ребра в матрицу смежности графа (длина ребра принимается равной единице):
                    self.__adjacency_matrix[v1 - 1][v2 - 1] = 1

        elif input_file_type == "-m":  # В файле дана матрица смежности.

            # Копируем матрицу смежности из файла:
            self.__adjacency_matrix = [[int(num) for num in input_file_line.split()] for input_file_line in input_file]

            # Вычисляем размер графа по длине первой (нулевой) строки матрицы смежности:
            self.__N = len(self.__adjacency_matrix[0])

        elif input_file_type == "-l":  # В файле дан список смежности

            # Определяем размер графа:

            self.__N = 0  # По началу считаем равным 0.

            for input_file_line in input_file:  # Перебираем строки файла исходных данных.

                # В каждой строке исходного файла указаны номера вершин графа,
                # поэтому, выбрав максимальный номер вершины среди всех номеров каждой строки,
                # получим размер графа:
                self.__N = max([self.__N] + list(map(lambda x: int(x), input_file_line.split())))

            input_file.seek(0)  # Сделаем возврат позиции чтения к началу файла.

            # Если вдруг последняя вершина в файле изолированная
            s = sum(1 for line in input_file)
            if s > self.__N:
                self.__N = s

            input_file.seek(0)  # Сделаем возврат позиции чтения к началу файла.

            # Строим заготовку матрицы смежности (пустую матрицу):

            self.__adjacency_matrix = []  # По началу пустая.

            for vertex_number in range(self.__N):  # Заполним матрицу смежности N списками, содержащими N нулей.
                self.__adjacency_matrix.append([0] * self.__N)

            # Непосредственное считывание графа из файла исходных данных:

            vertex_number = 0  # Начинаем с нулевой вершины (соответствует первой строке файла исходных данных).

            for input_file_line in input_file:  # Перебираем строки файла исходных данных.

                # Разбиваем строку файла на вершины, инцидентные данной:
                for connected_vertex_number in list(map(lambda x: int(x), input_file_line.split())):
                    # Записываем в матрицу смежности ребро: от данной вершине до инцидентной ей (ребро длины 1).
                    self.__adjacency_matrix[vertex_number][connected_vertex_number - 1] = 1

                # Переходим к рассмотрению следующей вершины:
                vertex_number += 1

        else:  # Если тип файла указан некорректно.

            print("Ошибка: Некорректный тип файла исходных данных.\n"
                      " Нажмите любую клавишу чтобы выйти...")
            exit()

        # В матрице смежности отсутствующие ребра помечаем как ребра длины бесконечность:

        for vi in range(self.__N):  # Перебор вершин по строкам матрицы смежности.

            for vj in range(self.__N):  # Перебор вершин по столбцам матрицы смежности.

                # Если ребро отсутствует (и рассматривается не диагональный эл-т матрицы смежности):
                if vi != vj and self.__adjacency_matrix[vi][vj] == 0:
                    # Заменяем на бесконечность
                    self.__adjacency_matrix[vi][vj] = INF

    # Название метода: "Весовая функция (weight)".
    # Принимает: номера двух вершин.
    # Возвращает: вес ребра, связывающего данные две вершины.
    def weight(self, vi, vj):

        # Вес ребра связывающего данные две вершины определяем из матрицы смежности:
        return self.__adjacency_matrix[vi][vj]

    # Название метода: "is_edge".
    # Принимает: номера двух вершин.
    # Возвращает: - True, если в графе есть ребро/дуга между данными вершинами
    #             - False, если в графе нет ребра/дуги между данными вершинами
    def is_edge(self, vi, vj):

        # Определяем наличие ребра как неравенство нулю соответствующего элемента матрицы смежности:
        return bool(self.__adjacency_matrix[vi][vj] != 0)

    # Название метода: "adjacency_matrix".
    # Принимает: ___ .
    # Возвращает: матрицу смежности графа/орграфа.
    def adjacency_matrix(self):

        # Возвращаем матрицу смежности графа:
        return self.__adjacency_matrix

    # Название метода: "size".
    # Принимает: ___ .
    # Возвращает: размер графа.
    def size(self):

        # Возвращаем размер графа:
        return self.__N

    # Название метода: "adjacency_list".
    # Принимает: номер вершины.
    # Возвращает: список вершин графа, смежных данной вершине.
    def adjacency_list(self, vertex_number):

        list_of_adjacent_vertices = []  # Список вершин смежных данной.

        # Перебираем все остальные вершины графа:
        for another_vertex_number in range(self.__N):

            # Саму вершину не считаем в искомом списке:
            if vertex_number == another_vertex_number:
                continue

            # Если есть путь из данной вершины к другой:
            if self.__adjacency_matrix[vertex_number][another_vertex_number] != INF:
                # Добавляем данное ребро
                list_of_adjacent_vertices.append(another_vertex_number)

        # Возвращаем список вершин смежных данной:
        return list_of_adjacent_vertices

    # Название метода: "list_of_edges".
    # Принимает: ___ .
    # Возвращает: список всех ребер графа ИЛИ список всех рёбер графа, инцидентных вершине v / исходящих из вершины v.
    # Примечание: данная функция, по сути, организует перегрузку функции, вызывая,
    #             в зависимости от числа поданных на вход аргументов одну из двух
    #             "перегружаемых" функций.
    def list_of_edges(self, *args):

        if len(args) == 0:  # Если на вход не подавались параметры.

            return self.list_of_edges_no_param()  # Вызов варианта функции без параметров.

        else:  # Если на вход не подавались параметры.

            return self.list_of_edges_one_param(args[0])  # Вызов варианта функции с одним параметром.

    # Название метода: "list_of_edges_no_param".
    # Принимает: ___ .
    # Возвращает: список всех ребер графа.
    def list_of_edges_no_param(self):

        # Список всех ребер графа:
        list_of_all_edges = []

        # Перебор матрицы смежности по строкам:
        for vi in range(self.__N):

            # Перебор матрицы смежности по столбцам:
            for vj in range(self.__N):

                # Если есть ребро между двумя неравными вершинами:
                if self.__adjacency_matrix[vi][vj] != 0 and self.__adjacency_matrix[vi][vj] != INF:
                    # Добавляем ребро в список всех ребер:
                    list_of_all_edges.append([vi, vj])

        # Возвращаем список всех ребер графа:
        return list_of_all_edges

    # Название метода: "list_of_edges_one_param".
    # Принимает: вершина v.
    # Возвращает: список рёбер графа, инцидентных вершине v / исходящих из вершины v.
    def list_of_edges_one_param(self, v):

        # Список рёбер графа, инцидентных вершине v / исходящих из вершины v:
        list_of_incident_vertices = []

        # Перебираем все остальные вершины графа:
        for vj in range(self.__N):

            # Если есть путь до вершины неравной данной:
            if self.__adjacency_matrix[v][vj] != 0 and self.__adjacency_matrix[v][vj] != INF:
                # Добавляем ребро в список ребер инцидентных данной вершине:
                list_of_incident_vertices.append([v, vj])

        # Возвращаем список рёбер графа, инцидентных вершине v / исходящих из вершины v:
        return list_of_incident_vertices

    # Название метода: "is_directed".
    # Принимает: ___ .
    # Возвращает: - True, если граф ориентированный
    #             - False, если граф простой
    def is_directed(self):

        # Перебор матрицы смежности по строкам:
        for vi in range(self.__N):

            # Перебор матрицы смежности по столбцам:
            for vj in range(self.__N):

                # Если в матрице смежности обнаружили дугу, то граф ориентированный:
                if self.__adjacency_matrix[vi][vj] != self.__adjacency_matrix[vj][vi]:
                    return True

        # В матрице не нашлось дуг, то он неориентированный:
        return False


# Поиск мостов и точек сочленения:
class find_bridges_and_cut_vertices:

    # Конструктор класса (инициализация переменных для алгоритма):
    def __init__(self, gr):

        self.__graph = gr  # Граф

        self.__N = gr.size()  # Число вершин графа

        self.__visited = [False] * self.__N  # Список посещений вершин
        self.__tin = [INF] * self.__N  # Время входа вершины в DFS
        self.__tup = [INF] * self.__N  # Минимум из времени захода в саму вершину v,
        # времен захода в вершины-концы обратных ребер и tup сыновей

        self.__timer = 0  # Таймер

        self.__bridges = []  # Найденные мосты
        self.__cut_points = []  # Найденные точки сочленения

    # DFS (рекурсивный), O(V+E):
    def dfs(self, v, p=-1):

        self.__visited[v] = True  # Вершина посещена поиском в глубину

        self.__tin[v] = self.__timer  # Время входа в вершину равно текущему времени на таймере

        self.__timer += 1  # Таймер увеличивается

        children = 0  # Число

        for u in self.__graph.adjacency_list(v):

            if u == p:
                continue

            if self.__visited[u]:  # Если посещали вершину u (обратное ребро)

                self.__tup[v] = min(self.__tup[v], self.__tin[u])

            else:  # Если не посещали вершину u (прямое ребро)

                self.dfs(u, v)

                self.__tup[v] = min(self.__tup[v], self.__tup[u])

                # Если нельзя другим путем добраться в v или выше, то (v,u) мост:
                if self.__tin[v] < self.__tup[u]:

                    self.__bridges += [sorted([v + 1, u + 1])]  # Добавляем мост в список мостов

                if self.__tin[v] <= self.__tup[u] and p != -1:

                    self.__cut_points += [v + 1]  # Добавляем точку сочленения в список точек сочленения

                children += 1  # Подсчитали еще одного потомка

        if p == -1 and children > 1:  # Корневая вершина - шарнир, если у нее есть несколько потомков
            self.__cut_points += [v + 1]

    # Получить ответ:
    def answ(self):

        # Запускаем DFS для каждой из вершин:
        for i in range(self.__N):
            self.dfs(i)

        return self.__bridges, self.__cut_points


# Получение матрицы смежности соответственного графа:
def correlated(am_old):
    am = [[i for i in row] for row in am_old]
    n = len(am[0])
    for i in range(n):
        for j in range(n):
            if am[i][j] != 0 and am[i][j] != INF:
                am[j][i] = am[i][j]
    return am


# --- Функция ввода данных в программу ---
#
# - Принимает : (1) Консольные аргументы при запуске программы.
#
# - Возвращает: (1) Граф.
#               (2) Способ вывода ответа на задачу (в консоль или в файл).
#               (3) Путь к файлу выходных данных или "", если его нет
#
def input_data(console_input_arguments):
    # Вызов справки при наличии соответствущего ключа (все остальные ключи игнорируются):
    if "-h" in console_input_arguments:
        print("""Справка:
        Задача: 3
        Автор: Богомольский Виталий
        Группа: М3О-211Б-21
        Ключи:
        -e "edges_list_file_path"
        -m "adjacency_matrix_file_path"
        -l "adjacency_list_file_path"
        -o "output_file_path"
        -h Справка
        """)

        print("Нажмите любую клавишу чтобы выйти...")
        exit()

    # Число входных параметров (ключей и их параметрами):
    number_of_input_parameters = len(console_input_arguments) - 1

    # Обработка ошибки: некорректное число входных параметров (то есть и некорректное число ключей):
    if number_of_input_parameters != 2 and number_of_input_parameters != 4:
        print("Ошибка. Некорректное число входных параметров.\n"
                  "Нажмите любую клавишу чтобы выйти...")
        exit()

    # Обработка ошибок для одного ключа (двух входных параметров):
    if number_of_input_parameters == 2:

        # Обработка ошибки: введен один только ключ и его один параметр, но этот ключ - "-о":
        if console_input_arguments[1] == "-o":
            print("Ошибка. Введен один ключ, но это '-о'.\n"
                      "Нажмите любую клавишу чтобы выйти...")
            exit()

        # Обработка ошибки: введен один только ключ и его один параметр, но этот ключ неизвестен:
        if console_input_arguments[1] not in ["-e", "-l", "-m"]:
            print("Ошибка. Введенный ключ неизвестен.\n"
                      "Нажмите любую клавишу чтобы выйти...")
            exit()

    # Обработка ошибок для двух ключей (четырех входных параметров)
    if number_of_input_parameters == 4:

        # Обработка ошибки: введено два ключа и два их параметра, но среди двух ключей нет ключа "-о":
        if "-o" not in [console_input_arguments[1]] + [console_input_arguments[3]]:
            print("Ошибка. Введено два ключа, но ни один из них не '-o'.\n"
                      "Нажмите любую клавишу чтобы выйти...")
            sys.exit()

        # Обработка ошибки: среди двух ключей содержится неизвестный ключ:
        for arg in [console_input_arguments[1]] + [console_input_arguments[3]]:

            if arg not in ["-e", "-l", "-m"]:
                print("Ошибка. Ключ '" + arg + "' неизвестен" +
                          "\nНажмите любую клавишу чтобы выйти...")
                exit()

        # Обработка ошибки: введено два ключа, но они одинаковые.
        if number_of_input_parameters == 4 and console_input_arguments[2] == console_input_arguments[4]:
            print("Ошибка. Введено два ключа, но они одинаковые.\n"
                      "Нажмите любую клавишу чтобы выйти...")
            sys.exit()

    # Определяем из входных параметров путь к файлу входных данных и его тип:

    input_file_path = ""  # Путь к файлу входных данных.
    input_file_type = ""  # Тип файла входных данных.
    how_to_output = ""  # Будет ли производиться вывод в файл
    output_file_path = ""  # Имя файла выходных данных (если таковой есть)

    if console_input_arguments[1] != "-o":  # Если первый ключ не "-o".

        input_file_path = console_input_arguments[2]
        input_file_type = console_input_arguments[1]

        # Здесь же определим, будет ли вывод в файл и получим путь к файлу результатов:
        if number_of_input_parameters == 4:
            how_to_output = "file"
            output_file_path = console_input_arguments[4]

    else:

        input_file_path = console_input_arguments[4]
        input_file_type = console_input_arguments[3]

        how_to_output = "file"
        output_file_path = console_input_arguments[2]

    if how_to_output == "":
        how_to_output = "console"

    # Создаем граф:

    graph = Graph(input_file_path, input_file_type)

    # Возвращаем граф, способ вывода данных, путь к файлу выходных данных:

    return graph, how_to_output, output_file_path


# --- Функция вывода данных из программы ---
#
# - Принимает : (1) Текст ответа.
#               (2) Способ вывода ответа (в консоль или в файл).
#               (3) Путь к файлу выходных данных (или "", если он не указан)
#
# - Возвращает: (1) Ничего. (выводит ответ в консоль или в файл)
#
def output_data(answer, how_to_output, output_file_path):
    if how_to_output == "file":  # Печать в файл.

        of = open(output_file_path, "w", encoding="utf-8")
        of.write(answer)

    else:  # Печать на экран.

        print(answer, end="")


##########################################################
#                   Часть 1: Ввод графа                  #
##########################################################


# Получим консольные аргументы, указанные при запуске программы:
console_input_arguments = sys.argv

# Вводится граф, способа вывода ответа на задачу (выводить в консоль или в файл)
# и путь к файлу выходных данных (или "" если его нет):
graph, how_to_output, output_file_path = input_data(console_input_arguments)

##########################################################
#     Часть 2: Применение алгоритмов для решения задачи  #
##########################################################

answer = ""  # Ответ на всё задание! Будет выводиться либо на экран, либо в файл.

bridges = None  # Мосты
cut_vertices = None  # Точки сочленения

algorithm = find_bridges_and_cut_vertices(graph)  # Класс алгоритма поиска мостов и шарниров

bridges, cut_vertices = algorithm.answ()  # Запускаем алгоритм, получаем ответ

# Преобразуем список мостов к виду с круглыми скобками:
bridges_str = str(list(map(lambda bridge: "(" + str(bridge[0]) + ", " + str(bridge[1]) + ")", bridges))).replace("'", "")

# Выводим ответ
answer += "Bridges:\n" + str(bridges_str) + "\n" + \
          "Cut vertices:\n" + str(cut_vertices) + "\n"

##########################################################
#                 Часть 3: Вывод ответа                  #
##########################################################


# Вывод ответа (в консоль или в файл):
output_data(answer, how_to_output, output_file_path)
