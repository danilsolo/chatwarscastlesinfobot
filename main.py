#coding:utf-8
import telebot
import logging
import datetime
import sqlite3

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)-3s]# %(levelname)-5s [%(asctime)s] %(message)s'
                    , level = logging.INFO)

# class a:
#     pass
#
# info = a()
#
# bots = dict()
# bots['infobotred']
# bots['infobotmint']
# bots['infobotblack']
# bots['infobotwhite']
# bots['infobotblue']
# bots['infobottwilight']
# bots['infobotyellow']
#
# bots = (infobotred, infobotmint, infobotblack, infobotwhite, infobotblue, infobottwilight, infobotyellow)

def niceprint(string):
    tabindex = 0
    out = ''
    for i in string:
        if i == ',':
            out += i
            out += '\n'
            out += '\t' * tabindex
            continue
        if i == '{':
            tabindex += 1
        if i == '}':
            tabindex -= 1
            out += '\n'
        out += i
    return out



bot = telebot.TeleBot('454423390:AAEU3fgrrqTYPquwzilge9AfP6Dd47X-5rQ')

castles = []
allcastles = ['🇻🇦', '🇬🇵', '🇨🇾', '🇮🇲', '🇪🇺', '🇲🇴', '🇰🇮']
out = ''

@bot.message_handler(func=lambda message: message.text and message.chat.type == 'private', content_types=['text'])
def getinfo(message):
    global castles
    global out
    logging.debug(niceprint(str(message)))
    logging.debug(str(message.from_user.username) + ': ' + message.text)

    if datetime.datetime.fromtimestamp(message.date) < datetime.datetime.now()-datetime.timedelta(seconds=20):
        logging.info('Cтарое сообщение')
        return

    if '💬Чат замка: ссылка' in message.text and message.forward_from.id == 265204902:
        logging.info(str(message.from_user.username) + ' прислал сообщение о замке' )


        # bot.send_message('@chatwarscastleinfo', message.text[0:130])
        logging.debug(message.text[:2])
        castle = message.text[:2]



        if castle in castles:
            bot.send_message(message.chat.id, 'Твой уже есть давай еще замков остались:' + str(set(allcastles)-set(castles)))
        else:
            castles.append(castle)

            castleinfo = message.text.splitlines()
            castlename = castleinfo[0][:2]
            castletime = castleinfo[1][:-2]
            castleweather = castleinfo[2][7:]
            castleres = castleinfo[castleinfo.index('Казна замка:') + 1]

            out += castlename + castletime + castleweather + castleres + '\n'

            logging.debug(out)

            bot.send_message(message.chat.id, 'Давай еще замков остались:' + str(set(allcastles) - set(castles)))

        if len(set(allcastles) - set(castles)) == 0:
            bot.send_message('@chatwarscastleinfo', out)
            out = ''
            castles = []




if __name__ == '__main__':
    bot.polling(none_stop=True)
