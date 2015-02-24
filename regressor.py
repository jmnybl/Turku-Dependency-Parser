import theano
import theano.tensor as T
import numpy
from theano.tensor.shared_randomstreams import RandomStreams
from wvlib import wvlib

def _outer_substract(x, y):
    x = x.dimshuffle(0, 1, 'x')
    x = T.addbroadcast(x, 2)
    return (x - y.T).T

def _gaussian_kernel(x, y, beta = 0.1):
    K = _outer_substract(x,y)
    return T.exp( -beta * K.norm(L=2,axis=1))

class N3Layer(object):

    def __init__(self,rng,inp,n_in,n_out):
        W_values = numpy.asarray(rng.uniform(low=-0.1,high=0.1,size=(n_in, n_out)),dtype=theano.config.floatX)
        B_values = numpy.asarray(rng.uniform(low=-0.1,high=0.1,size=(n_out,)),dtype=theano.config.floatX)
        self.W=theano.shared(W_values,name="W") #The weights
        self.b=theano.shared(B_values,name="b") #bias
        self.inp=inp
        self.output=(T.dot(self.inp,self.W)+self.b) #cubic func
        self.outputF=theano.function([self.inp],self.output) #cubic func
        self.L2_sqr=(self.W ** 2).sum()+(self.b **2).sum()

    def cost(self,y):
        return T.sum((self.output-y)**2)+0.0001*self.L2_sqr

class VRegressor(object):

    def __init__(self,n_in,n_out):
        self.n_in=n_in
        self.n_out=n_out
        self.rng=numpy.random.RandomState(seed=1)
        self.x_var=T.vector("x")
        self.y_var=T.vector("y")
        self.lrate_var=T.scalar(dtype=theano.config.floatX)
        self.n3=N3Layer(rng=self.rng,inp=self.x_var,n_in=self.n_in,n_out=self.n_out)
        self.n3cost=self.n3.cost(self.y_var)
        self.GW=T.grad(self.n3cost,self.n3.W)
        self.GB=T.grad(self.n3cost,self.n3.b)
        self.do_train=theano.function(inputs=[self.x_var,self.y_var,self.lrate_var],outputs=self.n3cost,updates=[(self.n3.W,self.n3.W-self.GW*self.lrate_var),(self.n3.b,self.n3.b-self.GB*self.lrate_var)])

    def predict(self,x):
        """x: input"""
        return self.n3.outputF(x)

    def update(self,x,y,lrate=0.01):
        """x: input, y: output"""
        return self.do_train(x,y,lrate)



class regressorWrapper(object):

    def __init__(self,word_model,label_model,regressor_model):
        # load word vectors
        self.word_vectors=wvlib.load(word_model, max_rank=10000).normalize()
        self.word_mapping=self.word_vectors.word_to_vector_mapping()
        # load label vectors (e.g. dependency type vectors)
        self.label_vectors=wvlib.load(label_model).normalize()
        self.label_mapping=self.label_vectors.word_to_vector_mapping()
        # regressor model
        self.regressor=regressor_model # TODO load the trained model

    def tokens2vectors(self,tokens):
        vectors=[]
        for token in tokens:
            try:
                vectors.append(self.word_mapping[token])
            except:
                vectors.append(numpy.zeros(self.word_vectors.config.vector_dim))
        return vectors

    def regress_and_update(self,tokens,label): # TODO: learning rate
        assert len(tokens)==2
        vectors=self.tokens2vectors(tokens)
        label_vector=self.label_mapping[label]
        error=self.regressor.update(numpy.concatenate(tuple(vectors)),label_vector) # TODO: this should return the predicted vector...



    def regress_vector(self,tokens):
        assert len(tokens)==2
        vectors=self.tokens2vectors(tokens)
        predicted=self.regressor.predict(numpy.concatenate(tuple(vectors))) # predicted vector
        label,sim=self.label_vectors.nearest(predicted.astype(numpy.float32))[0] # turn the vector into label
        return label # TODO return the predicted vector...
        

if __name__=="__main__":

    DI=600
    DO=10

    rng=numpy.random.RandomState(seed=2)
    vr=VRegressor(DI,DO)
    transform=numpy.asarray(rng.uniform(low=-1.5,high=1.5,size=(DI,DO)),dtype=theano.config.floatX)
    b=numpy.asarray(rng.uniform(low=-0.5,high=0.5,size=(DO,)),dtype=theano.config.floatX)
    # n3cost=n3.cost(y_var)
    # GW=T.grad(n3cost,n3.W)
    # GB=T.grad(n3cost,n3.b)
    # train=
    x_var=T.vector("x")
    data=theano.function([x_var],T.dot(x_var,transform)+b)
    for e in range(20000):
        x=numpy.asarray(rng.uniform(low=-1.5,high=1.5,size=(DI,)),dtype=theano.config.floatX)
        y=data(x)
        print vr.update(x,y)

    print vr.n3.W.get_value()-transform
    #     train(x,y)
    #     c2=n3cost.eval({x_var:x,y_var:y})
    #     print c2
    # print transform
    # print n3.W.get_value()
