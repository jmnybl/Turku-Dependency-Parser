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

def load_data(parser_states,models,classes,max_rank=600000,max_rows=-1):
    "models is a dict W->w2v, P->w2v. etc"
    dims={}
    for t,mod_name in models.iteritems():
        if mod_name is None:
            dims[t]=None
            continue
        if isinstance(mod_name,basestring):
            models[t]=wvlib.load(mod_name,max_rank=max_rank)
            models[t]._vectors.vectors=models[t]._vectors.vectors.astype(theano.config.floatX)
        dims[t]=models[t]._vectors.vectors[0].shape[0]
    gs_types=[]
    lines=[]
    with codecs.open(parser_states,"r","utf-8") as f_in:
        for line in f_in:
            line=line.strip()
            if not line:
                continue
            lines.append(line)
            if max_rows>0 and len(lines)>=max_rows:
                break
    #lines=lines[:5000]
    random.shuffle(lines)
    #How many indices per row, and how many inputs does that translate into?
    indices=0
    cols=0
    for w in lines[0].split()[1:]:
        t,_=w.split(":",1)
        if dims[t] is not None:
            cols+=dims[t]
            indices+=1
    word_indices=numpy.zeros((len(lines),indices),numpy.int32)
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
        idx=0
        for w in words:
            t,w=w.split(":",1)
            if dims[t]==None:
                #off
                continue
            #wv_row will be the row index in the vector embedding matrix
            if w!=u"NONE":
                try:
                    wv_row=models[t].rank(w)
                except KeyError:
                    wv_row=0
            else:
                wv_row=0
            word_indices[line_idx,idx]=wv_row
            idx+=1    
    #Yet gather a list of models so we know what these indices refer to
    model_list=[]
    for w in lines[0].split()[1:]:
        t,_=w.split(":",1)
        if dims[t] is not None:
            model_list.append(t)
    assert len(model_list)==word_indices.shape[1]
 
    # print "Word indices:", word_indices
    # print "Class matrix:", class_matrix
    print "Indices shape:",word_indices.shape
    print "Class matrix shape:",class_matrix.shape
    return model_list,word_indices,class_matrix

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
                                           dtype='int32'),
                             borrow=borrow)
    shared_y = theano.shared(numpy.asarray(data_y,
                                           dtype='int32'),
                             borrow=borrow)
    # When storing data on the GPU it has to be stored as floats
    # therefore we will store the labels as ``floatX`` as well
    # (``shared_y`` does exactly that). But during our computations
    # we need them as ints (we use labels as index, and if they are
    # floats it doesn't make sense) therefore instead of returning
    # ``shared_y`` we will have to cast it to int. This little hack
    # lets ous get around this issue
    return shared_x, shared_y#T.cast(shared_y, 'int32')


def test_mlp(learning_rate=0.02, L1_reg=0.00, L2_reg=0.000000001, n_epochs=1000,
             batch_size=13, n_hidden=197):
    """
    Demonstrate stochastic gradient descent optimization for a multilayer
    perceptron

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

   """

    classes={}
    models={#"W":"data/w2v_fin_50_wf.bin",
            "W":"/home/ginter/w2v/pb34_wf_200_v2.bin",
            "POS":"/home/ginter/parser-vectors/pos_ud.vectors.bin",
            #"POS":None,
            #"FEAT":"/home/ginter/parser-vectors/feat_ud.vectors.bin",
            "FEAT":None,
            "POS_FEAT":"/home/ginter/parser-vectors/pos_feat_ud.vectors.bin",
            #"POS_FEAT":None,
            }

    max_rank=1200000
    max_rows=1000000
    model_list, train_set_x, train_set_y=load_data("/home/ginter/parser-vectors/reg_traindata_ud.txt",models,classes,max_rank=max_rank,max_rows=max_rows)
    model_list2, test_set_x, test_set_y=load_data("/home/ginter/parser-vectors/reg_devdata_ud.txt",models,classes,max_rank=max_rank,max_rows=max_rows)
    model_list3, valid_set_x, valid_set_y=load_data("/home/ginter/parser-vectors/reg_devdata_ud.txt",models,classes,max_rank=max_rank,max_rows=max_rows)
    assert model_list==model_list2 and model_list2==model_list3
    
    #TODO: get rid of this hack!
    models["W"]._vectors.vectors[0,:]=[0.0]*models["W"]._vectors.vectors.shape[1]
    

    # # allocate symbolic variables for the data
    x = T.imatrix('x')  # 
    y = T.ivector('y')  # the labels are presented as 1D vector of integers
    
    # wv_layer=regressor_mlp.VSpaceLayerCatenation.from_wvlibs(model_list,x)
    # classifier_mlp = regressor_mlp.MLP.empty(n_in,n_hidden,len(classes),classes,wv_layer.output)
    classifier=regressor_mlp.MLP_WV.empty(n_hidden,classes,models,model_list)

    print >> sys.stderr, "Dimensionality of hidden layer input:", classifier.wv_layer.n_out()

    train_set_x,train_set_y=shared_dataset((train_set_x,train_set_y))
    test_set_x,test_set_y=shared_dataset((test_set_x,test_set_y))
    valid_set_x,valid_set_y=shared_dataset((valid_set_x,valid_set_y))

    # compute number of minibatches for training, validation and testing
    n_train_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0] / batch_size
    n_test_batches = test_set_x.get_value(borrow=True).shape[0] / batch_size


    # classifier.load("cls")
    # classifier.compile_train_classification()
    # classifier.compile_test()

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
    print '... training'

    # # early-stopping parameters
    patience = 1000000  # look as this many examples regardless
    patience_increase = 2  # wait this much longer when a new best is
    #                        # found
    improvement_threshold = 0.995  # a relative improvement of this much is
    #                                # considered significant
    validation_frequency = min(n_train_batches, patience / 2)
    #                               # go through this many
    #                               # minibatche before checking the network
    #                               # on the validation set; in this case we
    #                               # check every epoch

    best_validation_loss = numpy.inf
    best_iter = 0
    test_score = 0.
    start_time = time.clock()
    time.ctime()
    epoch = 0
    done_looping = False

    while (epoch < n_epochs) and (not done_looping):
        sys.stdout.flush()
        epoch = epoch + 1
        print >> sys.stderr, "Epoch", epoch, "started", time.ctime()
        for minibatch_index in xrange(n_train_batches):
            i=batch_size*minibatch_index
            xs=train_set_x.get_value(borrow=True)[i:i+batch_size]
            ys=train_set_y.get_value(borrow=True)[i:i+batch_size]
            #print "TSTX", classifier.wv_layer.calcvals(xs)
            minibatch_avg_cost = classifier.train_classification_model(xs,ys,learning_rate,L1_reg,L2_reg)
            #print minibatch_avg_cost
#            print classifier.test_classification_model(xs)
    #         # iteration number
            tst=classifier.test_classification_model(xs)
            iter = (epoch - 1) * n_train_batches + minibatch_index

            if (iter + 1) % validation_frequency == 0:
                predictions=classifier.test_classification_model(valid_set_x.get_value(borrow=True))
                this_validation_loss=((predictions==valid_set_y.get_value(borrow=True)).sum()*100.0)/valid_set_y.get_value(borrow=True).shape[0]
                
                print(
                    'epoch %i, minibatch %i/%i, validation acc %f %%' %
                    (
                         epoch,
                         minibatch_index + 1,
                         n_train_batches,
                         this_validation_loss
                    )
                    )
                time.ctime()
                classifier.save("cls")
                time.ctime()
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
