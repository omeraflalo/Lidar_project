import csv
import json

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, \
    ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
import joblib

from excelFormatter import format_and_save_data


# Normalizing and padding the shapes
def preprocess_shapes(shapes):
    x_y_shapes = [np.array(json.loads(shape)) for shape in shapes]

    max_length = max(len(shape) for shape in x_y_shapes)
    print(max_length)
    processed_shapes = []

    for shape in x_y_shapes:
        # Normalization
        min_val = np.min(shape, axis=0)
        max_val = np.max(shape, axis=0)
        norm_shape = shape - min_val
        if np.any(max_val != 0):  # Check if max value is not zero to avoid division by zero
            norm_shape /= max_val
        else:
            norm_shape = np.zeros_like(shape)  # or handle it differently

        # Padding
        pad_length = max_length - len(norm_shape)
        padded_shape = np.pad(norm_shape, ((0, pad_length), (0, 0)), mode='constant')

        processed_shapes.append(padded_shape)

    return np.array(processed_shapes)


# Function to flatten the shapes
def flatten_shapes(shapes):
    return np.array([shape.flatten() for shape in shapes])


version = "3"

X = []
Y = []
with open('models/version ' + version + '/raw_data.csv', 'r') as file:
    csvreader = csv.reader(file, delimiter=';')
    for row in csvreader:
        X.append(row[1])
        Y.append(row[0])

# Preprocess the shapes
X = preprocess_shapes(X)

# Flatten the shapes for scaling
X_flattened = flatten_shapes(X)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_flattened, Y, test_size=0.3, random_state=42)

# Standardize features by removing the mean and scaling to unit variance
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
# Classifier models to be evaluated
classifiers = {
    "KNN": KNeighborsClassifier(n_neighbors=3),
    "SVM": SVC(),
    "Random Forest": RandomForestClassifier(),
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(),
    "Naive Bayes": GaussianNB(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "AdaBoost": AdaBoostClassifier(),
    "Extra Trees": ExtraTreesClassifier(),
    "Linear Discriminant Analysis": LinearDiscriminantAnalysis(),
    "Quadratic Discriminant Analysis": QuadraticDiscriminantAnalysis(),
    "MLP Classifier": MLPClassifier(),
}

best_model = None
results = []
# Training and evaluating each classifier
for name, clf in classifiers.items():
    clf.fit(X_train, y_train)  # Train the classifier
    predictions = clf.predict(X_test)  # Make predictions
    accuracy = accuracy_score(y_test, predictions)
    print(f"\n{name} Classifier")
    print("Accuracy:", accuracy)
    print("\nClassification Report:\n", classification_report(y_test, predictions))
    report = classification_report(y_test, predictions, output_dict=True)
    joblib.dump(clf, f'models/version {version}/{name.lower().replace(" ", "_")}_model.pkl')

    results.append({
        "Classifier": name,
        "Accuracy": accuracy,
        **{f"{key} Precision": value['precision'] for key, value in report.items() if key != 'accuracy'},
        **{f"{key} Recall": value['recall'] for key, value in report.items() if key != 'accuracy'},
        **{f"{key} F1-Score": value['f1-score'] for key, value in report.items() if key != 'accuracy'}
    })

    # Determining the best model
    if best_model is None or accuracy > best_model[0]:
        best_model = [accuracy, name]

df = pd.DataFrame(results)

joblib.dump(scaler, f'models/version {version}/scaler.pkl')

# Export to Excel
excel_filename = f'models/version {version}/model_evaluations.xlsx'
format_and_save_data(results, excel_filename)

print(f"\nBest Model: {best_model[1]} Classifier with an Accuracy of {best_model[0]}")
