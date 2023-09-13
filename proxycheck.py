from colorama import init, Fore
import requests
# import threading
# from concurrent.futures import ThreadPoolExecutor

init()

def check_proxy(proxy):
    
    url = "https://www.google.com"  # You can change this URL to any website you want to test

    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }

    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(Fore.GREEN + f"{proxy} is valid")
            with open('conf/validproxies.config', 'a') as save:
                save.write(f"{proxy}\n")
        else:
            print(Fore.RED + f"{proxy} is invalid ==> code{response.status_code}")
    except Exception as e:
        # print(e)
        print(Fore.RED + f"{proxy} is invalid")

def read_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]
    

# proxies_file_path = 'proxies.config'
# proxy_list = read_proxies_from_file(proxies_file_path)

# with ThreadPoolExecutor(max_workers=100) as executor:
#     for proxy in proxy_list:
#         executor.submit(check_proxy, proxy)
