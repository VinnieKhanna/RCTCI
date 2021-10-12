import pandas as pd

### Data Collection

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
  cleaned_problems.append(cleaned_problem)

df = pd.DataFrame(reversed(cleaned_problems))
df.set_index('id', inplace=True)

# import HTMLSession from requests_html
from requests_html import HTMLSession
session = HTMLSession()
# Run JavaScript code on webpage

def get_and_render(row):
  r = session.get('https://leetcode.com/problems/' + row['title_slug'])
  r.html.render()
  return r.html.html

##contains rendered html for each page, now parse problem descriptions from each respective html
df['description'] = df.apply(lambda x: get_and_render(x), axis=1)

# ### Excel Output
# df.to_csv("problem_data.csv")