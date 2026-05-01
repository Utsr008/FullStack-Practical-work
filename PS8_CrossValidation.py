
# PS8 - Cross Validation Performance Analyzer Tool
# Dataset: Iris (UCI)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

# Load dataset
iris = load_iris()
X = iris.data
y = iris.target

# Models
models = {
    "Logistic Regression": LogisticRegression(max_iter=200),
    "KNN": KNeighborsClassifier(),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "SVM": SVC(),
    "Naive Bayes": GaussianNB()
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results = []
scores_dict = {}

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    scores_dict[name] = scores
    results.append([name, scores.mean(), scores.std()])

df = pd.DataFrame(results, columns=['Model','Mean Accuracy','Std Dev'])
print(df.sort_values(by='Mean Accuracy', ascending=False))

# Bar chart
plt.figure(figsize=(10,5))
sns.barplot(data=df, x='Model', y='Mean Accuracy')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()

# Boxplot
plt.figure(figsize=(10,5))
plt.boxplot(scores_dict.values(), labels=scores_dict.keys())
plt.xticks(rotation=30, ha='right')
plt.title("Cross Validation Score Distribution")
plt.tight_layout()
plt.show()

best = df.sort_values(by='Mean Accuracy', ascending=False).iloc[0]
print("\nBest Model:", best['Model'])
print("Accuracy:", round(best['Mean Accuracy'],4))
