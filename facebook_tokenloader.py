import re
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
import requests


def parse_auth(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    script_content = soup.find(type="text/javascript").string
    access_token_string = re.search('access_token=[a-zA-Z0-9]*&', script_content).group(0)
    access_token_string_modified = re.search('[a-zA-Z0-9]*&', access_token_string).group(0)
    access_token_string_final = re.search('[a-zA-Z0-9]*', access_token_string_modified).group(0)

    return access_token_string_final


def get_xauth_token(long_token):
    """Retrieves the XAuthToken using the access_token_string"""
    USER_AGENT = "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)"

    HEADERS = {
        'app_version': '6.9.4',
        'platform': 'ios',
        "content-type": "application/json",
        "User-agent": USER_AGENT,
        "Accept": "application/json"
    }

    new_url = 'https://api.gotinder.com/v2/auth/login/facebook'
    new_data = {"token": long_token}
    r_new = requests.post(new_url, headers=HEADERS, json=new_data)

    return r_new.json()


def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(
        "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&client_id=464891386855067&ret=login&fallback_redirect_uri=221e1158-f2e9-1452-1a05-8983f99f7d6e&ext=1556057433&hash=Aea6jWwMP_tDMQ9y")

    input("press enter once you logged in")
    long_token = parse_auth(driver.page_source)
    driver.close()
    xauth = get_xauth_token(long_token)['data']['api_token']
    print(f"\nXAuthToken: {xauth}")


if __name__ == '__main__':
    main()
