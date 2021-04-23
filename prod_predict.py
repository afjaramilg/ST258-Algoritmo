# check scikit-learn version
import sklearn
import csv 
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor


raw_dataset = pd.read_csv('clean_weather_energy.csv',
                          na_values='?', comment='\t', header=0,
                          sep=',', skipinitialspace=True)


dataset = raw_dataset.copy()
dataset = dataset.dropna()
dataset = pd.get_dummies(dataset, columns=['weather_id'], prefix='', prefix_sep='')

train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

train_features = train_dataset.copy()
train_features = train_features.drop([
    'generation biomass',
    'generation other renewable',
    'generation solar',
    'generation wind onshore'
], axis=1)


train_labels = train_dataset[[
    'generation biomass',
    'generation other renewable',
    'generation solar',
    'generation wind onshore'
]]


test_features = test_dataset.copy()
test_features = test_features.drop([
    'generation biomass',
    'generation other renewable',
    'generation solar',
    'generation wind onshore'
], axis=1)


test_labels = test_dataset[[
    'generation biomass',
    'generation other renewable',
    'generation solar',
    'generation wind onshore'
]]

#print(test_features.columns)

#exit(1)

# little layers, many nodes, ooga booga
# best so far 500, 200, 75
regr = MLPRegressor(hidden_layer_sizes=(500, 200, 75),
    random_state=1, max_iter=1000).fit(train_features, train_labels)

def get_hourly_prod():
    # get weather function here
    weather = test_features[:24]
    ans_raw = regr.predict(weather)
    ans = np.zeros(24)
    for i in range(24):
        for j in range(4):
            ans[i] += ans_raw[i][j]

    return ans

print(regr.score(train_features, train_labels))
print(regr.score(test_features, test_labels))


print(get_hourly_prod())