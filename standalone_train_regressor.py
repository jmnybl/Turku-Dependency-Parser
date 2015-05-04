import cPickle as pickle
from wvlib import wvlib
import codecs
import os
import sys
import time

import numpy

import theano
import theano.tensor as T


import random

import regressor_mlp

def load_data(parser_states,models,classes):
    "models is a dict W->w2v, P->w2v. etc"
    dims={}
    for t,mod_name in models.iteritems():
        if mod_name is None:
            dims[t]=None
            continue
        if isinstance(mod_name,basestring):
            models[t]=wvlib.load(mod_name,max_rank=800)
        dims[t]=models[t]._vectors.vectors.shape[1]
    gs_types=[]
    lines=[]
    with codecs.open(parser_states,"r","utf-8") as f_in:
        for line in f_in:
            line=line.strip()
            if not line:
                continue
            lines.append(line)
    lines=lines[:100]
    random.shuffle(lines)
    #How much of space do we need?
    cols=0
    for w in lines[0].split()[1:]:
        t,_=w.split(":",1)
        if dims[t] is not None:
            cols+=dims[t]
    word_vecs=numpy.zeros((len(lines),cols),theano.config.floatX)
    class_matrix=numpy.zeros((len(lines),),numpy.int32)
    for line_idx,line in enumerate(lines):
        line=line.strip()
        words=line.split()
        #The first one is the type
        #the rest are type:word (can also be type:NONE)
        pred_type=words[0]
        cls_index=classes.setdefault(pred_type,len(classes))
        class_matrix[line_idx]=cls_index
        gs_types.append(pred_type)
        words=words[1:]
        dim=0
        for w in words:
            t,w=w.split(":",1)
            t_dims=dims[t]
            if t_dims==None:
                continue
            if w!=u"NONE":
                vec=models[t].word_to_vector_mapping().get(w,None)
                if vec is None:
                    vec=models[t].word_to_vector_mapping().get(w.lower(),None)
            if w==u"NONE" or vec is None:
                word_vecs[line_idx,dim:(dim+t_dims)]=numpy.zeros(t_dims,theano.config.floatX)
            else:
                word_vecs[line_idx,dim:(dim+t_dims)]=vec
            dim+=t_dims
    print word_vecs
    print class_matrix
    print "Word vecs:",word_vecs.shape
    print "Class matrix:",class_matrix.shape
    return word_vecs,class_matrix



def shared_dataset(data_xy, borrow=True):
    """ Function that loads the dataset into shared variables

    The reason we store our dataset in shared variables is to allow
    Theano to copy it into the GPU memory (when code is run on GPU).
    Since copying data into the GPU is slow, copying a minibatch everytime
    is needed (the default behaviour if the data is not in a shared
    variable) would lead to a large decrease in performance.
    """
    data_x, data_y = data_xy
    shared_x = theano.shared(numpy.asarray(data_x,
                                           dtype=theano.config.floatX),
                             borrow=borrow)
    shared_y = theano.shared(numpy.asarray(data_y,
                                           dtype=theano.config.floatX),
                             borrow=borrow)
    # When storing data on the GPU it has to be stored as floats
    # therefore we will store the labels as ``floatX`` as well
    # (``shared_y`` does exactly that). But during our computations
    # we need them as ints (we use labels as index, and if they are
    # floats it doesn't make sense) therefore instead of returning
    # ``shared_y`` we will have to cast it to int. This little hack
    # lets ous get around this issue
    return shared_x, T.cast(shared_y, 'int32')


