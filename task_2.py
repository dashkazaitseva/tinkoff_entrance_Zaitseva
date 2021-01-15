"""Вам необходимо написать консольную версию игры судоку с двумя режимами игры:

Режим игры для пользователя: генерируется поле с заданным (вводящимся с клавиатуры) количеством заполненных клеточек.
 Пользователь должен решить предложенное судоку, совершая ходы, представляющие собой запросы из трёх чисел (Строка, Колонка, Число). 
 После каждого хода пользователя поле должно обновляться.

Режим игры для компьютера: поле задаётся с клавиатуры аналогичным способом, но играете не вы, а ваша стратегия. 
Ваш алгоритм должен решить этот судоку или сообщить о невозможности его решения. Каждый ход компьютера так же выводится 
на стандартный поток вывода в формате (Строка, Колонка, Число), состояние поля визуализируется на каждой итерации работы алгоритма.

Первый режим должен предусматривать «сохранение» и «загрузку» игры, то есть при игре игра может быть в любой момент завершена
 пользователем и сохранена в виде файла .pkl, а также загружена из соответствующего файла и продолжена. При реализации придерживайтесь
  принципов объектно-ориентированного программирования (сессия игры должна представлять собой класс, содержащий в себе состояние игры, 
  с соответствующими методами и свойствами).
"""

import random
import pickle

