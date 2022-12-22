from requests.api import request
import json


class ComplexRestConnector:
    login_uri = 'auth/login/'

    def __init__(self, address: str, username: str, password: str):

        response = request('post', address + '/' + self.login_uri, data={'login': username, 'password': password})
        response = json.loads(response.text)
        print(response)
        token = response['token']
        self.cookies = {
            'auth_token': 'Bearer ' + token
        }
        self.address = address

    def _get_full_url(self, url):
        return self.address + '/' + url

    def post(self, url, data):
        response = request('post', self._get_full_url(url), cookies=self.cookies, data=data)
        return json.loads(response.text)

    def get(self, url):
        response = request('get', self._get_full_url(url), cookies=self.cookies)
        return json.loads(response.text)

    def put(self, url, data):
        response = request('put', self._get_full_url(url), cookies=self.cookies, data=data)
        return json.loads(response.text)

    def delete(self, url):
        response = request('delete', self._get_full_url(url), cookies=self.cookies)
        return json.loads(response.text)