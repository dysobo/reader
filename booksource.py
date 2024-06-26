import requests
import json

class ReaderClient:
    def __init__(self, username, password, reader_url):
        self.username = username
        self.password = password
        self.reader_url = reader_url
        self.session = requests.Session()

    def login(self):
        url = f"{self.reader_url}/login"
        data = {"username": self.username, "password": self.password, "isLogin": True}
        headers = {"Content-Type": "application/json"}
        response = self.session.post(url, data=json.dumps(data), headers=headers)
        print(json.dumps(response.json(), sort_keys=True, indent=4))

    def get_book_sources(self, source_url):
        try:
            response = requests.get(source_url)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch book sources from {source_url}: {e}")
            return None

    def send_book_sources(self, source_url):
        data = self.get_book_sources(source_url)
        if data:
            url = f"{self.reader_url}/saveBookSources/"
            headers = {"Content-Type": "application/json"}
            response = self.session.post(url=url, headers=headers, json=data)
            print(response.json())

    def delete_book_sources(self):
        url = f"{self.reader_url}/deleteAllBookSources"
        response = self.session.post(url)
        print(response.json())

# 多个账号和书源地址，此处填写自己的账号和密码
accounts = [
    {"username": "user1", "password": "password1"},
    {"username": "user2", "password": "password2"}
]

book_source_urls = [
    "https://www.gitlink.org.cn/api/yi-c/yd/raw/sy.json?ref=master",
    "https://www.another-source.com/books.json"
]

reader_url = "http://192.168.0.39:7777/reader3"  # reader地址，此处可以填外网访问地址

for account in accounts:
    for source_url in book_source_urls:
        client = ReaderClient(account["username"], account["password"], reader_url)
        client.login()
        client.delete_book_sources()  # 删除原书源
        client.send_book_sources(source_url)
