from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, \
    ExtraTreesClassifier, BaggingClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier, PassiveAggressiveClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

from sklearn.ensemble import VotingClassifier, StackingClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import Lasso, ElasticNet, RidgeClassifierCV, Perceptron
from sklearn.svm import LinearSVC

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
    "MLP Classifier": MLPClassifier(max_iter=1000),
    "Ridge Classifier": RidgeClassifier(),
    "SGD Classifier": SGDClassifier(),
    "Nearest Centroid": NearestCentroid(),
    "Passive Aggressive": PassiveAggressiveClassifier(),
    "Bagging": BaggingClassifier(),
    "HistGradientBoosting": HistGradientBoostingClassifier(),
    "Ridge Classifier CV": RidgeClassifierCV(),
    "Perceptron": Perceptron(),
    "Linear SVC": LinearSVC(dual='auto', max_iter=1500)
}
