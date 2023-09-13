from aiogram.types import BotCommand


async def set_group_commands():
    commands = [
        BotCommand(
            command='shelter',
            description='Начать игру в бункер'
        ),
        BotCommand(
            command='end',
            description="Закрыть сессию текущего бункера (если она есть)"
        )
    ]
    return commands


async def set_private_commands():
    commands = [
        BotCommand(
            command='start',
            description='Регистрация у бота'
        ),
        BotCommand(
            command='rules',
            description="Узнать правила игры"
        )
    ]
    return commands
