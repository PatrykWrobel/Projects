from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os
import glob
from datetime import date
import datetime
import csv
from csv_module import create_orders, read_csv
import requests
import json
import sys
from csv import writer





def site_login():  #......Logowanie (SELENIUM)

    print('-----LOGOWANIE-----')
    driver.get("https://admin.smartweb.io/")
    driver.find_element_by_id("username").send_keys("LOGIN")        #.....wklejenie loginu
    driver.find_element_by_id("password").send_keys("PASSWORD")      #......wklejenie hasła
    driver.find_element_by_class_name("login-btn").click()          #............klik logowanie
    print('----------------------------------------------')
    print('----------------------------------------------')
    print('-----ZALOGOWANO-----')
    print('----------------------------------------------')
    print('----------------------------------------------')
    time.sleep(3)
    os.system('cls')

def after_login():
    print('Wybór danych do pobrania')
    driver.get("https://admin.smartweb.io/?page=page&sub=edit&edit=export")         #przejście do eksportu w Smartweb
    select = Select(driver.find_element_by_id('exportChoices'))           #.....wybór pola rozwijanego Choose
    select.select_by_visible_text('Orders')       #.....wybór Orders
    time.sleep(3)
    driver.find_element_by_xpath('//label[@for="radio_csv"]').click()           #.....wybór csv
    time.sleep(3)
    driver.find_element_by_id("next_button").click()             # klik Next
    time.sleep(3)

    if date.today().weekday() == 0:          #....sprawdzenie czy jest poniedziałek
        driver.find_element_by_xpath('//label[@for="radio_date"]').click()           #.....wybór radio button - By period
        driver.find_element_by_id("date_from").clear()            #.....czyszcenie pola Start
        previous_date = datetime.datetime.today() - datetime.timedelta(days=3)           #.....jeżeli poniedziałek ustaw datę 3 dni wstecz
        previous_date_formatted = previous_date.strftime('%d/%m/%Y')            # format daty do wklejenia
        driver.find_element_by_id("date_from").send_keys(previous_date_formatted)      #....przesłanie daty
        driver.find_element_by_id("next_button").click()           #....klik Next button
        select = Select(driver.find_element_by_id('templateSelect'))
        driver.find_element_by_class_name("Import_baselinker").click()          #.....wybór z listy rozwijanej Import_Baselinker
        # select.select_by_value('ignore-source;ignore-GENERAL;ORDER_DATE;PAYMENT_TITLE')
        time.sleep(2)
        driver.find_element_by_id("next_button").click()           #.....klik Next button
        time.sleep(2)
        print('Pobieranie pliku')
        driver.find_element_by_id("download_button").click()           #....klik Download button
        print("Plik pobrano")
    else:                                                                     #....jeżeli nie poniedziałek
        driver.find_element_by_xpath('//label[@for="radio_date"]').click()         #.....wybór Radio button By period
        driver.find_element_by_id("date_from").clear()           #.........wyczyszczenie pola Start daty
        previous_date = datetime.datetime.today() - datetime.timedelta(days=1)       #....ustawienie daty 1 dzień wstecz
        previous_date_formatted = previous_date.strftime('%d/%m/%Y')        #........format daty
        driver.find_element_by_id("date_from").send_keys(previous_date_formatted)         #przesłanie daty
        # driver.find_element_by_xpath('//label[@for="radio_date"]').click()
        driver.find_element_by_id("next_button").click()          #...klik Next button
        select = Select(driver.find_element_by_id('templateSelect'))
        driver.find_element_by_class_name("Import_baselinker").click()         #...wybór templatki do pobrania
        # select.select_by_value('ignore-source;ignore-GENERAL;ORDER_DATE;PAYMENT_TITLE')
        time.sleep(3)
        driver.find_element_by_id("next_button").click()           #         ....klik Next button
        time.sleep(3)
        print('Pobieranie pliku')
        time.sleep(3)
        driver.find_element_by_id("download_button").click()     #       ....klik Download button
        print("Plik pobrano")


def FileNameRemove():          #...usuwanie pliku poprzedniego
    print('Usuwanie pliku')
    files = glob.glob('C:/Users/nazwa/PycharmProjects/Pat/Nomax/API/pobrane/*')
    for f in files:
        os.remove(f)
        print('Plik usunięto', f)

