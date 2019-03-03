import pandas as pd
import numpy as np

class Duplicator:
    def __init__(self, **kwargs):
        """
        Consructor for duplicating component
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])

        setattr(self, 'data', pd.read_csv("Dataset/" + self.category + "/data", sep='\s+', header=None))

    def print_origin_data(self, verbose=False):
        """ 
        Prints original data in a redable form
        """
        if verbose:
            schema = open("Dataset/" + self.category + "/schema").read().splitlines()
            df = pd.read_csv("Dataset/" + self.category + "/data", sep='\s+', header=None, names=schema)
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
        self.size, self.num_attr = self.data.shape

        self.data.insert(0, 'isDuplicate', np.zeros(self.size))
        self.data.insert(0, 'id', range(self.size)) 
        total = 0

        for i in range(self.size):
            n = np.random.zipf(k) - 1
            # add n many duplicates into our current dataframe
            if n > 0:
                dup = self.data.iloc[i]
                dup['isDuplicate'] = 1.0
                self.data = self.data.append(n*[dup], ignore_index=True)
            total = total + n
        print(self.data)
        print("ADDED {} MANY RAW DUPLICATES".format(total))

    def add_random_duplicate(self, k):
        pass
            

if __name__ == "__main__":
    duplicator = Duplicator(category="GermanBank")
    duplicator.add_raw_duplicate(4)

    
