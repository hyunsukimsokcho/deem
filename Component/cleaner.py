import pandas as pd
import numpy as np
import concurrent.futures
class Cleaner:

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        setattr(self, 'size', self.data.shape[0])
    
    def literal_clean(self, df1, i1, j1, df2=None, i2=None, j2=None):
        duplicate_ind_list = []
        if df2 == None:
            self.size, self.num_attr = self.data.shape
            for i in range(i1, j1 - 1):
                for j in range(i+1, j1):
                    if self.data.iloc[i].equals(self.data.iloc[j]):
                        duplicate_ind_list.append(j)
        else:
            pass

        self.data.drop(self.data.index[list(set(duplicate_ind_list))], inplace=True)

    def batch_clean(self, n):

        with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
            batch_jobs = []
            batch_size = int(np.floor(self.size / n))
            for i in range(n-1):
                #batch_jobs.append(executor.submit(self.literal_clean, self.data[]))
                pass





if __name__ == "__main__":
    df = pd.DataFrame([range(4)]*3, columns=['A', 'B', 'C', 'D'])
    cleaner = Cleaner(data=df)
    print(cleaner.data)
    cleaner.literal_clean(cleaner.data, 0, cleaner.size)
    print(cleaner.data)
