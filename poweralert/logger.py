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

    def command_executed(self, content, user_id, server_id, server_name):
        logging.info(f"Command executed: {content} - {user_id}. In {server_name} ({server_id})")
    
    def cooldown(self, content, user_id, server_id, server_name):
        logging.info(f"Cooldown: {content} - {user_id}. In {server_name} ({server_id})")
    
    def arguments(self, content, user_id, server_id, server_name):
        logging.info(f"Invalid Args: {content} - {user_id}. In {server_name} ({server_id})")
