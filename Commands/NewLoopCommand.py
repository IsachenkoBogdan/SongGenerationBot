from aiogram.types import Message

from Commands.ICommand import ICommand
from Keyboard.MainKeyboard import MainKeyboard


class NewLoopCommand(ICommand):
    # TODO: Доработать текст
    audio_mode_text = {
        True: '🔊 <b>Режим с аудио включён!</b> Ты получишь не только текст, но и уникальное аудиопроизведение.',
        False: '📝 <b>Ты выбрал получение только текста.</b> Теперь я создам для тебя текст песни без аудио.'
    }

    text = (
        '🎉 <b>Приступим к созданию твоего хита?</b> Я здесь, чтобы помочь тебе воплотить музыкальные мечты! '
        'По умолчанию каждая твоя идея превратится не только в текст, но и в уникальное аудиопроизведение. '
        'Хочешь изменить настройки? Просто нажми на кнопку!\n\n'
        '✍️ <b>Отправь мне начальные строки</b> — и я превращу их в полноценный трек. Вдохновение уже в пути!\n\n'
        '{audio}\n\n'
        '👇 <b>Давай создадим что-то незабываемое вместе!</b>')

    def __init__(self, selected_type, edit_message_flag=False, audio_mode=True):
        self.selected_type = selected_type
        self.edit_message_flag = edit_message_flag
        self.audio_mode = audio_mode

    async def execute(self, message: Message) -> None:
        keyboard = MainKeyboard(self.selected_type, self.audio_mode).get_keyboard()
        text = self.text.format(audio=self.audio_mode_text[self.audio_mode])

        if self.edit_message_flag:
            await message.edit_text(text=text, reply_markup=keyboard, parse_mode='html')
            return

        await message.answer(text=text, reply_markup=keyboard, parse_mode='html')
