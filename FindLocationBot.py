import googlemaps
import webbrowser
from geopy.geocoders import Nominatim
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from credits import bot_token
import googlemaps
import pandas as pd
import time
import json
need_to_do = "1.- The bot should provide information about the nearest establishments within the user-specified radius in kilometers."
print(need_to_do)
kilometers = 0
bot = Bot(token=bot_token)
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
commandlist = "1-/start,2-for second function send your geolocation"
searchplace = ""
searchplace_name = ""
def start(update, context):
    context.bot.send_message(update.effective_chat.id,need_to_do)
#тут мы делаем систему расщетов киломаетра чтобы считала таким образом растояние в гугл мап от указаной геолокацие
def kilometers_to_meters(kilometers):
    try:
        return kilometers * 1_000
    except:
        return 0

def info_loc_kilometers(update,context):
    global kilometers
    if len(context.args) == 1:
        print(int(context.args[0]))
        kilo = int(context.args[0])

def info_loc_place(update,context):
    global searchplace
    if len(context.args) == 1:
        place = str(context.args[0])
        
    elif len(context.args) == 2:
        place = str(context.args[0],context.args[1])
        searchplace = place
    elif len(context.args) == 3:
        place = str(context.args[0],context.args[1],context.args[2])

    elif len(context.args) == 4:
        place = str(context.args[0],context.args[1],context.args[2],context.args[3])

    elif len(context.args) == 5:
        place = str(context.args[0],context.args[1],context.args[2],context.args[3],context.args[4])

def info_loc_place_name(update,context):
    global searchplace_name
    if len(context.args) == 1:
        place_name = str(context.args[0])

        
    elif len(context.args) == 2:
        place_name = str(context.args[0],context.args[1])
        searchplace_name = place_name
    elif len(context.args) == 3:
        place_name = str(context.args[0],context.args[1],context.args[2])
        searchplace_name = place_name
    elif len(context.args) == 4:
        place_name = str(context.args[0],context.args[1],context.args[2],context.args[3])
        searchplace_name = place_name
    elif len(context.args) == 5:
        place_name = str(context.args[0],context.args[1],context.args[2],context.args[3],context.args[4])
        searchplace_name = place_name
