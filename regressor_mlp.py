"""
Most of this code is cut'n'pasted from the Theano MLP tutorial
by @fginter.

"""
__docformat__ = 'restructedtext en'

import json
import os
import sys
import time

import numpy

import theano
import theano.tensor as T


import scipy
import codecs
from wvlib import wvlib

class VSpaceLayer(object):

    """A layer which has a vector of numerical indices on its input
    and the corresponding matrix rows on the output"""

    @classmethod
    def from_wvlib(cls,wvlib_obj,input):
        """Input should be an int vector which selects the matrix rows"""
        return cls(wvlib_obj.vectors(),input)

    @classmethod
    def from_matrix(cls,matrix,input):
        """Input should be an int vector which selects the matrix rows"""
        return cls(matrix.astype(theano.config.floatX),input)

    def __init__(self,matrix,input):
        self.input=input
        self.wordvecs = theano.shared(
            value=matrix,
            name='M',
            borrow=True
        )
        self.output=theano.sparse_grad(self.wordvecs[self.input])
        self.params=[self.wordvecs]


class VSpaceLayerCatenation(object):

    @classmethod
    def from_wvlibs(cls,wvlib_dict,wvlib_order,input):
        """Input is an int matrix. Each row contains one example and
        each column the index of one lexical entry in the embedding
        matrix. wvlib_dict is a dictionary "name"->wvlib and wvlib_order is a list of these names.
        """
        input_T=input.dimshuffle(1,0) #Transpose because each layer works on one column
        vsls=[]
        for i,name in enumerate(wvlib_order):
            vsls.append(VSpaceLayer.from_wvlib(wvlib_dict[name],input_T[i]))
        return cls(vsls,wvlib_dict,wvlib_order,input)

    @classmethod
    def load(cls,fileprefix,input=None):
        if input is None:
            input=T.imatrix("M")
        with open(fileprefix+"_vs_order.json","r") as f:
            wvlib_order=json.load(f)
        wvlib_dict={}
        for name in wvlib_order:
            if name not in wvlib_dict:
                wvlib_dict[name]=wvlib.load(fileprefix+"_"+name+".bin")
                wvlib_dict[name]._vectors.vectors=wvlib_dict[name]._vectors.vectors.astype(theano.config.floatX)
        return cls.from_wvlibs(wvlib_dict,wvlib_order,input)

    def save(self,fileprefix):
        with open(fileprefix+"_vs_order.json","w") as f:
            json.dump(self.wvlib_order,f)
        for name,wvlib_obj in self.wvlib_dict.iteritems():
            if wvlib_obj is None:
                continue
            out=fileprefix+"_"+name+".bin"
            print >> sys.stderr, "Saving...", out
            wvlib_obj.save_bin(out)

    def __init__(self,vspace_layers,wvlib_dict,wvlib_order,input):
        self.input=input
        self.vspace_layers=vspace_layers
        self.wvlib_dict=wvlib_dict
        self.wvlib_order=wvlib_order
        self.output=T.concatenate([l.output for l in self.vspace_layers],axis=1)
        self.params=[]
        for l in self.vspace_layers:
            self.params.extend(l.params)
        x=T.imatrix('X')
        self.calcvals=theano.function([x],outputs=self.output,givens={self.input:x})

    def n_out(self):
        """How many output dimensions will I have?"""
        return sum(l.wordvecs.get_value(borrow=True).shape[1] for l in self.vspace_layers)

