import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier

def train_models(X, y):
    clf1 = xgb.XGBClassifier(n_estimators=200)
    clf2 = RandomForestClassifier(n_estimators=200)

    clf1.fit(X, y)
    clf2.fit(X, y)

    return clf1, clf2