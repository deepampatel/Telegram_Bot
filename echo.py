import json
import requests
import time
import urllib
from dbhelper import DBHelper

db = DBHelper()
movie_key='your movie key'
key_ow = 'your weather api key'
TOKEN = "your bot access token"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        str1 = update["message"]["text"]
        str2 = str1.split(' ', 1)
        if str2[0] == "#movie":
            try:
                keymovie = str2[1]
                url11 = (
                'https://api.themoviedb.org/3/search/movie?api_key={}&query='.format(movie_key) + keymovie)
                url222 = url11.replace(" ", "%20")
                f = urllib.request.urlopen(url222)
                json_string = f.read()
                obj_json = json.loads(json_string.decode())
                title = obj_json['results'][0]['original_title']
                overview = obj_json['results'][0]['overview']
                release_date = obj_json['results'][0]['release_date']
                average_vote = obj_json['results'][0]['vote_average']
                text = "Title:{}\nOverview:{}\nRelease Date:{}\nVote:{}".format(title, overview, release_date,
                                                                                average_vote)
                chat = update["message"]["chat"]["id"]
                send_message(text, chat)
            except:
                chat = update["message"]["chat"]["id"]
                send_message("Sorry,no movie match found!", chat)
        elif str2[0] == "#weather":
            try:
                city = str2[1]
                url1 = ('http://api.openweathermap.org/data/2.5/weather?q=' + city + ',in&appid=' + key_ow)
                f = urllib.request.urlopen(url1)
                json_var1 = f.read()
                obj1_json = json.loads(json_var1.decode())
                temper = (obj1_json['main']['temp'])
                temper = temper - 273.15
                wind = (obj1_json['wind']['speed'])
                pres = (obj1_json['main']['pressure'])
                humi = (obj1_json['main']['humidity'])
                name = (obj1_json['name'])
                text = "City:{}\nTemperature:{}°C\nWindspeed:{}m/s\nPressure:{}hpa\nHumidity:{}%".format(name,
                                                                                                         round(temper,
                                                                                                               2), wind,
                                                                                                         pres, humi)
                chat = update["message"]["chat"]["id"]
                send_message(text, chat)
            except:
                chat = update["message"]["chat"]["id"]
                send_message("Sorry,no weather results found!", chat)
        elif str2[0] == 'Help':
            chat = update["message"]["chat"]["id"]
            text = "You can search for movie info by sending #movie movie_name,similarly you can get weather results by sending #weather city_name."
            send_message(text, chat)
        else:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            items = db.get_items(chat)
            if text == "/done":
                keyboard = build_keyboard(items)
                send_message("Select an item to delete", chat, keyboard)
            elif text == "/start":
                send_message(
                    "Welcome to your personal To Do list. Send any text to me and I'll store it as an item. Send /done to remove items",
                    chat)
            elif text in items:
                db.delete_item(text, chat)
                items = db.get_items(chat)
                keyboard = build_keyboard(items)
                send_message("Select an item to delete", chat, keyboard)
            else:
                db.add_item(text, chat)
                items = db.get_items(chat)
                message = "\n".join(items)
                send_message(message, chat)

def build_keyboard(items):
    keyboard = [[item] for item in items]
    ReplyKeyboardMarkup = {'keyboard': keyboard, 'one_time_keyboard': True}
    return json.dumps(ReplyKeyboardMarkup)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, ReplyKeyboardMarkup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if ReplyKeyboardMarkup is not None:
        url += "&ReplyKeyboardMarkup={}".format(ReplyKeyboardMarkup)
    get_url(url)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.01)


if __name__ == '__main__':
    main()
