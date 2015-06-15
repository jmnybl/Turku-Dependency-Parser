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
        return cls(matrix,input)

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
    def load(cls,dirname,input=None):
        if input is None:
            input=T.imatrix("M")
        with open(os.path.join(dirname,"vs_order.json"),"w") as f:
            wvlib_order=json.load(f)
        wvlib_dict={}
        for name in wvlib_order:
            if name not in wvlib_dict:
                wvlib_dict[name]=wvlib.load(os.path.join(dirname,name+".bin"))
        return cls.from_wvlibs(wvlib_dict,wvlib_order,input)

    def save(self,dirname):
        with open(os.path.join(dirname,"vs_order.json"),"w") as f:
            json.dump(self.wvlib_order,f)
        for name,wvlib_obj in self.wvlib_dict.iteritems():
            if wvlib_obj is None:
                continue
            out=os.path.join(dirname,name+".bin")
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
        W=numpy.load(os.path.join(dir_name,file_name+"_W.npy"))
        b=numpy.load(os.path.join(dir_name,file_name+"_b.npy"))
        return cls(input,W,b,classes)

    @classmethod
    def empty(cls,n_in,classes,input=None):
        if input is None:
            input=T.matrix('x',theano.config.floatX)
        n_out=len(classes)
        W=numpy.zeros((n_in,n_out),theano.config.floatX)
        b=numpy.zeros((n_out,),theano.config.floatX)
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
        W=numpy.load(os.path.join(dir_name,file_name+"_W.npy"))
        b=numpy.load(os.path.join(dir_name,file_name+"_b.npy"))
        return cls(input,W,b)

    @classmethod
    def empty(cls,n_in,n_out,rng=None,input=None):
        if input is None:
            input=T.matrix('x')
        if rng is None:
            rng = numpy.random.RandomState(5678)
        W = numpy.asarray(rng.uniform(low=-numpy.sqrt(6.0 / (n_in + n_out)),high=numpy.sqrt(6.0 / (n_in + n_out)),size=(n_in, n_out)),
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
        lin_output = T.dot(input, self.W) + self.b
        self.output = (
            lin_output if activation is None
            else activation(lin_output)
        )
        self.params = [self.W, self.b]


# start-snippet-2
class MLP(object):
    """Multi-Layer Perceptron Class

    A multilayer perceptron is a feedforward artificial neural network model
    that has one layer or more of hidden units and nonlinear activations.
    Intermediate layers usually have as activation function tanh or the
    sigmoid function (defined here by a ``HiddenLayer`` class)  while the
    top layer is a softamx layer (defined here by a ``LogisticRegression``
    class).
    """

    @classmethod
    def load(cls,dir_name,input=None):
        if input is None:
            input=T.matrix('x')
        hidden_layer=HiddenRepLayer.load(os.path.join(dir_name,"hidden"),input)
        softmax_dtype=SoftMaxLayer.load(os.path.join(dir_name,"smax_dtype"),input=hidden_layer.output)
        return cls(hidden_layer,softmax_dtype)

    @classmethod
    def empty(cls,n_in,n_hidden,classes,input=None):
        if input is None:
            input=T.matrix('x')
        hidden_layer=HiddenRepLayer.empty(n_in,n_hidden,input=input)
        softmax_dtype=SoftMaxLayer.empty(n_hidden,classes,input=hidden_layer.output)
        return cls(hidden_layer,softmax_dtype)
    
    def save(self,dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        self.hiddenLayer.save(os.path.join(dir_name,"hidden"))
        self.softmax_dtype.save(os.path.join(dir_name,"smax_dtype"))
        

    def __init__(self, hidden_layer, softmax_dtype):
        """Initialize the parameters for the multilayer perceptron

        """
        
        self.hiddenLayer = hidden_layer
        self.softmax_dtype = softmax_dtype
        self.input=self.hiddenLayer.input
        self.params = self.hiddenLayer.params
        self.train_classification_dtype = self.compile_train_classification(self.softmax_dtype) #)
        self.test_classification_dtype=self.compile_test(self.softmax_dtype) #

    def compile_test(self,softmax_layer):

        x = T.matrix('x',theano.config.floatX)
        return theano.function(
            inputs=[x],
            outputs=softmax_layer.y_pred,
            givens={self.hiddenLayer.input:x}
            )

    def compile_train_classification(self,softmax_layer):
        """Builds the function self.train_classification_model(x,y,l_rate) which returns the cost. softmax_layer should be one
        of the softmax_layers in the mlp"""

        x = T.matrix('x',theano.config.floatX)  # minibatch, input
        y = T.vector('y','int32')  # minibatch, output
        l_rate = T.scalar('lrate',theano.config.floatX) #Learning rate
        l1_reg = T.scalar('l1_reg',theano.config.floatX) #Learning rate
        l2_reg = T.scalar('l2_reg',theano.config.floatX) #Learning rate

        L1 = (
            abs(self.hiddenLayer.W).sum()
            + abs(softmax_layer.W).sum()
        )

        L2_sqr = (
            (self.hiddenLayer.W ** 2).sum()
            + (softmax_layer.W ** 2).sum() + (self.hiddenLayer.b ** 2).sum() + (softmax_layer.b ** 2).sum()
        )


        neg_likelihood=-T.mean(T.log(softmax_layer.p_y_given_x)[T.arange(y.shape[0]), y])
        classification_cost=neg_likelihood+l1_reg*L1+l2_reg*L2_sqr
        gparams = [T.grad(classification_cost, param) for param in self.params+softmax_layer.params]

        # specify how to update the parameters of the model as a list of
        # (variable, update expression) pairs

        updates = [
            (param, param - l_rate * gparam)
            for param, gparam in zip(self.params, gparams)
            ]

        # compiling a Theano function `train_model` that returns the cost, but
        # in the same time updates the parameter of the model based on the rules
        # defined in `updates`
        return theano.function(
            inputs=[x,y,l_rate,l1_reg,l2_reg],
            outputs=classification_cost,
            updates=updates,
            givens={
                self.hiddenLayer.input: x
                }
            )


class MLP_WV(object):

    """A class with vector embeddings layer at the input and a MLP sitting on top
    input are indices into the embeddings"""
    
    @classmethod
    def load(cls,dir_name,input=None):
        if input is None:
            input=T.imatrix('M')
        wv_layer=VSpaceLayerCatenation.load(dir_name,input)
        mlp=MLP.load(dir_name,wv_layer.output)
        return cls(mlp,wv_layer,input)

    @classmethod
    def empty(cls,n_hidden,classes,wvlib_dict,wvlib_order,input=None):
        if input is None:
            input=T.imatrix('M')
        wv_layer=VSpaceLayerCatenation.from_wvlibs(wvlib_dict,wvlib_order,input=input)
        hidden_in=wv_layer.n_out()
        mlp=MLP.empty(hidden_in,n_hidden,classes,input=wv_layer.output)
        return cls(mlp,wv_layer,input)
    
    def save(self,dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        self.mlp.save(dir_name)
        self.wv_layer.save(dir_name)

    def __init__(self,mlp,wv_layer,input):
        self.mlp=mlp
        self.wv_layer=wv_layer
        self.input=input
        self.compile_test()
        self.params=self.mlp.params+self.wv_layer.params
        self.compile_train_classification()

    def compile_test(self):

        x = T.imatrix('x')
        self.test_classification_model=theano.function(
            inputs=[x],
            outputs=self.mlp.softMaxLayer.y_pred,
            givens={self.wv_layer.input:x}
            )

    def compile_train_classification(self):
        """Builds the function self.train_classification_model(x,y,l_rate) which returns the cost"""

        x = T.imatrix('x')  # minibatch, input
        y = T.ivector('y')  # minibatch, output
        l_rate = T.scalar('lrate',theano.config.floatX) #Learning rate
        l1_reg = T.scalar('l1_reg',theano.config.floatX) #Learning rate
        l2_reg = T.scalar('l2_reg',theano.config.floatX) #Learning rate

        neg_likelihood=-T.mean(T.log(self.mlp.softMaxLayer.p_y_given_x)[T.arange(y.shape[0]), y])
        classification_cost=neg_likelihood+l1_reg*self.mlp.L1+l2_reg*self.mlp.L2_sqr
        gparams = [T.grad(classification_cost, param) for param in self.params]

        # specify how to update the parameters of the model as a list of
        # (variable, update expression) pairs

        updates = [
            (param, param - l_rate * gparam)
            for param, gparam in zip(self.params, gparams)
            ]

        # compiling a Theano function `train_model` that returns the cost, but
        # in the same time updates the parameter of the model based on the rules
        # defined in `updates`
        self.train_classification_model = theano.function(
            inputs=[x,y,l_rate,l1_reg,l2_reg],
            outputs=classification_cost,
            updates=updates,
            givens={
                self.wv_layer.input: x
                }
            )