def FileNameChange():
    newfile = 'test.csv'
    path = os.listdir('C:/Users/nazwa/PycharmProjects/Pat/Nomax/API/pobrane/')
    # print(path[0])
    new_file = os.rename('C:/Users/nazwa/PycharmProjects/Pat/Nomax/API/pobrane/' + path[0], 'C:/Users/nazwa/PycharmProjects/Pat/Nomax/API/pobrane/' + newfile)
    print('Zmieniono nazwę')          #zmiana nazwy pobranego pliku na test.csv


def FileOpen():         #otwarcie pobranego pliku
    with open('C:/Users/nazwa/PycharmProjects/Pat/Nomax/API/pobrane/test.csv', encoding='iso-8859-4') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)
        next(csv_reader)
        array = []
        id_array = []
        ORDER_ID = 0
        ORDER_DATE = 1
        ORDER_TOTAL = 2
        ORDER_COMMENT_CUSTOMER = 3
        DELIVERY_PRICE = 6
        USER_USERNAME = 24
        PAYMENT_TITLE = 4
        DELIVERY_TITLE = 5

        # Customer
        CUSTOMER_PHONE = 22
        CUSTOMER_EMAIL = 23
        CUSTOMER_FIRSTNAME = 15
        CUSTOMER_LASTNAME = 16
        CUSTOMER_COMPANY = 17
        CUSTOMER_ADDRESS = 19
        CUSTOMER_CITY = 20
        CUSTOMER_POSTCODE = 21
        CUSTOMER_CVR = 18

        # Shipping
        CUSTOMER_SHIPPING_FIRSTNAME = 25
        CUSTOMER_SHIPPING_LASTNAME = 26
        CUSTOMER_SHIPPING_COMPANY = 27
        CUSTOMER_SHIPPING_ADDRESS = 28
        CUSTOMER_SHIPPING_POSTCODE = 29
        CUSTOMER_SHIPPING_CITY = 30
        CUSTOMER_SHIPPING_PHONE = 31

        # Products information
        PRODUCT_ID = 7
        PRODUCT_NUMBER = 8
        PRODUCT_TITLE1 = 9
        PRODUCT_TITLE2 = 10
        PRODUCT_AMOUNT = 11
        PRODUCT_PRICE = 12
        PRODUCT_DISCOUNT = 13
        PRODUCT_WEIGHT = 14


        for row in csv_reader:
            id_array.append(row[ORDER_ID])
            last_id = id_array[-1]           #....utworzenie ostatniego nr id z pliku
            object = {

                "ORDER_ID": row[ORDER_ID],
                "ORDER_DATE": row[ORDER_DATE],
                "ORDER_COMMENT_CUSTOMER": row[ORDER_COMMENT_CUSTOMER],
                "CUSTOMER_PHONE": row[CUSTOMER_PHONE],
                "CUSTOMER_EMAIL": row[CUSTOMER_EMAIL],
                "ORDER_CURRENCY": "NOK",
                "ORDER_TOTAL": row[ORDER_TOTAL],
                "PAYMENT_TITLE": row[PAYMENT_TITLE],
                "DELIVERY_PRICE": row[DELIVERY_PRICE],
                "USER_USERNAME": row[USER_USERNAME],
                "DELIVERY_TITLE": row[DELIVERY_TITLE],
                "CUSTOMER_FIRSTNAME": row[CUSTOMER_FIRSTNAME],
                "CUSTOMER_LASTNAME": row[CUSTOMER_LASTNAME],
                "CUSTOMER_COMPANY": row[CUSTOMER_COMPANY],
                "CUSTOMER_ADDRESS": row[CUSTOMER_ADDRESS],
                "CUSTOMER_CITY": row[CUSTOMER_CITY],
                "CUSTOMER_POSTCODE": row[CUSTOMER_POSTCODE],

                "CUSTOMER_SHIPPING_FIRSTNAME": row[CUSTOMER_SHIPPING_FIRSTNAME],
                "CUSTOMER_SHIPPING_LASTNAME": row[CUSTOMER_SHIPPING_LASTNAME],
                "CUSTOMER_SHIPPING_COMPANY": row[CUSTOMER_SHIPPING_COMPANY],
                "CUSTOMER_SHIPPING_ADDRESS": row[CUSTOMER_SHIPPING_ADDRESS],
                "CUSTOMER_SHIPPING_POSTCODE": row[CUSTOMER_SHIPPING_POSTCODE],
                "CUSTOMER_SHIPPING_CITY": row[CUSTOMER_SHIPPING_CITY],
                "CUSTOMER_SHIPPING_PHONE": row[CUSTOMER_SHIPPING_PHONE],

                "CUSTOMER_CVR": row[CUSTOMER_CVR],
                # info o produktach
                "PRODUCT_ID": row[PRODUCT_ID],
                "PRODUCT_NUMBER": row[PRODUCT_NUMBER],
                "PRODUCT_TITLE1": row[PRODUCT_TITLE1],
                "PRODUCT_TITLE2": row[PRODUCT_TITLE2],
                "PRODUCT_AMOUNT": row[PRODUCT_AMOUNT],
                "PRODUCT_PRICE": row[PRODUCT_PRICE],
                "PRODUCT_DISCOUNT": row[PRODUCT_DISCOUNT],
                "PRODUCT_WEIGHT": row[PRODUCT_WEIGHT]

            }
            array.append(object) #utworzenie  tablicy z pobranego pliku
        # print(data)
    return array, last_id

