import csv
from bs4 import BeautifulSoup
import time
from termcolor import colored
import math
from dict2xml import dict2xml
import string

start_time = time.time()

def createNomaxPrice(price):
    if price:
        # print(float(price) * 33.3)
        roundedPrice = roundup(float(price.replace(',', '.')) * 35)
        # return str(float(price) * 33.3) + " | " + str(roundedPrice)
        return roundedPrice
    else:
        return "NIE MA CENY ----------------"

def roundup(x):
    length = len(str(int(x)))
    if (length == 3 and int(x) >= 200):
        length += 1
    # print(length, x)
    return int(math.ceil(x / 10.0**(length-2)) * 10**(length-2) - 1)

def Tag_add(new_tag):

    strip_descr = new_tag.rstrip(' ').replace('TA Technix ', '').replace('air suspension kit', 'Luftfjæring Sett').replace('lowering springs', '').replace('fits for', 'Passer til:').replace('Baujahr', 'year').replace('Tieferlegung ', 'lowering').replace('Federn', 'Air Suspensjon:').replace('year','År').replace('lowering','Senking:').replace('front load','Frontlast').replace('rear load','Bakbelastning').replace('only front axle','Bare foraksel').replace('front strut','Frontstiver').replace('additional thread adjustment','').replace('/Viair','').replace('air spring kit','Kit til luftbælge').replace('rear axle','bagaksel').replace('air spring kit','Kit til luftbælge').replace('airride','Airride sett')
    new_description1 = strip_descr.replace('#Z#Z', '</p><p>').replace('#Z', '</br>') + '</br><div class="PW_tuv">TUV dokumentasjon</div>'
    # print(new_description1)
    return new_description1

def Stock_open():
    with open('Stock TA Technix.csv', encoding='iso-8859-4') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        array = []
        for row in csv_reader:
            Ean = row[1]
            Stock = row[2]
            object = {
                "Ean": Ean,
                "Stock":Stock
                }
            array.append(object)
        return array

Stock_open = Stock_open()

def Stock_update(number):
    for row in Stock_open:
        if row['Ean'] == number:
            stock = row['Stock']
            return stock

def create_images(images):
    array = []
    for row in images:
        if row != '':
            img = row[row.rfind("/") + 1:]
            # print(img)
            img_new = ('ta/' + img)
            # print(img_new)
            array.append(img_new)
    x = '|'.join(array)
    # print(x)
    return x

def Title_change(title_change,car):

    title_new = title_change.split(' fits for ')[0]
    New_Title = title_new.replace('TA Technix', '').replace('hardness adjustable', '').replace('/Viair', '').replace('airride','Airride Sett').replace('hardeness adjustable ','').replace('hardness adjustable ','').replace('air suspension kit for air suspension/','').replace(' hardness adjustable','').replace(' suspension kit','')
    print(New_Title)
    Title = "{} {} {} {}".format(New_Title, 'TA Technix',car[0],car[1])

    return Title

