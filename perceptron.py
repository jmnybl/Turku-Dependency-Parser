import numpy

class GPerceptron(object):

    def __init__(self,w_len,float_array_type=numpy.float64,float_type=numpy.float64_):
        self.w_len=w_len
        self.float_array_type=float_array_type
        self.float_type=float_type
        self.w=numpy.zeros(w_len,float_type)
        self.w_avg=numpy.zeros(w_len,float_type)

    def feature2dim(self,feature_name):
        """
        Translates `feature_name` (string) to weight vector dimension (int)
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

        This is a pure-Python fallback, a cython version will need to be implemented for speed
        """
        res=0.0
        for feature_name,count in features.iter_items():
            dim=self.feature2dim(feature_name)
            res+=self.w*count
        return res

    
§