# def CSV_Open():
#     with open('C:/Users/nazwa/PycharmProjects/Pat/Nomax/API/Sending.csv', encoding='iso-8859-4') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=';')
#         next(csv_reader)
#         next(csv_reader)
#         array = []
#         for row in csv_reader:
#             id = row[0]
#             # print(id)
#             array.append(id)
#             data = array[-1]
#         print('Ostatni pobrany ID: ', data)
#     return data
#
# txt_data = CSV_Open()

def WriteDataTXT():          #........zapisanie ostatniego nr z pobranego pliku do pliku .txt

    with open('C:/Users/nazwa/PycharmProjects/Pat/Nomax/API/data.txt', 'w') as f:

        id = f.write(last_id1)

    f.close()
    return id

def OpenDataTXT():                #....zczytanie ostatniego zapisanego nr id z pliku .txt
    f = open("C:/Users/nazwa/PycharmProjects/Pat/Nomax/API/data.txt", "r")

    return f.read()

def Compare(get_last_id):
    array = []
    csv_data = FileOpen()[0]               #.......przekazanie obiektu z pobranego pliku
    last_id = get_last_id            #.....ostatni id z pliku .txt przeazany z send_compare z pętli while
    print(last_id)
    for row in csv_data:
        # print(row['ORDER_ID'])
        if int(last_id) < int(row['ORDER_ID']):   #.....porównanie czy ostatni id z pliku .txt jest mniejszy od id z pobranego pliku

            object = {

            "ORDER_ID": row['ORDER_ID'],
            "ORDER_DATE": row['ORDER_DATE'],
            "ORDER_COMMENT_CUSTOMER": row['ORDER_COMMENT_CUSTOMER'],
            "CUSTOMER_PHONE": row['CUSTOMER_PHONE'],
            "CUSTOMER_EMAIL": row['CUSTOMER_EMAIL'],
            "ORDER_CURRENCY": "NOK",
            "ORDER_TOTAL": row['ORDER_TOTAL'],
            "PAYMENT_TITLE": row['PAYMENT_TITLE'],
            "DELIVERY_PRICE": row['DELIVERY_PRICE'],
            "USER_USERNAME": row['USER_USERNAME'],
            "DELIVERY_TITLE": row['DELIVERY_TITLE'],
            "CUSTOMER_FIRSTNAME": row['CUSTOMER_FIRSTNAME'],
            "CUSTOMER_LASTNAME": row['CUSTOMER_LASTNAME'],
            "CUSTOMER_COMPANY": row['CUSTOMER_COMPANY'],
            "CUSTOMER_ADDRESS": row['CUSTOMER_ADDRESS'],
            "CUSTOMER_CITY": row['CUSTOMER_CITY'],
            "CUSTOMER_POSTCODE": row['CUSTOMER_POSTCODE'],

            "CUSTOMER_SHIPPING_FIRSTNAME": row['CUSTOMER_SHIPPING_FIRSTNAME'],
            "CUSTOMER_SHIPPING_LASTNAME": row['CUSTOMER_SHIPPING_LASTNAME'],
            "CUSTOMER_SHIPPING_COMPANY": row['CUSTOMER_SHIPPING_COMPANY'],
            "CUSTOMER_SHIPPING_ADDRESS": row['CUSTOMER_SHIPPING_ADDRESS'],
            "CUSTOMER_SHIPPING_POSTCODE": row['CUSTOMER_SHIPPING_POSTCODE'],
            "CUSTOMER_SHIPPING_CITY": row['CUSTOMER_SHIPPING_CITY'],
            "CUSTOMER_SHIPPING_PHONE": row['CUSTOMER_SHIPPING_PHONE'],

            "CUSTOMER_CVR": row['CUSTOMER_CVR'],
            # info o produktach
            "PRODUCT_ID": row['PRODUCT_ID'],
            "PRODUCT_NUMBER": row['PRODUCT_NUMBER'],
            "PRODUCT_TITLE1": row['PRODUCT_TITLE1'],
            "PRODUCT_TITLE2": row['PRODUCT_TITLE2'],
            "PRODUCT_AMOUNT": row['PRODUCT_AMOUNT'],
            "PRODUCT_PRICE": row['PRODUCT_PRICE'],
            "PRODUCT_DISCOUNT": row['PRODUCT_DISCOUNT'],
            "PRODUCT_WEIGHT": row['PRODUCT_WEIGHT']
            }
            array.append(object)

    # print(array)
    return array

