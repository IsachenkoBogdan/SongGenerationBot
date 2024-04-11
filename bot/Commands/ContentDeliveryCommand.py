import re
from os import remove

from aiogram.types import Message, FSInputFile

from bot.Commands import ICommand
from bot.Content import TextContentGenerator, AudioContentGenerator
from bot.Utils import Utils


class ContentDeliveryCommand(ICommand):
    errors = {
        'TextGenerationFailed': 'Упс... В процессе генерации текста возникла проблемка. 🤖 Пожалуйста, '
                                'попробуй ещё разок!',
        'AudioGenerationFailed': 'О нет, кажется, что-то пошло не так с созданием аудио. 🎵 Давай попробуем ещё раз'
    }

    start_generation_message = ('🎨<b>Творческий процесс запущен!</b> Мы работаем над созданием твоего шедевра. '
                                'Это займёт немного времени, спасибо за терпение. 🕒')
    finish_generation_message = (
        '<b>Вот что у нас получилось!</b> 📝\n\n{generated_text}\n\n'
        '✍️ Если хочешь что-то изменить — всегда можно начать заново.'
    )

    def __init__(self, style_type: str, audio_mode: bool, initial_text: str):
        self.style_type = style_type
        self.audio_mode = audio_mode
        self.initial_text = initial_text

    async def handle_text_content(self, message: Message) -> str:
        generated_text = await TextContentGenerator(self.style_type, self.initial_text).generate_content(
            self.initial_text)

        if not generated_text:
            await message.edit_text(text=self.errors['TextGenerationFailed'], parse_mode='html')
            return ''

        await message.edit_text(text=self.finish_generation_message.format(generated_text=generated_text), parse_mode='html')
        return generated_text

    async def handle_audio_content(self, message: Message, generated_text: str) -> None:
        generated_text = Utils.replace_english_chars(generated_text, 'пупупу')
        generated_text = re.sub(r'<b>(.*?)</b>', r'\1', generated_text)

        if self.audio_mode:
            generated_audio_path = await AudioContentGenerator().generate_content(generated_text)
            if not generated_audio_path:
                await message.edit_text(text=self.errors['AudioGenerationFailed'], parse_mode='html')
                return

            audio_file = FSInputFile(path=generated_audio_path, filename='Music.wav')
            await message.bot.send_audio(message.chat.id, audio=audio_file)

            # После отправки файл больше не нужен, значит можно удалить
            remove(generated_audio_path)

    async def execute(self, message: Message) -> None:
        await message.edit_text(text=self.start_generation_message, parse_mode='html')

        generated_text = await self.handle_text_content(message)
        if not generated_text:
            return

        await self.handle_audio_content(message, generated_text)
