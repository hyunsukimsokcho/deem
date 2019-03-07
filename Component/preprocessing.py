import pandas as pd
import copy
import numpy as np
from sklearn.preprocessing import StandardScaler

class Preprocessing:
    def __init__(self, dataset):
        self.dataset = dataset
      
    def adult_custom_preprocessing(self, df):
        """
        Reference : IBM AIF360
        The Custom pre-processing for Adult Census Data is from
        https://github.com/IBM/AIF360/blob/master/aif360/algorithms/preprocessing/optim_preproc_helpers/data_preproc_functions.py
          and
        https://github.com/fair-preprocessing/nips2017/blob/master/Adult/code/Generate_Adult_Data.ipynb
        """
        def group_edu(x):
            if x <= 5:
                return '<6'
            elif x >= 13:
                return '>12'
            else:
                return x

        def age_cut(x):
            if x >= 70:
                return '>=70'
            else:
                return x

        def group_race(x):
            if x == "White":
                return 1.0
            else:
                return 0.0

        # Cluster education and age attributes.
        # Limit education range
        
        #df['education_num'] = df['education_num'].apply(lambda x: group_edu(x))
        #df['education_num'] = df['education_num'].astype('category')
        
        # Group age by decade
        # Limit age range
        #df['age'] = df['age'].apply(lambda x: x//10*10)
        #df['age'] = df['age'].apply(lambda x: age_cut(x))

        # Recode sex and race
        # df['@sex'] = df['@sex'].replace({'Female': 0.0, 'Male': 1.0})
        df['@race'] = df['@race'].apply(lambda x: group_race(x))

        return df
    
    
    def german_custom_preprocessing(self, df):
        
        """ Reference : IBM AIF360
            Custom pre-processing for German Credit Data
            https://github.com/IBM/AIF360/blob/master/aif360/algorithms/preprocessing/optim_preproc_helpers/data_preproc_functions.py
        """
        def group_credit_hist(x):
            if x in ['A30', 'A31', 'A32']:
                return 'None'
            elif x == 'A33':
                return 'Delay'
            elif x == 'A34':
                return 'Other'
            else:
                return 'NA'

        def group_employ(x):
            if x == 'A71':
                return 'Unemployed'
            elif x in ['A72', 'A73']:
                return '<4 years'
            elif x in ['A74', 'A75']:
                return '>4 years'
            else:
                return 'NA'

        def group_savings(x):
            if x in ['A61', 'A62']:
                return '<500'
            elif x in ['A63', 'A64']:
                return '>500'
            elif x == 'A65':
                return 'Unknown/None'
            else:
                return 'NA'

        gender_map = {'A91': "Male", 'A93': "Male", 'A94': "Male", 'A92': "Female", 'A95': "Female"}
        df['@sex'] = df['@sex'].replace(gender_map)

        # group credit history, savings, and employment
        df['history'] = df['history'].apply(lambda x: group_credit_hist(x))
        df['savings'] = df['savings'].apply(lambda x: group_savings(x))
        df['employment'] = df['employment'].apply(lambda x: group_employ(x))
        #df['@age'] = df['@age'].apply(lambda x: np.float(x >= 25))

        return df


    def transform(self, train_data, test_data):

     
        if self.dataset == "AdultCensus":
  
            '''
            In IBM, they used only 4 attributes
            sex race age(decade) education_years
            '''            
            train_data.drop(['workclass', 'fnlwgt', 'education', 'martial_status', 'occupation', 'relationship', 'capital_gain', 'capital_loss', 'hours_per_week', 'country'], axis=1, inplace=True)
            test_data.drop(['workclass', 'fnlwgt', 'education', 'martial_status', 'occupation', 'relationship', 'capital_gain', 'capital_loss', 'hours_per_week', 'country'], axis=1, inplace=True)
            
            train_dta = self.adult_custom_preprocessing(train_data)
            test_data = self.adult_custom_preprocessing(test_data)
            
        elif self.dataset == "GermanBank":
            '''
            In IBM, they used only 5 attributes
            age, sex, credit_history, savings, employment
            '''
            
            train_data.drop(['acc_stat', 'duration', 'purpose', 'amt', 'installment_rate', 'debtors', 'residence_period', 'prop', 'other_plans', 'housing', 'curr_credit', 'job', 'num_family', 'phone', 'foreign'], axis=1, inplace=True)
            test_data.drop(['acc_stat', 'duration', 'purpose', 'amt', 'installment_rate', 'debtors', 'residence_period', 'prop', 'other_plans', 'housing', 'curr_credit', 'job', 'num_family', 'phone', 'foreign'], axis=1, inplace=True)
            
            train_data = self.german_custom_preprocessing(train_data)
            test_data = self.german_custom_preprocessing(test_data)    
        
        elif self.dataset == "CompasRecidivism":
            columns = ["two_yr_recidivism" ,"score_factor" ,"@age_Above_FourtyFive" ,"@age_Below_TwentyFive" ,"@african_american" ,"@asian" ,"@hispanic" ,"@native_american" ,"@other"]
            train_data['@sex'] = train_data['@sex'].apply(lambda x: "Female" if x==1 else "Male")
            test_data['@sex'] = test_data['@sex'].apply(lambda x: "Female" if x==1 else "Male")
            
            train_data[columns] = train_data[columns].astype('object')
            test_data[columns] = test_data[columns].astype('object')

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
        elif self.dataset == 'GermanBank':
            data_copy = data.copy()
            data_copy["y"] = data_copy["y"].apply(lambda x: 0 if x == 2 else 1)
            x_data = data_copy.drop("y", axis = 1)
            y_data = data_copy["y"]
        elif self.dataset == 'CompasRecidivism':
            data_copy = data.copy()
            x_data = data_copy.drop("misdemeanor", axis = 1)
            y_data = data_copy["misdemeanor"]
            
        num_data = x_data.select_dtypes(exclude='object')
        cat_data = x_data.select_dtypes(include='object')

        if train:
            num_data = pd.DataFrame(self.scalar.fit_transform(num_data), columns=num_data.columns)
        else:
            num_data = pd.DataFrame(self.scalar.transform(num_data), columns=num_data.columns)
        cat_data = pd.get_dummies(cat_data)

        x_data = pd.concat([num_data, cat_data], axis=1)
        return x_data, y_data
