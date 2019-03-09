import pandas as pd
import numpy as np
import concurrent.futures

class Cleaner:

    def __init__(self, **kwargs):
        """
        Constructor for cleaning component
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])
        setattr(self, 'size', self.data.shape[0])
    
    def literal_clean(self, df1, df2=None, isPair=False, isParallel=False):
        """
        Cleans existing duplicate in data frame by pairwise comparison.

        @description
            It's behavior is different if it's part of parallel execution.
            In such cases, it just returns the list of index to remove and 
            deal with removal in parallel_clean scope

        @params
            df1: First data frame to compare with
            df2: Explicit second data frame to compare with (If this is None, default is df1)
            isParallel: boolean value indicating if this is part of parallel execution
        """
        duplicate_ind_list = []
        df1_list = df1.index.tolist()
        if not isPair:
            for i in df1_list[:-1]:
                for j in df1_list[i+1:]:
                    if df1.iloc[i].equals(df1.iloc[j]):
                        duplicate_ind_list.append(j)
        else:
            df2_list = df2.index.tolist()
            for i in df1_list:
                for j in df2_list:
                    if df1.loc[i].equals(df2.loc[j]):
                        duplicate_ind_list.append(j)
        if isParallel:
            return duplicate_ind_list
        else:
            if isPair:
                df2.drop(list(set(duplicate_ind_list)), inplace=True)
            else:
                df1.drop(list(set(duplicate_ind_list)), inplace=True)

    def parallel_clean(self, n):
        """
        @description
            Clean duplicate in parallelized fashion.

        @params
            n: number of tasks that the entire work will be splitted into (for parallel exec.)
        """
        total_duplicate_ind_list = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=100) as executor:
            batch_jobs = []
            batch_size = int(np.floor(self.size / n))

            for i in range(n-2):
                for j in range(i, n-1):
                    if i == j:
                        batch_jobs.append(executor.submit(self.literal_clean, self.data[i*batch_size:(i+1)*batch_size], isParallel=True))
                    else:
                        batch_jobs.append(executor.submit(self.literal_clean, self.data[i*batch_size:(i+1)*batch_size], df2=self.data[j*batch_size:(j+1)*batch_size], isPair=True, isParallel=True))

            for i in range(n-1):
                batch_jobs.append(executor.submit(self.literal_clean, self.data[i*batch_size:(i+1)*batch_size], df2=self.data[(n-1)*batch_size:], isPair=True, isParallel=True))

            batch_jobs.append(executor.submit(self.literal_clean, self.data[(n-1)*batch_size:], isParallel=True))

            for job in concurrent.futures.as_completed(batch_jobs):
                if job.cancelled():
                    print("[PARALLEL_CLEAN: JOB cancelled]: Check what's causing abnormal behavior")
                    continue
                elif job.done():
                    job_result = job.result()
                    total_duplicate_ind_list += job_result
        self.data.drop(list(set(total_duplicate_ind_list)), inplace=True)





if __name__ == "__main__":
    df = pd.DataFrame([range(4)]*3, columns=['A', 'B', 'C', 'D'])
    cleaner = Cleaner(data=df)
    print(cleaner.data)
    cleaner.literal_clean(cleaner.data)
    print(cleaner.data)
