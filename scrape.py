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


# df['description'] = df.progress_apply(lambda x: get_and_render(x), axis=1)
# driver.quit()
# df.to_csv("problem_data.csv")


### SELENIUM FOR PROBLEM RUN-TIME

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re
import operator

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

tqdm.pandas()

all_runtimes = {}
problemID = 0

def getWebsite(slug, page):
  driver.get(f'https://leetcode.com/problems/{slug}/discuss/?currentPage={page}&orderBy=most_votes&query=')
  delay = 20
  try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-zjcz7i-TopicListContainer')))
    # WAIT TILL CONTENT IS LOADED
    print("Page is ready!")
  except TimeoutException:
    print("Loading took too much time!")
    return "<timed out, manual entry>"
  time.sleep(3)
  html = driver.page_source
  posts = html.split('topic-title__3LYM')
  # topic-title__3LYM
  if len(posts) < 10:
    try:
      time.sleep(3)
      WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-zjcz7i-TopicListContainer')))
      # WAIT TILL CONTENT IS LOADED
      print("Page is ready!")
    except TimeoutException:
      print("Loading took too much time!")
      return "<timed out, manual entry>"  

  if len(posts) < 10:
    # above does not always work...
    print("Loading took too much time!")
    return "<timed out, manual entry>" 
  html = driver.page_source
  posts = html.split('topic-title__3LYM')[2:]
  return posts

def get_and_render_discussions(row): 
  global all_runtimes
  global problemID
  problemID += 1 
  # if problemID != 8: return
  time.sleep(3)
  posts = None
  runtimes = {}

  for i in range(1, 3):
    posts = getWebsite(row['title_slug'], i)
    for post in posts:
      post_title = post[2:].split('</div>')[0]
      if re.search("O\(.*\)", post_title):
        # print(post_title)
        runtime = post_title.split('O(')[1]
        counter = 1
        for idx, letter in enumerate(runtime):
          if letter == '(':
            counter += 1
          elif letter == ')':
            counter -= 1
          if counter == 0:
            runtime = runtime[:idx]
            break
        runtime = runtime.strip().lower()
        if runtime not in runtimes:
          runtimes[runtime] = 0
        runtimes[runtime] += 1

  print("runtimes: ", runtimes)

  if len(runtimes.items()) == 0:
    return "<timed out, manual entry>" 
  else:
    runtimes = sorted(runtimes.items(), key=operator.itemgetter(1),reverse=True)
    runtime = runtimes[0][0]
    print(problemID, ": ", runtime)
    all_runtimes[problemID] = runtime
    return runtime

df['runtime'] = df.progress_apply(lambda x: get_and_render_discussions(x), axis=1)
print(all_runtimes)
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
