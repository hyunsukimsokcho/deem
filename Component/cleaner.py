import pandas as pd
import numpy as np
class Cleaner:

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
    
    def literal_clean(self):
        duplicate_ind_list = []
        self.size, self.num_attr = self.data.shape
        for i in range(self.size - 1):
            for j in range(i+1, self.size):
                if self.data.iloc[i].equals(self.data.iloc[j]):
                    duplicate_ind_list.append(j)

        self.data.drop(self.data.index[list(set(duplicate_ind_list))], inplace=True)

if __name__ == "__main__":
    print([range(4)]*3)
    df = pd.DataFrame([range(4)]*3, columns=['A', 'B', 'C', 'D'])
    cleaner = Cleaner(data=df)
    cleaner.literal_clean()