def Kyoretoy_cat():

    file_from_Kyoretoy = 'CATEGORY_FINAL2.csv'

    with open(file_from_Kyoretoy, encoding='Utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)
        kyoretoy = []
        for row in csv_reader:
            car_id = row[0]
            car_name = row[1]
            model_name = row[3]
            product_id = row[4]
            product_name = row[5]
            id_model = row[2]

            object = {

                'CAR_ID': car_id,
                'CAR_NAME': car_name,
                'MODEL_ID': id_model,
                'MODEL_NAME': model_name,
                'PRODUCT_ID': product_id,
                'PRODUCT_NAME': product_name

                 }
            kyoretoy.append(object)
        return kyoretoy

Kyoretoy = Kyoretoy_cat()

def Tuning_model():

    file_from_step3 = 'CATEGORY_Tunning.csv'

    with open(file_from_step3, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)
        tuning_csv = []
        for row in csv_reader:
            cat_id = row[2]
            parent_id = row[0]
            model_name = row[3]
            pictures = row[4]
            object = {

                'CATEGORY_ID_NEW': cat_id,
                'PARENT_ID': parent_id,
                'TITLE_NO': model_name,
                'PICTURES': pictures,
                "MARKA_NAME": row[1]

            }
            tuning_csv.append(object)
        return tuning_csv

tuning = Tuning_model()

def find_names(model_id):



    for model in tuning:
        if model_id == model["CATEGORY_ID_NEW"]:
            marka = model['MARKA_NAME']
            model = model["TITLE_NO"]

            return(marka, model)

def Split_cat(cat):
    array = []
    new_cat = cat.split('|')
    array.extend(new_cat)
    Tunning_cat(array)

    subcat = array
    for model in array:
        # print(model)
        for line in Kyoretoy:
            if model == line["MODEL_ID"] and line['PRODUCT_NAME'] == "Suspensjon":
                subcat.append(line["PRODUCT_ID"])
    # print(subcat)

    # print(Tunning_cat(array)[1])
    main_category = Tunning_cat(array)[0]
    # print(main_category)
    subcat.extend(Tunning_cat(array)[1])

    # print(main_category)
    # print(subcat)

    join_subcat = "|".join(subcat)

    return main_category, join_subcat

def Tunning_cat(models):    #przekazanie modeli z Kyoretoy

    tuning_array_sub = []
    main_cat = models[0]
    for line in Kyoretoy:
        if main_cat == line["MODEL_ID"] and line['PRODUCT_NAME'] == "Suspensjon":
            for tuning_models in tuning:
                if line["MODEL_NAME"] == tuning_models["TITLE_NO"]:
                    main_cat = tuning_models["CATEGORY_ID_NEW"]
                    parent_id = tuning_models['PARENT_ID']
                    # print(main_cat)
                    tuning_array_sub.append(parent_id)
                    # print(tuning_array_sub)


    # print(models)
    lenth = len(models)


    # print(lenth)


    if lenth > 1:
        itercars = iter(models)
        next(itercars)
        for model in itercars:
            for line in Kyoretoy:
                if model == line["MODEL_ID"] and line['PRODUCT_NAME'] == "Suspensjon":
                    for tuning_models in tuning:
                        if line["MODEL_NAME"] == tuning_models["TITLE_NO"]:
                            tuning_array_sub.append(tuning_models["CATEGORY_ID_NEW"])
    # print("all sub",tuning_array_sub)


    return (main_cat,tuning_array_sub)

#Rozdzielenie po marce samochodu
def split_by_brand (string):
    car_array = ['Audi', 'Bmw', 'Chevrolet', 'Citroen', 'Dacia', 'Daihatsu', 'Dodge', 'Fiat', 'Ford', 'Honda',
                 'Hyundai', 'Isuzu', 'Iveco', 'Jeep', 'Kia', 'Land', 'Mazda', 'Mercedes', 'Mitsubishi', 'Nissan',
                 'Opel', 'Peugeot', 'Porsche', 'Renault', 'Seat', 'Skoda', 'SsangYong', 'Subaru', 'Suzuki', 'Toyota',
                 'Volkswagen', 'Volvo', "Vw", "Citroën", "Tesla", "Jaguar", "Mini", "Saab", "Lexus", "Infiniti", "Maserati",
                 'Chrysler', 'Alfa', 'Aston',"Fiat/", "Lancia", "Mercedes-Benz","Smart"]
    string = string.split()
    brands_cased = [brand.upper() for brand in car_array]
    for index,word in enumerate(string):
        if word.upper() in brands_cased:
            return ' '.join(string[:index]),' '.join(string[index:])

def create_header(title):
    Title = '<span style="font-size: 20px; font-weight: bold;">' + title + '</span><br><br>'
    return Title


def Category_lowering(nazwa_pliku):

    with open(nazwa_pliku, encoding='Utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)
        next(csv_reader)
        soup = BeautifulSoup('', 'lxml')
        count = 0
        id = 40907     #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   pierwszy wolny id   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        mapa = []
        for row in csv_reader:
            product_no = row[0]
            ean = row[1]
            marka = row[2]
            model = row[3]
            typ = row[4]
            year = row[5]
            cat_id = row[6]
            descr = row[7]
            # print(descr)
            price_brutto = row[8].replace('.','')
            price_netto = row[9]
            set = row[10]
            url = row[11]
            picture = row[12:16]
            # print(picture)

            weight = row[18]
            main_category = Split_cat(cat_id)[0]
            # print(main_category)
            marka_model = find_names(main_category)
            # print(marka_model)
            TITLE = Title_change(row[17],marka_model)
            # print(TITLE)
            # print(product_no)
            name, car = split_by_brand(TITLE)
            object = {
                "PRODUCT": {
                'PRODUCT_ID': id,
                'EAN': ean,
                "NUMBER": product_no,
                'TITLE_NO': wrapWithCdata(TITLE),
                "STOCK": Stock_update(row[1]),
                'CATEGORY_ID': main_category,
                'SUB_CATEGORY_ID': Split_cat(cat_id)[1],
                'DESCRIPTION_LONG_NO': wrapWithCdata(create_header(TITLE) + Tag_add(descr)),
                'PRICE': createNomaxPrice(price_brutto),
                'WEIGHT': weight,
                'PICTURES': create_images(picture),
                "DISCOUNT_GROUP": 51,
                "STATUS": 1,
                "DISABLE_ON_EMPTY": 1,
                "DELIVERY_ID": 4,
                "MANUFACTURER_ID": 2676,
                "PRICEINDEX_ANNONSFYND": 1,
                "PRICEINDEX_FACEBOOK": 1,
                "PRICEINDEX_GOOGLE_ADWORDS": 1,
                "PRICEINDEX_FB2019": 1,
                "PRICEINDEX_NORSKOPISY": 1,
                "PRICEINDEX_NOWY": 1,
                "GOOGLE_CATEGORY_ID": 2935,
                "SEO_TITLE_NO": "{} | {}".format(TITLE, "Nomax.no🥇"),
                "SEO_DESCRIPTION_NO": "{} {} {} {} {}".format("Kjøp Høy Kvalitet", name, "Til Din", car,"hos NOMAX.NO ✅ 2 - 5 Års Garanti ✅ Norges Beste Tilbud ✅ Sjekk Ut Nå❗."),
                "DELETE": 1
                            }}

            tag = dict2xml(object).replace('<PRODUCT>', '\n<PRODUCT>').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
            id += 1
            count += 1
            mapa.append(tag)
        print(colored("Liczba zapisanych produktów: ", "yellow"), count)
        return mapa


def wrapWithCdata(string):
    return "<![CDATA[" + string + "]]>"


plik_wsadowy = "Final_category_Luftfahrwerke - air suspension kit.csv"

plik_wyjsciowy = "Import_delete" + plik_wsadowy.replace(".csv", ".xml")

mapa1 = Category_lowering(plik_wsadowy)     # print(plik_wyjsciowy)

with open(plik_wyjsciowy, "w", encoding='utf-8') as f:
    f.write("<PRODUCTS>")
    for i in mapa1:
        f.write(str(i))
    f.write("\n</PRODUCTS>")
print(colored("Plik utworzony","blue"))

def execution_time(nowTime, startTime):
    show_time = (nowTime - startTime)
    minutes = show_time // 60
    show_time %= 60
    seconds = show_time
    print("Czas wykonania: %d:%d" % (minutes, seconds))


execution_time(time.time(), start_time)

