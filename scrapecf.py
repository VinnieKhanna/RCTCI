import pandas as pd
from tqdm import tqdm
import time
import numpy as np

""" You may need to use pip install pyppdf if
you get an error asking to install Chromium
"""
# import pyppdf.patch_pyppeteer

### Data Collection

import time
import requests
import json

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

### SELENIUM FOR PROBLEM RUN-TIME
import re
import operator
import csv

tqdm.pandas()

all_runtimes = {}
problemID = 0

def getWebsite(page):
  driver.get(f'https://codeforces.com/problemset/page/{page}?order=BY_RATING_ASC/')
  delay = 20
  try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'pagination')))
    # WAIT TILL CONTENT IS LOADED
    print("Page is ready!")
  except TimeoutException:
    print("Loading took too much time!")
    return "<timed out, manual entry>"
  time.sleep(5)
  html = driver.page_source
  problems = html.split('<tbody>')[1].split("<tr>")[2:]

  print(len(problems))
  if len(problems) < 10:
    print(f"PAGE {page} took too long...")
    time.sleep(5)
    html = driver.page_source
    problems = html.split('<tbody>')[1].split("<tr>")[2:]

  return problems

def get_problem_info(problem):
  data = problem.split("<td")

  # get title
  title = None
  try:
    title = data[2].split('<a')[1].split(">")[1].split("</a")[0].strip()
  except:
    return None, None, None

  # get tags
  tags = data[2].split("tags=")
  if tags:
    tags = tags[1:]
    tags = [tag.split("\"")[0] for tag in tags]

  # get difficulty
  difficulty = data[4].split("ProblemRating\">")[1].split("<")[0]

  # get website
  website = None
  try:
    website = data[2].split('<a href=\"')[1].split(">")[0].strip()
    print(website)
  input()

  return title, tags, difficulty

#input-specification

def get_and_render_discussions(): 
  problemID = 0

  data = []

  for page in range(1, 73): #73
    time.sleep(3)
    problems = getWebsite(page)
    for problem in problems:
      title, tags, difficulty = get_problem_info(problem)
      if title:
        title = title.encode("ascii", "ignore")
        title = title.decode()
        # print(title)
        problemID += 1
        data.append({'id': problemID, 'title': title, 'tags': tags, 'difficulty': difficulty})

  # with open('cf_metadata.txt', 'r') as fp:
  #   line = fp.read()
  #   line = line.decode('utf-8','ignore').encode("utf-8")
  #   data = json.load(line, encoding="utf8")

  print(data)

  csv_columns = ['id', 'title', 'tags', 'difficulty']
  csv_file = "problem_data_cf.csv"
  try:
    with open(csv_file, 'w', newline='', encoding="utf-8") as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
      writer.writeheader()
      for d in data:
        print(d)
        writer.writerow(d)
  except IOError:
    print("I/O error")


get_and_render_discussions()
driver.quit()
# df.to_csv("problem_data2.csv")