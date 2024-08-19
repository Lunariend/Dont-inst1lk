# Leak By RedTiger Teams

from os import system
from time import sleep
from colorama import init, Fore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

init(autoreset=True)

class Bot:
    def __init__(self):
        system("cls || clear")
        self.printBanner()
        print(Fore.YELLOW + "[~] Chargement du pilote, veuillez patienter...")

        try:
            options = Options()
            options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
            )
            self.driver = webdriver.Chrome(options=options)

            print(Fore.GREEN + "[+] Pilote chargé avec succès")
            print()
        except Exception as e:
            print(Fore.RED + f"[!] Erreur lors du chargement du pilote : {e}")
            exit()

        self.url = "https://zefoy.com"
        self.captcha_xpath = "/html/body/div[5]/div[2]/form/div/div/div/div/button"
        self.services = {
            "followers": {
                "title": "Abonnés",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[2]/div/button",
                "status": None,
            },
            "likes": {
                "title": "Likes",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[3]/div/button",
                "status": None,
            },
            "comment_likes": {
                "title": "Likes coms",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[4]/div/button",
                "status": None,
            },
            "views": {
                "title": "Vues",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[5]/div/button",
                "status": None,
            },
            "shares": {
                "title": "Partages",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[6]/div/button",
                "status": None,
            },
            "favorites": {
                "title": "Favoris",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[7]/div/button",
                "status": None,
            },
        }

    def start(self):
        self.driver.get(self.url)

        print(Fore.MAGENTA + "[!] En cas d'erreur 502 Bad Gateway")
        print(Fore.MAGENTA + "[!] veuillez rafraîchir la page")
        print()

        self.wait_for_xpath(self.captcha_xpath)

        print(Fore.YELLOW + "[~] Veuillez compléter le captcha")

        self.wait_for_xpath(self.services["followers"]["xpath"])

        print(Fore.GREEN + "[+] Captcha complété avec succès")
        print()

        self.driver.minimize_window()
        self.check_services()

        for index, service in enumerate(self.services):
            title = self.services[service]["title"]
            status = self.services[service]["status"]

            print(Fore.BLUE + f"[{str(index + 1)}] {title}".ljust(20), status)

        while True:
            try:
                choice = int(input(Fore.YELLOW + "[-] Choisissez une option : "))
            except ValueError:
                continue  # Cela assure que la boucle continue après une ValueError

            if choice in range(1, 7):
                break

        self.select_service(choice)

    def select_service(self, choice):
        div = 6 + choice
        service_key = list(self.services.keys())[choice - 1]

        self.driver.find_element(By.XPATH, self.services[service_key]["xpath"]).click()

        print()
        video_url = input(Fore.MAGENTA + "[-] URL de la vidéo : ")
        print()

        self.start_service(div, video_url)

    def start_service(self, div, video_url):
        url_input_xpath = f"/html/body/div[{div}]/div/form/div/input"
        search_btn_xpath = f"/html/body/div[{div}]/div/form/div/div/button"
        send_btn_xpath = f"/html/body/div[{div}]/div/div/div[1]/div/form/button"

        input_element = self.driver.find_element(By.XPATH, url_input_xpath)
        input_element.clear()
        input_element.send_keys(video_url)

        while True:
            # Cliquez sur le bouton de recherche
            self.driver.find_element(By.XPATH, search_btn_xpath).click()

            # Tentez de cliquer sur le bouton d'envoi s'il est présent
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, send_btn_xpath))
                ).click()
            except TimeoutException:
                # Si le bouton d'envoi n'est pas trouvé, cliquez à nouveau sur le bouton de recherche
                self.driver.find_element(By.XPATH, search_btn_xpath).click()

            remaining_time = self.check_remaining_time(div)

            if remaining_time is not None:
                print(Fore.YELLOW + f"[~] En attente pendant {remaining_time} secondes")
                sleep(remaining_time)

    def check_remaining_time(self, div):
        remaining_time_xpath = f"/html/body/div[{div}]/div/div/span[1]"

        try:
            element = self.driver.find_element(By.XPATH, remaining_time_xpath)
            text = element.text

            if "Veuillez patienter" in text:
                minutes = text.split("Veuillez patienter ")[1].split(" ")[0]
                seconds = text.split(" seconde")[0].split()[-1]
                sleep_duration = int(minutes) * 60 + int(seconds) + 5

                return sleep_duration
            else:
                return None
        except NoSuchElementException:
            return None

    def check_services(self):
        for service in self.services:
            xpath = self.services[service]["xpath"]

            try:
                element = self.driver.find_element(By.XPATH, xpath)

                if element.is_enabled():
                    self.services[service]["status"] = Fore.GREEN + "[Online]"
                else:
                    self.services[service]["status"] = Fore.RED + "[Offline]"
            except NoSuchElementException:
                self.services[service]["status"] = Fore.RED + "[Offline]"

    def wait_for_xpath(self, xpath):
        while True:
            try:
                self.driver.find_element(By.XPATH, xpath)
                return True
            except NoSuchElementException:
                sleep(1)

    def printBanner(self):
        print(

        Fore.RED +  """


            ·▄▄▄▄   ▄▄▄· ▄▄▌ ▐ ▄▌ ▄▄▄· 
            ██▪ ██ ▐█ ▀█ ██· █▌▐█▐█ ▀█ 
            ▐█· ▐█▌▄█▀▀█ ██▪▐█▐▐▌▄█▀▀█  Tool-Tiktok
            ██. ██ ▐█ ▪▐▌▐█▌██▐█▌▐█ ▪▐▌
            ▀▀▀▀▀•  ▀  ▀  ▀▀▀▀ ▀▪ ▀  ▀ 


                 Discord : fullsafe.
        Discord support : https://discord.gg/tdTUvwVpMY
﹥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━﹤
"""
        )


if __name__ == "__main__":
    bot = Bot()
    bot.start()
