import requests
from bs4 import BeautifulSoup
import pyshorteners
import os

try:
    import colorama
    from termcolor import colored
except ImportError:
    os.system('pip install colorama termcolor')
    import colorama
    from termcolor import colored

def install_dependencies():
    try:
        import colorama
        from termcolor import colored
    except ImportError:
        os.system('pip install colorama termcolor')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_phone_details(phone_number):
    # Construct the URL with the phone number
    url = f'https://calltracer.in/{phone_number}'
    
    # Send a request to the website
    response = requests.get(url)
    
    try:
        # Use BeautifulSoup to parse the HTML response
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the desired details from the webpage
        details = {}
        for row in soup.find_all('div', class_='row'):
            label = row.find('div', class_='col-md-3').text.strip()
            value = row.find('div', class_='col-md-9').text.strip()
            details[label] = value
        
        return details
    except Exception as e:
        return f"Unable to fetch details. Error: {e}"

# Install dependencies if not installed
install_dependencies()

# Now, input the victim's phone number
victim_number = input(colored("Enter the phone number OF target: ", 'cyan'))

# Get victim details
victim_details = get_phone_details(victim_number)

# Construct the calltracer.in link
calltracer_link = f'https://calltracer.in/{victim_number}'

# Shorten the link
s = pyshorteners.Shortener()
shortened_link = s.tinyurl.short(calltracer_link)

# Print the shortened link
print(colored(f"Finding victim's phone number {victim_number}: details", 'yellow'))

# Save snapshot image
snapshot_url = f'https://api.apiflash.com/v1/urltoimage?access_key=97af63da550b487ba8bbf1b04402dd8f&url={shortened_link}'
snapshot_response = requests.get(snapshot_url)

# Get the documents folder path
documents_folder = os.path.join(os.path.expanduser('~'), 'Documents')

# Create the 'cutehack' folder in the documents folder if it doesn't exist
folder_path = os.path.join(documents_folder, 'cutehack')
os.makedirs(folder_path, exist_ok=True)

# Save the image in the folder
image_path = os.path.join(folder_path, f'snapshot_{victim_number}.png')
with open(image_path, 'wb') as image_file:
    image_file.write(snapshot_response.content)

print(colored("GOT THE NUMBER DETAILS SUCCESSFULLY", 'green'))

# Send snapshot and shortened link to Telegram bot
bot_token = "6466748827:AAHePYdTpc-ViDkkiPvAeGammV7Q-XHyit8"
bot_username = "@number_imformation_bot"
user_id = input(colored("Enter your Telegram user ID: ", 'cyan'))

telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
telegram_params = {
    "chat_id": user_id,
    "text": colored(f" ¥victims details¥\n\n Click below link for victim's phone number details\n\n *number* ={victim_number}:\n\n *details*= {shortened_link}\n\n\n\nThis Tool Was Made By @krishna12120\n\nJoin our channel for more tools\nhttps://t.me/+MAlg7F1xCSE1NmE1", 'magenta')
}

telegram_response = requests.post(telegram_url, params=telegram_params)

if telegram_response.ok:
    print(colored("Details sent to Telegram bot successfully!", 'cyan'))
else:
    print(colored("Failed to send Details to Telegram bot.", 'red'))

# Clear the terminal after execution
clear_terminal()