class SoftMaxLayer(object):
    """Multi-class Logistic Regression Class

    The logistic regression is fully described by a weight matrix :math:`W`
    and bias vector :math:`b`. Classification is done by projecting data
    points onto a set of hyperplanes, the distance to which is used to
    determine a class membership probability.
    """

    @classmethod
    def load(cls,file_name,input=None):
        if input is None:
            input=T.matrix('x',theano.config.floatX)
        with open(file_name+"_classes.json","r") as f:
            classes=json.load(f)
        W=numpy.load(file_name+"_W.npy").astype(theano.config.floatX)
        b=numpy.load(file_name+"_b.npy").astype(theano.config.floatX)
        return cls(input,W,b,classes)

    @classmethod
    def empty(cls,n_in,classes,input=None,rng=None):
        if input is None:
            input=T.matrix('x',theano.config.floatX)
        if rng is None:
            rng = numpy.random.RandomState(5678)
        #W = numpy.asarray(rng.uniform(low=-numpy.sqrt(6.0 / (n_in + n_out)),high=numpy.sqrt(6.0 / (n_in + n_out)),size=(n_in, n_out)),
        #        dtype=theano.config.floatX
        #    )
        n_out=len(classes)
        W = numpy.asarray(rng.uniform(low=-0.01,high=0.01,size=(n_in, n_out)),
                dtype=theano.config.floatX
            )
        b=numpy.asarray(rng.uniform(low=-0.01,high=0.01,size=(n_out,)),theano.config.floatX)

        #W=numpy.zeros((n_in,n_out),theano.config.floatX)
        #b=numpy.zeros((n_out,),theano.config.floatX)
        return cls(input,W,b,classes)

    
    def save(self,file_name):
        with open(file_name+"_classes.json","w") as f:
            json.dump(self.classes,f)
        numpy.save(file_name+"_W.npy",self.W.get_value(borrow=True))
        numpy.save(file_name+"_b.npy",self.b.get_value(borrow=True))

    def __init__(self, input, W, b, classes):
        """ Initialize the parameters of the logistic regression

        :type input: theano.tensor.TensorType
        :param input: symbolic variable that describes the input of the
                      architecture (one minibatch)

        :type n_in: int
        :param n_in: number of input units, the dimension of the space in
                     which the datapoints lie

        :type n_out: int
        :param n_out: number of output units, the dimension of the space in
                      which the labels lie

        """

        self.classes=classes
        self.W = theano.shared(
            value=W,
            name='W',
            borrow=True
        )
        self.b = theano.shared(value=b,
            name='b',
            borrow=True
        )

        # symbolic expression for computing the matrix of class-membership
        # probabilities
        # Where:
        # W is a matrix where column-k represent the separation hyper plain for
        # class-k
        # x is a matrix where row-j  represents input training sample-j
        # b is a vector where element-k represent the free parameter of hyper
        # plain-k

        self.input=input
        self.p_y_given_x = T.nnet.softmax(T.dot(input, self.W) + self.b)
        # symbolic description of how to compute prediction as class whose
        # probability is maximal
        self.y_pred = T.argmax(self.p_y_given_x, axis=1)
        # end-snippet-1
        # parameters of the model
        self.params = [self.W, self.b]


    def negative_log_likelihood(self, y):
        """Return the mean of the negative log-likelihood of the prediction
        of this model under a given target distribution.

        .. math::

            \frac{1}{|\mathcal{D}|} \mathcal{L} (\theta=\{W,b\}, \mathcal{D}) =
            \frac{1}{|\mathcal{D}|} \sum_{i=0}^{|\mathcal{D}|}
                \log(P(Y=y^{(i)}|x^{(i)}, W,b)) \\
            \ell (\theta=\{W,b\}, \mathcal{D})

        :type y: theano.tensor.TensorType
        :param y: corresponds to a vector that gives for each example the
                  correct label

        Note: we use the mean instead of the sum so that
              the learning rate is less dependent on the batch size
        """
        # start-snippet-2
        # y.shape[0] is (symbolically) the number of rows in y, i.e.,
        # number of examples (call it n) in the minibatch
        # T.arange(y.shape[0]) is a symbolic vector which will contain
        # [0,1,2,... n-1] T.log(self.p_y_given_x) is a matrix of
        # Log-Probabilities (call it LP) with one row per example and
        # one column per class LP[T.arange(y.shape[0]),y] is a vector
        # v containing [LP[0,y[0]], LP[1,y[1]], LP[2,y[2]], ...,
        # LP[n-1,y[n-1]]] and T.mean(LP[T.arange(y.shape[0]),y]) is
        # the mean (across minibatch examples) of the elements in v,
        # i.e., the mean log-likelihood across the minibatch.
        return -T.mean(T.log(self.p_y_given_x)[T.arange(y.shape[0]), y])
        # end-snippet-2



