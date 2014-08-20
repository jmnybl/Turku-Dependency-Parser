#cython: boundscheck=False, wraparound=False, cdivision=True

import cython
import numpy
cimport numpy
from cpython cimport bool
from libc.stdint cimport int32_t
#cimport murmurhash

from libc.stdint cimport uint64_t, int64_t
cdef extern from "MurmurHash3.h":
    void MurmurHash3_x86_32(void * key, uint64_t len, uint64_t seed, void* out)

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
    Translates `feature_name` (string) to the corresponding weight vector dimension (int).
    """
    cdef int32_t v
    cdef int32_t w_len=self.w_len

    py_byte_string = feature_name.encode('UTF-8')
    cdef char* c_string = py_byte_string

    MurmurHash3_x86_32(c_string, len(py_byte_string), 0, &v) # feature_name.hash() #sklearn.utils.murmurhash.murmurhash3_32(feature_name)
    if v<0:
        return (-v)%w_len
    else:
        return v%w_len
