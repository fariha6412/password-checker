import requests
import hashlib


def request_api_data(query_char):
    """gets api response"""
    try:
        url = 'https://api.pwnedpasswords.com/range/' + query_char
        res = requests.get(url)
        if res.status_code != 200:
            raise RuntimeError(f'Error :{res.status_code}, check the api')
        return res
    except TypeError as err:
        raise RuntimeError(f'Error : give a string as a password')


def get_pwned_api_count(response, pass_tail):
    """returns how many times your password was pwned"""
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == pass_tail:
            return count
    return 0


def pwned_api_check(password):
    """checks if password exits in api response and prints it's pwned status"""
    sha1password = hashlib.sha1(password.encode()).hexdigest().upper()
    pass_head, pass_tail = sha1password[:5], sha1password[5:]
    response = request_api_data(pass_head)
    count = get_pwned_api_count(response, pass_tail)
    if count:
        print(f'{password} was found {count} times. You should change it!')
    else:
        print(f'{password} was not found. Carry on!')
