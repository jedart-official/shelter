from Database.main import session_db, MessageDB


async def add_message_to_db(chat_id: int, message_id: int, session_id: int):
    session_db.add(MessageDB(chat_id=chat_id, message_id=message_id, session_id=session_id))
    session_db.commit()
