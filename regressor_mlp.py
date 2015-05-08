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

class SoftMaxLayer(object):
    """Multi-class Logistic Regression Class

    The logistic regression is fully described by a weight matrix :math:`W`
    and bias vector :math:`b`. Classification is done by projecting data
    points onto a set of hyperplanes, the distance to which is used to
    determine a class membership probability.
    """

    @classmethod
    def load(cls,file_name,input):
        with open(os.path.join(dir_name,file_name+"_classes.json"),"r") as f:
            classes=json.load(f)
        W=numpy.load(os.path.join(dir_name,file_name+"_W.npy"))
        b=numpy.load(os.path.join(dir_name,file_name+"_b.npy"))
        return cls(input,W,b,classes)

    @classmethod
    def empty(cls,input,n_in,n_out,classes):
        W=numpy.zeros((n_in,n_out),theano.config.floatX)
        b=numpy.zeros((n_out,),theano.config.floatX)
        return cls(input,W,b,classes)

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
            value=W,dtype=theano.config.floatX
            ),
            name='W',
            borrow=True
        )
        self.b = theano.shared(value=b,dtype=theano.config.floatX),
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
    def load(cls,file_name,input):
        W=numpy.load(os.path.join(dir_name,file_name+"_W.npy"))
        b=numpy.load(os.path.join(dir_name,file_name+"_b.npy"))
        return cls(input,W,b)

    @classmethod
    def empty(cls,input,n_in,n_out,rng=None):
        if rng is None:
            rng = numpy.random.RandomState(5678)

        W = numpy.asarray(rng.uniform(low=-numpy.sqrt(6. / (n_in + n_out)),high=numpy.sqrt(6. / (n_in + n_out)),size=(n_in, n_out)),
                dtype=theano.config.floatX
            )
        b=numpy.zeros((n_out,),theano.config.floatX)
        return cls(input,W,b)


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

        self.W = theano.shared(value=W_values, name='W', borrow=True)
        self.b = theano.shared(value=b_values, name='b', borrow=True)
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

    def load(self,dir_name):
        with open(os.path.join(dir_name,"classes.json"),"r") as f:
            self.classes=json.load(f)
        self.softMaxLayer.W.set_value(numpy.load(os.path.join(dir_name,"softmax_w.npy")))
        self.softMaxLayer.b.set_value(numpy.load(os.path.join(dir_name,"softmax_b.npy")))
        self.hiddenLayer.W.set_value(numpy.load(os.path.join(dir_name,"hidden_w.npy")))
        self.hiddenLayer.b.set_value(numpy.load(os.path.join(dir_name,"hidden_b.npy")))

    def save(self,dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(os.path.join(dir_name,"classes.json"),"w") as f:
            json.dump(self.classes,f)
        numpy.save(os.path.join(dir_name,"softmax_w.npy"),self.softMaxLayer.W.get_value(borrow=True))
        numpy.save(os.path.join(dir_name,"softmax_b.npy"),self.softMaxLayer.b.get_value(borrow=True))
        numpy.save(os.path.join(dir_name,"hidden_w.npy"),self.hiddenLayer.W.get_value(borrow=True))
        numpy.save(os.path.join(dir_name,"hidden_b.npy"),self.hiddenLayer.b.get_value(borrow=True))
        

    def __init__(self, rng, input, n_in, n_hidden, n_out, classes):
        """Initialize the parameters for the multilayer perceptron

        :type rng: numpy.random.RandomState
        :param rng: a random number generator used to initialize weights

        :type input: theano.tensor.TensorType
        :param input: symbolic variable that describes the input of the
        architecture (one minibatch)

        :type n_in: int
        :param n_in: number of input units, the dimension of the space in
        which the datapoints lie

        :type n_hidden: int
        :param n_hidden: number of hidden units

        :type n_out: int
        :param n_out: number of output units, the dimension of the space in
        which the labels lie

        """
        
        self.classes=classes

        # Since we are dealing with a one hidden layer MLP, this will translate
        # into a HiddenLayer with a tanh activation function connected to the
        # LogisticRegression layer; the activation function can be replaced by
        # sigmoid or any other nonlinear function
        self.input=input
        self.hiddenLayer = HiddenRepLayer(
            rng=rng,
            input=self.input,
            n_in=n_in,
            n_out=n_hidden
        )

        # The logistic regression layer gets as input the hidden units
        # of the hidden layer
        self.softMaxLayer = SoftMaxLayer(
            input=self.hiddenLayer.output,
            n_in=n_hidden,
            n_out=n_out
        )
        # end-snippet-2 start-snippet-3
        # L1 norm ; one regularization option is to enforce L1 norm to
        # be small
        self.L1 = (
            abs(self.hiddenLayer.W).sum()
            + abs(self.softMaxLayer.W).sum()
        )

        # square of L2 norm ; one regularization option is to enforce
        # square of L2 norm to be small
        self.L2_sqr = (
            (self.hiddenLayer.W ** 2).sum()
            + (self.softMaxLayer.W ** 2).sum() + (self.hiddenLayer.b ** 2).sum() + (self.softMaxLayer.b ** 2).sum()
        )

        # negative log likelihood of the MLP is given by the negative
        # log likelihood of the output of the model, computed in the
        # logistic regression layer
        
#        self.negative_log_likelihood = (
#            self.logRegressionLayer.negative_log_likelihood
#        )
        # same holds for the function computing the number of errors
#        self.errors = self.logRegressionLayer.errors

        # the parameters of the model are the parameters of the two layer it is
        # made out of
        self.params = self.hiddenLayer.params + self.softMaxLayer.params
        # end-snippet-3

        self.compile_train_classification() #compiles self.train_classification_model(x,y,l_rate)
        self.compile_test() #compiles self.test_classification_model(x)

    def compile_test(self):

        x = T.matrix('x',theano.config.floatX)
        self.test_classification_model=theano.function(
            inputs=[x],
            outputs=self.softMaxLayer.y_pred,
            givens={self.hiddenLayer.input:x}
            )

    def compile_train_classification(self):
        """Builds the function self.train_classification_model(x,y,l_rate) which returns the cost"""

        x = T.matrix('x',theano.config.floatX)  # minibatch, input
        y = T.vector('y','int32')  # minibatch, output
        l_rate = T.scalar('lrate',theano.config.floatX) #Learning rate
        l1_reg = T.scalar('l1_reg',theano.config.floatX) #Learning rate
        l2_reg = T.scalar('l2_reg',theano.config.floatX) #Learning rate

        neg_likelihood=-T.mean(T.log(self.softMaxLayer.p_y_given_x)[T.arange(y.shape[0]), y])
        classification_cost=neg_likelihood+l1_reg*self.L1+l2_reg*self.L2_sqr
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
                self.hiddenLayer.input: x
                }
            )







