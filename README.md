# RCTCI
Recracking the Coding Interview: CS 4650 Natural Language Processing
## Directory Structure
Following our project progress chronologically, we began our work with the three Python scripts, `scrape.py`, `scrapecf.py`, and `clean_data.py`. To parse LeetCode and Codeforces coding problem data, we used the first two scripts respectively. These scripts use Selenium to automate this process. Running either of these scripts will perform the entire data collection for their respective websites, which takes several hours. `clean_data.py` houses many cleaner helper functions. Most of these only need(ed) to be run once, so much of this file's old functionality is commented out. Each of these scripts individually output dataframes to csv files, which are placed in the `/data` directory. The `/data` directory contains many permutations of our data, at differing states of the cleaning or data collection process.

Because our tasks are very computationally expensive, we are using a shared Google Colab notebook. All the spreadsheets in `/data` are also hosted in a shared Google Drive folder that we mount when running in the Colab environment. This is the recommended way to run the notebook.

## Installation Instructions
After creating a Google Drive folder with all relevant spreadsheets in the root directory/same directory as the Colab notebook, you should be able to start stepping through cells. The notebook has a table of contents for organizational convenience.


