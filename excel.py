import xlsxwriter
from parser import array
import telebot

bot = telebot.TeleBot('6013552535:AAFfMCy61PmnBomip3U82DoLRkp9FKsMvas')
@bot.message_handler(commands=['н'])

def hello(message):
    bot.send_message(message.chat.id,'Ворк....')

    def writer(parametr):
        book = xlsxwriter.Workbook(
            r"C:\mylife\python\PycharmProjects\pythonProject1\parser_ebay-kleinanzeigen\excel\data.xlsx")
        page = book.add_worksheet("Tovar")

        row = 0
        column = 0
        #page.write('A1', 'Hello..')
        page.set_column("A:A", 10)
        page.set_column("B:B", 20)
        page.set_column("C:C", 120)
        page.set_column("D:D", 80)

        for item in parametr():
            page.write(row, column, item[0])
            page.write(row, column + 1, item[1])
            page.write(row, column + 2, item[2])
            page.write(row, column + 3, item[3])
            row += 1

        doc = open('C:\mylife\python\PycharmProjects\pythonProject1\parser_ebay-kleinanzeigen\excel\data.xlsx', 'rb')
        bot.send_document(message.chat.id, doc)
        bot.send_message(message.chat.id, 'Готово')

        book.close()

    writer(array)
bot.polling()
