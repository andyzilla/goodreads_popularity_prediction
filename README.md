# goodreads_popularity_prediction

As a publisher, when marketing a new book, I want to determine the title and description that will maximise the number of readers.

## 1) Installation instructions
### 1.1 Environment Setup
- You can use docker to load all requirements, as detailed in requirements.txt (run "make build")

### 1.2. Download Dataset from Kaggle
- Make a copy of .env-template as ".env" and include your Kaggle credentials (username and key).
- Run "make data"
 TODO: explain we're using files from 600k onwards (contain) description


## 2) Usage instructions

This project contains the following notebooks:

### 00 - EDA.ipynb
- Input: Kaggle dataset, keeping only the files that contain the column "Description"
- Content: Initial EDA, which was used as a base to design the data cleaning function.

### 00 - EDA Without Duplicated titles.ipynb
- Input: Kaggle dataset, keeping only the files that contain the column "Description"
- Content: repetition of the exploratory questions of the EDA, using the clean dataset.

### 01 - Clean Dataset.ipynb
- Input: Kaggle dataset, keeping only the files that contain the column "Description"
- Output: clean dataset saved on '../data/clean_dataset.csv'
- Content: Applies clean_dataset function from utils.py and saves the clean datased on '../data/clean_dataset.csv' 

### 02 - Model training and evaluation.ipynb
- Input: clean dataset saved on '../data/clean_dataset.csv'
- Output: final model saved on '../models/final_model.clf'
- Content: Uses the functions defined in the model.py to create the train and test datasets, load and evaluate models

### 03 - Error Analysis.ipynb
- Input: final model saved on '../models/final_model.clf'
- Content: analysis of false positives