import csv

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score

from lidarUtills import measure_to_x_y

# Normalizing and padding the shapes
def preprocess_shapes(shapes):
    x_y_shapes = []
    for shape in shapes:
        if len(shape) == 0:
            continue
        x_y_shape = []
        for measure in shape:
            measure = measure[1:-1].split(",")
            angle = int(float(measure[0]))
            distance = float(measure[1])

            x_y_shape.append(measure_to_x_y(angle, distance))
        x_y_shapes.append(x_y_shape)

    max_length = max(len(shape) for shape in x_y_shapes)
    print(max_length)
    processed_shapes = []

    for shape in x_y_shapes:
        # Normalization (example: scale between 0 and 1)
        norm_shape = shape - np.min(shape, axis=0)
        norm_shape /= np.max(norm_shape, axis=0)

        # Padding
        pad_length = max_length - len(norm_shape)
        padded_shape = np.pad(norm_shape, ((0, pad_length), (0, 0)), mode='constant')

        processed_shapes.append(padded_shape)

    return np.array(processed_shapes)

# Function to flatten the shapes
def flatten_shapes(shapes):
    return np.array([shape.flatten() for shape in shapes])

X = []
Y = []
with open('trainData/raw_data.csv', 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        X.append(row[1:])
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

# Initialize KNN classifier with, say, 3 neighbors
knn = KNeighborsClassifier(n_neighbors=3)

# Train the classifier
knn.fit(X_train, y_train)

# Make predictions
predictions = knn.predict(X_test)

# Evaluate the classifier
print("Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:\n", classification_report(y_test, predictions))

joblib.dump(knn, 'knn_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
