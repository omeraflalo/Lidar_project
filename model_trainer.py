import joblib
from sklearn.metrics import classification_report, accuracy_score


class ModelTrainer:
    def __init__(self, classifiers):
        self.classifiers = classifiers

    def train_and_evaluate(self, X_train, X_test, y_train, y_test, version):
        results = []
        best_model = [0, '']

        for name, clf in self.classifiers.items():
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)

            accuracy = accuracy_score(y_test, predictions)
            report = classification_report(y_test, predictions, output_dict=True)
            joblib.dump(clf, f'models/version {version}/{name.lower().replace(" ", "_")}_model.pkl')

            results.append({
                "Classifier": name,
                "Accuracy": accuracy,
                **{f"{key} Precision": value['precision'] for key, value in report.items() if key != 'accuracy'},
                **{f"{key} Recall": value['recall'] for key, value in report.items() if key != 'accuracy'},
                **{f"{key} F1-Score": value['f1-score'] for key, value in report.items() if key != 'accuracy'}
            })

            if accuracy > best_model[0]:
                best_model = [accuracy, name]

        return results, best_model
