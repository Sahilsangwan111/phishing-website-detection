import pandas as pd

# dataset load
df = pd.read_csv("data/dataset.csv")

# basic info
print(df.head())
print(df.shape)

# label check
print(df['Result'].value_counts())
# convert labels
df['Result'] = df['Result'].replace(-1, 0)

# check again
print(df['Result'].value_counts())
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# features & target
X = df.drop(['Result', 'id'], axis=1)
y = df['Result']

# split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# prediction
y_pred = model.predict(X_test)

# accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))

# save model
pickle.dump(model, open("model.pkl", "wb"))