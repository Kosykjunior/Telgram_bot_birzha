import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def stock_price(bot, update, user_data):
    message = update.message.text.strip().upper()

    if message == "/stock":
        update.message.reply_text("Пожалуйста, введите символ акции.")
        return

    stock_symbol = message
    api_key = "HOMORV88P44AC7LY"
    request_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={api_key}"
    response = requests.get(request_url)
    if response.status_code == 200:
        stock_data = response.json()
        if "Global Quote" in stock_data:
            stock_price = stock_data["Global Quote"]["05. price"]
            update.message.reply_text(f"Текущая цена на {stock_symbol} = ${stock_price}.")
        else:
            update.message.reply_text(f"Данные не найдены для {stock_symbol}.")
    else:
        update.message.reply_text("Произошла ошибка при получении данных об акциях.")

def help_command(bot, update):
    update.message.reply_text("Чтобы узнать цену акции, просто введите «/stock», а затем символ акции.")

def main():
    bot_token = "6295456285:AAFC-ikRiQOS_dwci_x23KbOIKGFaOB3T-8"
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    help_handler = CommandHandler("help", help_command)
    dispatcher.add_handler(help_handler)

    stock_price_handler = MessageHandler(Filters.text, stock_price, pass_user_data=True)
    dispatcher.add_handler(stock_price_handler)

    updater.start_polling()

if __name__ == "__main__":
    main()