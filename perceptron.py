from __future__ import division
import math
import numpy
import os.path
import json
import logging
import multiprocessing

logging.basicConfig(level=logging.INFO)

class PerceptronSharedState(object):

    """This object actually holds the shared memory arrays and variables
    needed for the multi-process learning. The `GPerceptron` objects 
    update this state through shared memory."""
    
    @classmethod
    def load(cls,model_name,retrainable=False):
        """
        Load the perceptron state from `model_name` (which is a directory holding all model files)

        `retrainable`: should we load also the weight vector and
                       meta-data necessary for restarting the
                       training?
        """
        if not os.path.exists(model_name):
            raise ValueError(model_name+": no such model")
        with open(os.path.join(model_name,"config.json"),"r") as f:
            d=json.load(f) #dictionary with parameters
        if os.path.exists(os.path.join(model_name,"w.npy")) and retrainable:
            w=numpy.load(os.path.join(model_name,"w.npy"))
        else:
            w=None
        w_avg=numpy.load(os.path.join(model_name,"w_avg.npy"))
        float_array_type=w_avg.dtype
        gp=cls(w=w,w_avg=w_avg,float_array_type=float_array_type,**d)
        return gp

class GPerceptron(object):

    @classmethod
    def load(cls,model_name,retrainable=False):
        """
        Load the perceptron from `model_name` (which is a directory holding all model files)

        `retrainable`: should we load also the weight vector and
                       meta-data necessary for restarting the
                       training?
        """
        if not os.path.exists(model_name):
            raise ValueError(model_name+": no such model")
        with open(os.path.join(model_name,"config.json"),"r") as f:
            d=json.load(f) #dictionary with parameters
        w=numpy.load(os.path.join(model_name,"w.npy"))
        if os.path.exists(os.path.join(model_name,"w.npy")) and retrainable:
            w=numpy.load(os.path.join(model_name,"w.npy"))
        else:
            w=None
        w_avg=numpy.load(os.path.join(model_name,"w_avg.npy"))
        float_array_type=w_avg.dtype
        gp=cls(w=w,w_avg=w_avg,float_array_type=float_array_type,**d)
        return gp

    def save(self,model_name,retrainable=False):
        """
        Save the model. If `retrainable` is set, also save the current
        vector and other run-time information needed to restart the
        training.
        """
        if not os.path.exists(model_name):
            os.makedirs(model_name)
        numpy.save(os.path.join(model_name,"w_avg.npy"),self.w_avg)
        d={"w_len":self.w_len}
        if retrainable:
            numpy.save(os.path.join(model_name,"w.npy"),self.w)
            d["w_avg_N"]=self.w_avg_N
        with open(os.path.join(model_name,"config.json"),"w") as f:
            json.dump(d,f)

    def __init__(self,w_len,w_avg=None,w=None,w_avg_N=0,float_array_type=numpy.float64):
        self.w_len=w_len
        self.float_array_type=float_array_type 
        if w==None:
            self.w=numpy.zeros(w_len,float_array_type)
        else:
            self.w=w
        if w_avg==None:
            self.w_avg=numpy.zeros(w_len,float_array_type) #Running sum of self.w for the averaged perceptron
        else:
            self.w_avg=w_avg
        self.w_avg_N=w_avg_N #How many vectors are summed in w_avg?

    def feature2dim(self,feature_name):
        """
        Translates `feature_name` (string) to the corresponding weight vector dimension (int)
        """
        v=hash(feature_name)
        if v<0:
            return (-v)%self.w_len
        else:
            return v%self.w_len
        
    def score(self,features):
        """
        Gives the score for the features, where features is
        a dict()-like object mapping feature_name:count
        """
        res=0.0
        for feature_name,weight in features.iteritems():
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
        for feature_name,feature_weight in gold_features.iteritems():
            norm2+=(feature_weight-system_features.get(feature_name,0.0))**2
        #loop over features in system pred. which are not in gold
        for feature_name,feature_weight in system_features.iteritems():
            if feature_name not in gold_features: #must not count these twice
                norm2+=feature_weight**2
        tau=(1.0+system_score-gold_score)/norm2 ### P-A update weight TODO:Check the loss f()!
        print ">>>>>>", system_score, gold_score
        assert tau>=0.0 and norm2>=0.0
        #print "tau:",tau,"norm2:",norm2
        #print system_features,gold_features
        #Do the update
        for feature_name,feature_weight in gold_features.iteritems():
            dim=self.feature2dim(feature_name)
            self.w[dim]+=tau*(feature_weight-system_features.get(feature_name,0.0))
            self.w_avg[dim]+=self.w[dim]
        #loop over features in system pred. which are not in gold
        for feature_name,feature_weight in system_features.iteritems():
            if feature_name not in gold_features: #must not count these twice
                dim=self.feature2dim(feature_name)
                self.w[dim]+=tau*(feature_weight-system_features.get(feature_name,0.0))
                self.w_avg[dim]+=self.w[dim]
                

if __name__=="__main__":
    #Little test only, really
    gp=GPerceptron(w_len=100000)
    gp.save("test.gp",retrainable=True)
    gp=GPerceptron.load("test.gp",retrainable=True)

    
