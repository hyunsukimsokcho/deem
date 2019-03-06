import pandas as pd
import numpy as np
import copy
import os

class Duplicator:
    def __init__(self, **kwargs):
        """
        Consructor for duplicating component
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])

        setattr(self, 'schema', open("Dataset/" + self.category + "/schema").read().splitlines())
        if os.path.isfile("Dataset/" + self.category + "/data"):
            # No test_data provided from src
            # Cross-validation needed
            setattr(self, 'data', pd.read_csv("Dataset/" + self.category + "/data", sep=r'[,\t ]+', header=None, names=self.schema))
            mask = np.random.rand(len(self.data)) < 0.8
            setattr(self, 'train_data', self.data[mask])
            setattr(self, 'test_data', self.data[~mask])
        else:
            # test_data provided from src
            setattr(self, 'train_data', pd.read_csv("Dataset/" + self.category + "/train.data", sep=r'[,\t ]+', header=None, names=self.schema, na_values='?'))

            setattr(self, 'test_data', pd.read_csv("Dataset/" + self.category + "/test.data", sep=r'[,\t ]+', header=None, names=self.schema, na_values='?'))
    def print_origin_data(self, verbose=False):
        """ 
        Prints original data in a redable form
        """
        if verbose:
            df = pd.read_csv("Dataset/" + self.category + "/data", sep='\s+', header=None, names=self.schema)
        else:
            df = pd.read_csv("Dataset/" + self.category + "/data", sep='\s+', header=None)
        print(df)

    def add_raw_duplicate(self, k):
        """
        @description
            Generate duplicate of each tuple according to zipfian dist.

        @params
            k: maximum number of duplicates to generate according to zipfian dist. (k>1)
            (As k increases, number of duplicates decreases. k=4 brings about 100 duplicates; HEURISTIC)
        """
        self.size, self.num_attr = self.train_data.shape
        self.test_data = self.test_data.copy()
        #self.train_data.insert(0, 'isDuplicate', np.zeros(self.size))
        #self.train_data.insert(0, 'id', range(self.size)) 
        total = 0

        for i in range(self.size):
            n = np.random.zipf(k) - 1
            # add n many duplicates into our current dataframe
            if n > 0:
                dup = self.train_data.iloc[i]
#                 dup['isDuplicate'] = 1.0
                self.train_data = self.train_data.append(n*[dup], ignore_index=True)
            total = total + n
        #print(self.data)
        print("ADDED {} MANY RAW DUPLICATES".format(total))

    def add_random_duplicate(self, k):
        pass
            

if __name__ == "__main__":
    # possible category: "GermanBank", "AdultCensus", "CompasRecidivism"
    duplicatorB = Duplicator(category="GermanBank")
    print(duplicatorB.train_data)
    print(duplicatorB.test_data)

    duplicatorC = Duplicator(category="CompasRecidivism")
    print(duplicatorC.train_data)
    print(duplicatorC.test_data)
    duplicatorA = Duplicator(category="AdultCensus")
    print(duplicatorA.train_data)
    print(duplicatorA.test_data)
#    print(duplicator.data)
#    duplicator.add_raw_duplicate(4)
#
#    Censusduplicator = Duplicator(category="AdultCensus")
#    print(Censusduplicator.train_data)
#
#    Compasduplicator = Duplicator(category="CompasRecidivism")
#    print(Compasduplicator.data)

    
