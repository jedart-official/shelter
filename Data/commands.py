from aiogram.types import BotCommand


async def set_group_commands() -> list[BotCommand]:
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
