from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****


    for i in range(X.shape[0]):
        scores = X[i].dot(W)
        scores -= np.max(scores) #numeric instability
        scores_normalised = np.exp(scores)/np.sum(np.exp(scores))
        loss+= (-1)*np.log(scores_normalised[y[i]])

        for j in range(W.shape[1]):
            dW[:,j] += X[i]*scores_normalised[j]
        dW[:,y[i]]-=X[i]

    dW/=X.shape[0]
    dW += 2*W*reg

    loss/= X.shape[0]
    loss += reg * np.sum(W * W)


    #Checks
    # print(scores.shape)
    # print(scores_normalised.shape)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    scores = X.dot(W)
    max_scores = np.max(scores,axis=1).reshape(-1,1)
    scores -= max_scores
    scores_normalised = np.exp(scores)/np.sum(np.exp(scores),axis=1,keepdims=True)
    loss =  np.sum((-1)*np.log(scores_normalised[range(X.shape[0]),y]))

    #Checks
    # print(scores.shape)
    # print(scores_normalised.shape)


    #Using an indicator matrix
    # y_ind = np.zeros_like(scores) # Indicator matrix : N x class
    # y_ind[range(X.shape[0]),y]=1
    # dW += X.T.dot(scores_normalised)
    # dW -= X.T.dot(y_ind)

    #Without indicator_matrix (Optimised)
    scores_normalised[range(X.shape[0]),y] -= 1
    dW += X.T.dot(scores_normalised)

    #Checks


    dW/=X.shape[0]
    dW += 2*W*reg

    loss/= X.shape[0]
    loss += reg * np.sum(W * W)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
