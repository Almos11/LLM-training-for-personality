from telethon.sync import TelegramClient
from googletrans import Translator
import json

PHONE_NUMBER = '$$$'
TELEGRAM_APP_ID = '$$$'
TELEGRAM_APP_HASH = '$$$'

def save_to_json(file_to_save, file_name: str) -> None:
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(file_to_save, f, ensure_ascii=False)

def get_dialogs(limit = 100):
    """Get all dialogs from the Telegram."""
    dialogs = client.iter_dialogs(limit=limit)
    dialogs = [dialog for dialog in dialogs if dialog.is_user and not dialog.entity.bot and dialog.title != 'Telegram' and dialog.title != 'Александр Мосин']
    return dialogs

def parse_messages(dialog, limit = 10):
    """Get all messages from the dialog."""
    all_messages_list = []
    count = 0
    for message in client.iter_messages(dialog):
        if isinstance(message.message, str):
            dict_message = {
                    "date": message.date.isoformat(),
                    "message": message.message,
                    "out": message.out,
                }
            all_messages_list.append(dict_message)
            count += 1
    return all_messages_list

with TelegramClient(PHONE_NUMBER, TELEGRAM_APP_ID, TELEGRAM_APP_HASH) as client:
    dialogs = get_dialogs()
    for dialog in dialogs:
        print(dialog.title)
        all_messages_list = parse_messages(dialog)
        save_to_json(all_messages_list, f"data/{dialog.id}.json")


    
