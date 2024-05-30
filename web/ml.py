import numpy as np
import pandas as pd
import pickle

df = pd.read_csv('ml_model.csv')
y = df['Group']
X = df.drop('Group', axis=1)

#Creating training and testing datasets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)

#Training Model
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

# Predicting the Test set results
predictions = rf.predict(X_test)

# Saving model using pickle
pickle.dump(rf, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load( open('model.pkl','rb'))
features = np.array([[2, 689, 1, 77, 18, 1, 29, 0, 1322, 0.731, 1.327]])
print(model.predict(features))