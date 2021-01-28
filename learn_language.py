import os
import requests
import json
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from keys import IBM_WATSON_API_URL, IBM_WATSON_API_KEY, SENDGRID_API_KEY, FROM_EMAIL, TO_EMAILS
from config import num_words_per_day, learn_language, language_mapping


def translate(language, text):
    
    language_code = language_mapping.get(language.lower())
    
    if language_code is None:
        raise ValueError(f"The language entered {language} is not recognised.")
    
    model_id = 'en-' + language_code
    
    url = f"{IBM_WATSON_API_URL}/v3/translate?version=2018-05-01"
    
    payload = json.dumps({"text": text, "model_id": model_id})
    
    response = requests.post(url,
                             auth=("apikey", IBM_WATSON_API_KEY),
                             headers={'Content-Type': 'application/json'},
                             data=payload)
    
    if response.status_code != 200:
        raise Exception(f"There was an error while making the request {response.content}")
    
    results = response.json()
    
    return results["translations"]


def get_random_words(num_words):
    words = []
    with open('learn_words.txt') as file:
        for word in file:
            words.append(word.strip())
    
    random_words = []
    for i in range(num_words):
        random_words.append(random.choice(words))
    
    return random_words


def get_email_content(language, words, translations):
    email_body = f"<strong> Your {len(words)} {language.title()} words for today are: </strong> <br />"
    for english_word, translation_dict in zip(words, translations):
        email_body = email_body + f"{english_word.title()}  -  {translation_dict['translation'].title()} <br/>"
    
    email_subject = f"Your {len(words)} {language.title()} words for today!"
    
    return email_subject, email_body


def send_email(from_email, to_emails, subject, body):
    
    message = Mail(
    from_email=from_email,
    to_emails=to_emails,
    subject=subject,
    html_content=body)
    
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    
    response = sg.send(message)
    
    print(response.status_code, response.body)

    
def main(num_words_per_day, learn_language):
    random_words = get_random_words(num_words_per_day)
    translations = translate(learn_language, random_words)
    subject, body = get_email_content(learn_language, random_words, translations)
    send_email(FROM_EMAIL, TO_EMAILS, subject, body)
    
if __name__ == '__main__':
    main(num_words_per_day,learn_language)
    
    




