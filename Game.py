from random import randint

ship_list = [3, 2, 2, 1, 1, 1, 1]
field_size = 6

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Координаты удара вне поля"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли по этим координатам"


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, nose_coords, lenght, orientation):
        self.nose_coords = nose_coords
        self.lenght = lenght
        self.orientation = orientation
        self.lives = lenght

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.lenght):
            cur_x = self.nose_coords.x
            cur_y = self.nose_coords.y

            if self.orientation == 0:
                cur_x += i

            elif self.orientation == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=field_size):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = u"\u25A0"
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        # res = ""
        res = "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace(u"\u25A0", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Убил")
                    return False
                else:
                    print("Ранил")
                    return True

        self.field[d.x][d.y] = u"\u272B"
        print("Мимо")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=field_size):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.ai = AI(co, pl)
        self.user = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        board = Board(size=self.size)
        attempts = 0
        for lenght in ship_list:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                orientation = randint(0, 1)
#Если корабль длинный, то получаем от рандинт числа в таком диапазоне, чтобы по длине корабль помещался
                if orientation == 0:
                        x, y = randint(0, field_size - lenght - 1), randint(0, field_size)
                else:
                        x, y = randint(0, field_size), randint(0, field_size - lenght - 1)
                ship = Ship(Dot(x, y), lenght, orientation)
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-" * 27)
        print("       Морской бой")
        print("Введите координаты удара в")
        print("формате: Номер строки (1-6)")
        print("ПРОБЕЛ, номер столбца (1-6)")

    def print_boards(self):
        print("-" * 27)
        print("Доска игрока:")
        print(self.user.board)
        print("-" * 27)
        print("Доска компьютера:")
        print(self.ai.board)

    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                print("-" * 27)
                # print("Ход игрока!")
                repeat = self.user.move()
            else:
                print("-" * 27)
                # print("Ход компьютера!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

#            if self.ai.board.count == 7:
#            if self.ai.board.count == len(self.ai.board.ships)
            if self.ai.board.defeat():
                print("-" * 20)
                print("Игрок выиграл!")
                break

#            if self.us.board.count == 7:
#            if self.us.board.count == len(self.us.board.ships)
            if self.user.board.defeat():
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()

