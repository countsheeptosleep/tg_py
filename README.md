# tg_py
Алгоритмы теории графов на python

Подробное описание каждой программы и способов ее работы в соответствующем main.py

В общих чертах:

1 - Программа, рассчитывающая следующие характеристики графа/орграфа:
вектор степеней вершин, матрицу расстояний, диаметр, радиус,
множество центральных вершин (для графа), множество периферийных
вершин (для графа). Расчёт производится алгоритмом Флойда-Уоршелла.
Входные данные для работы программы задаются следующими ключами

2 - Программа, определяющая связность. Для графа – связность, а также
количество и состав компонент связности. Для орграфа – сильную, слабую
связность, или несвязность. А также количество и состав компонент
связности и сильной связности. Для определения используется поиск в
ширину.  (Косарайо)

3 - Программа, находящая мосты и шарниры в графе. Для орграфа находятся
мосты и шарниры в соотнесённом графе.