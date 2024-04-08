from aiogram.types import Message

from Keyboard.MainKeyboard import MainKeyboard
from Commands.ICommand import ICommand
from config import styles_data


class HelloCommand(ICommand):
    # TODO: Поменять имя бота
    text = (
        '🎶 Привет! Я твой Музыкальный Мастер Бот 🎵. Я здесь, чтобы превратить твои идеи в музыку. Вот как я '
        'могу тебе помочь:\n\n'
        '1️⃣ Текст: Дай мне начало, и я сочиню для тебя песню.\n'
        '2️⃣ Аудио: Позволь мне озвучить текст песни, создав уникальное аудиопроизведение.\n'
        '3️⃣ Текст + Аудио: Хочешь и то, и другое? Без проблем! Получи и текст, и аудио.\n\n'
        '👇 Просто выбери один из вариантов ниже, а затем отправь мне начальные строки твоей будущей хитовой '
        'песни. Давай создадим что-то особенное вместе!'
    )

    async def execute(self, message: Message) -> None:
        keyboard = MainKeyboard(selected_type=styles_data[0]['callback_data']).get_keyboard()
        await message.answer(
            text=self.text,
            reply_markup=keyboard,
            parse_mode='html')