class Grid:
    """Игровое поле и действия, связанные с ним"""
    def __init__(self, n):
        self.n = n
        self.field = [[(i * self.n + i // self.n + j) % (self.n * self.n) + 1 for j in range(self.n * self.n)] for i in range(self.n * self.n)]

    def __del__(self):
        pass

    def display(self):
        #отображение поля
        print('   ', end = '', sep = '')
        for i in range(self.n ** 2):
            print('[', i + 1, ']', sep = '', end = '')
            if (i % self.n == self.n - 1):
                print(' ', sep = '', end = '')
        print()
        for i in range(self.n ** 2):
             print('[', i + 1, ']', sep = '', end = ' ')
             for j in range(self.n**2):
                 print('?' if self.field[i][j] == 0 else self.field[i][j], sep = '', end ='  ')
                 if (j % self.n == self.n - 1):
                     print(' ', sep = '', end = '')
        
             if(i % self.n == self.n - 1):
                print('\n', sep = '', end = '')
             print()
        print()


    #методы для генерации верного случайного поля
    def transp(self):
        self.field = list(map(list, zip(*self.field)))

    def swap_rows_s(self):
        l1 = random.randrange(0, self.n, 1)
        a1 = random.randrange(0, self.n, 1)
        l2 = random.randrange(0, self.n, 1)
        while (l2 == l1):
            l2 = random.randrange(0, self.n, 1)
        self.field[a1 * self.n + l1], self.field[a1 * self.n + l2] = self.field[a1 * self.n + l2], self.field[a1 * self.n + l1]
        
    def swap_colums_s(self):
        Grid.transp(self)
        Grid.swap_rows_s(self)
        Grid.transp(self)        

    def swap_rows_a(self):
        a1 = random.randrange(0, self.n, 1)
        a2 = random.randrange(0, self.n, 1)
        while (a1 == a2):
            a2 = random.randrange(0, self.n, 1)
        for i in range(self.n):
             self.field[a1*self.n + i], self.field[a2*self.n + i] = self.field[a2*self.n + i], self.field[a1*self.n + i]  

    def swap_colums_a(self):
        Grid.transp(self)
        Grid.swap_rows_a(self)
        Grid.transp(self)


    #генерация поля
    def gen(self):
        self.field = [[(i * self.n + i // self.n + j) % (self.n * self.n) + 1 for j in range(self.n * self.n)] for i in range(self.n * self.n)]
        actions = ['Grid.transp(self)', 'Grid.swap_colums_s(self)' , 'Grid.swap_rows_s(self)', 'Grid.swap_colums_a(self)', 'Grid.swap_rows_a(self)']
        #Grid.display(self)
        for _ in range(13):
            eval(actions[random.randrange(0, len(actions), 1)])
            #Grid.display(self)

    #считывание поля

    def gett(self):
        for i in range(self.n ** 2):
            a = list(map(int, input().split()))
            for j in range(self.n ** 2):
                self.field[i][j] = a[j]

    #проверка на корректность

    def check(self):
        a = {i for i in range(1, self.n ** 2 + 1)}
        for i in range(self.n ** 2):
            b = set()
            for j in range(self.n ** 2):
                b.add(self.field[i][j])
            if (a != b):
                return False

        for j in range(self.n ** 2):
            b = set()
            for i in range(self.n ** 2):
                b.add(self.field[i][j])
            if (a != b):
                return False

        for i in range (self.n):
            for j in range(self. n):
                b = set()
                for k in range(self.n):
                    for l in range(self.n):
                        b.add(self.field[i * self.n + k][j * self.n + l])
                if (a != b):
                    return False
        
        return True


    #удаление некоторых ячеек (этап генерации поля)
    def cleanse(self, compl):
        cnt = self.n ** 4 - compl
        while (cnt > 0):
            r = random.randrange(0, self.n ** 2, 1)
            c = random.randrange(0, self.n ** 2, 1)
            while (self.field[r][c] == 0):
                r = random.randrange(0, self.n ** 2, 1)
                c = random.randrange(0, self.n ** 2, 1)
            self.field[r][c] = 0
            cnt -= 1

    #авторешатель
    def autosolve(self):
        vari = [[set(range(1, self.n ** 2 + 1)) for _ in range(self.n ** 2)] for __ in range (self.n ** 2)]

        cont = True

        while (cont):
            cont = False

            for i in range(self.n ** 2):
                b = set()
                for j in range(self.n ** 2):
                    if (self.field[i][j] != 0):
                        a = len(b)
                        b.add(self.field[i][j])
                        if (len(b) != a + 1):
                            return False
                for j in range(self.n ** 2):
                    vari[i][j] = vari[i][j].difference(b)


            for j in range(self.n ** 2):
                b = set()
                for i in range(self.n ** 2):
                    if (self.field[i][j] != 0):
                        a = len(b)
                        b.add(self.field[i][j])
                        if (len(b) != a + 1):
                            return False
                for i in range(self.n ** 2):
                    vari[i][j] = vari[i][j].difference(b)

            for i in range(self.n):
                for j in range(self.n):
                    b = set()
                    for k in range(self.n):
                        for l in range(self.n):
                            r = i * self.n + k
                            c = j * self.n + l
                            if (self.field[r][c] != 0):
                                a = len(b)
                                b.add(self.field[r][c])
                                if (len(b) != a + 1):
                                    return False
                    for k in range(self.n):
                        for l in range(self.n):
                            r = i * self.n + k
                            c = j * self.n + l
                            vari[r][c] = vari[r][c].difference(b)
            
            for i in range(self.n ** 2):
                for j in range(self.n ** 2):
                    if (self.field[i][j] != 0):
                        continue
                    if (len(vari[i][j]) == 0):
                        return False
                    if (len(vari[i][j]) == 1):
                        cont = True
                        for el in vari[i][j]:
                            self.field[i][j] = el
            
            if (cont == False):
                a, b = -1, -1
                for i in range(self.n ** 2):
                    for j in range(self.n ** 2):
                        if (self.field[i][j] == 0):
                            if (a == -1 and b == -1):
                                a, b = i, j
                            if (len(vari[i][j]) < len(vari[a][b])):
                                a, b = i, j
                #print(a + 1, b + 1, vari[a][b])
                for el in vari[a][b]:
                    
                    q = [[self.field[i][j] for j in range(self.n**2)] for i in range(self.n**2)]
                    self.field[a][b] = el
                    #Grid.display(self)
                    Grid.autosolve(self) 
                    if (Grid.check(self)):
                        return True
                    #Grid.display(self)
                    self.field = q
                return False
        return Grid.check(self)


class Game:
    def __init__(self, n, mod, compl):
        self.mod = mod
        self.n = n
        self.grid = Grid(n)
        self.grid1 = Grid(n)
        self.compl = compl
        Game.play(self)

    
    #режим компьютера ---- подзадача два
    def auto_game(self):
        
        #считать сетку
        print('Введите условия в формате 9 чисел через пробел на каждой строке')
        Grid.gett(self.grid)

        stat = Grid.autosolve(self.grid)
        if (stat):
            Grid.display(self.grid)
        else:
            print('Невозможно решить данное судоку')


    #играет человек ---- подзадача один
    def user_game(self):
        if (int(input('''Для загрузки старой игры введите 2
        Для начала новой - 1 ''')) == 2):
            pkl_file = open('data.pkl', 'rb')
            self.grid = pickle.load(pkl_file)
            pkl_file.close()
            self.grid1 = self.grid
            Grid.autosolve(self.grid1)
            self.n = self.grid.n
        else:
            Grid.gen(self.grid)
            Grid.cleanse(self.grid, self.compl)
            self.grid1.field = [[self.grid.field[i][j] for j in range(self.n**2)] for i in range(self.n**2)]

            while (not Grid.autosolve(self.grid1)):
                Grid.gen(self.grid)
                Grid.cleanse(self.grid, self.compl)
                self.grid1.field = [[self.grid.field[i][j] for j in range(self.n**2)] for i in range(self.n**2)]
            
        Grid.display(self.grid)
        print('Формат взаимодействия: введите номер строки, столбца и число')
        correct = Grid.check(self.grid)
        outs = ['Продолжайте', 'Всё получится!', 'Пробуйте', 'Дорогу осилит идущий', 'Давайте', 'Дерзайте']
        while (not correct):
            a, b, c = map(int, input(outs[random.randrange(0, len(outs), 1)]).split())
            a -= 1
            b -= 1
            
            if (self.grid1.field[a][b] == c):
                self.grid.field[a][b] = c
                Grid.display(self.grid)
                correct = Grid.check(self.grid)
            else:
                print('Неверно, подумайте ещё')
            print('Для сохранения игры введите 2, для продолжения 1')
            if (int(input()) == 2):
                oput = open('data.pkl', 'wb')
                pickle.dump(self.grid, oput)
                oput.close()
                break
        print("Поздравляю, вы справились!")


    #игра
    def play(self):
        if self.mod == 0:
            self.user_game()
        else:
            self.auto_game()

Game(3, 1, 40)