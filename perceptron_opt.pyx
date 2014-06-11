import cython
import numpy
cimport numpy
from cpython cimport bool

DOUBLETYPE = numpy.float64
ctypedef numpy.float64_t DOUBLETYPE_t

@cython.boundscheck(False)
def _score_f(self,features,bool test_time=False, unicode prefix=u""):
    """
    Gives the score for the features, where features is
    a dict()-like object mapping feature_name:count
    """
    cdef DOUBLETYPE_t res=0.0
    cdef DOUBLETYPE_t weight
    cdef unsigned long dim
    cdef unicode feature_name
    cdef numpy.ndarray[DOUBLETYPE_t, ndim=1] w
    if test_time:
        w=self.w_avg
    else:
        w=self.w
    for feature_name,weight in features.iteritems():
        dim=_feature2dim(self,prefix+feature_name)
        res+=w[dim]*weight
    if test_time:
        res/=self.update_counter.value
    return res


def _feature2dim(self, unicode feature_name):
    """
    Translates `feature_name` (string) to the corresponding weight vector dimension (int)
    """
    cdef long int v
    cdef long int w_len=self.w_len
    v=hash(feature_name)
    if v<0:
        return (-v)%w_len
    else:
        return v%w_len
