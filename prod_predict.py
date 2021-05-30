# check scikit-learn version
import sklearn
import csv 
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_percentage_error

import pymongo

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





def get_hourly_prod():
    client = pymongo.MongoClient("mongodb+srv://luis:bbkNOQ65@scrapping.w5sjz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    capacity = client.integrador.form.find_one()
    capacity['other'] = 0


    # get weather function here
    weather = test_features[:24]
    ans_raw = regr.predict(weather)
    ans = np.zeros(24)
    for i in range(24):
        for ind, j in [(0, 'biomasa'), (1, 'other'), (2, 'solar'), (3, 'eolica')]:
            ans[i] += ans_raw[i][ind] * float(capacity[j])

    return ans

print("train set R^2", regr.score(train_features, train_labels))
print("test set R^2", regr.score(test_features, test_labels))
print("train MAPE", mean_absolute_percentage_error(regr.predict(train_features), train_labels))
print("test MAPE", mean_absolute_percentage_error(regr.predict(test_features), test_labels))

##print(get_hourly_prod())


"""
# delete later------------
client.integrador.form.delete_many({})
client.integrador.form.insert_one({
'solar': 5,
'eolica': 6,
'biomasa': 7,
})
#-------------------------
"""
