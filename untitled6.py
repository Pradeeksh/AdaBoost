# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13gmsh9T-yxS-FThbhfKgTs0ZyQbUsZaj
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

train = pd.read_csv("train.csv")

train

test = pd.read_csv("test.csv")

test

df = pd.concat([train,test])

df.head()

df.tail()

df.info()

df.describe()

df = pd.concat([train,test])

df['Age'] = df['Age'].fillna(value=df['Age'].median())
df['Fare'] = df['Fare'].fillna(value=df['Fare'].median())

df.info()

df.describe()

df['Embarked'] = df['Embarked'].fillna('S')
df.isnull().sum()

df.loc[ df['Age'] <= 16, 'Age'] = 0
df.loc[(df['Age'] > 16) & (df['Age'] <= 32), 'Age'] = 1
df.loc[(df['Age'] > 32) & (df['Age'] <= 48), 'Age'] = 2
df.loc[(df['Age'] > 48) & (df['Age'] <= 64), 'Age'] = 3
df.loc[ df['Age'] > 64, 'Age'] = 4

df['Cabin'] = df['Cabin'].fillna('Missing')
df['Cabin'] = df['Cabin'].str[0]
df['Cabin'].value_counts()

df_1 = df.drop(['Name', 'Ticket'], axis = 1)
df_1.head()

df_dummies = pd.get_dummies(df_1, drop_first = True)
df_dummies.head()

df_train = df_dummies[df_dummies['Survived'].notna()]
df_train.info()

df_test = df_dummies[df_dummies['Survived'].isna()]
df_test.info()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df_train.drop(['PassengerId','Survived'],axis=1),
                                                    df_train['Survived'], test_size=0.30,
                                                    random_state=101, stratify = df_train['Survived'])

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

ada = AdaBoostClassifier(DecisionTreeClassifier(),n_estimators=100, random_state=0)
ada.fit(X_train,y_train)

predictions = ada.predict(X_test)

from sklearn.metrics import classification_report
print(classification_report(y_test,predictions))

print (f'Train Accuracy - : {ada.score(X_train,y_train):.3f}')
print (f'Test Accuracy - : {ada.score(X_test,y_test):.3f}')

TestForPred = df_test.drop(['PassengerId', 'Survived'], axis = 1)
t_pred = ada.predict(TestForPred).astype(int)

PassengerId = df_test['PassengerId']

adaSub = pd.DataFrame({'PassengerId': PassengerId, 'Survived':t_pred })
adaSub.head()

adaSub.to_csv("1_Ada_Submission.csv", index = False)

