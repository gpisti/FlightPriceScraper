import json, os, sys

from datetime import date
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.by import By

WAIT_TIMEOUT = 5  # Meghatározza, mennyi időt szánjon a kód, 1 napnyi repülőjegyek lementésére (Adat hiány esetén növelendő)
FOR_PATH = "\\".join(sys.argv[0].split("\\")[:-1]) # PATH_FOR_ADATOKTXT segédváltozója
PATH_FOR_ADATOKTXT = f'{FOR_PATH}\\adatok.txt'  # Az adatok.txt file elérési útja
DAYS = 5  # Adatok frissétése esetén ennyi napot lefedve szedi össze az új adatokat (a mai nap nem számít bele)


# A megadott dátumhoz képest határozza meg a holnapi nap dátumát éééé-hh-nn formátumban
def next_day(today):
    year = int(str(today)[:4])
    month = int(str(today)[5:7])
    day = int(str(today)[8:])
    if month in [4, 6, 9, 11]:  # 30 nap
        if day + 1 > 30:
            month += 1
            day = 1
        else:
            day += 1

    elif month in [1, 3, 5, 7, 8, 10, 12]:  # 31 nap
        if day + 1 > 31 and month == 12:
            year += 1
            month = 1
            day = 1
        elif day + 1 > 31:
            month += 1
            day = 1
        else:
            day += 1
    else:
        if day + 1 > 28:
            month += 1
            day = 1
        else:
            day += 1

    return f"{str(year).zfill(4)}-{str(month).zfill(2)}-{str(day).zfill(2)}"


# Adatokat scrapel, és írja ki az adatok.txt-be
def get_tickets(date):
    data = {}
    fki = open("adatok.txt", "a")
    driver.get(f"https://www.kiwi.com/hu/search/tiles/debrecen-magyarorszag/anywhere/{date}/anytime")
    driver.implicitly_wait(WAIT_TIMEOUT)
    try:
        accept_cookie_button = driver.find_element(webdriver.common.by.By.ID, "cookies_accept")
        accept_cookie_button.click()
    except Exception:
        pass

    prices = driver.find_elements(By.XPATH, "//span[contains(@class, 'length-9') or contains(@class, 'length-10')]")
    locations = driver.find_elements(By.XPATH,
                                     '//div[contains(@class, "flex items-center justify-between de:group-hover:text-primary-foreground")]')


    pp = [x.text for x in prices]
    ll = [x.text for x in locations]


    for i in range(len(pp)):
        intpp = ""
        for e in pp[i]:
            if e in "0123456789":
                intpp += e
        if len(intpp) != 0:
            data[ll[i]] = [int(intpp), date]
        else:
            data[ll[i]] = [0, date]
    if dict(sorted(data.items(), key=lambda x: x[1])) != {}:
        print(dict(sorted(data.items(), key=lambda x: x[1])), file=fki)
    fki.close()


# Konzolos UI:
def main_menu():
    table = PrettyTable()
    table.field_names = ["Sorszám", "Lehetőségek"]

    table.add_rows([
        ["1.", "Városok kilistázása"],
        ["2.", "Város alapú keresés"],
        ["3.", "Dátum alapú keresés"],
        ["4.", "Overall legolcsóbb"],
        ["5.", "Adatok frissítése"],
    ])

    return table


# Város alapján, megkeresi mikor a legolcsóbb utazni
def city_search():
    cheapest = []
    city = input("Adja meg a város nevét!\n->")
    for dict in allData:
        for k, v in dict.items():
            if k == city.title():
                cheapest.append(v)
    if len(cheapest) == 0:
        return "Ide nem indul egy repülő sem."
    mc = min([x[0] for x in cheapest])
    for i in cheapest:
        if i[0] == mc:
            return f"{i[0]} Ft\n{i[1]}"
    return "HIBA"


# Dátum alapján, megkeresi hova a legolcsóbb utazni
def date_search():
    match = []
    date = input("Adja meg az indulás időpontját! (éééé-hh-nn)\n->")
    for dict in allData:
        for k, v in dict.items():
            if v[1] == date:
                match.append([k, v[0]])
    if len(match) == 0:
        return "Sajnos ekkor nem indul egy járat sem!"

    mc = min([x[1] for x in match])

    for i in match:
        if i[1] == mc:
            return f"{i[0]}\n{i[1]} Ft"


# Megkeresi, hogy mikor és hova a legolcsóbb utazni
def overall_cheapest():
    priceDict = {}
    for dict in allData:
        for k, v in dict.items():
            priceDict[k] = v
    cheapest = list(priceDict.values())[0][0]
    cd = [list(priceDict.keys())[0], list(priceDict.values())[0][0]]
    for k, v in priceDict.items():
        if v[0] <= cheapest:
            cheapest = v[0]
            cd = [k, v[1]]
    return f"{cd[0]}\n{cd[1]}\n{cheapest} Ft"


# Az elérhető városok neveit sorolja fel
def list_cities():
    cities = []
    for dict in allData:
        for i in dict.keys():
            if i not in cities:
                cities.append(i)
    c = 1
    for i in cities:
        c += 1
        print(i, end=", ")
        if c == 5:
            print()
            c = 1
    print()

# A már meglévő "elavult" adatokat frissíti
def refresh_data():
    global driver
    driver = webdriver.Firefox()

    if os.path.exists(PATH_FOR_ADATOKTXT):
        os.remove("adatok.txt")
        gen = open("adatok.txt", "w")
        gen.close()

    tdate = str(date.today())
    for i in range(DAYS+1):
        get_tickets(tdate)
        tdate = next_day(tdate)
    driver.close()


# Létrehozza az összes adatot tartalmazó listát, amivel az egész project dolgozik
def create_allData():
    fbe = open("adatok.txt")
    allData = [json.loads(line.replace("'", '"')) for line in fbe]
    fbe.close()
    return allData


if __name__ == "__main__":
    if os.path.exists(PATH_FOR_ADATOKTXT) == False:
        refresh_data()
    allData = create_allData()

    print(main_menu())
    for action in sys.stdin:
        try:
            allData
        except NameError:
            allData = create_allData()

        match action.strip():
            case "1":
                list_cities()
            case "2":
                print(city_search())
            case "3":
                print(date_search())
            case "4":
                print(overall_cheapest())
            case "5":
                refresh_data()
