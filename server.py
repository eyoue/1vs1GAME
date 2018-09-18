import tornado.websocket
import tornado.web
import tornado.ioloop
import json

class EchoWebSocket(tornado.websocket.WebSocketHandler):

    count = 0 # Такой себе id (Можно и лучше)
    session_id = 0 # Это, например сессии
    users = json.loads('{"id":[], "session_id":[], "obj":[], "hod":[]}') # Тут храню все о пользователях

    # Проверки для запуска соединения
    def check_origin(self, origin):
        return True

    # Открываем соединение
    def open(self):
        # Заполняем всё что можем: ид, ход, сессию
        EchoWebSocket.count = EchoWebSocket.count + 1
        EchoWebSocket.users["id"].append(EchoWebSocket.count)
        EchoWebSocket.users["obj"].append(self)
        EchoWebSocket.users["hod"].append(None)

        # Создаем пары юзеров
        if ((len(EchoWebSocket.users["obj"]) != 0)):
            if (len(EchoWebSocket.users["obj"]) % 2 == 0):
                EchoWebSocket.users["session_id"].append(EchoWebSocket.session_id)
                EchoWebSocket.users["obj"][EchoWebSocket.users["obj"].index(self)-1].write_message('start_1')
                self.write_message('start_2')
                EchoWebSocket.session_id = EchoWebSocket.session_id + 1
            else:
                EchoWebSocket.users["session_id"].append(EchoWebSocket.session_id)

        print(EchoWebSocket.users)

    # Если пришло сообщение
    def on_message(self, message):
        if (message == 'start'):
            self.write_message(u"You id: " + str(EchoWebSocket.users["id"][EchoWebSocket.users["obj"].index(self)]))

        # Сделал строку хода как: Ha1.. Hd4
        # H - ход
        # a - attac
        # d - def
        # 1,2,3,4 - места на игроке

        # Работаем только с парой юзеров.
        # Там внизу что-то очень страшное, но если разобраться: Если это юзеры
        # из одной сессии, проверяем кто и как походил. Выдаем результат.
        if (message[0] == 'H'):
            i = EchoWebSocket.users["obj"].index(self)
            EchoWebSocket.users["hod"][i] = message[1]+message[2]

            if ((EchoWebSocket.users["session_id"][i] == EchoWebSocket.users["session_id"][i - 1])):
                if ((EchoWebSocket.users["hod"][i] != None) & (EchoWebSocket.users["hod"][i - 1] != None)):
                    if (('a' in EchoWebSocket.users["hod"][i-1]) & ('a' in EchoWebSocket.users["hod"][i])):
                        EchoWebSocket.users["obj"][i].write_message('hitALL')
                        EchoWebSocket.users["obj"][i-1].write_message('hitALL')

                    elif (('d' in EchoWebSocket.users["hod"][i-1]) & ('d' in EchoWebSocket.users["hod"][i])):
                        EchoWebSocket.users["obj"][i].write_message('NOhit')
                        EchoWebSocket.users["obj"][i-1].write_message('NOhit')

                    elif (('a' in EchoWebSocket.users["hod"][i]) & ('d' in EchoWebSocket.users["hod"][i-1])):
                        str1 = EchoWebSocket.users["hod"][i]
                        str2 = EchoWebSocket.users["hod"][i-1]
                        if (int(str1[-1]) != int(str2[-1])):
                            EchoWebSocket.users["obj"][i-1].write_message('hitYOU')
                            EchoWebSocket.users["obj"][i].write_message('hitOPONENT')
                        elif (int(str1[-1]) == int(str2[-1])):
                            EchoWebSocket.users["obj"][i - 1].write_message('NOhit')
                            EchoWebSocket.users["obj"][i].write_message('NOhit')

                    elif (('d' in EchoWebSocket.users["hod"][i]) & ('a' in EchoWebSocket.users["hod"][i-1])):
                        str1 = EchoWebSocket.users["hod"][i]
                        str2 = EchoWebSocket.users["hod"][i-1]
                        if (int(str1[-1]) != int(str2[-1])):
                            EchoWebSocket.users["obj"][i].write_message('hitYOU')
                            EchoWebSocket.users["obj"][i-1].write_message('hitOPONENT')
                        elif (int(str1[-1]) == int(str2[-1])):
                            EchoWebSocket.users["obj"][i - 1].write_message('NOhit')
                            EchoWebSocket.users["obj"][i].write_message('NOhit')
                    EchoWebSocket.users["hod"][i] = None
                    EchoWebSocket.users["hod"][i-1] = None


            elif ((EchoWebSocket.users["session_id"][i] == EchoWebSocket.users["session_id"][i + 1])):
                if ((EchoWebSocket.users["hod"][i] != None) & (EchoWebSocket.users["hod"][i + 1] != None)):
                    if (('a' in EchoWebSocket.users["hod"][i+1]) & ('a' in EchoWebSocket.users["hod"][i])):
                        EchoWebSocket.users["obj"][i].write_message('hitALL')
                        EchoWebSocket.users["obj"][i+1].write_message('hitALL')

                    elif (('d' in EchoWebSocket.users["hod"][i+1]) & ('d' in EchoWebSocket.users["hod"][i])):
                        EchoWebSocket.users["obj"][i].write_message('NOhit')
                        EchoWebSocket.users["obj"][i+1].write_message('NOhit')

                    elif (('a' in EchoWebSocket.users["hod"][i]) & ('d' in EchoWebSocket.users["hod"][i + 1])):
                        str1 = EchoWebSocket.users["hod"][i]
                        str2 = EchoWebSocket.users["hod"][i + 1]
                        if (int(str1[-1]) != int(str2[-1])):
                            EchoWebSocket.users["obj"][i + 1].write_message('hitYOU')
                            EchoWebSocket.users["obj"][i].write_message('hitOPONENT')
                        elif (int(str1[-1]) == int(str2[-1])):
                            EchoWebSocket.users["obj"][i + 1].write_message('NOhit')
                            EchoWebSocket.users["obj"][i].write_message('NOhit')

                    elif (('d' in EchoWebSocket.users["hod"][i]) & ('a' in EchoWebSocket.users["hod"][i + 1])):
                        str1 = EchoWebSocket.users["hod"][i]
                        str2 = EchoWebSocket.users["hod"][i + 1]
                        if (int(str1[-1]) != int(str2[-1])):
                            EchoWebSocket.users["obj"][i].write_message('hitYOU')
                            EchoWebSocket.users["obj"][i + 1].write_message('hitOPONENT')
                        elif (int(str1[-1]) == int(str2[-1])):
                            EchoWebSocket.users["obj"][i + 1].write_message('NOhit')
                            EchoWebSocket.users["obj"][i].write_message('NOhit')
                    EchoWebSocket.users["hod"][i] = None
                    EchoWebSocket.users["hod"][i + 1] = None

        # Закрываем сессию. Если один вышел, выкинуть и второго.
        if (message == 'close'):
            if (self in EchoWebSocket.users["obj"]):
                if (len(EchoWebSocket.users["obj"]) > 1):
                    i = EchoWebSocket.users["obj"].index(self)

                    if (EchoWebSocket.users["session_id"][i] == EchoWebSocket.users["session_id"][i - 1]):
                        EchoWebSocket.users["id"].remove(EchoWebSocket.users["id"][i])
                        EchoWebSocket.users["id"].remove(EchoWebSocket.users["id"][i - 1])

                        EchoWebSocket.users["session_id"].remove(EchoWebSocket.users["session_id"][i])
                        EchoWebSocket.users["session_id"].remove(EchoWebSocket.users["session_id"][i - 1])

                        EchoWebSocket.users["hod"].remove(EchoWebSocket.users["hod"][i])
                        EchoWebSocket.users["hod"].remove(EchoWebSocket.users["hod"][i - 1])

                        EchoWebSocket.users["obj"][i].write_message('close')
                        EchoWebSocket.users["obj"][i - 1].write_message('close')

                        EchoWebSocket.users["obj"].remove(EchoWebSocket.users["obj"][i])
                        EchoWebSocket.users["obj"].remove(EchoWebSocket.users["obj"][i - 1])

                    elif (EchoWebSocket.users["session_id"][i] == EchoWebSocket.users["session_id"][i + 1]):
                        EchoWebSocket.users["id"].remove(EchoWebSocket.users["id"][i])
                        EchoWebSocket.users["id"].remove(EchoWebSocket.users["id"][i + 1])

                        EchoWebSocket.users["session_id"].remove(EchoWebSocket.users["session_id"][i])
                        EchoWebSocket.users["session_id"].remove(EchoWebSocket.users["session_id"][i + 1])

                        EchoWebSocket.users["hod"].remove(EchoWebSocket.users["hod"][i])
                        EchoWebSocket.users["hod"].remove(EchoWebSocket.users["hod"][i + 1])

                        EchoWebSocket.users["obj"][i].write_message('close')
                        EchoWebSocket.users["obj"][i + 1].write_message('close')

                        EchoWebSocket.users["obj"].remove(EchoWebSocket.users["obj"][i])
                        EchoWebSocket.users["obj"].remove(EchoWebSocket.users["obj"][i + 1])

                elif (len(EchoWebSocket.users["obj"]) == 1):
                    i = EchoWebSocket.users["obj"].remove(self)
                    EchoWebSocket.users["id"].remove(EchoWebSocket.users["id"][i])
                    EchoWebSocket.users["session_id"].remove(EchoWebSocket.users["session_id"][i])
                    EchoWebSocket.users["hod"].remove(EchoWebSocket.users["hod"][i])
                    EchoWebSocket.users["obj"][i].write_message('close')
                    EchoWebSocket.users["obj"].remove(EchoWebSocket.users["obj"][i])
            print(EchoWebSocket.users)



if __name__=='__main__':
    app = tornado.web.Application([
        (r"/", EchoWebSocket)
    ])
    app.listen(8881)
    tornado.ioloop.IOLoop.instance().start()





