def get_location1(update,context):
    global kilometers
    global searchplace_name
    global searchplace
    #принимаем апи код чтобы с помощью него можно была взять ифну от гугл мап
    map_client = googlemaps.Client("AIzaSyCDcfVulM_ctVR-UCceyL6LtlnXcFZxTAE")
    # берем инфу о долготе и широте нахождение пользывателя
    loc1 = Nominatim(user_agent="GetLoc")
    latlng1 = update.message.location
    # тут мы делаем из инфу пользывателя и широте и долготе строковый вид чтобы бпотом геокодер смог принять это инфу так как инт и лист классы(подразделение) и другие он не принимает
    geo_loc1 = str(latlng1["latitude"]) + "," + str(latlng1["longitude"])
    getLoc1 = loc1.geocode(geo_loc1)
    print(geo_loc1)
    
    
    # printing address
    print("address:",getLoc1.address)
    print("Latitude = ", getLoc1.latitude, "\n")
    print("Longitude = ", getLoc1.longitude)
    location = (geo_loc1)
    
    first_messge = update.message.text
    second_messge = update.message.text
    third_messge = update.message.text
    context.bot.send_message(update.effective_chat.id,"enter /place .... after /place .... after place_name ... ")
    kilometers = info_loc_kilometers
    searchplace = info_loc_place
    searchplace_name = info_loc_place_name
    search_string = searchplace
    distance = kilometers_to_meters(kilometers)
    business_list = []
 
    response = map_client.places_nearby(
        location=location,
        keyword=search_string,
        name=searchplace_name,
        radius=distance
    )
    business_list.extend(response.get('results'))
    next_page_token = response.get('next_page_token')
 
    while next_page_token:
        time.sleep(2)
        response = map_client.places_nearby(
        location=location,
        keyword=search_string,
        name=searchplace_name,
        radius=distance,
        page_token=next_page_token
        )
        business_list.extend(response.get('results'))
        next_page_token = response.get('next_page_token')
    
    df = pd.DataFrame(business_list)
    geo = df.to_dict()
    #выводим места на принте
    print(df['vicinity'])
    print(geo)
    perem = df.to_json()
    perem = json.loads(perem)
    str_send = json.dumps(perem['vicinity'], ensure_ascii=False)
    #скрешиваем юрл с местам чторбы таким образом нормально находила нужное места
    df['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df['place_id']
    #кладем инфу в эксель файл
    df.to_excel('places list.xlsx',index=False)
    # выводим инфу к боту в телеграм
    context.bot.send_message(update.effective_chat.id,str_send)
    
def commands(update,context):
    context.bot.send_message(update.effective_chat.id,"спиксок комманд:" + commandlist)
start_handler = CommandHandler('start', start)
find_handler = CommandHandler('find', find)


get_location1_handler = MessageHandler(Filters.location,get_location1)
commands_handler = CommandHandler('commands',commands)
info_loc_place_handler = CommandHandler('place',info_loc_place)
info_loc_place_name_handler = CommandHandler('place_name',info_loc_place_name)
info_loc_kilomaters_handler = CommandHandler('kilometers',info_loc_kilometers)





dispatcher.add_handler(start_handler)
dispatcher.add_handler(find_handler)
dispatcher.add_handler(commands_handler)
dispatcher.add_handler(info_loc_place_handler)
dispatcher.add_handler(info_loc_place_name_handler)
dispatcher.add_handler(info_loc_kilomaters_handler)
dispatcher.add_handler(get_location1_handler)
updater.start_polling()
updater.idle()






# calling the Nominatim tool
#loc = Nominatim(user_agent="GetLoc")
 
# entering the location name
#getLoc = loc.geocode("31.3868117,37.3197863")
 
# printing address
#print(getLoc.address)
 
#printing latitude and longitude
#print("Latitude = ", getLoc.latitude, "\n")
#print("Longitude = ", getLoc.longitude)


#def get_location(update,context):
#    loc = Nominatim(user_agent="GetLoc")
#    latlng = update.message.location
#    geo_loc = str(latlng["latitude"]) + "," + str(latlng["longitude"])
#    print(geo_loc)
#    getLoc = loc.geocode(geo_loc)
    
    # printing address
#    print("address:",getLoc.address)
#    print("Latitude = ", getLoc.latitude, "\n")
#    print("Longitude = ", getLoc.longitude)
#get_location_handler = MessageHandler(Filters.location,get_location)
#dispatcher.add_handler(get_location_handler)


















# import googlemaps
# import webbrowser
# from geopy.geocoders import Nominatim
# from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
# from credits import bot_token
# import googlemaps
# import pandas as pd
# import time
# import json
# need_to_do = "1.-бот должен будет писать ближайшие заведение в радиусе километров заполнеными пользывателем"
# print(need_to_do)
# 
# bot = Bot(token=bot_token)
# updater = Updater(token=bot_token, use_context=True)
# dispatcher = updater.dispatcher
# commandlist = "1-/start,2-для воторйой функцие оправте свою геопозицию"
# 
# def start(update, context):
#     context.bot.send_message(update.effective_chat.id,need_to_do)
# def find(update,context):
#     url = 'https://www.google.com/maps/place/'
#     space = "-"
#     if len(context.args) == 1:
#         arg1 = context.args[0]
#         url_address = url + arg1
#         print("the url address:",url_address)
#         context.bot.send_message(update.effective_chat.id,"the url adress in google map:" + url_address)
#     if len(context.args) == 2:
#         arg1 = context.args[0]
#         arg2 = context.args[1]
#         url_address = url + arg1 + space + arg2
#         print("the url address:",url_address)
#         context.bot.send_message(update.effective_chat.id,"the url adress in google map:" + url_address)
#     if len(context.args) == 3:
#         arg1 = context.args[0]
#         arg2 = context.args[1]
#         arg3 = context.args[2]
#         url_address = url + arg1 + space + arg2 + space + arg3
#         print("the url address:",url_address)
#         context.bot.send_message(update.effective_chat.id,"the url adress in google map:" + url_address)
#     if len(context.args) == 4:
#         arg1 = context.args[0]
#         arg2 = context.args[1]
#         arg3 = context.args[2]
#         arg4 = context.args[3]
#         url_address = url + arg1 + space + arg2 + space + arg3 + space + arg4
#         print("the url address:",url_address)
#         context.bot.send_message(update.effective_chat.id,"the url adress in google map:" + url_address)
#     if len(context.args) == 5:
#         arg1 = context.args[0]
#         arg2 = context.args[1]
#         arg3 = context.args[2]
#         arg4 = context.args[3]
#         arg5 = context.args[4]
#         url_address = url + arg1 + space + arg2 + space + arg3 + space + arg4 + space + arg5
#         print("the url address:",url_address)
#         context.bot.send_message(update.effective_chat.id,"the url adress in google map:" + url_address)
#     if len(context.args) == 6:
#         arg1 = context.args[0]
#         arg2 = context.args[1]
#         arg3 = context.args[2]
#         arg4 = context.args[3]
#         arg5 = context.args[4]
#         arg6 = context.args[5]
#         url_address = url + arg1 + space + arg2 + space + arg3 + space + arg4 + space + arg5 + space + arg6
#         print("the url address:",url_address)
#         context.bot.send_message(update.effective_chat.id,"the url adress in google map:" + url_address)
#     if len(context.args) == 7:
#         arg1 = context.args[0]
#         arg2 = context.args[1]
#         arg3 = context.args[2]
#         arg4 = context.args[3]
#         arg5 = context.args[4]
#         arg6 = context.args[5]
#         arg7 = context.args[6]
#         url_address = url + arg1 + space + arg2 + space + arg3 + space + arg4 + space + arg5 + space + arg6 + space + arg7
#         print("the url address:",url_address)
#         context.bot.send_message(update.effective_chat.id,"the url adress in google map:" + url_address)
#     if len(context.args) == 8:
#         arg1 = context.args[0]
#         arg2 = context.args[1]
#         arg3 = context.args[2]
#         arg4 = context.args[3]
#         arg5 = context.args[4]
#         arg6 = context.args[5]
#         arg7 = context.args[6]
#         arg8 = context.args[7]
#         url_address = url + arg1 + space + arg2 + space + arg3 + space + arg4 + space + arg5 + space + arg6 + space + arg7 + space + arg8
#         print("the url address:",url_address)
#         context.bot.send_message(update.effective_chat.id,"the url adress in google map:" + url_address)
#     if len(context.args) == 9:
#         arg1 = context.args[0]
#         arg2 = context.args[1]
#         arg3 = context.args[2]
#         arg4 = context.args[3]
#         arg5 = context.args[4]
#         arg6 = context.args[5]
#         arg7 = context.args[6]
#         arg8 = context.args[7]
#         arg9 = context.args[8]
#         url_address = url + arg1 + space + arg2 + space + arg3 + space + arg4 + space + arg5 + space + arg6 + space + arg7 + space + arg8 + space + arg9
#         print("the url address:",url_address)
#         context.bot.send_message(update.effective_chat.id,"the url adress in google map:" + url_address)
#     if len(context.args) == 10:
#         arg1 = context.args[0]
#         arg2 = context.args[1]
#         arg3 = context.args[2]
#         arg4 = context.args[3]
#         arg5 = context.args[4]
#         arg6 = context.args[5]
#         arg7 = context.args[6]
#         arg8 = context.args[7]
#         arg9 = context.args[8]
#         arg10 = context.args[9]
#         url_address = url + arg1 + space + arg2 + space + arg3 + space + arg4 + space + arg5 + space + arg6 + space + arg7 + space + arg8 + space + arg9 + space + arg10
#         print("the url address:",url_address)
#         context.bot.send_message(update.effective_chat.id,"the url adress in google map:" + url_address)
# 
# def kilometers_to_meters(kilometers):
#     try:
#         return kilometers * 1_000
#     except:
#         return 0
# #AIzaSyCDcfVulM_ctVR-UCceyL6LtlnXcFZxTAE
# 
# #API_KEY = open('API_KEY.txt','r').read()
# #print("the api key:",API_KEY)
# def get_location1(update,context):
#     map_client = googlemaps.Client("AIzaSyCDcfVulM_ctVR-UCceyL6LtlnXcFZxTAE")
#     loc1 = Nominatim(user_agent="GetLoc")
#     latlng1 = update.message.location
#     geo_loc1 = str(latlng1["latitude"]) + "," + str(latlng1["longitude"])
#     getLoc1 = loc1.geocode(geo_loc1)
#     print(geo_loc1)
# 
# 
#     # printing address
#     print("address:",getLoc1.address)
#     print("Latitude = ", getLoc1.latitude, "\n")
#     print("Longitude = ", getLoc1.longitude)
#     location = (geo_loc1)
# 
#     first_messge = update.message.text
#     second_messge = update.message.text
#     third_messge = update.message.text
#     searchplace = input("enter what are you finding:")
#     searchplace_name = input("enter name of place that you finding:")
#     kilometers = int(input("enter how much kilometers:"))
#     search_string = searchplace
#     distance = kilometers_to_meters(kilometers)
#     business_list = []
# 
#     response = map_client.places_nearby(
#         location=location,
#         keyword=search_string,
#         name=searchplace_name,
#         radius=distance
#     )
#     business_list.extend(response.get('results'))
#     next_page_token = response.get('next_page_token')
# 
#     while next_page_token:
#         time.sleep(2)
#         response = map_client.places_nearby(
#         location=location,
#         keyword=search_string,
#         name=searchplace_name,
#         radius=distance,
#         page_token=next_page_token
#         )
#         business_list.extend(response.get('results'))
#         next_page_token = response.get('next_page_token')
# 
#     df = pd.DataFrame(business_list)
#     geo = df.to_dict()
#     print("places",df['vicinity'])
# 
#     perem = df.to_json()
#     perem = json.loads(perem)
#     str_send = json.dumps(perem['vicinity'], ensure_ascii=False)
#     df['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df['place_id']
#     df.to_excel('places list.xlsx',index=False)
# 
#     context.bot.send_message(update.effective_chat.id,str_send)
# 
# def commands(update,context):
#     context.bot.send_message(update.effective_chat.id,"спиксок комманд:" + commandlist)
# start_handler = CommandHandler('start', start)
# find_handler = CommandHandler('find', find)
# 
# 
# get_location1_handler = MessageHandler(Filters.location,get_location1)
# commands_handler = CommandHandler('commands',commands)
# 
# 
# 
# 
# 
# 
# dispatcher.add_handler(start_handler)
# dispatcher.add_handler(find_handler)
# dispatcher.add_handler(commands_handler)
# 
# dispatcher.add_handler(get_location1_handler)
# updater.start_polling()
# updater.idle()