# start-snippet-1
class HiddenRepLayer(object):

    @classmethod
    def load(cls,file_name,input=None):
        if input is None:
            input=T.matrix('x')
        W=numpy.load(file_name+"_W.npy").astype(theano.config.floatX)
        b=numpy.load(file_name+"_b.npy").astype(theano.config.floatX)
        return cls(input,W,b)

    @classmethod
    def empty(cls,n_in,n_out,rng=None,input=None):
        if input is None:
            input=T.matrix('x')
        if rng is None:
            rng = numpy.random.RandomState(5678)
        #W = numpy.asarray(rng.uniform(low=-numpy.sqrt(6.0 / (n_in + n_out)),high=numpy.sqrt(6.0 / (n_in + n_out)),size=(n_in, n_out)),
        #        dtype=theano.config.floatX
        #    )
        W = numpy.asarray(rng.uniform(low=-0.01,high=0.01,size=(n_in, n_out)),
                dtype=theano.config.floatX
            )
        b=numpy.zeros((n_out,),theano.config.floatX)
        return cls(input,W,b)

    def save(self,file_name):
        numpy.save(file_name+"_W.npy",self.W.get_value(borrow=True))
        numpy.save(file_name+"_b.npy",self.b.get_value(borrow=True))


    def __init__(self, input, W, b, activation=T.tanh):
        """
        Typical hidden layer of a MLP: units are fully-connected and have
        sigmoidal activation function. Weight matrix W is of shape (n_in,n_out)
        and the bias vector b is of shape (n_out,).

        NOTE : The nonlinearity used here is tanh

        Hidden unit activation is given by: tanh(dot(input,W) + b)

        :type rng: numpy.random.RandomState
        :param rng: a random number generator used to initialize weights

        :type input: theano.tensor.dmatrix
        :param input: a symbolic tensor of shape (n_examples, n_in)

        :type n_in: int
        :param n_in: dimensionality of input

        :type n_out: int    
        :param n_out: number of hidden units

        :type activation: theano.Op or function
        :param activation: Non linearity to be applied in the hidden
                           layer
        """

        # end-snippet-1

        # `W` is initialized with `W_values` which is uniformely sampled
        # from sqrt(-6./(n_in+n_hidden)) and sqrt(6./(n_in+n_hidden))
        # for tanh activation function
        # the output of uniform if converted using asarray to dtype
        # theano.config.floatX so that the code is runable on GPU
        # Note : optimal initialization of weights is dependent on the
        #        activation function used (among other things).
        #        For example, results presented in [Xavier10] suggest that you
        #        should use 4 times larger initial weights for sigmoid
        #        compared to tanh
        #        We have no info for other function, so we use the same as
        #        tanh.

        self.input=input

        self.W = theano.shared(value=W, name='W', borrow=True)
        self.b = theano.shared(value=b, name='b', borrow=True)
        lin_output=T.dot(input, self.W) + self.b
        #self.output= (lin_output)**3.0
        self.output = (
            lin_output if activation is None
            else activation(lin_output)
        )
        self.params = [self.W, self.b]
        self.n_out=self.W.get_value(borrow=True).shape[1]


