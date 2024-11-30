import importlib.util
import subprocess
import sys
import httpx  # تم إضافة httpx
import json
import random
from time import sleep
from colorama import init, Fore, Style
from rich.console import Console
from rich.progress import Spinner
import time
import os
import pyfiglet
from datetime import datetime

libraries = ["httpx", "requests", "colorama", "rich", "pyfiglet"]  # إضافة httpx إلى قائمة المكتبات

# إعداد Rich و Colorama
console = Console()
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_library_installed(library_name):
    """تحقق إذا كانت المكتبة مثبتة."""
    return importlib.util.find_spec(library_name) is not None

def install_libraries():
    for library in libraries:
        if is_library_installed(library):
            print(f"✅ {library} is already installed.")
            clear_screen()
        else:
            try:
                print(f"🔄 Installing {library}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", library])
                print(f"✅ {library} installed successfully!")
                clear_screen()
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {library}. Error: {e}")

install_libraries()


def get_user_agent():
    return "Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36 Telegram-Android/11.2.2 (Xiaomi M1908C3JGG; Android 12; SDK 31; AVERAGE)"

# دالة لإنشاء شعار مميز
def create_gradient_banner(text):
    banner = pyfiglet.figlet_format(text, font='slant').splitlines()
    colors = [Fore.GREEN + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.RED + Style.BRIGHT]
    total_lines = len(banner)
    section_size = total_lines // len(colors)
    for i, line in enumerate(banner):
        if i < section_size:
            print(colors[0] + line)
        elif i < section_size * 2:
            print(colors[1] + line)
        else:
            print(colors[2] + line)

# دالة لطباعة معلومات حول القنوات الاجتماعية
def print_info_box(social_media_usernames):
    colors = [Fore.CYAN, Fore.MAGENTA, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTWHITE_EX]
    box_width = max(len(social) + len(username) for social, username in social_media_usernames) + 4
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')
    for i, (social, username) in enumerate(social_media_usernames):
        color = colors[i % len(colors)]
        print(color + f'| {social}: {username} |')
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')

# دالة الانتظار مع تأخير عشوائي
def wait_with_random_delay(message: str = "Processing your request..."):
    delay = random.randint(10, 19)
    with console.status(f"[bold cyan]{message}", spinner="dots") as status:
        for i in range(delay):
            sleep(1)
            status.update(f"[bold green]{message} ({i+1}/{delay} seconds)")
    console.print(f"[bold magenta]Done! Total wait time: {delay} seconds.")

# دالة لقراءة بيانات المستخدم من ملف

# قراءة بيانات المستخدم من ملف
def get_user_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"{Fore.RED}Error reading the file: {str(e)}")
        return None

# استرجاع التوكين مع إعادة المحاولة
def extract_token(max_retries=5, retry_delay=5):
    user_info = get_user_from_file('data.txt')
    if not user_info:
        return f"{Fore.RED}Error: Could not load user information from data.txt"

    url = "https://api.pineye.io/api/v2/Login"
    payload = {"userinfo": user_info}
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'Content-Type': "application/json",
    }

    retries = 0
    while retries < max_retries:
        try:
            with httpx.Client() as client:
                response = client.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    response_data = response.json()
                    token = response_data.get('data', {}).get('token')
                    if token:
                        print(f"{Fore.GREEN}Token retrieved successfully: {token}")
                        return token
                    else:
                        print(f"{Fore.RED}Token not found in the response. Retrying...")
                else:
                    print(f"{Fore.RED}Request failed with status code: {response.status_code}. Retrying...")
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {str(e)}. Retrying...")

        retries += 1
        sleep(retry_delay)  # الانتظار قبل إعادة المحاولة

    return f"{Fore.RED}Failed to retrieve token after {max_retries} attempts."

# وظيفة لإرجاع User-Agent (كمثال)


