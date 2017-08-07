#!/usr/bin/python3
# -*- coding: utf-8 -*-

# file:    server.py
# created: Mon Aug  7 21:56:19 2017
# author:  Ivan Bondarev


from socket import *

def user_command(command):
    if command == 'exit':
        pass

def from_users(data):
    global CLIADR, CLIDATA, CLISAVE
    data = pickle.loads(data)
    if len(data) <= 1:
        print(data)
        return 0
    else:
        command = data[0]
        data = data[1]
        name = data[1]



def main():
    HOST = ""           # пусто - указывает на то что в blind() может исп-ся люб адрес
    PORT = 21521        # порт
    BUFSIZ = 1024       # буфер
    ADDR = (HOST, PORT) # адрес

    SOCK = socket(AF_INET, SOCK_DGRAM)    # создание сокета UDP/IP
    SOCK.bind(ADDR)                       # Устанавливаем привязку адреса

    CLIADR = dict()    # Словарь пользователей
    CLIDATA = dict()   # Данные клиентов
    CLISAVE = dict() # Сохраняем данные на сервере

    '''загружаем сохраненные данные пользователей'''
    try:
        f = open('CLIDATA.pkl', 'rb')  # загрузка данных их файла
        CLISAVE = pickle.load(f)     # Словарь игроков
        print('the data is loaded')
    except FileNotFoundError:
        print("no data is uploaded")

    print('waiting for connection...')
    '''основной цикл'''
    done = True
    while done:
        data, addr = SOCK.recvfrom(BUFSIZ)    # ожидание сообщений
        data = pickle.loads(data)                   # распаковываем данные
        ''''''
        if data[0] == 'exit':       # выход игрока
            CLISAVE[data[1]] = CLIDATA[data[1]] # сохраняем координаты на выходе
            # очищаем словари
            del(CLIADR[data[1]])
            del(CLIDATA[data[1]])
            f = open('CLIDATA.pkl', 'wb')  # сохраняем на жд
            pickle.dump(CLISAVE, f)
            f.close()
            if not CLIADR: # если последний игрок вышел из игры
                print('server offline')
                break
                done = False # остановка сервера

        elif data[0] == 'coord':    # вход игрока, запрос сохраненных данных
            CLIADR[data[1]] = addr # добавляем в словарь пользователей
            try:                    # ищем сохранения
                CLIDATA[data[1]] = CLISAVE[data[1]]
            except KeyError:        # если нет, то присваиваем базовае хар-ки
                CLIDATA[data[1]] = data[2], data[3], data[4]

        else:  # обновляем данные клиента
            CLIDATA[data[1]] = data[2], data[3], data[4]   # обновляем данные

        data = pickle.dumps(CLIDATA)               # запаковываем словарь с данными клиентов
        for key in sorted(CLIADR):
            SOCK.sendto(data, CLIADR[key])   # посылаем данные всем клиентам

        print(CLIADR)

    SOCK.close()

if __name__ == "__main__":
    main()
