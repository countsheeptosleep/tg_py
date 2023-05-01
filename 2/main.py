import sys
import os

'''
----- СПРАВКА К КОДУ -----

Задача: 2
Автор: Б Виталий
Группа: М3О-211Б-21
Ключи:
    -e "edges_list_file_path"
    -m "adjacency_matrix_file_path"
    -l "adjacency_list_file_path"
    -o "output_file_path"
    -h Справка

----- УСЛОВИЕ ЗАДАЧИ 2 -----

Программа, определяющая связность. Для графа – связность, а также
количество и состав компонент связности. Для орграфа – сильную, слабую
связность, или несвязность. А также количество и состав компонент
связности и сильной связности. Для определения используется поиск в
ширину.
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
игнорируются.
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

            os.system("Ошибка: Не удалось открыть файл исходных данных.\n"
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

            os.system("Ошибка: Некорректный тип файла исходных данных.\n"
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

        # Если граф ориентированный, не идет речь о смежности вершин:
        if self.is_directed():
            os.system("Ошибка: В орграфе не ведем речь о смежности вершин.\n"
                      " Нажмите любую клавишу чтобы выйти...")
            exit()

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


# Класс "Вершина":
class Node:

    # Конструктор класса "Вершина"
    def __init__(self, v, prev=[], next=[]):
        self.__v = v  # Номер вершины
        self.__prev = prev  # Инцидентные вершины с входящих ребер
        self.__next = next  # Инцидентные вершины с выходящих ребер
        self.__parent = None  # Вершина-родитель, после рассмотрения которой в алгоритме внесли данную вершину в одно
        # из деревьев леса
        self.__depth = None  # Глубина вершины в BFS

    def set_depth(self, depth):
        self.__depth = depth

    def get_depth(self):
        return self.__depth

    # Добавить вершину с входящих ребер:
    def add_prev(self, prev):
        self.__prev = self.__prev + [prev]

    # Добавить вершину с выходящих ребер:
    def add_next(self, next):
        self.__next = self.__next + [next]

    # Получить вершины с входящих ребер:
    def get_prev(self):
        return self.__prev

    # Получить вершины с выходящих ребер:
    def get_next(self):
        return self.__next

    # Установить номер вершины:
    def set_v(self, v):
        self.__v = v

    # Получить номер вершины:
    def get_v(self):
        return self.__v

    # Установить вершину родителя:
    def set_parent(self, parent):
        self.__parent = parent

    # Получить вершину-родителя:
    def get_parent(self):
        return self.__parent

    # Печать вершины (из данной компоненты)
    def print_node(self):
        print(self.__v, "from", list(map(lambda x: x.get_v(), self.__prev)), "to",
              list(map(lambda x: x.get_v(), self.__next)))

    # Получить списком номер данной вершины и всех следующих из нее:
    def get_node_and_nexts(self, added=[]):
        added += [self]
        for v in self.__next:
            if v not in added:
                added += v.get_node_and_nexts(added)[len(added):]
        return sorted(list(map(lambda v: v.get_v() + 1, added)))

    # Debug:
    # def print_node_and_nexts(self, printed=[]):
    #     self.print_node()
    #     printed += [self]
    #     for v in self.__next:
    #         if v not in printed:
    #             v.print_node_and_nexts(printed)


# Класс "Дерево"
class Tree:

    # Конструктор класса "Дерево"
    def __init__(self, root):
        self.__root = root

    # Печать дерева:
    def tree_print(self):
        if self.__root:
            self.__root.print_node_and_nexts()

    # Установить корень дерева:
    def set_root(self, root):
        self.__root = root

    # Получить корень дерева:
    def get_root(self, root):
        return self.__root

    # Получить список вершин дерева:
    def get_nodes(self):
        if self.__root:
            return self.__root.get_node_and_nexts([])


# Класс "Лес"
class Forest:

    # Конструктор леса
    def __init__(self):
        self.__trees = []

    # Добавление дерева в лес
    def add_tree(self, tree):
        self.__trees = self.__trees + [tree]

    # Получение деревьев из леса
    def get_trees(self):
        return self.__trees

    # Печать деревьев леса:
    def forest_print(self):
        print("FOREST")
        tree_number = 1
        for tree in self.get_trees():
            print("Tree №", tree_number, sep="")
            tree.tree_print()
            tree_number += 1


# --- Функция поиска в ширину ---
# Принимает:
#   1) Матрица смежности графа
#   2) Порядок, в котором нужно запускать BFS (или False, если BFS запускается во возрастанию номеров вершин)
# Возвращает:
#   1) Лес BFS
#   2) Время выхода каждой вершины из BFS
# Сложность: без построения леса и расчета тактов - O(|V|+|E|)
def bfs(am, established_order_of_enumeration=False):

    N = len(am[0])  # Число вершин графа

    Nodes = [Node(v=i) for i in range(N)]  # Список объектов всех вершин графа,
    # каждая из вершин пока имеет только номер и не имеет ребер

    forest = Forest()  # Лес - ответ, пока пустой

    leave_time = [0] * N  # Время выхода каждой вершины из BFS, пока заполнено нулями

    queue = []  # Очередь посещений

    visited = []  # Посещенные вершины

    tact = 0  # Такты работы BFS

    while len(visited) != N:  # Пока не переберем все вершины графа, запускаем очередной проход BFS

        # Если не указан порядок, в котором нужно запускать BFS:
        if not established_order_of_enumeration:

            # Стартовая вершина для очередного дерева выбирается как наименьшая по номеру из не посещенных
            start_node = [node for node in Nodes
                          if node not in visited][0]  # Начальная вершина

        # Если указан порядок, в котором нужно запускать BFS:
        else:

            # Стартовая вершина для очередного дерева выбирается как наименьшая по номеру из не посещенных в указанном
            # списке-порядке:
            start_node = Nodes[[v for v in established_order_of_enumeration
                                if v not in list(map(lambda x: x.get_v(), visited))][0]]  # Начальная вершина

        # Стартовая вершина находится на глубине 1 поиска в ширину
        start_node.set_depth(1)

        # Добавляем начальную вершину в очередь:
        queue.append(start_node)

        # Создаем в лесу BFS новое дерево, состоящее из одной только вершины - стартовой
        forest.add_tree(Tree(start_node))

        # Добавляем начальную вершину в помеченные:
        visited.append(start_node)

        while queue:  # Пока не пройдем всю очередь (максимально не заполним дерево)

            current_node = queue.pop(0)  # Берем следующую вершину из очереди

            # Учет тактового времени для спуска в вершину:

            parent = current_node.get_parent()  # Родитель текущей вершины

            for i in range(current_node.get_depth()-1):  # Проходим вверх по вершинам-родителям,

                # увеличивая их тактовое время:
                leave_time[parent.get_v()] = tact + parent.get_depth()  # Устанавливаем тактовое время родителя
                parent = parent.get_parent()  # Переходим к родителю родителя

            # Тактовое время вершины:

            real_parent = current_node.get_parent()

            if real_parent:
                tact = leave_time[real_parent.get_v()]
            else:
                tact += 1  # Следующий такт

            leave_time[current_node.get_v()] = tact  # Коснулись текущей вершины - записываем такт

            # Определяем соседей рассматриваемой вершины:
            neighbours = [node for node in Nodes
                          if am[current_node.get_v()][node.get_v()] != 0
                          and am[current_node.get_v()][node.get_v()] != INF]  # Определяем соседей

            # Перебираем соседей вершины:
            for neighbour in neighbours:

                # Если сосед не помечен:
                if neighbour not in visited:

                    # Добавляем его в очередь и помечаем:
                    queue.append(neighbour)
                    visited.append(neighbour)

                    # Достраиваем дерево BFS:
                    current_node.add_next(neighbour)  # Из текущей вершины есть ребро к соседу
                    neighbour.add_prev(current_node)  # К соседу есть ребро из текущей вершины

                    # Абстрактный параметр для последующего подсчета тактов:
                    neighbour.set_parent(current_node)  # Текущая вершина - это "родитель" для соседа, это значит,
                    # что сосед был добавлен в дерево именно при вызове BFS из текущей вершины

                    neighbour.set_depth(current_node.get_depth() + 1)

            # Примечание: счет тактов ведется неполный, но с сохранением правильного теоретического порядка.
            # Пропускаются промежуточные такты спуска, кроме того, подъем обратно всегда осуществляется до стартовой
            # вершины.

            # Учет тактового времени подъема из вершины:

            parent = current_node.get_parent()  # Родитель текущей вершины

            for i in range(current_node.get_depth() - 1):  # Проходим вверх по вершинам-родителям,
                # увеличивая их тактовое время:

                tact += 1  # Тактовое время
                leave_time[parent.get_v()] = tact  # Устанавливаем тактовое время родителя
                parent = parent.get_parent()  # Переходим к родителю родителя

    # Debug: (print leave time)
    # for i in range(len(leave_time)):
    #   print(i+1, leave_time[i])

    return forest, leave_time


# Транспонирование матрицы смежности
def transpose(am_old):
    am = [[i for i in row] for row in am_old]
    return [[am[j][i] for j in range(len(am))] for i in range(len(am[0]))]


# Получение матрицы смежности соответственного графа:
def correlated(am_old):
    am = [[i for i in row] for row in am_old]
    n = len(am[0])
    for i in range(n):
        for j in range(n):
            if am[i][j] != 0 and am[i][j] != INF:
                am[j][i] = am[i][j]
    return am


# Алгоритм Косарайю:
def kosaraju(graph):

    am_init = graph.adjacency_matrix()  # Матрица смежности исходного графа
    am_transposed = transpose(am_init)  # Матрица смежности инвертированного графа

    # Лес BFS инвертированного графа и время выхода его вершин из BFS:
    forest_inverted, leave_time_inverted = bfs(am_transposed)

    # Из времени выхода вершин инвертированного графа
    # рассчитаем порядок обращения к вершинам исходного графа во втором BFS:
    established_order_of_enumeration = [x[1] for x in sorted(

        zip(leave_time_inverted, [i for i in range(graph.size())])

        , key=lambda tup: tup[0])]

    established_order_of_enumeration.reverse()

    # Лес BFS исходного графа и время выхода его вершин из BFS:
    forest_init, leave_time_init = bfs(am_init, established_order_of_enumeration)

    return forest_init


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
        Задача: 2
        Автор: Богомольский Виталий
        Группа: М3О-211Б-21
        Ключи:
        -e "edges_list_file_path"
        -m "adjacency_matrix_file_path"
        -l "adjacency_list_file_path"
        -o "output_file_path"
        -h Справка
        """)

        os.system("Нажмите любую клавишу чтобы выйти...")
        exit()

    # Число входных параметров (ключей и их параметрами):
    number_of_input_parameters = len(console_input_arguments) - 1

    # Обработка ошибки: некорректное число входных параметров (то есть и некорректное число ключей):
    if number_of_input_parameters != 2 and number_of_input_parameters != 4:
        os.system("Ошибка. Некорректное число входных параметров.\n"
                  "Нажмите любую клавишу чтобы выйти...")
        exit()

    # Обработка ошибок для одного ключа (двух входных параметров):
    if number_of_input_parameters == 2:

        # Обработка ошибки: введен один только ключ и его один параметр, но этот ключ - "-о":
        if console_input_arguments[1] == "-o":
            os.system("Ошибка. Введен один ключ, но это '-о'.\n"
                      "Нажмите любую клавишу чтобы выйти...")
            exit()

        # Обработка ошибки: введен один только ключ и его один параметр, но этот ключ неизвестен:
        if console_input_arguments[1] not in ["-e", "-l", "-m"]:
            os.system("Ошибка. Введенный ключ неизвестен.\n"
                      "Нажмите любую клавишу чтобы выйти...")
            exit()

    # Обработка ошибок для двух ключей (четырех входных параметров)
    if number_of_input_parameters == 4:

        # Обработка ошибки: введено два ключа и два их параметра, но среди двух ключей нет ключа "-о":
        if "-o" not in [console_input_arguments[1]] + [console_input_arguments[3]]:
            os.system("Ошибка. Введено два ключа, но ни один из них не '-o'.\n"
                      "Нажмите любую клавишу чтобы выйти...")
            sys.exit()

        # Обработка ошибки: среди двух ключей содержится неизвестный ключ:
        for arg in [console_input_arguments[1]] + [console_input_arguments[3]]:

            if arg not in ["-e", "-l", "-m"]:
                os.system("Ошибка. Ключ '" + arg + "' неизвестен" +
                          "\nНажмите любую клавишу чтобы выйти...")
                exit()

        # Обработка ошибки: введено два ключа, но они одинаковые.
        if number_of_input_parameters == 4 and console_input_arguments[2] == console_input_arguments[4]:
            os.system("Ошибка. Введено два ключа, но они одинаковые.\n"
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

# Слабые компоненты связности:
wcc = list(map(lambda tree: tree.get_nodes(),
                      bfs(correlated(graph.adjacency_matrix()))[0].get_trees()))

# Сильные компоненты связности:
scc = list(map(lambda tree: tree.get_nodes(),
               kosaraju(graph).get_trees()))

# Число компонент связности:
number_of_scc = len(scc)
number_of_wcc = len(wcc)

if not graph.is_directed():  # Если граф неориентированный:

    if number_of_scc == 1:  # Одна сильная компонента связности

        answer += "Graph is connected.\n"

    else:  # Много сильных компонент связности

        answer += "Graph is not connected and contains " + str(number_of_scc) + " connected components.\n"

    answer += "Connected components:\n"
    answer += str(scc) + "\n"

else:  # Если граф ориентированный

    if number_of_wcc == 1:  # Одна слабая компонента связности

        answer += "Diraph is connected.\n"
        answer += "Connected components:\n"
        answer += str(wcc) + "\n"

    else:  # Много слабых компонент связности

        answer += "Diraph is not connected and contains " + str(number_of_wcc) + " connected components.\n"
        answer += "Connected components:\n"
        answer += str(wcc) + "\n"

    if number_of_scc == 1:  # Одна сильная компонента связности

        answer += "Digraph is strongly connected.\n"
        answer += "Strongly connected components:\n"
        answer += str(scc) + "\n"

    else:  # Много сильных компонент связности

        answer += "Digraph is weakly connected and contains " + str(number_of_scc) + " strongly connected components.\n"
        answer += "Strongly connected components:\n"
        answer += str(scc) + "\n"


##########################################################
#                 Часть 3: Вывод ответа                  #
##########################################################


# Вывод ответа (в консоль или в файл):
output_data(answer, how_to_output, output_file_path)
