import pandas as pd
import os
from sklearn.model_selection import train_test_split
import xgboost as xgb
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import accuracy_score, mean_squared_error
import pickle

path = "data"

dfCom = pd.read_excel(os.path.join(path, "Animal_feature_v4.xlsx"))
print(dfCom.shape) #(23080, 46)

labels = ['distance', 'direction']

label_distance = dfCom[labels[0]]
label_direction = dfCom[labels[1]]

dfX = dfCom.loc[:,~dfCom.columns.isin(labels)]


########Model1: distance################
# split data into train and test sets

dfX_model1 = dfX.copy()
naRows = label_distance.isna()

dfX_model1 = dfX_model1[~naRows]
label_distance = label_distance[~naRows]

label_distance_max = label_distance.max()
label_distance_min = label_distance.min()

label_distance_quatile1 = label_distance.quantile(0.1)

def normalizeDistance(distance_y):
    return (distance_y - label_distance_min) / (label_distance_max-label_distance_min)

def deNormalize(normalize_distance):
    return normalize_distance * (label_distance_max-label_distance_min) + label_distance_min


# label_distance[0]
# n1 = normalizeDistance(label_distance[0])
# deNormalize(n1)

label_distance = label_distance.apply(lambda x: normalizeDistance(x))

seed = 7
test_size = 0.33
X_train, X_test, y_train, y_test = train_test_split(dfX_model1, label_distance, test_size=test_size, random_state=seed)

model = XGBRegressor()

model.fit(X_train, y_train)

ypred = model.predict(X_test)

print("mean_squared_error:",mean_squared_error(ypred, y_test))


# save
pickle.dump(model, open(os.path.join("model","xgb_regressor.pkl"), "wb"))

##coverback to denormalize distance##
ypred_denormalize = [deNormalize(x) if x > 0 else label_distance_quatile1 for x in ypred ]


########Model2: direaction################
dfX_model2 = dfX.copy()
naRows = label_direction.isna()

dfX_model2 = dfX_model2[~naRows]
label_direction = label_direction[~naRows]

seed = 7
test_size = 0.33
X_train, X_test, y_train, y_test = train_test_split(dfX_model2, label_direction, test_size=test_size, random_state=seed)


# fit model no training data
model_classify = XGBClassifier(learning_rate=0.1,
                    n_estimators=1000,
                    max_depth=5,
                    min_child_weight=1,
                    gamma=0,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    objective='multi:softmax',
                    nthread=4,
                    num_class=4,
                    seed=27)

model_classify.fit(X_train, y_train, eval_metric="auc")

ypred_direction = model_classify.predict(X_test)

# evaluate predictions
accuracy = accuracy_score(y_test, ypred_direction)
print("Accuracy: %.2f%%" % (accuracy * 100.0)) #Accuracy: 36.71%

file_name = "xgb_classifier.pkl"

# save
pickle.dump(model_classify, open(os.path.join("model",file_name), "wb"))
# load
# xgb_model_loaded = pickle.load(open(os.path.join("model",file_name), "rb"))
