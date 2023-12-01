import json
import requests
import urllib
import Format_Manager

filename = 'apis/telegramID.txt'

with open(filename) as f:
    IDS = f.read().splitlines()

chat_id = str(IDS[0])
TOKEN = str(IDS[1])
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

class Message_Receiver:
    def __init__(self, text, last_update_id):
        self.text = text
        self.last_update_id = last_update_id

    
    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content
    
    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js
    
    def get_updates(self, offset=None):
        url = URL + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js
    
    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)
    
    def get_last_chat_id_and_text(self, updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)
    
    def send_message(self, text):
        text = Format_Manager.capitalise_word(text)
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        self.get_url(url)
        
    def send_image(self, image_file):
        files = {'photo': open(image_file, 'rb')}
        status = requests.post(URL + "sendPhoto?chat_id=" + chat_id, files=files) 
        return
    
    def send_video(self, video_file):
        files = {'video': open(video_file, 'rb')}
        status = requests.post(URL + "sendVideo?chat_id=" + chat_id, files=files) 
        return

    def get_response(self):
        print("Entering get response")
        updates = self.get_updates(self.last_update_id)
        print(f"Update ID = {self.last_update_id}")
        if len(updates["result"]) > 0:
            print("Update found")
            self.last_update_id = self.get_last_update_id(updates) + 1
            print(f"Update ID = {self.last_update_id}")
            self.text = updates["result"][0]["message"]["text"]
            print(f'Received update - {updates["result"][0]["message"]["text"]}')
        else:
            self.text = ''
        self.text = Format_Manager.lowercase_word(self.text)
        print(f"Leaving get response with text: {self.text}")
        return self.text
    
    
    def get_confirmation(self, Octavius_Vocab):
    
        response = self.get_response()

        if response in Octavius_Vocab.affirmativelist:
            return True
        else:
            return False





def generate_receiver():
    Octavius_Receiver = Message_Receiver("", None)
    return Octavius_Receiver