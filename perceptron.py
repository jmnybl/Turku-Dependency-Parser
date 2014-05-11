from __future__ import division
import numpy

class GPerceptron(object):

    def __init__(self,w_len,float_array_type=numpy.float64,float_type=numpy.float64_):
        self.w_len=w_len
        self.float_array_type=float_array_type 
        self.float_type=float_type
        self.w=numpy.zeros(w_len,float_type)
        self.w_avg=numpy.zeros(w_len,float_type) #Running sum of self.w for the averaged perceptron
        self.w_avg_N=0 #How many vectors are summed in w_avg?

    def feature2dim(self,feature_name):
        """
        Translates `feature_name` (string) to the corresponding weight vector dimension (int)
        """
        v=hash(feature_name)
        if v<0:
            return (-feature_name)%self.w_len
        else:
            return feature_name%self.w_len
        
    def score(self,features):
        """
        Gives the score for the features, where features is
        a dict()-like object mapping feature_name:count
        """
        res=0.0
        for feature_name,weight in features.iter_items():
            dim=self.feature2dim(feature_name)
            res+=self.w[dim]*weight
        return res

    
    def update(self,system_features,gold_features,system_score,gold_score):
        """
        Updates the weight vector w.r.t. to the
        difference between `features` and `gold_features`
        """
        self.w_avg_N+=1 #count the update runs, so we can take the average vector at the end

        norm2=0.0 #denominator for tau, the P-A update weight
        #loop over features in gold
        for feature_name,feature_weight in gold_features:
            norm2+=(feature_weight-system_features.get(feature_name,0.0))**2
        #loop over features in system pred. which are not in gold
        for feature_name,feature_weight in system_features:
            if feature_name not in gold_features: #must not count these twice
                norm2+=feature_weight**2
        
        tau=math.abs(system_score-gold_score)/norm2 ### P-A update weight TODO:Check the loss f()!

        #Do the update
        for feature_name,feature_weight in gold_features:
            dim=self.feature2dim[feature_name]
            self.w[dim]+=tau*(feature_weight-system_features.get(feature_name,0.0))
            self.w_avg[dim]+=self.w[dim]
        #loop over features in system pred. which are not in gold
        for feature_name,feature_weight in system_features:
            if feature_name not in gold_features: #must not count these twice
                dim=self.feature2dim[feature_name]
                self.w[dim]+=tau*(feature_weight-system_features.get(feature_name,0.0))
                self.w_avg[dim]+=self.w[dim]
                
