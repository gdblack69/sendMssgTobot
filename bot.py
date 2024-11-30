from telethon import TelegramClient, events
import config

# Initialize the source client
source_client = TelegramClient(config.SOURCE_SESSION_FILE, config.SOURCE_API_ID, config.SOURCE_API_HASH)

# Event handler for new messages
@source_client.on(events.NewMessage())
async def handle_message(event):
    print("Received message:", event.text)
    # Your bot's logic for handling the message goes here
    # For example, you might forward the message, extract information, etc.

# Main function to start the bot client
async def main():
    await source_client.start()  # Start the client
    print("Bot is running...")
    await source_client.run_until_disconnected()  # Run the bot until disconnected