class MLP_WV(object):

    """A class with vector embeddings layer at the input and a MLP sitting on top
    input are indices into the embeddings. Two softmax output layers exist, one for
    the next move, and one for the type"""
    
    @classmethod
    def load(cls,dir_name,input=None):
        if input is None:
            input=T.imatrix('M')
        wv_layer=VSpaceLayerCatenation.load(os.path.join(dir_name,"wv"),input)
        hidden_dep=HiddenRepLayer.load(os.path.join(dir_name,"hidden_dep"),input=wv_layer.output)
        softmax_dtype=SoftMaxLayer.load(os.path.join(dir_name,"smax_dtype"),input=hidden_dep.output)
        softmax_move=SoftMaxLayer.load(os.path.join(dir_name,"smax_move"),input=hidden_dep.output)
        return cls(wv_layer,hidden_dep,softmax_dtype,softmax_move,input)

    @classmethod
    def empty(cls,n_hidden,classes,wvlib_dict,wvlib_order,input=None):
        if input is None:
            input=T.imatrix('M')
        wv_layer=VSpaceLayerCatenation.from_wvlibs(wvlib_dict,wvlib_order,input=input)
        hidden_in=wv_layer.n_out()
        hidden_dep=HiddenRepLayer.empty(hidden_in,n_hidden,input=wv_layer.output)
        softmax_dtype=SoftMaxLayer.empty(n_hidden,classes,input=hidden_dep.output)
        softmax_move=SoftMaxLayer.empty(n_hidden,{"SHIFT":0,"RIGHT":1,"LEFT":2,"SWAP":3},input=hidden_dep.output)
        return cls(wv_layer,hidden_dep,softmax_dtype,softmax_move,input)
    
    def save(self,dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        self.hidden_dep.save(os.path.join(dir_name,"hidden_dep"))
        self.softmax_dtype.save(os.path.join(dir_name,"smax_dtype"))
        self.softmax_move.save(os.path.join(dir_name,"smax_move"))
        self.wv_layer.save(os.path.join(dir_name,"wv"))

    def __init__(self,wv_layer,hidden_dep,softmax_dtype,softmax_move,input):
        self.input=input
        self.wv_layer=wv_layer
        self.hidden_dep=hidden_dep
        self.softmax_dtype=softmax_dtype
        self.softmax_move=softmax_move
        self.params=self.hidden_dep.params+self.wv_layer.params #These are optimized across all softmax layers
        self.train_classification_dtype = self.compile_train_classification(self.softmax_dtype) #)
        self.test_classification_dtype=self.compile_test(self.softmax_dtype) #
        self.test_scores_dtype=self.compile_test_scores(self.softmax_dtype) #
        self.train_classification_move = self.compile_train_classification(self.softmax_move) #)
        self.test_classification_move=self.compile_test(self.softmax_move) #
        self.test_scores_move=self.compile_test_scores(self.softmax_move) #

    def features_to_input(self,feats):
        """
        feats is a list of lists of state-related features as used in standalone training
        something like this:
        W:tunne POS:N FEAT:Case=Nom|Number=Sing POS_FEAT:N|Case=Nom|Number=Sing W:NONE POS:NONE FEAT:NONE POS_FEAT:NONE|NONE
        
        because we work in a mini-batch mode, we take a list of lists, not a list
        
        these need to match the order for which the W2V layer was built, and are obtained from State()
        
        """
        res=numpy.zeros((len(feats),len(self.wv_layer.vspace_layers)),numpy.int32)
        for row_idx,feat_list in enumerate(feats):
            col_idx=0
            for w in feat_list:
                t,w=w.split(":",1)
                if self.wv_layer.wvlib_dict.get(t) is None:
                    #this feature type is off
                    continue
                #wv_row will be the row index in the vector embedding matrix
                if w!=u"NONE":
                    try:
                        wv_row=self.wv_layer.wvlib_dict[t].rank(w)
                        #print "KNOWN", t, w.encode("utf-8")
                    except KeyError:
                        #print "UNK", t, w.encode("utf-8")
                        wv_row=0
                else:
                    wv_row=0
                res[row_idx,col_idx]=wv_row
                #print "SETTING ", t, w.encode("utf-8"), row_idx, col_idx, wv_row
                col_idx+=1
        assert col_idx==res.shape[1]
        return res
        
        

    def compile_test(self,softmax_layer):
        """softmax_layer is one of the possible output layers (this net will have several)"""
        x = T.imatrix('x')
        return theano.function(
            inputs=[x],
            outputs=softmax_layer.y_pred,
            givens={self.wv_layer.input:x}
            )

    def compile_test_scores(self,softmax_layer):
        """Same as compile_test, but returns the scores themselves, not the argmax class"""
        x=T.imatrix('x')
        return theano.function(
            inputs=[x],
            outputs=softmax_layer.p_y_given_x,
            givens={self.wv_layer.input:x}
            )


    def compile_train_classification(self,softmax_layer):
        """Builds the function self.train_classification_model(x,y,l_rate) which returns the cost. softmax_layer should be one
        of the softmax_layers in the mlp"""

        x = T.imatrix('x')  # minibatch, input
        y = T.ivector('y')  # minibatch, output
        l_rate = T.scalar('lrate',theano.config.floatX) #Learning rate
        l1_reg = T.scalar('l1_reg',theano.config.floatX) #Learning rate
        l2_reg = T.scalar('l2_reg',theano.config.floatX) #Learning rate

        L1 = (
            abs(self.hidden_dep.W).sum()
            + abs(softmax_layer.W).sum()
        )

        L2_sqr = (
            (self.hidden_dep.W ** 2).sum()
            + (softmax_layer.W ** 2).sum() + (self.hidden_dep.b ** 2).sum() + (softmax_layer.b ** 2).sum()
        )


        neg_likelihood=-T.mean(T.log(softmax_layer.p_y_given_x)[T.arange(y.shape[0]), y])
        classification_cost=neg_likelihood+l2_reg*L2_sqr+l1_reg*0.0#L1+l2_reg*L2_sqr
        gparams = [T.grad(classification_cost, param) for param in self.params+softmax_layer.params]

        # specify how to update the parameters of the model as a list of
        # (variable, update expression) pairs

        updates = [
            (param, param - l_rate * gparam)
            for param, gparam in zip(self.params+softmax_layer.params, gparams)
            ]

        # compiling a Theano function `train_model` that returns the cost, but
        # in the same time updates the parameter of the model based on the rules
        # defined in `updates`
        return theano.function(
            inputs=[x,y,l_rate,l1_reg,l2_reg],
            outputs=classification_cost,
            updates=updates,
            givens={
                self.wv_layer.input: x
                }
            )
