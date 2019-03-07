import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from numpy.linalg import inv
from numpy.linalg import norm

class Poisoner:
    def __init__(self, train_x, train_y, test_x, test_y, fraction):
        #-------------------------------------------------------------------------------
        # Input
        #-------------------------------------------------------------------------------
        # train_x : Preprocessed feature of training data. (data type : pandas.DataFrame)
        # train_y : label of training data (data type : pandas.DataFrame)
        # test_x :
        # test_y : 
        #-------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------
        # Attributes
        #-------------------------------------------------------------------------------
        # raw_train_x : Preprocessed feature of training data. (data type : np.array)
        # raw_train_y : label of training data (data type : np.array)
        # test_x : Preprocessed feature of test data (data type : np.array)
        # test_y : label of test data (data type : pd.Series)
        # poison_x : added poison data (data type : np.array)
        # poison_y : added poison data (data type : np.array)
        #-------------------------------------------------------------------------------
        
        self.raw_train_x = np.array(train_x)
        self.raw_train_y = np.array(train_y)
        self.test_x = np.array(test_x)
        self.test_y = test_y
        
        raw_train = train_x.copy()
        raw_train[train_y.name] = train_y
        sample = raw_train.sample(frac = fraction)
        
        self.poison_x = np.array(sample.drop(train_y.name, axis = 1))
        self.poison_y = -np.array(sample[train_y.name]) # set initial label as flipped
                
    
    
    def add_poison(self, test_fraction):
        #-------------------------------------------------------------------------------
        # Poisoning Lasso-Like Linear Classification                                    
        #-------------------------------------------------------------------------------        
        # Description : Adding poisoned data into training data
        # Reference : "Detection of Adversarial Training Examples in Poisoning Attacks 
        #              through Anomaly Detection"  Section 3 - Algorithm 1
        #--------------------------------------------------------------------------------
        val_num = int(test_fraction * len(self.test_x))
        feature_num = 5
        
        for iter in range(100):
            poison_train_x = np.concatenate((self.poison_x, self.raw_train_x), axis = 0)
            poison_train_y = np.concatenate((self.poison_y, self.raw_train_y), axis = 0)
            
            # train the model with poisoned training set
            poison_model = LogisticRegression(random_state = 0, penalty = 'l1')
            poison_model.fit(poison_train_x, poison_train_y)
            
            # get the accuracy of the model (NOT NECESSARY)
            predicted_classes = poison_model.predict(self.test_x)
            opt_acc = accuracy_score(predicted_classes, self.test_y.values)
            print("%.4f%%"%(opt_acc*100))
            
            # get the current parameter of the model
            w = poison_model.coef_
            b = poison_model.intercept_
            
            # compute the derivative of the objective function w.r.t. for each poisoning points.
            Sigma = 0
            mu = 0
            for i in poison_train_x[:,:feature_num]:
                Sigma = Sigma + np.outer(i,i)
                mu = mu + i 
            Sigma = Sigma/len(poison_train_x)
            mu = mu/len(poison_train_x)
            Mat = np.concatenate((Sigma, np.expand_dims(mu, axis=1)), axis=1)
            mu = np.append(mu, [1], axis=0)
            Mat = np.concatenate((Mat, np.expand_dims(mu, axis=0)), axis=0)
            
            X_mat = np.expand_dims(self.poison_x[:,:feature_num],axis=2)
            w_vec = np.expand_dims(w[0,:feature_num], axis=0)
            res1 = np.matmul(X_mat, w_vec)
            wxb_vec = np.matmul(self.poison_x[:,:feature_num], np.expand_dims(w[0,:feature_num], axis=1))\
                                +b[0]-self.poison_y.reshape(-1,1)
            res2 = np.matmul(np.expand_dims(np.eye(feature_num), axis=2), wxb_vec.T)
            res2 = np.transpose(res2, (2,0,1))
            M_vec = res1+res2
            w_stack_vec = np.expand_dims(np.tile(w[0,:feature_num],(M_vec.shape[0],1)), axis=1)
            Mw_vec = np.concatenate((M_vec, w_stack_vec), axis=1)
            
            derW_vec = -np.matmul(inv(Mat),Mw_vec)[:,0:feature_num,:]
            derB_vec = -np.matmul(inv(Mat),Mw_vec)[:,-1,:]
            
            temp = np.matmul(self.test_x[:val_num, :feature_num],derW_vec) + np.expand_dims(derB_vec,axis=1)
            temp2 = np.inner(self.test_x[:val_num], w)+b - np.expand_dims(self.test_y[:val_num],axis=1)
            derO_vec = (temp2 * temp).sum(axis = 1)
            deltaX_vec = derO_vec / val_num / len(poison_train_x)
            self.poison_x[:, :feature_num]=self.poison_x[:, :feature_num]+3000*deltaX_vec
            
   