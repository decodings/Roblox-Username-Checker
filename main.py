import requests, threading, itertools

class Main:
    def __init__(self):
        with open('usernames.txt', 'r', encoding = 'UTF-8') as file:
            self.usernames = file.read().splitlines()
        self.usernamePool = itertools.cycle(self.usernames)

    def getCsrfToken(self):
        return requests.post('https://auth.roblox.com/').headers['x-csrf-token']

    def check(self):
        username = next(self.usernamePool)
        headers = {
            'x-csrf-token': self.getCsrfToken()
        }
        json = {
            'birthday': '2001-12-31T21:00:00.000Z',
            'context': 'Signup',
            'username': username
        }
        response = requests.post('https://auth.roblox.com/v1/usernames/validate', headers = headers, json = json)
        if response.json()['code'] == 1:
            print('\x1b[38;5;9m%s is taken.' % username)
        elif response.json()['code'] == 0:
            print('\x1b[38;5;33m%s is valid.' % username)
            with open('valid.txt', 'a+', encoding = 'UTF-8') as file:
                file.write('%s\n' % username)
        else:
            print(response.json())

    def run(self):
        for _ in range(len(self.usernames)):
            threading.Thread(target = self.check).start()

if __name__ == '__main__':
    Main().run()
