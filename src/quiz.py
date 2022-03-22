import requests
import json
from random import randint, shuffle
import html.parser
from get import dbQuery, dbInsertUpdate


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

def answer(id, correct):
  res = dbQuery('''SELECT * FROM visaAnswers WHERE id=?;''', (id,))
  if len(res) != 0:
    if correct:
      sql = '''UPDATE visaAnswers SET correct = correct + 1 WHERE id=?'''
    else:
      sql = '''UPDATE visaAnswers SET false = false + 1 WHERE id=?'''
    dbInsertUpdate(sql, (id,))
  else:
    if correct:
      sql = '''INSERT INTO visaAnswers VALUES (?,?,?)'''
      params = (id, 1, 0)
    else:
      sql = '''INSERT INTO visaAnswers VALUES (?,?,?)'''
      params = (id, 0, 1)
    dbInsertUpdate(sql, params)

def stats(id):
  res = dbQuery('''SELECT * FROM visaAnswers WHERE id=?;''', (id,))
  if len(res) != 0:
    correct = res[0][1]
    false = res[0][2]
    prct = correct / (correct+false) * 100
    stats = f' on vastannut oikein {prct}%:iin kysymyksistä!\nOikein: {correct}\nVäärin: {false}\n'
  else:
    stats = False
  return stats