# جلب التاريخ والوقت الحالي
def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# استدعاء Tap API
def perform_tap_request(token):
    count = fetch_booster_data(token)
    if not token:
        print(f"{Fore.RED}Error: Token is required for this request.")
        return

    url = "https://api.pineye.io/api/v1/Tap"
    params = {'count': count}
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'authorization': f"Bearer {token}",
        'Origin': "https://launch.gominers.xyz",
        'Sec-Fetch-Site': "cross-site",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://launch.gominers.xyz/",
        'Accept-Language': "en-US,en;q=0.9",
        'Date-Time': get_current_datetime()
    }

    try:
        print(f"{Fore.BLUE}[{get_current_datetime()}] Sending Tap request with count: {count}")
        with httpx.Client() as client:  # استخدام httpx بدلاً من requests
            response = client.get(url, params=params, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                balance = response_data.get('data', {}).get('balance', None)
                energy = response_data.get('data', {}).get('energy', {})
                current_energy = energy.get('currentEnergy', None)
                max_energy = energy.get('maxEnergy', None)
                print(f"[{get_current_datetime()}]"+f"{Fore.CYAN} You win Coins: {count}")
                print(f"[{get_current_datetime()}]"+f"{Fore.CYAN} Balance: {balance}")
                print(f"[{get_current_datetime()}]"+f"{Fore.CYAN} Current Energy: {current_energy}")
                print(f"[{get_current_datetime()}]"+f"{Fore.CYAN} Max Energy: {max_energy}")
            if balance == 200000:
            	buy_booster(token)
            	print(f"[{get_current_datetime()}]"+f"{Fore.CYAN} Updat Now Boster: ")

            if current_energy == max_energy:
                print(get_current_datetime()+f"{Fore.RED}Max Energy reached. Waiting for 30 minutes...")
                time.sleep(1800)
                print(f"{Fore.GREEN}Energy has been replenished!")
    except httpx.HTTPStatusError as e:
        print(f"{Fore.RED}HTTP Status Error: {str(e)}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}")



def fetch_card_ids(token):
    url = "https://api.pineye.io/api/v1/PranaGame/Marketplace"

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'x-chat-id': "707813877",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://app.pineye.io",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://app.pineye.io/",
        'accept-language': "en-US,en;q=0.9"
    }

    while True:  # إعادة المحاولة حتى ننجح
        try:
            with httpx.Client() as client:
                response = client.get(url, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                     # عرض الرد بالكامل

                    # استخراج البيانات من "categories"
                    data_section = data.get('data', {})
                    categories = data_section.get('categories', [])

                    # قائمة لتخزين الأيدي المستخرجة
                    extracted_ids = []

                    if not categories:
                        print(f"{Fore.RED}No categories found in response.")
                        return []

                    # استخراج الأيدي الخاصة بكل قسم ومجموعة داخل الأقسام
                    for category in categories:
                        collections = category.get('collections', [])
                        for collection in collections:
                            cards = collection.get('cards', [])
                            for card in cards:
                                # فحص وجود 'title' في البطاقة
                                if 'title' in card:
                                    card_id = card.get('id')
                                    extracted_ids.append(card_id)
                                    print(f"{Fore.GREEN}Extracted cardId: {card_id} with title: {card.get('title')}")

                    if extracted_ids:
                        print(f"{Fore.GREEN}Extracted cardIds:")

                        # حفظ الأيدي في ملف profit.txt
                        with open("profit.txt", "w") as file:
                            for card_id in extracted_ids:
                                file.write(f"{card_id}\n")  # كتابة كل id في سطر جديد
                        print(f"{Fore.GREEN}Card IDs have been saved to profit.txt.")
                    else:
                        print(f"{Fore.RED}No cards with title found.")

                    return extracted_ids  # الخروج بعد النجاح

                else:
                    print(f"{Fore.RED}Error: {response.status_code} - {response.text}")
                    print(f"{Fore.YELLOW}Retrying...")  # رسالة تفيد بإعادة المحاولة
                    time.sleep(5)  # تأخير 5 ثوانٍ قبل المحاولة التالية

        except httpx.RequestError as exc:
            print(f"{Fore.RED}An error occurred while making the request: {exc}")
            print(f"{Fore.YELLOW}Retrying...")  # رسالة تفيد بإعادة المحاولة
            time.sleep(5)  # تأخير 5 ثوانٍ قبل المحاولة التالية

# استدعاء الدالة مع إدخال التوكين


# استدعاء الدالة مع إدخال التوكين


def fetch_booster_data(token):
    url = "https://api.pineye.io/api/v1/Booster"
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json",
        'authorization': f"Bearer {token}",
        'Origin': "https://launch.gominers.xyz",
        'Sec-Fetch-Site': "cross-site",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://launch.gominers.xyz/",
        'Accept-Language': "en-US,en;q=0.9",
        'Date-Time': get_current_datetime()
    }

    try:
        print(f"{Fore.BLUE}[{get_current_datetime()}] Sending Booster request...")
        # استخدام httpx بدلاً من requests
        with httpx.Client() as client:
            response = client.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                # إذا كانت البيانات تحتوي على عنصر "Multitap"
                for item in data.get('data', []):
                    if item.get('title') == 'Multitap':
                        current_level = item.get('currentLevel', 0)
                        return current_level + 1
                print(f"{Fore.YELLOW}No 'Multitap' found in the response data.")
            else:
                print(f"{Fore.RED}Request failed with status code {response.status_code}")
    except httpx.RequestError as e:
        print(f"{Fore.RED}A request error occurred: {str(e)}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}")

    # في حالة فشل أي شيء، نرجع 1 بشكل افتراضي
    return 1
    
