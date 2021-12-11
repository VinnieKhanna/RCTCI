# RCTCI
Recracking the Coding Interview: CS 4650 Natural Language Processing
## Directory Structure
Following our project progress chronologically, we began our work with the three Python scripts, `scrape.py`, `scrapecf.py`, and `clean_data.py`. To parse LeetCode and Codeforces coding problem data, we used the first two scripts respectively. These scripts use Selenium to automate this process. Running either of these scripts will perform the entire data collection for their respective websites, which takes several hours. `clean_data.py` houses many cleaner helper functions. Most of these only need(ed) to be run once, so much of this file's old functionality is commented out. Each of these scripts individually output dataframes to csv files, which are placed in the `/data` directory. The `/data` directory contains many permutations of our data, at differing states of the cleaning or data collection process.

Because our tasks are very computationally expensive, we are using a shared Google Colab notebook. All the spreadsheets in `/data` are also hosted in a shared Google Drive folder that we mount when running in the Colab environment. This is the recommended way to run the notebook.

## Installation Instructions
First, create a folder named 'CS4650' in your Google Drive root directory. Then copy the contents of the data folder (but NOT the data folder itself) into your CS4650 folder in your Google Drive. Open up Recracking the Coding Interview in Colab.You should be able to start stepping through cells. The notebook has a table of contents for organizational convenience. Note: it is highly recommended to run the code with a Colab GPU enabled.


## Running the Code
Running the code for data analysis should be straightforward and self-explanatory. Below, we will detail the **minimum required steps** for running specific models.
### Baseline Models with Logistic Regression
First, run the entire notebook up to and including data analysis, stopping at Embeddings. Within Embeddings, you only need to run the 2nd and final cell under the BERT subsection. You may now skip to Classification Model Training. From there, navigate to Logistic Regression. Ignoring the first cell, you may now choose which model to run. The three predictive class options are clearly labeled in the comments, so simply uncomment the option you are looking for and comment out the rest. Note that this will set up Logistic Regression to run on pre-trained BERT embeddings. Next, run the following two cells. If you want to run with BERT embeddings, skip the cell using the TF-IDF vectorizer, as that will overwrite what the model will use. If however you do want to see the TF-IDF + LR baseline, go ahead and run that cell (and optionally skip the above few instructions). Once again, comment out the class you want to use if you want to see the TF-IDF experiment. Finally, run the following cell to see your results.
### LSTM Models
First, run the entire notebook up to and including data analysis, stopping at Embeddings. Within Embeddings, you only need to run the 2nd and final cell under the BERT subsection. You may now skip to Classification Model Training. Run the first 3 cells, including initializing the LSTMModel class. Now skip to Difficulty Model > LSTM. Run the first cell, then choose which of the 6 options you would like to run (BERT or TF-IDF and which predictive class). Options are contained within three ### comment symbols. Run the rest of the cells in this section to see results!
### TF-IDF + SMOTE + Logistic Regression with ELI5 Weights on Runtime, Difficulty, and Topics
Run the first 5 cells of the notebook (up to and including the cell that '%ls'). Then, jump to 'Runtime Model with Logistic Regression, TF-IDF, SMOTE' in the table of contents and run the 3 cells inside. Repeat for 'Difficulty Model with Logistic Regression, TF-IDF, SMOTE' and 'Difficulty Model with Logistic Regression, TF-IDF, SMOTE'.

### BERT for Sequence Classification
Run the first 5 cells of the notebook (up to and including the cell that '%ls'). Then, jump to 'BertforSequenceClassification' in the table of contents. 'Runtime', 'Difficulty', and 'Topics' are each present as sections under 'BertforSequenceClassification'. Run the cells in each section to see the results.