def Save_Compare(compare):          #.....zapisanie wierszy uzyskanych z funkcji Compare()
    with open('Sending.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['ORDERS'])
        writer.writerow(compare[0].keys())
        for row in compare:
            # print(row)
            writer.writerow(row.values())
    f.close()


def Send_Orders(map):                  #.....wysyłka zamówień do baselinkera

    orders = create_orders(map)               #.......uzyskanie obiektów z modułu csv_module

    for order in orders:

        print(order)
        parameters = json.dumps(order)

        data = {
            'token': '100.....-........-.................................',
            'method': 'addOrder',
            'parameters': parameters
        }

        response = requests.post('https://api.baselinker.com/connector.php', data=data)

        print(response)

        show = response.json()
        print(show)

flag = 0
count = 1
while flag < 31:     #.....ustawienie flagi na 32 cykle (co 15 min - 8 h)
    print('---------Start nowej sesji nr. ', count, '----------')
    options = Options()
    prefs = {"download.default_directory": "C:\\Users\\nazwa\\PycharmProjects\\Pat\\Nomax\\API\\pobrane"}    # ............ustawienie domyślnej ściezki do zapisu pliku
    options.add_experimental_option("prefs", prefs)
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("no-default-browser-check")
    options.add_argument("--remote-debugging-port=9222")
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--test-type")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("addCustomRequestHeader=true")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"')
    options.add_argument("--allow-running-insecure-content")
    options.add_argument('--headless')       #...................ukrycie okna przeglądarki

    # .............ściezka do webdrivera
    driver = webdriver.Chrome("C:/Users/nazwa/Documents/chromedriver_win32/chromedriver.exe", chrome_options=options)

    site_login()
    FileNameRemove()
    after_login()
    time.sleep(3)
    FileNameChange()
    FileOpen()
    last_id1 = (FileOpen()[1])         #......przekazanie ostatniego id z pobranego pliku
    print(last_id1, OpenDataTXT())
    if last_id1 != OpenDataTXT():             #......porównanie czy ostatni id z pobranego pliku jest różny z id z pliku .txt
        send_compare = Compare(OpenDataTXT())             #.....przekazanie id z pliku .txt do funkcji Compare()
        WriteDataTXT()                 #zapisanie ostatniego id
        Save_Compare(send_compare)
        # driver.close()
        #zapisanie obiektu otrzymanego z funkcji Compare
        plik_wsadowy = "Sending.csv"
        map = read_csv(plik_wsadowy)                 #czytanie pliku Sending.csv z modulu csv_module
        print("Nowe zamówienia")
        Send_Orders(map)                        #....przekazanie ordersów z modułu do funkcji wysyłającej
    else:
        print("Brak nowego zamówienia")
        # driver.close()

    print('Zamknięto sesję nr. ', count, ' ', datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    print('Czas do następnej sesji - 15 minut')
    minutesToSleep = (15 - datetime.datetime.now().minute % 15)
    # time.sleep(minutesToSleep * 60)
    time.sleep(minutesToSleep * 60)
    flag += 1
    count += 1
else:
    print('--------------------------------------------------------------------')
    print('__________---To była ostatnia sesja dzisiejszego dnia---____________')
    print('--------------------------------------------------------------------')
    time.sleep(4)
    os.system("taskkill -f -im conhost.exe")
