from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

PATH = "Your path to chrome driver"
GAME_URL = "http://orteil.dashnet.org/experiments/cookie/"

# create a bot to click on the cookie as fast as possible
s = Service(executable_path=PATH)
# create an instance of Chrome WebDriver
driver = webdriver.Chrome(service=s)
driver.get(GAME_URL)
# get the current time
start_time = time.time()
current_time = time.time()
# get all the price data
all_prices = []
store = driver.find_elements(By.CSS_SELECTOR, "#store b")
ids = driver.find_elements(By.CSS_SELECTOR, "#store div")
id_list = [id.get_attribute("id") for id in ids]
for item in store:
    if item.text != "":
        price_str = item.text.split("-")[1].strip()
        if "," in price_str:
            price_str = price_str.replace(",", "")
        price = int(price_str)
        all_prices.append(price)
# create a dictionary to map indices and ids
id_map = {i: id_list[i] for i in range(len(id_list))}

while True:
    cookie = driver.find_element(By.ID, "cookie")
    cookie.click()
    # for every 5 second
    if time.time() > current_time + 5:
        # check what is the most expensive item we afford to buy
        money_str = driver.find_element(By.ID, "money").text
        if "," in money_str:
            money_str = money_str.replace(",", "")
        money_value = int(money_str)
        for i in range(len(all_prices) - 1, -1, -1):
            if money_value >= all_prices[i]:
                item_to_buy = driver.find_element(By.ID, id_map[i])
                item_to_buy.click()
                break
        # update the current time
        current_time = time.time()
    # after 5 minutes since the game start, stop the bot and print "cookies/second"
    if time.time() >= start_time + 60 * 1:
        break

score = driver.find_element(By.CSS_SELECTOR, "#saveMenu #cps")
print(f"Your cookies/second is {score.text}.")
driver.quit()

