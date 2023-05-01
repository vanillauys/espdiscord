import logging


class logger:
    def __init__(self):
        logging.basicConfig(
            filename='bot.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def on_ready(self, bot_name, bot_id):
        logging.info(f"Logged in as {bot_name} (ID: {bot_id})")

    def command_executed(self, content, user_id):
        logging.info(f"Command executed: {content} - {user_id}")
