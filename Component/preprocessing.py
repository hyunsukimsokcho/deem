import pandas as pd
import copy
from sklearn.preprocessing import StandardScaler

class Preprocessing:
    def __init__(self, dataset):
        self.dataset = dataset
    
    def transform(self, train_data, test_data):
        if self.dataset == "AdultCensus":
            train_data.drop(['fnlwgt', 'education'], axis=1, inplace=True)
            test_data.drop(['fnlwgt', 'education'], axis=1, inplace=True)
            train_data = train_data.dropna().reset_index(drop=True)
            test_data = test_data.dropna().reset_index(drop=True)

        self.scalar = StandardScaler()
        x_train, y_train = self.data_preprocessing(train_data)
        x_test, y_test = self.data_preprocessing(test_data, False)

        missing_cols = set(x_train.columns) - set(x_test.columns)
        for column in missing_cols:
            print(column)
            x_test[column] = 0
        x_test = x_test[x_train.columns]
            
        return x_train, y_train, x_test, y_test
            
    def data_preprocessing(self, data, train=True):
        if self.dataset == "AdultCensus":
            data_copy = data.copy()
            data_copy["target"] = data_copy["target"].apply(lambda x:-1 if (x=='<=50K' or x=='<=50K.') else 1)
            x_data = data_copy.drop('target', axis =1)
            y_data = data_copy["target"]        

        num_data = x_data.select_dtypes(include='int')
        cat_data = x_data.select_dtypes(include='object')
        if train:
            num_data = pd.DataFrame(self.scalar.fit_transform(num_data), columns=num_data.columns)
        else:
            num_data = pd.DataFrame(self.scalar.transform(num_data), columns=num_data.columns)
        cat_data = pd.get_dummies(cat_data)

        x_data = pd.concat([num_data, cat_data], axis=1)
        return x_data, y_data