from tkinter import *
from random import *

window = Tk()
window.title('Игра')
c = Canvas(window, width=640, height=640, bg='Navy')
c.pack()

wer3 = c.create_text(590, 10, text='0', font=('Arial', 10, 'bold'), fill='green')
wer = 0
store = 0

def delete_left_player():
    c.delete(player1)
    c.create_text(80, 7, text='Вс. самолет взорвался', font=('Arial', 9, 'bold'), fill='orange')

def store_plus():
    global store, wer3
    store+=1
    c.delete(wer3)
    wer3 = c.create_text(590, 10, text=store, font=('Arial', 10, 'bold'), fill='green')


def delete_right_player():
    c.delete(player2)
    c.create_text(80, 17, text='Вс. самолет взорвался', font=('Arial', 9, 'bold'), fill='orange')

def game_over():
    global wer, livemonitor
    if wer == 0:
        c.create_text(320, 320, text='GAME OVER', font=('Arial', 79, 'bold'), fill='red')
        wer4 = c.create_text(320, 440, text=f'Store: {store}', font=('Arial', 70, 'bold'), fill='yellow')
        livemonitor.config(text=f'Game Over, store: {store}')
        window.unbind('<Left>')
        window.unbind('<Right>')
        exit_btn = Button(window, text='Выход', command=window.destroy, font=('Arial', 14))
        exit_btn.pack()

        wer = 1

# переменная live
live = 100

wer2 = list()

# вычитание live
def live_minus():
    global live
    live-=1
    livemonitor.config(text=f'Lives: {live}')
    if live<=0:
        game_over()

def create_prise():
    global wer2
    prise_x = randint(20, 610)
    prise = c.create_oval(prise_x, 10, prise_x + 10, 20, fill="red")
    wer2.append(prise)

wer1 = 0


# Новая Функция движения врагов
def move_enemies():
    global wer1, wer2
    # для каждого врага из N
    for i in range(N):
        # берем номер врага c номером i из списка
        enemy = enemies[i]

        # и его скорости
        vx = x_speeds[i]
        vy = y_speeds[i]

        # получаем текущие координаты врага
        x1, y1 = c.coords(enemy)
        x2 = x1 + 40
        y2 = y1 + 40

        # получаем текущие координаты игрока
        i1, j1 = c.coords(player)
        i2 = i1 + 40
        j2 = j1 + 40

        if ((x1 < i1 < x2) and (y1 < j1 < y2)) or ((x1 < i2 < x2) and (y1 < j2 < y2)):
            if (x2 > i1 > x1) or (x1 < i2 < x2):
                vx *= -1
                live_minus()

            if (y2 > j1 > y1) or (y1 < j2 < y2):
                vy *= -1
                live_minus()

        if ((x1 < i1-44 < x2) and (y1 < j1+20 < y2)) or ((x1 < i2-44 < x2) and (y1 < j2+20 < y2)):
            delete_left_player()

        if ((x1 < i1+84 < x2) and (y1 < j1+20 < y2)) or ((x1 < i2+44 < x2) and (y1 < j2+20 < y2)):
            delete_right_player()

        # если враг на границе по x - развернуть скорость по x
        if x1 <= 0 or x2 >= 640:
            vx *= -1

        # аналогично по y
        if y1 <= 0 or y2 >= 640:
            vy *= -1

        # сохраняем скорости обратно в список
        x_speeds[i] = vx
        y_speeds[i] = vy

        # передвигаем врага
        c.move(enemy, vx, vy)

    wer1+=1

    if wer1 %200==0:
        create_prise()

    for i in range(len(wer2)):
        prise = wer2[i]

        a1, b1, a2, b2 = c.coords(prise)

        if ((i1 < a1 < i2) and (y1 < b1 < y2)) or ((i1 < a2 < i2) and (y1 < b2 < y2)):
            store_plus()


        c.move(prise, 0, 5)

    # повторяем через полсекунды
    if live>=0:
        c.after(20, move_enemies)





# Вправо
def right_move(event): c.move('borisy', 10, 0)

# Влево
def left_move(event): c.move('borisy', -10, 0)


# ДОБАВЛЯЕМ ЗВЁЗДНОЕ НЕБО
for h in range(100):
    i = randint(0, 640)
    k = randint(0, 640)
    r = randint(1, 3)
    x1 = float(i)
    y1 = float(k)
    x2 = float(i + r)
    y2 = float(k + r)
    c.create_oval(x1, y1, x2, y2, fill="Yellow")

# загружаем картинки – враг и игрок
enemy_image = PhotoImage(file='ememy.gif')
player_image = PhotoImage(file='player.gif')

# количество врагов
N = 4

# списки со скоростями
x_speeds = []
y_speeds = []

# список с врагами
enemies = []

# создаем N врагов
for i in range(N):
    # придумываем координаты
    x = randint(20, 610)
    y = randint(20, 610)

    # создаем врага
    enemy = c.create_image(x, y, image=enemy_image, anchor=NW)

    # придумываем скорость
    vx = randint(-15, 15)
    vy = randint(-15, 15)

    # добавляем врага в список
    enemies.append(enemy)

    # добавляем скорости в списки
    x_speeds.append(vx)
    y_speeds.append(vy)

# создаем интерфейс live
livemonitor = Label(window, text=f'Lives: {live}', font=('Verdana', 16, 'bold'))
livemonitor.pack()

player = c.create_image(300, 350, image=player_image, anchor=NW, tags='borisy')
player1 = c.create_image(255, 370, image=player_image, anchor=NW, tags='borisy')
player2 = c.create_image(345, 370, image=player_image, anchor=NW, tags='borisy')

# при нажатии клавиш управления курсором вызываем соответствующую функцию
window.bind('<Left>', left_move)
window.bind('<Right>', right_move)

# спустя 2 секунды (2000 мс) после запуска выполнить move_enemy
c.after(2000, move_enemies)

window.mainloop()
