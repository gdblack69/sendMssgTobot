from keep_alive import keep_alive  # Correct import
from telethon import TelegramClient, events
import os
import asyncio
import traceback
import config  # Import the config.py file

# API credentials for source chat
SOURCE_API_ID = config.SOURCE_API_ID
SOURCE_API_HASH = config.SOURCE_API_HASH
SOURCE_CHAT_ID = config.SOURCE_CHAT_ID

# API credentials for destination account
DESTINATION_API_ID = config.DESTINATION_API_ID
DESTINATION_API_HASH = config.DESTINATION_API_HASH
DESTINATION_BOT_USERNAME = config.DESTINATION_BOT_USERNAME

# Paths for session files
SOURCE_SESSION_FILE = config.SOURCE_SESSION_FILE
DESTINATION_SESSION_FILE = config.DESTINATION_SESSION_FILE

# Ensure session files are present
if not os.path.exists(SOURCE_SESSION_FILE):
    print("Source session file not found. Creating a new session...")
if not os.path.exists(DESTINATION_SESSION_FILE):
    print("Destination session file not found. Creating a new session...")

# Initialize Telegram clients
source_client = TelegramClient(SOURCE_SESSION_FILE, SOURCE_API_ID, SOURCE_API_HASH)
destination_client = TelegramClient(DESTINATION_SESSION_FILE, DESTINATION_API_ID, DESTINATION_API_HASH)

# Function to handle disconnections and reconnections
async def handle_disconnection():
    while True:
        try:
            await source_client.run_until_disconnected()
        except Exception as e:
            print(f"Error: {e}. Reconnecting...")
            await asyncio.sleep(5)  # Wait before attempting to reconnect
            await source_client.start()  # Restart the client

# Event handler for messages in the source chat
@source_client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
async def forward_message(event):
    # Extract the original message
    source_id_message = event.raw_text

    # Custom message format with highlighted source message
    custom_message = f"""
"{source_id_message}"
 
 If the quoted text within double quotation mark is not a trading signal, respond with "Processing your question....". If it is a trading signal, extract the necessary information and fill out the form below. The symbol should be paired with USDT. Use the highest entry price. The stop loss price will be taken from inside the double quotation mark and if it is not given then calculate it as 0.5% below the entry price. Use the lowest take profit price given inside the double quoted message and if none is provided then calculate take profit price as 2% above the entry price.Provide only the completed form, no other text.[Remember inside the double quotation mark 'cmp'= current market price, 'sl'= stop loss, 'tp'=take profit]


Symbol:
Price:
Stop Loss:
Take Profit:
Take Profit:
"""

    # Send the formatted message to the bot
    async with destination_client:
        try:
            await destination_client.send_message(DESTINATION_BOT_USERNAME, custom_message)
            print("Custom message forwarded to destination bot.")
        except Exception as e:
            print(f"Error while forwarding the message: {e}")

# Main function to start both clients
async def main():
    print("Starting both clients...")
    # Start both clients
    await source_client.start()
    await destination_client.start()
    print("Bot is running... Waiting for messages...")
    await handle_disconnection()  # Handle reconnections

# Entry point - running within the existing event loop
if __name__ == "__main__":
    keep_alive()  # Keep the bot alive
    async def run_bot():
        while True:  # Loop to restart the script on error
            try:
                # Run the main function within the existing event loop
                await main()
            except Exception as e:
                print(f"Error occurred: {e}. Restarting the script...")
                await asyncio.sleep(5)  # Optional sleep to prevent rapid restarts

    # Start the event loop to run the bot
    asyncio.run(run_bot())
