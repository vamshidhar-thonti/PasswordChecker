import requests
from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = pwned_api_check(str(request.form['password']))
        if int(data) == 0:
            result = 'Your password hasn\'t been breached. \N{smiling face with sunglasses}'
        else:
            result = f'Your password has been exposed {data} times. \N{confused face}'
        return render_template('index.html', result=result)
    else:
        return 'Something went wrong! :('


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char  # C6008F9CAB4083784CBD1874F76618D2A97
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check=''):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

# if __name__ == '__main__':
# for password in input('Enter the password you want to check: ').split():
#     count = pwned_api_check(password)
#     if count:
#         print(f'{password} was found {count} times... you should probably change your password')
#     else:
#         print(f'{password} was not found. You can use this password!! :)')
