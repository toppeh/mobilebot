import requests
import json
from random import randint, shuffle
import html.parser


def getQuizQuestion():
  url = 'https://opentdb.com/api.php?amount=1&type=multiple'
  response = requests.get(url, timeout=4)
  quiz = json.loads(response.text)
  quiz = setAllAnswers(quiz['results'][0])
  return(quiz)

def setAllAnswers(quiz):
  #  convert object to dict and set all answers
  html_parser = html.parser.HTMLParser()
  index = randint(0, 3)
  ret = dict()
  ret['question'] = html_parser.unescape(quiz['question'])
  ret['all_answers'] = list()
  for answer in quiz['incorrect_answers']:
    ret['all_answers'].append(html_parser.unescape(answer))
  shuffle(ret['all_answers']) # shuffle so if the answers are all numbers the correct one wont stand out 
  ret['all_answers'].insert(index, html_parser.unescape(quiz['correct_answer']))
  ret['correct_answer_index'] = index
  return ret