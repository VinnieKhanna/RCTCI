import pandas as pd
from tqdm import tqdm
import time

""" You may need to use pip install pyppdf if
you get an error asking to install Chromium
"""
# import pyppdf.patch_pyppeteer

### Data Collection

import time
import requests
import json

htmlText = requests.get('https://leetcode.com/api/problems/algorithms/').text
problemData = json.loads(htmlText)
problems = problemData['stat_status_pairs']
cleaned_problems = []
for problem in problems:
  cleaned_problem = {}
  cleaned_problem['id'] = problem['stat']['question_id']
  cleaned_problem['title'] = problem['stat']['question__title']
  cleaned_problem['title_slug'] = problem['stat']['question__title_slug']
  cleaned_problem['difficulty'] = problem['difficulty']['level']
  if not problem['paid_only']:
    cleaned_problems.append(cleaned_problem)

df = pd.DataFrame(reversed(cleaned_problems))
df.set_index('id', inplace=True)


### SELENIUM FOR PROBLEM DESCRIPTIONS

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

tqdm.pandas()

def get_and_render(row):
  time.sleep(3)
  driver.get('https://leetcode.com/problems/' + row['title_slug'])
  delay = 20
  try:
    # WAIT TILL CONTENT IS LOADED
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'question-content__JfgR')))
    print("Page is ready!")
  except TimeoutException:
    print("Loading took too much time!")
    return "<timed out, manual entry>"

  html = driver.page_source
  html = html[html.find('content__u3I1 question-content__JfgR'):]
  problem = html[html.find('div'): html.find('/div')]
  print(problem)
  return problem

def get_and_render_topics(row):
  time.sleep(3)
  driver.get('https://leetcode.com/problems/' + row['title_slug'])
  delay = 20
  try:
    # WAIT TILL CONTENT IS LOADED
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1hky5w4')))
    print("Page is ready!")
  except TimeoutException:
    print("Loading took too much time!")
    return "<timed out, manual entry>"

  html = driver.page_source
  html = html[html.find('css-1hky5w4'):]
  html = html[html.find('topic-tag__1jni'):]
  html = html[:html.find('/div')]
  print(html)
  return html

df['description'] = df.progress_apply(lambda x: get_and_render(x), axis=1)
df['topics'] = df.progress_apply(lambda x: get_and_render_topics(x), axis=1)
driver.quit()
df.to_csv("problem_data.csv")

# with open("Output.txt", "w", encoding='utf-8') as text_file:
#     text_file.write(html)

# Old requests_html stuff:
# import HTMLSession from requests_html
# from requests_html import HTMLSession
# session = HTMLSession()
# # Run JavaScript code on webpage

# def get_and_render(row):
#   r = session.get('https://leetcode.com/problems/' + row['title_slug'])
#   r.html.render()
#   html = str(r.html.html)

#   #TODO: This is where I am string parsing someone help
#   html = html[html.find('content__u3I1 question-content__JfgR'):]
#   problem = html[html.find('div'): html.find('/div')]

#   # print(r.html.html) # make sure this is never 429
#   # raise Exception('Paused')
#   return problem

# ##contains rendered html for each page, now parse problem descriptions from each respective html
# df['description'] = df.apply(lambda x: get_and_render(x), axis=1)
# # print(df)
# # print(df.keys())
# ### Excel Output
# df.to_csv("problem_data.csv")
# print("Problem:")
# print(df.iloc[0]['description'][0:1000])
