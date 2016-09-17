from config import *
from urllib.parse import parse_qs
import webbrowser
import pickle
from datetime import datetime, timedelta
import vk


class Integration:
    access_token = None
    user_id = None
    api = None

    def __init__(self):
        self.get_saved_auth_params()
        if not self.access_token or not self.user_id:
            self.access_token, self.user_id = self.get_auth_params()
        self.api = self.get_api()

    def get_saved_auth_params(self):
        with open(authFile, 'rb') as pkl_file:
            token = pickle.load(pkl_file)
            expires = pickle.load(pkl_file)
            uid = pickle.load(pkl_file)
        if datetime.now() < expires:
            self.access_token = token
            self.user_id = uid

    def get_auth_params(self):
        auth_url = ("https://oauth.vk.com/authorize?client_id={app_id}"
                    "&scope=wall,messages&redirect_uri=http://oauth.vk.com/blank.html"
                    "&display=page&response_type=token".format(app_id=appID))
        webbrowser.open_new_tab(auth_url)
        redirected_url = input("Paste here url you were redirected:\n")
        aup = parse_qs(redirected_url)
        aup['access_token'] = aup.pop(
            'https://oauth.vk.com/blank.html#access_token')
        self.save_auth_params(aup['access_token'][0], aup['expires_in'][0],
                              aup['user_id'][0])
        return aup['access_token'][0], aup['user_id'][0]

    def save_auth_params(self, expires_in, user_id):
        expires = datetime.now() + timedelta(seconds=int(expires_in))
        with open(authFile, 'wb') as output:
            pickle.dump(self.access_token, output)
            pickle.dump(expires, output)
            pickle.dump(user_id, output)

    def get_api(self):
        session = vk.Session(access_token=self.access_token)
        return vk.API(session)

    def get_unreadable_message(self):
        print(self.api.messages.get(filters=1))

    def send_message(self, user_id, message, **kwargs):
        data_dict = {
            'user_id': user_id,
            'message': message,
        }
        data_dict.update(**kwargs)
        return self.api.messages.send(**data_dict)