def fetch_and_save_ids(token, max_retries=5, retry_delay=5):
    url = "https://api.pineye.io/api/v1/Social"
    
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json, text/plain, */*",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'x-chat-id': "707813877",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://app.pineye.io",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://app.pineye.io/",
        'accept-language': "en-US,en;q=0.9"
    }
    
    retries = 0
    while retries < max_retries:
        try:
            with httpx.Client() as client:
                response = client.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    ids = extract_ids(data)
                    
                    with open("quest.txt", "w") as file:
                        for _id in ids:
                            file.write(f"{_id}\n")
                    
                    print(f"{Fore.GREEN}Extracted {len(ids)} IDs and saved to quest.txt.")
                    return  # نجاح، إنهاء الوظيفة
                
                else:
                    print(f"{Fore.YELLOW}Error: {response.status_code} - {response.text}")
                    retries += 1
                    print(f"{Fore.YELLOW}Retrying... Attempt {retries}/{max_retries}")
                    time.sleep(retry_delay)
                    
        except httpx.RequestError as exc:
            print(f"{Fore.RED}An error occurred while making the request: {exc}")
            retries += 1
            print(f"{Fore.YELLOW}Retrying... Attempt {retries}/{max_retries}")
            time.sleep(retry_delay)
    
    print(f"{Fore.RED}Failed to fetch data after {max_retries} retries.")

# استخراج الـ IDs من البيانات المستلمة
def extract_ids(data):
    ids = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "id":
                ids.append(value)
            elif isinstance(value, (dict, list)):
                ids.extend(extract_ids(value))
    elif isinstance(data, list):
        for item in data:
            ids.extend(extract_ids(item))
    return ids

def claim_social_follower(token, max_retries=5, retry_delay=5):
    url = "https://api.pineye.io/api/v1/SocialFollower/claim"

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json, text/plain, */*",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'x-chat-id': "707813877",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://app.pineye.io",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://app.pineye.io/",
        'accept-language': "en-US,en;q=0.9"
    }

    try:
        # قراءة القيم من الملف
        with open("quest.txt", "r") as file:
            social_ids = [line.strip() for line in file if line.strip()]
        
        if not social_ids:
            print(f"{Fore.RED}Error: The file quest.txt is empty.")
            return
        
        # قراءة المؤشر الحالي (آخر قيمة تم معالجتها)
        if os.path.exists("current_index.txt"):
            with open("current_index.txt", "r") as index_file:
                current_index = int(index_file.read().strip() or 0)
        else:
            current_index = 0

        # بدء العملية من المؤشر الحالي
        with httpx.Client() as client:
            for i in range(current_index, len(social_ids)):
                social_id = social_ids[i]
                params = {'socialId': social_id}
                retries = 0
                success = False

                while retries < max_retries and not success:
                    try:
                        response = client.post(url, params=params, headers=headers)
                        if response.status_code == 200:
                            data = response.json()
                            print(f"{Fore.GREEN}Success for socialId {social_id}: {data}")
                            success = True
                        else:
                            print(f"{Fore.YELLOW}Error for socialId {social_id}: {response.status_code} - {response.text}")
                    except httpx.RequestError as exc:
                        print(f"{Fore.RED}Request error for socialId {social_id}: {exc}")
                    
                    if not success:
                        retries += 1
                        print(f"{Fore.BLUE}Retrying... Attempt {retries}/{max_retries}")
                        time.sleep(retry_delay)
                
                if not success:
                    print(f"{Fore.RED}Failed to process socialId {social_id} after {max_retries} retries.")
                
                # تحديث المؤشر بعد كل محاولة
                with open("current_index.txt", "w") as index_file:
                    index_file.write(str(i + 1))
                
                # إضافة تأخير لمنع الحظر
                time.sleep(5)

            # إذا تمت معالجة جميع الـ IDs في الملف، يتم إنهاء الدالة
            if i == len(social_ids) - 1:
                print(f"{Fore.GREEN}All social IDs have been processed. Exiting the function.")
                return

    except FileNotFoundError:
        print(f"{Fore.RED}Error: The file quest.txt was not found.")
    except Exception as exc:
        print(f"{Fore.RED}An unexpected error occurred: {exc}")


