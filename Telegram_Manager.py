import json
import requests
import urllib
from time import time, ctime, sleep




class Message_Receiver:
    def __init__(self, directory):
        self.text = ""
        self.last_update_id = None
        self.chatID, self.URL = self.Get_Tokens(directory)

    def Get_Tokens(self, directory):
        filename = 'telegramID.txt'
        with open(f'{directory}/apis/{filename}') as f:
            IDS = f.read().splitlines()
        chat_id = str(IDS[0])
        TOKEN = str(IDS[1])
        URL = "https://api.telegram.org/bot{}/".format(TOKEN)
        return chat_id, URL


    def Get_URL(self, update_url):
        response = requests.get(update_url)
        content = response.content.decode("utf8")
        return content

    def Get_JSON_From_URL(self, update_url):
        content = self.Get_URL(update_url)
        js = json.loads(content)
        return js

    def Get_Updates(self, offset=None):
        update_url = self.URL + "getUpdates?timeout=100"
        if offset:
            update_url += "&offset={}".format(offset)
        js = self.Get_JSON_From_URL(update_url)
        return js

    def Get_Last_Update_ID(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def Send_Message(self, text):

        try:
            print(ctime() + " - Sending Message - " + text)
            text = urllib.parse.quote_plus(text)
            send_url = self.URL + "sendMessage?text={}&chat_id={}".format(text, self.chatID)
            self.Get_URL(send_url)
            return True

        except Exception as e:
            print(f"{ctime()} - Error reaching URL, cannot send message")
            print(e)
            return False

    def Get_Response(self):
        self.text = ""
        try:
            updates = self.Get_Updates(self.last_update_id)

            if len(updates["result"]) is not None:

                if len(updates["result"]) > 0:

                    self.last_update_id = int(updates["result"][0]["update_id"])

                    print(ctime() + " - Received Update")
                    # print(updates)

                    date_time = int(str(time()).split(".")[0])
                    time_since_message = updates["result"][0]["message"]["date"] - date_time
                    self.last_update_id = self.Get_Last_Update_ID(updates) + 1

                    if abs(time_since_message) < 20:
                        self.text = updates["result"][0]["message"]["text"]
                        print(ctime() + ' - Update Text - "' + self.text + '"')

                    else:
                        print(ctime() + " - Message timed out")

            return self.text

        except Exception as e:
            print("Caught exception")
            try:
                if str(updates["error_code"]) == str(409):
                    print("Is 409 error")
                    exit()

            except:
                pass
            print(f"{ctime()} - Error reaching URL, cannot get updates")
            print(e)
            self.text = ''
            sleep(5)
            return self.text


def generate_receiver(directory):
    Octavius_Receiver = Message_Receiver(directory)
    return Octavius_Receiver
