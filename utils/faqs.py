import requests
from bs4 import BeautifulSoup


def get_swinburne_faqs():
    response = requests.get('https://www.swinburneonline.edu.au/faqs/')
    soup = BeautifulSoup(response.content, 'html.parser')
    # get faq cards
    faqs_cards = soup.select('.faqs-group .card')
    result = []
    # loop through and get questions and answers
    for faq in faqs_cards:
        question_el = faq.select_one('.card-header h5 > div:nth-child(2)')
        answer_el = faq.select_one('.card-body .content')
        # add to result if question and answer exist
        if question_el and answer_el:
            question = question_el.get_text(strip=True, separator=' ')
            answer = answer_el.get_text(strip=True, separator=' ')
            result.append((question, answer))
    return result

def get_monash_faqs():
    response = requests.get('https://online.monash.edu/faqs/')
    soup = BeautifulSoup(response.content, 'html.parser')
    faqs_cards = soup.select('.faqs-group .card')
    result = []
    # loop through and get questions and answers
    for faq in faqs_cards:
        question_el = faq.select_one('.card-header h5')
        answer_el = faq.select_one('.card-body')
        # add to result if question and answer exist
        if question_el and answer_el:
            question = question_el.get_text(strip=True, separator=' ')
            answer = answer_el.get_text(strip=True, separator=' ')
            result.append((question, answer))
    return result

def get_rmit_faqs():
    response = requests.get('https://www.rmit.edu.au/study-with-us/applying-to-rmit/frequently-asked-questions')
    soup = BeautifulSoup(response.content, 'html.parser')
    faqs_cards = soup.select('.accordion-group .accordion-default')
    result = []
    # loop through and get questions and answers
    for faq in faqs_cards:
        question_el = faq.select_one('.accordion-heading h3')
        answer_el = faq.select_one('.accordion-body .content p')
        # add to result if question and answer exist
        if question_el and answer_el:
            question = question_el.get_text(strip=True, separator=' ')
            answer = answer_el.get_text(strip=True, separator=' ')
            result.append((question, answer))
    return result
