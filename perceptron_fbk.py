# These are pure-python fallback functions
# used in case cython import fails for some
# reason

def _score_f(self,features,test_time=False, prefix=u""):
    """
    Gives the score for the features, where features is
    a dict()-like object mapping feature_name:count
    """
    res=0.0
    if test_time:
        w=self.w_avg
    else:
        w=self.w
    for feature_name,weight in features.iteritems():
        dim=self.feature2dim(prefix+feature_name)
        res+=w[dim]*weight
    if test_time:
        res/=self.update_counter.value
    return res

def _feature2dim(self,feature_name):
    """
    Translates `feature_name` (string) to the corresponding weight vector dimension (int)
    """
    v=hash(feature_name)
    if v<0:
        return (-v)%self.w_len
    else:
        return v%self.w_len