def test_mlp(learning_rate=0.01, L1_reg=0.00, L2_reg=0.000001, n_epochs=1000,
             batch_size=20, n_hidden=200):
    """
    Demonstrate stochastic gradient descent optimization for a multilayer
    perceptron

    This is demonstrated on MNIST.

    :type learning_rate: float
    :param learning_rate: learning rate used (factor for the stochastic
    gradient

    :type L1_reg: float
    :param L1_reg: L1-norm's weight when added to the cost (see
    regularization)

    :type L2_reg: float
    :param L2_reg: L2-norm's weight when added to the cost (see
    regularization)

    :type n_epochs: int
    :param n_epochs: maximal number of epochs to run the optimizer

    :type dataset: string
    :param dataset: the path of the MNIST dataset file from
                 http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz


   """

    classes={}
    models={"W":"/home/ginter/w2v-old/w2v_fin_50_wf.bin",
            "POS":"/home/ginter/parser-vectors/pos_ud.vectors.bin",
            #"FEAT":"/home/ginter/parser-vectors/feat_ud.vectors.bin",
            "FEAT":None,
            "POS_FEAT":"/home/ginter/parser-vectors/pos_feat_ud.vectors.bin",
            #"POS_FEAT":None,
            }

    train_set_x, train_set_y=load_data("/home/ginter/parser-vectors/reg_traindata_ud.txt",models,classes)
    test_set_x, test_set_y=load_data("/home/ginter/parser-vectors/reg_devdata_ud.txt",models,classes)
    valid_set_x, valid_set_y=load_data("/home/ginter/parser-vectors/reg_devdata_ud.txt",models,classes)
        
    train_set_x,train_set_y=shared_dataset((train_set_x,train_set_y))
    test_set_x,test_set_y=shared_dataset((test_set_x,test_set_y))
    valid_set_x,valid_set_y=shared_dataset((valid_set_x,valid_set_y))

    # compute number of minibatches for training, validation and testing
    n_train_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0] / batch_size
    n_test_batches = test_set_x.get_value(borrow=True).shape[0] / batch_size

    # ######################
    # # BUILD ACTUAL MODEL #
    # ######################
    # print '... building the model'

    # # allocate symbolic variables for the data
    # index = T.lscalar()  # index to a [mini]batch
    x = T.matrix('x')  # the data is presented as rasterized images
    y = T.ivector('y')  # the labels are presented as 1D vector of
    rng = numpy.random.RandomState(1234)

    # # construct the MLP class
    
    classifier = regressor_mlp.MLP(
         rng=rng,
         input=x,
         n_in=train_set_x.get_value(borrow=True).shape[1],
         n_hidden=n_hidden,
         n_out=len(classes)
    )

    # # start-snippet-4
    # # the cost we minimize during training is the negative log likelihood of
    # # the model plus the regularization terms (L1 and L2); cost is expressed
    # # here symbolically
    # cost = (
    #     classifier.negative_log_likelihood(y)
    #     + L1_reg * classifier.L1
    #     + L2_reg * classifier.L2_sqr
    # )
    # # end-snippet-4

    # # compiling a Theano function that computes the mistakes that are made
    # # by the model on a minibatch
    # test_model = theano.function(
    #     inputs=[index],
    #     outputs=classifier.errors(y),
    #     givens={
    #         x: test_set_x[index * batch_size:(index + 1) * batch_size],
    #         y: test_set_y[index * batch_size:(index + 1) * batch_size]
    #     }
    # )

    # validate_model = theano.function(
    #     inputs=[index],
    #     outputs=classifier.errors(y),
    #     givens={
    #         x: valid_set_x[index * batch_size:(index + 1) * batch_size],
    #         y: valid_set_y[index * batch_size:(index + 1) * batch_size]
    #     }
    # )

    # # start-snippet-5
    # # compute the gradient of cost with respect to theta (sotred in params)
    # # the resulting gradients will be stored in a list gparams
    # gparams = [T.grad(cost, param) for param in classifier.params]

    # # specify how to update the parameters of the model as a list of
    # # (variable, update expression) pairs

    # # given two list the zip A = [a1, a2, a3, a4] and B = [b1, b2, b3, b4] of
    # # same length, zip generates a list C of same size, where each element
    # # is a pair formed from the two lists :
    # #    C = [(a1, b1), (a2, b2), (a3, b3), (a4, b4)]
    # updates = [
    #     (param, param - learning_rate * gparam)
    #     for param, gparam in zip(classifier.params, gparams)
    # ]

    # # compiling a Theano function `train_model` that returns the cost, but
    # # in the same time updates the parameter of the model based on the rules
    # # defined in `updates`
    # train_model = theano.function(
    #     inputs=[index],
    #     outputs=cost,
    #     updates=updates,
    #     givens={
    #         x: train_set_x[index * batch_size: (index + 1) * batch_size],
    #         y: train_set_y[index * batch_size: (index + 1) * batch_size]
    #     }
    # )
    # # end-snippet-5

    # ###############
    # # TRAIN MODEL #
    # ###############
    # print '... training'

    # # early-stopping parameters
    # patience = 1000000  # look as this many examples regardless
    # patience_increase = 2  # wait this much longer when a new best is
    #                        # found
    # improvement_threshold = 0.995  # a relative improvement of this much is
    #                                # considered significant
    # validation_frequency = min(n_train_batches, patience / 2)
    #                               # go through this many
    #                               # minibatche before checking the network
    #                               # on the validation set; in this case we
    #                               # check every epoch

    # best_validation_loss = numpy.inf
    # best_iter = 0
    # test_score = 0.
    # start_time = time.clock()

    # epoch = 0
    # done_looping = False

    # while (epoch < n_epochs) and (not done_looping):
    #     sys.stdout.flush()
    #     epoch = epoch + 1
    #     for minibatch_index in xrange(n_train_batches):

    #         minibatch_avg_cost = train_model(minibatch_index)
    #         # iteration number
    #         iter = (epoch - 1) * n_train_batches + minibatch_index

    #         if (iter + 1) % validation_frequency == 0:
    #             # compute zero-one loss on validation set
    #             validation_losses = [validate_model(i) for i
    #                                  in xrange(n_valid_batches)]
    #             this_validation_loss = numpy.mean(validation_losses)

    #             print(
    #                 'epoch %i, minibatch %i/%i, validation error %f %%' %
    #                 (
    #                     epoch,
    #                     minibatch_index + 1,
    #                     n_train_batches,
    #                     this_validation_loss * 100.
    #                 )
    #             )

    #             # if we got the best validation score until now
    #             if this_validation_loss < best_validation_loss:
    #                 #improve patience if loss improvement is good enough
    #                 if (
    #                     this_validation_loss < best_validation_loss *
    #                     improvement_threshold
    #                 ):
    #                     patience = max(patience, iter * patience_increase)

    #                 best_validation_loss = this_validation_loss
    #                 best_iter = iter

    #                 # test it on the test set
    #                 test_losses = [test_model(i) for i
    #                                in xrange(n_test_batches)]
    #                 test_score = numpy.mean(test_losses)

    #                 print(('     epoch %i, minibatch %i/%i, test error of '
    #                        'best model %f %%') %
    #                       (epoch, minibatch_index + 1, n_train_batches,
    #                        test_score * 100.))

    #         if patience <= iter:
    #             done_looping = True
    #             break

    # end_time = time.clock()
    # print(('Optimization complete. Best validation score of %f %% '
    #        'obtained at iteration %i, with test performance %f %%') %
    #       (best_validation_loss * 100., best_iter + 1, test_score * 100.))
    # print >> sys.stderr, ('The code for file ' +
    #                       os.path.split(__file__)[1] +
    #                       ' ran for %.2fm' % ((end_time - start_time) / 60.))


if __name__ == '__main__':
    test_mlp()
