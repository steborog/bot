from aiogram.types import BotCommand

start_key: str = "start"
search_key: str = "search"
history_key: str = "history"

commands = {
    start_key: BotCommand(command=start_key, description="Увійти або зареєструватися"),
    search_key: BotCommand(command=search_key, description="Пошук даних за номером"),
    history_key: BotCommand(command=history_key, description="Переглянути історію пошуку")
}
