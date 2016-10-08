# This script deploys a few models to predict a recipe's cuisine from its ingredients

# Imports
import pandas as pd
import numpy as np
import re
from nltk import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.cross_validation import cross_val_score, cross_val_predict
from sklearn.naive_bayes import BernoulliNB

# Read in data
df = pd.read_csv('../ingredients_combined/ingredients_reduced.csv')