# تعريف الدالة لشراء البوستر باستخدام httpx
def buy_booster(token,  max_retries=5, retry_delay=5):
    url = "https://api.pineye.io/api/v2/profile/BuyBooster"
    id = random.randint(1,2)
    params = {
        'boosterId': id
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'x-chat-id': "707813877",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://app.pineye.io",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://app.pineye.io/",
        'accept-language': "en-US,en;q=0.9"
    }

    retries = 0
    while retries < max_retries:
        try:
            with httpx.Client() as client:
                response = client.post(url, params=params, headers=headers)
                
                if response.status_code == 200:
                    print(f"{Fore.GREEN}Booster purchased successfully! Response: {response.json()}")
                    return response.json()  # نجاح، إنهاء الوظيفة مع إرجاع الرد
                else:
                    print(f"{Fore.YELLOW}Error: {response.status_code} - {response.text}")
                    retries += 1
                    print(f"{Fore.YELLOW}Retrying... Attempt {retries}/{max_retries}")
                    time.sleep(retry_delay)
        except httpx.RequestError as exc:
            print(f"{Fore.RED}An error occurred while making the request: {exc}")
            retries += 1
            print(f"{Fore.YELLOW}Retrying... Attempt {retries}/{max_retries}")
            time.sleep(retry_delay)
    
    print(f"{Fore.RED}Failed to purchase booster after {max_retries} retries.")
    return None  # فشل العملية بعد استنفاد المحاولات

# استدعاء الدالة



def main():
    create_gradient_banner("Bot Pin Eye")  # عرض الشعار
    print_info_box([("Telegram", "https://t.me/YOU742"), ("Coder", "@Ke4oo")])  # معلومات وسائل التواصل
    print(Fore.GREEN + "Welcome to the Script!")
    
    token = extract_token()  # استخراج التوكين
    if token and "Error" not in token:
        #fetch_card_ids(token)
        fetch_and_save_ids(token)    
        wait_with_random_delay()
        claim_social_follower(token)
          # الانتظار مع تأخير عشوائي
        while True:
        	perform_tap_request(token) 
        	
        	wait_with_random_delay()
         # تنفيذ طلب Tap
    else:
        print(token)

if __name__ == "__main__":
    
    main()