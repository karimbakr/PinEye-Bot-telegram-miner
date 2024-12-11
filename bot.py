import aiohttp
import asyncio
import json
from colorama import Fore, init , Style
from datetime import datetime
import os
import importlib.util 
import pyfiglet
import  subprocess
import sys
libraries = ["httpx", "requests", "colorama", "rich", "pyfiglet"]

# تهيئة colorama لدعم الألوان في الأنظمة المختلفة
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
def print_message(message, color):
    """طباعة رسالة مع تاريخ ولون محدد"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # تحديد اللون باستخدام colorama
    if color == "green":
        color_code = Fore.GREEN
    elif color == "blue":
        color_code = Fore.BLUE
    elif color == "magenta":
        color_code = Fore.MAGENTA
    elif color == "red":
        color_code = Fore.RED
    elif color == "cyan":
        color_code = Fore.CYAN
    else:
        color_code = Fore.WHITE  # اللون الافتراضي

    # طباعة الرسالة مع اللون المحدد
    print(f"{color_code}[{current_time}] {message}")

async def read_userinfo_from_file(filename):
    """قراءة قيمة userinfo من ملف خارجي"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            userinfo = file.read().strip()
            return userinfo
    except FileNotFoundError:
        print_message(f"Error: File '{filename}' not found.", "red")
        return None

async def send_request():
    url = "https://api2.pineye.io/api/v2/Login"
    
    # قراءة userinfo من الملف
    userinfo = await read_userinfo_from_file("data.txt")
    if not userinfo:
        return None

    payload = {
        "userinfo": userinfo
    }

    headers = {
        'User-Agent': get_user_agent(),
        'Accept': "application/json, text/plain, */*",
        'Content-Type': "application/json",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        'chatid': "707813877",
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://app.pineye.io",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://app.pineye.io/",
        'accept-language': "en-US,en;q=0.9"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            result = await response.json()

            # استخراج التوكن والبيانات الأخرى
            token = result.get("data", {}).get("token", "Token not found")
            balance = result.get("data", {}).get("profile", {}).get("balance", "Balance not found")
            level = result.get("data", {}).get("profile", {}).get("level", {}).get("no", "Level not found")

            # طباعة النتائج بشكل جمالي
            print_message(f"Welcome Sir: {token[:10]}", "green")
            print_message(f"Balance: {balance}", "blue")
            print_message(f"Level: {level}", "magenta")

            return token

async def send_DailyReward(token):
    url = "https://api2.pineye.io/api/v1/DailyReward/claim"

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

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 400:
                print_message("DailyReward: Today Is Done", "magenta")
            elif response.status == 200:
                	print_message("DailyReward: Successful ✅", "magenta")
                	
            else:
                print_message(f"Error: {response.status}, {await response.text()}", "red")


async def seend_clk(token):
    url = "https://api2.pineye.io/api/v1/Tap"
    co = ("1")
    params = {
        'count': f"{co}"
    }
    
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
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            response_json = await response.json()

            # استخراج maxEnergy و currentEnergy
            max_energy = response_json["data"]["energy"]["maxEnergy"]
            current_energy = response_json["data"]["energy"]["currentEnergy"]
            #count = response_json["data"]["appliedTapCount"]

            # طباعة القيم المستخرجة
            print_message(f"MaxEnergy: {max_energy}", "green")
            print_message(f"currentEnergy: {current_energy}", "green")
            energy_decrement = max_energy - current_energy
            if energy_decrement > 0:
                print_message(f"Total win: {energy_decrement}. You win this amount! For Now ", "blue")
            await asyncio.sleep(6)
            if current_energy <= 50:
            	print_message(f"currentEnergy: {current_energy} is Down script stop for a while ..", "green")
            	await asyncio.sleep(1800)
            	
            
async def fetch_quest(token):
    url = "https://api2.pineye.io/api/v1/Social"
    
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
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            # تحويل الرد إلى JSON
            response_json = await response.json()

            # طباعة البيانات للتحقق من الهيكل
           # print(json.dumps(response_json, indent=2))

            # التحقق من وجود مفتاح "data" في الاستجابة
            if "data" in response_json and isinstance(response_json["data"], list):
                # استخراج كل id حيث isClaimed يساوي false
                ids = [item.get("id") for item in response_json["data"] if item.get("isClaimed") == False]

                # حفظ جميع الـ ids في ملف quid.txt
                with open("quid.txt", "w") as file:
                    file.write("\n".join(str(id) for id in ids))

                print(f"IDs saved to quid.txt: {ids}")
            else:
                print("The 'data' key is not in the expected format or not found.")
# تشغيل الدالة


async def claim_social_id(token):
    # قراءة القيم من ملف quid.txt
    try:
        with open("quid.txt", "r") as file:
            social_ids = file.readlines()
        
        # إزالة الأسطر الفارغة والبيانات غير المرغوب فيها
        social_ids = [social_id.strip() for social_id in social_ids if social_id.strip()]
        
    except FileNotFoundError:
        print("File 'quid.txt' not found!")
        return

    # إعداد الرابط والرؤوس
    url = "https://api2.pineye.io/api/v1/SocialFollower/claim"

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

    # إرسال الطلبات لكل socialId
    async with aiohttp.ClientSession() as session:
        for social_id in social_ids:
            params = {
                'socialId': social_id
            }

            async with session.post(url, params=params, headers=headers) as response:
                response_text = await response.json()
                
                print_message(f"quest id  : {social_id} : {response_text}" , "green")
                await asyncio.sleep(10)

# تشغيل الكودclaim_social_id

async def main():
    create_gradient_banner("Bot Pin Eye")  # عرض الشعار
    print_info_box([("Telegram", "https://t.me/YOU742"), ("Coder", "@Ke4oo")])  # معلومات وسائل التواصل
    print(Fore.GREEN + "Welcome to the Script!")
    token = await send_request()
    if token and token != "Token not found":
        await fetch_quest(token)
        await claim_social_id(token)        
        await seend_clk(token)
        await send_DailyReward(token)
        while True:
        	await seend_clk(token)

        	                

# تشغيل البرنامج
asyncio.run(main())
