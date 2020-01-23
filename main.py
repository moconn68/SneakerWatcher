import requests
import os
from bs4 import BeautifulSoup
from twilio.rest import Client
from shoe import Shoe
import config


def send_sms(message):
    try:
        twilio_sid = os.environ['TWILIO_ACCOUNT_SID']
    except KeyError:
        twilio_sid = config.TWILIO_ACCOUNT_SID
    try:
        twilio_token = os.environ['TWILIO_ACCOUNT_AUTH_TOKEN']
    except KeyError:
        twilio_token = config.TWILIO_ACCOUNT_AUTH_TOKEN
    try:
        sending_phone = os.environ['SENDING_PHONE']
    except KeyError:
        sending_phone = config.SENDING_PHONE
    try:
        receiving_phone = os.environ['RECEIVING_PHONE']
    except KeyError:
        receiving_phone = config.RECEIVING_PHONE
    try:
        twilio_client = Client(twilio_sid, twilio_token)
    except:
        return 1, "Error initializing Twilio client - please verify your credentials."
    try:
        twilio_client.messages.create(to=receiving_phone,
                                  from_=sending_phone,
                                  body=message)
    except:
        return 1, "Error sending message - please verify phone number(s)."
    print("MESSAGE DELIVERED")
    return 0, None


def main():
    shoes = []
    shoes.append(
        Shoe("Yeezreel RF Size 12", "https://stockx.com/adidas-yeezy-boost-350-v2-yeezreel-reflective?size=12", 350))
    shoes.append(
        Shoe("Yeezreel RF Size 13", "https://stockx.com/adidas-yeezy-boost-350-v2-yeezreel-reflective?size=13", 350))
    shoes.append(Shoe("Yechiel NRF Size 12.5", "https://stockx.com/adidas-yeezy-boost-350-v2-yecheil?size=12.5", 350))

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', }

    message = ""
    for shoe in shoes:
        res = requests.get(shoe.url, headers=headers)
        parser = BeautifulSoup(res.text, features="html.parser")
        shoe.price = parser.find('div', attrs={'class': 'sale-value'}).text
        # print("Name: {}\tPrice: {}\n".format(shoe.name, shoe.price))
        message = message + "Name: {}\tPrice: {}\n".format(shoe.name, shoe.price)

    # message = message + "SENT ON AWS"
    return send_sms(message)


if __name__ == "__main__":
    main()
