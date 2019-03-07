import pandas as pd
import numpy as np
import copy
import os
import concurrent.futures
from utils import timer

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
        setattr(self, 'size', self.train_data.shape[0])

    def print_origin_data(self, verbose=False):
        """ 
        Prints original data in a redable form
        """
        if verbose:
            df = pd.read_csv("Dataset/" + self.category + "/data", sep='\s+', header=None, names=self.schema)
        else:
            df = pd.read_csv("Dataset/" + self.category + "/data", sep='\s+', header=None)
        print(df)

    def parallel_duplicate(self, n, k):
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            batch_jobs = []
            batch_size = int(np.floor(self.size / n))
            for i in range(n-1):
                batch_jobs.append(executor.submit(self.add_raw_duplicate, self.train_data[i*batch_size:(i+1)*batch_size-1], k, parallel=True))
            batch_jobs.append(executor.submit(self.add_raw_duplicate, self.train_data[(n-1)*batch_size:], k, parallel=True))
            for job in concurrent.futures.as_completed(batch_jobs):
                if job.cancelled():
                    print("cancelled")
                    continue
                elif job.done():
                    job_result = job.result()
                    frames = [self.train_data, job_result]
                    self.train_data = pd.concat(frames, ignore_index=True)
                    #self.train_data = self.train_data.append(job_result, ignore_index=True)

        print(self.train_data)
            
    def add_raw_duplicate(self, data, k, parallel=False):
        """
        @description
            Generate duplicate of each tuple according to zipfian dist.

        @params
            k: maximum number of duplicates to generate according to zipfian dist. (k>1)
            (As k increases, number of duplicates decreases. k=4 brings about 100 duplicates; HEURISTIC)
        """
        self.size, self.num_attr = self.train_data.shape
        self.test_data = self.test_data.copy()
        total = 0
        data = data.reset_index(drop=True)
        data_len = data.shape[0]
        if parallel:
            data_dup_only = data[0:0]

        for i in range(data_len):
            n = np.random.zipf(k) - 1
            # add n many duplicates into our current dataframe
            if n > 0:
                dup = data.iloc[i]
                if parallel:
                    data_dup_only = data_dup_only.append(n*[dup], ignore_index=True)
                else:
                    data = data.append(n*[dup], ignore_index=True)
                
            total = total + n
        print("ADDED {} MANY RAW DUPLICATES".format(total))
        if parallel:
            return data_dup_only
        else: 
            return data

    def add_random_duplicate(self, k):
        pass
            

if __name__ == "__main__":
    t = timer()
    # possible category: "GermanBank", "AdultCensus", "CompasRecidivism"
#    duplicatorB = Duplicator(category="GermanBank")
#    print(duplicatorB.train_data)
#    print(duplicatorB.test_data)
#    t.tictic()
#    duplicatorB.add_raw_duplicate(duplicatorB.train_data, 4)
#    t.toctoc("NO parallel")
#    t.tictic()
#    duplicatorB.parallel_duplicate(5, 4)
#    t.toctoc("parallelized")

#    duplicatorC = Duplicator(category="CompasRecidivism")
#    print(duplicatorC.train_data)
#    print(duplicatorC.test_data)

    duplicatorA = Duplicator(category="AdultCensus")
#    print(duplicatorA.train_data)
#    print(duplicatorA.test_data)
    t.tictic()
    duplicatorA.parallel_duplicate(5, 4)
    t.toctoc("PARALLELIZED")
#    print(duplicator.data)
    duplicatorD = Duplicator(category="AdultCensus")
    t.tictic()
    duplicatorD.add_raw_duplicate(duplicatorD.train_data, 4)
    t.toctoc("NO PARALLEL")
#
#    Censusduplicator = Duplicator(category="AdultCensus")
#    print(Censusduplicator.train_data)
#
#    Compasduplicator = Duplicator(category="CompasRecidivism")
#    print(Compasduplicator.data)
