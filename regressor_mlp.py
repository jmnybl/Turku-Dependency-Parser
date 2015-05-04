"""
Most of this code is cut'n'pasted from the Theano MLP tutorial
by @fginter.

"""
__docformat__ = 'restructedtext en'


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

    def __init__(self, input, n_in, n_out):
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

        self.input=input
        # start-snippet-1
        # initialize with 0 the weights W as a matrix of shape (n_in, n_out)
        self.W = theano.shared(
            value=numpy.zeros(
                (n_in, n_out),
                dtype=theano.config.floatX
            ),
            name='W',
            borrow=True
        )
        # initialize the baises b as a vector of n_out 0s
        self.b = theano.shared(
            value=numpy.zeros(
                (n_out,),
                dtype=theano.config.floatX
            ),
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
        self.p_y_given_x = T.nnet.softmax(T.dot(input, self.W) + self.b)

        # symbolic description of how to compute prediction as class whose
        # probability is maximal
        self.y_pred = T.argmax(self.p_y_given_x, axis=1)
        # end-snippet-1

        # parameters of the model
        self.params = [self.W, self.b]

# start-snippet-1
class HiddenRepLayer(object):
    def __init__(self, rng, input, n_in, n_out, W=None, b=None,
                 activation=T.tanh):
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

        ### TODO: add shared memory support
        if W is None:
            W_values = numpy.asarray(
                rng.uniform( 
                   low=-numpy.sqrt(6. / (n_in + n_out)),
                    high=numpy.sqrt(6. / (n_in + n_out)),
                    size=(n_in, n_out)
                ),
                dtype=theano.config.floatX
            )

            W = theano.shared(value=W_values, name='W', borrow=True)

        if b is None:
            b_values = numpy.zeros((n_out,), dtype=theano.config.floatX)
            b = theano.shared(value=b_values, name='b', borrow=True)

        self.W = W
        self.b = b

        lin_output = T.dot(input, self.W) + self.b
        self.output = (
            lin_output if activation is None
            else activation(lin_output)
        )
        # parameters of the model
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

    def __init__(self, rng, input, n_in, n_hidden, n_out):
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
        self.params = self.hiddenLayer.params + self.softmaxLayer.params
        # end-snippet-3

        self.compile_train_classification() #compiles self.train_classification_model(x,y,l_rate)

    def compile_train_classification(self):
        """Builds the function self.train_classification_model(x,y,l_rate) which returns the cost"""

        x = T.matrix('x',theano.config.floatX)  # minibatch, input
        y = T.matrix('y',theano.config.floatX)  # minibatch, output
        l_rate = T.dscalar('lrate',theano.config.floatX) #Learning rate

        classification_cost=((self.softmaxLayer.y_regress-y)**2).sum()
        gparams = [T.grad(classification_cost, param) for param in self.params]

        # specify how to update the parameters of the model as a list of
        # (variable, update expression) pairs

        updates = [
            (param, param - l_rate * gparam)
            for param, gparam in zip(classifier.params, gparams)
            ]

        # compiling a Theano function `train_model` that returns the cost, but
        # in the same time updates the parameter of the model based on the rules
        # defined in `updates`
        self.train_classification_model = theano.function(
            inputs=[x,y,l_rate],
            outputs=classification_cost,
            updates=updates,
            givens={
                self.hiddenLayer.input: x
                }
            )








    # def eval(self,X,types_model,correct_classes):
    #     tst = theano.function(
    #         inputs=[],
    #         outputs=self.softmaxLayer.y_regress,
    #         givens=[(self.hiddenLayer.input,X)]
    #     )
    #     regressions=tst()
    #     correct=0
    #     for i in xrange(len(correct_classes)):
    #         pred=types_model.nearest(regressions[i],n=1)
    #         if pred[0][0]==correct_classes[i]:
    #             correct+=1
    #     return float(correct)/len(correct_classes)
            
# #jmnybl@epsilon-it:~/git_checkout/parser-vectors.git/reg_traindata.txt
# #jmnybl@epsilon-it:~/git_checkout/parser-vectors.git/reg_testdata.txt
# def load_data(parser_states,type_model,word_model):
#     type_wv=wvlib.load(type_model)
#     word_wv=wvlib.load(word_model,max_rank=800000)
#     _,word_dim=word_wv._vectors.vectors.shape
#     _,type_dim=type_wv._vectors.vectors.shape
#     gs_types=[]
#     lines=[]
#     with codecs.open(parser_states,"r","utf-8") as f_in:
#         for line in f_in:
#             line=line.strip()
#             if not line:
#                 continue
#             lines.append(line)
#     #lines=lines[:100000]
    
#     word_vecs=numpy.zeros((len(lines),word_dim*(len(lines[0].split())-1)),theano.config.floatX)
#     type_vecs=numpy.zeros((len(lines),type_dim),theano.config.floatX)
#     for line_idx,line in enumerate(lines):
#         line=line.strip()
#         words=line.split()
#         #The first one is the type
#         #the rest are the words (can also be NONE)
#         pred_type=words[0]
#         gs_types.append(pred_type)
#         words=words[1:]
#         for w_idx,w in enumerate(words):
#             if w==u"NONE" or w not in word_wv.word_to_vector_mapping():
#                 word_vecs[line_idx,(w_idx*word_dim):(w_idx*word_dim+word_dim)]=numpy.zeros(word_dim,theano.config.floatX)
#             else:
#                 word_vecs[line_idx,(w_idx*word_dim):(w_idx*word_dim+word_dim)]=word_wv.word_to_vector_mapping()[w]
#         type_vecs[line_idx]=type_wv.word_to_vector_mapping()[pred_type]
#     print "Word vecs:",word_vecs.shape
#     print "Type vecs:",type_vecs.shape
#     return theano.shared(word_vecs,borrow=True),theano.shared(type_vecs,borrow=True),type_wv,gs_types

# def load_data_into_figs(parser_states,word_model):
#     word_wv=wvlib.load(word_model,max_rank=800000)
#     _,word_dim=word_wv._vectors.vectors.shape
#     lines=[]
#     with codecs.open(parser_states,"r","utf-8") as f_in:
#         for line in f_in:
#             line=line.strip()
#             if not line:
#                 continue
#             lines.append(line)
#     word_vecs=numpy.zeros((len(lines)*(len(lines[0].split())-1),word_dim),theano.config.floatX)
#     types=[]
#     zero_counters=[]
#     counter=0
#     for line_idx,line in enumerate(lines):
#         line=line.strip()
#         words=line.split()
#         #The first one is the type
#         #the rest are the words (can also be NONE)
#         pred_type=words[0]
#         types.append(pred_type)
#         words=words[1:]
#         for w_idx,w in enumerate(words):
#             if w==u"NONE" or w not in word_wv.word_to_vector_mapping():
#                 zero_counters.append(counter)
#             else:
#                 word_vecs[counter]=word_wv.word_to_vector_mapping()[w]
#             counter+=1
#     word_vecs=((word_vecs-word_vecs.min())/(word_vecs.max()-word_vecs.min())*255).astype(numpy.uint8)
#     for x in zero_counters:
#         word_vecs[x]=numpy.zeros(word_dim,numpy.uint8)
#     L,_=word_vecs.shape
#     L/=len(types) #This many rows per image
#     print "L=",L
#     for idx,t in enumerate(types):
#         if not os.path.exists("my_data/"+t):
#             os.system("mkdir my_data/"+t)
#         fname=os.path.join("my_data",t,"%d.png"%idx)
#         scipy.misc.imsave(fname,word_vecs[idx*L:idx*L+L])
#     print word_vecs.min(),word_vecs.max()
#     print "Word vecs:",word_vecs.shape
    


# def test_mlp(learning_rate=0.0000001, L1_reg=0.00, L2_reg=0.001, n_epochs=1000,
#              dataset='mnist.pkl.gz', batch_size=100, n_hidden=20):
#     """
#     Demonstrate stochastic gradient descent optimization for a multilayer
#     perceptron

#     This is demonstrated on MNIST.

#     :type learning_rate: float
#     :param learning_rate: learning rate used (factor for the stochastic
#     gradient

#     :type L1_reg: float
#     :param L1_reg: L1-norm's weight when added to the cost (see    regularization)

#     :type L2_reg: float
#     :param L2_reg: L2-norm's weight when added to the cost (see
#     regularization)

#     :type n_epochs: int
#     :param n_epochs: maximal number of epochs to run the optimizer

#     :type dataset: string
#     :param dataset: the path of the MNIST dataset file from
#                  http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz


#    """
    
#     #datasets = load_data(dataset)
#     train_set_x, train_set_y, _, _=load_data("/home/jmnybl/git_checkout/parser-vectors.git/reg_traindata.txt","/home/jmnybl/git_checkout/parser-vectors.git/vectors.bin","/usr/share/ParseBank/vector-space-models/FIN/w2v_pbv3_wf.rev01.bin")
#     test_set_x, test_set_y, type_wv, gs_types=load_data("/home/jmnybl/git_checkout/parser-vectors.git/reg_testdata.txt","/home/jmnybl/git_checkout/parser-vectors.git/vectors.bin","/usr/share/ParseBank/vector-space-models/FIN/w2v_pbv3_wf.rev01.bin")

#     # compute number of minibatches for training, validation and testing
#     n_train_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size
#     n_test_batches = test_set_x.get_value(borrow=True).shape[0] / batch_size

#     ######################
#     # BUILD ACTUAL MODEL #
#     ######################
#     print '... building the model'

#     # allocate symbolic variables for the data
#     index = T.lscalar()  # index to a [mini]batch
#     x = T.matrix('x',theano.config.floatX)  # the data is presented as rasterized images
#     y = T.matrix('y',theano.config.floatX)  # the labels are presented as 10D vector of
#                         # [int] labels

#     rng = numpy.random.RandomState(1234)

#     # construct the MLP class
#     classifier = MLP(
#         rng=rng,
#         input=x,
#         n_in=train_set_x.get_value(borrow=True).shape[1],
#         n_hidden=n_hidden,
#         n_out=train_set_y.get_value(borrow=True).shape[1]
#     )
#     # classifier = LR(
#     #     rng=rng,
#     #     input=x,
#     #     n_in=train_set_x.get_value(borrow=True).shape[1],
#     #     n_out=train_set_y.get_value(borrow=True).shape[1],
#     # )

#     # start-snippet-4
#     # the cost we minimize during training is the negative log likelihood of
#     # the model plus the regularization terms (L1 and L2); cost is expressed
#     # here symbolically
#     cost = (
#         classifier.cost(y)
#         + L1_reg * classifier.L1
#         + L2_reg * classifier.L2_sqr
#     )
#     # end-snippet-4

#     # compiling a Theano function that computes the mistakes that are made
#     # by the model on a minibatch
#     test_model = theano.function(
#         inputs=[index],
#         outputs=classifier.cost(y),
#         givens={
#             x: test_set_x[index * batch_size:(index + 1) * batch_size],
#             y: test_set_y[index * batch_size:(index + 1) * batch_size]
#         }
#     )

#     validate_model = theano.function(
#         inputs=[index],
#         outputs=classifier.cost(y),
#         givens={
#             x: test_set_x[index * batch_size:(index + 1) * batch_size],
#             y: test_set_y[index * batch_size:(index + 1) * batch_size]
#         }
#     )
    
#     # start-snippet-5
#     # compute the gradient of cost with respect to theta (sotred in params)
#     # the resulting gradients will be stored in a list gparams
#     gparams = [T.grad(cost, param) for param in classifier.params]

#     # specify how to update the parameters of the model as a list of
#     # (variable, update expression) pairs

#     # given two list the zip A = [a1, a2, a3, a4] and B = [b1, b2, b3, b4] of
#     # same length, zip generates a list C of same size, where each element
#     # is a pair formed from the two lists :
#     #    C = [(a1, b1), (a2, b2), (a3, b3), (a4, b4)]
#     updates = [
#         (param, param - learning_rate * gparam)
#         for param, gparam in zip(classifier.params, gparams)
#     ]

#     # compiling a Theano function `train_model` that returns the cost, but
#     # in the same time updates the parameter of the model based on the rules
#     # defined in `updates`
#     train_model = theano.function(
#         inputs=[index],
#         outputs=cost,
#         updates=updates,
#         givens={
#             x: train_set_x[index * batch_size: (index + 1) * batch_size],
#             y: train_set_y[index * batch_size: (index + 1) * batch_size]
#         }
#     )
#     # end-snippet-5

#     ###############
#     # TRAIN MODEL #
#     ###############
#     print '... training'

#     counter=1
#     while True:
#         for minibatch_index in xrange(n_train_batches):
#             minibatch_avg_cost = train_model(minibatch_index)
#             #print "avgcost", minibatch_avg_cost
#         validation_losses = [validate_model(i) for i in xrange(n_test_batches)]
#         this_validation_loss = numpy.mean(validation_losses)
#         print counter, "VAL", this_validation_loss
#         counter+=1
#         if counter%10==0:
#             print "      ACC=%.2f%%"%(classifier.eval(test_set_x, type_wv, gs_types)*100)
#         sys.stdout.flush()

#     # early-stopping parameters
#     patience = 50000  # look as this many examples regardless
#     patience_increase = 2  # wait this much longer when a new best is
#                            # found
#     improvement_threshold = 0.5  # a relative improvement of this much is
#                                    # considered significant
#     validation_frequency = min(n_train_batches, patience / 500)
#                                   # go through this many
#                                   # minibatche before checking the network
#                                   # on the validation set; in this case we
#                                   # check every epoch

#     best_validation_loss = numpy.inf
#     best_iter = 0
#     test_score = 0.
#     start_time = time.clock()

#     epoch = 0
#     done_looping = False

#     while (epoch < n_epochs) and (not done_looping):
#         epoch = epoch + 1
#         for minibatch_index in xrange(n_train_batches):

#             minibatch_avg_cost = train_model(minibatch_index)
#             # iteration number
#             iter = (epoch - 1) * n_train_batches + minibatch_index

#             if (iter + 1) % validation_frequency == 0:
#                 # compute zero-one loss on validation set
#                 validation_losses = [validate_model(i) for i
#                                      in xrange(n_test_batches)]
#                 this_validation_loss = numpy.mean(validation_losses)

#                 print(
#                     'epoch %i, minibatch %i/%i, validation error %f' %
#                     (
#                         epoch,
#                         minibatch_index + 1,
#                         n_train_batches,
#                         this_validation_loss
#                     )
#                 )

#                 # # if we got the best validation score until now
#                 # if this_validation_loss < best_validation_loss:
#                 #     #improve patience if loss improvement is good enough
#                 #     if (
#                 #         this_validation_loss < best_validation_loss *
#                 #         improvement_threshold
#                 #     ):
#                 #         patience = max(patience, iter * patience_increase)

#                 #     best_validation_loss = this_validation_loss
#                 #     best_iter = iter

#                 #     # test it on the test set
#                 #     test_losses = [test_model(i) for i
#                 #                    in xrange(n_test_batches)]
#                 #     test_score = numpy.mean(test_losses)

#                 #     print(('     epoch %i, minibatch %i/%i, test error of '
#                 #            'best model %f %%') %
#                 #           (epoch, minibatch_index + 1, n_train_batches,
#                 #            test_score * 100.))

#             if patience <= iter:
#                 done_looping = True
#                 break

#     end_time = time.clock()
#     print(('Optimization complete. Best validation score of %f %% '
#            'obtained at iteration %i, with test performance %f %%') %
#           (best_validation_loss * 100., best_iter + 1, test_score * 100.))
#     print >> sys.stderr, ('The code for file ' +
#                           os.path.split(__file__)[1] +
#                           ' ran for %.2fm' % ((end_time - start_time) / 60.))


# if __name__ == '__main__':
#     load_data_into_figs("/home/jmnybl/git_checkout/parser-vectors.git/reg_traindata.txt","/usr/share/ParseBank/vector-space-models/FIN/w2v_pbv3_wf.rev01.bin")
#     #load_data("/home/jmnybl/git_checkout/parser-vectors.git/reg_traindata.txt","/home/jmnybl/git_checkout/parser-vectors.git/vectors.dtype.tdtjk.bin","/usr/share/ParseBank/vector-space-models/FIN/w2v_pbv3_wf.rev01.bin")
#     #test_mlp()
