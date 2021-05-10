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

train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)


output_labels = [
    'generation biomass',
    'generation other renewable',
    'generation solar',
    'generation wind onshore'
]

train_features = train_dataset.copy()
train_features = train_features.drop(output_labels, axis=1)
train_labels = train_dataset[output_labels]


test_features = test_dataset.copy()
test_features = test_features.drop(output_labels, axis=1)
test_labels = test_dataset[output_labels]

#print(test_features.columns)

#exit(1)

# little layers, many nodes, ooga booga
# best so far 400 220 180 140 
# 400, 260, 180, 140, 100
regr = MLPRegressor(hidden_layer_sizes=(400, 260, 180, 140, 100),
    random_state=1, max_iter=1000).fit(train_features, train_labels)


# the amount of KW you can produce in 1 hour
# with each energy source
capacity = [
    20, # biomass
    20, # other
    70, # solar
    10, # wind
]


def get_hourly_prod():
    # get weather function here
    weather = test_features[:24]
    ans_raw = regr.predict(weather)
    ans = np.zeros(24)
    for i in range(24):
        for j in range(4):
            ans[i] += ans_raw[i][j] * capacity[j]

    return ans

print(regr.score(train_features, train_labels))
print(regr.score(test_features, test_labels))


print(get_hourly_prod())