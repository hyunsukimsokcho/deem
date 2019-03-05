import numpy as np

class Reweighing:
    def __init__(self, data, label, feature, p_group, up_group):
        """
        Constructor for reweighing component
        """
        self.data = data
        self.label = label
        self.p_feature = feature + "_" + p_group
        self.up_feature = feature + "_" + up_group

    def change_data(self, data, label):
        """
        Change raw data to poisoned data
        """
        self.data = data
        self.label = label
        
    def calculate_weight(self):
        """
        Calculate weight for each data parition
        """
        data = self.data
        label = self.label
        size = len(data)

        p_index = self.data.index[data[self.p_feature]==1].tolist()
        up_index = self.data.index[data[self.up_feature]==1].tolist()
        f_index = label.index[label.values==1].tolist()    
        uf_index = label.index[label.values==0].tolist()

        f_up_index = list(set(f_index)&set(up_index))
        f_p_index = list(set(f_index)&set(p_index))
        uf_up_index = list(set(uf_index)&set(up_index))
        uf_p_index = list(set(uf_index)&set(p_index))
                            
        weight_f_up = len(f_index) * len(up_index) / (size * len(f_up_index))
        weight_f_p = len(f_index) * len(p_index) / (size * len(f_p_index))
        weight_uf_up = len(uf_index) * len(up_index) / (size * len(uf_up_index))
        weight_uf_p = len(uf_index) * len(p_index) / (size * len(uf_p_index))
                                            
        weight = np.zeros(size)
        weight[f_up_index] = weight_f_up
        weight[f_p_index] = weight_f_p
        weight[uf_up_index] = weight_uf_up
        weight[uf_p_index] = weight_uf_p

        return weight

    def fairness_measure(self, model):
        """
        For trained model, calculate demographic parity
        """
        data = self.data
        prediction = model.predict(self.data)
        p_index = data.index[data[self.p_feature]==1].tolist()
        up_index = data.index[data[self.up_feature]==1].tolist()

        p_prediction = prediction[p_index]
        up_prediction = prediction[up_index]
        p_ratio = np.sum(p_prediction) / len(p_prediction)
        up_ratio = np.sum(up_prediction) / len(up_prediction)
        return up_ratio/p_ratio

