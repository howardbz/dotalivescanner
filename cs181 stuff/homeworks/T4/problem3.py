# CS 181, Spring 2019
# Homework 4: Clustering and EM
# Name:
# Email:

import numpy as np
import matplotlib.pyplot as plt

# This line loads the images for you. Don't change it!
pics = np.load("images.npy")

# Your code here. You may change anything below this line.
class PCA(object):
    # d is the number of principal components
    def __init__(self, d):
        self.d = d
        #self.resultarray = np.zeros((6000, 28, 28))
        self.val_array = np.zeros(6000)
        self.reshaped = np.zeros((6000, 784))
        self.vec_array = np.zeros((6000, 6000))
        #self.feature_space = np.zeros((6000, ))
        self.tracearray = np.zeros(500)

    def svd(self, X):
        u, s, vh = np.linalg.svd(X) 
        return u, s, vh

    def pca(self, X):
        index = X.T
        cov = np.cov(index)
        self.val_array, self.vec_array = np.linalg.eig(cov)
        print('val', self.val_array.shape)
        print('vec', self.vec_array.shape)
        print('values', self.val_array)

        partial_trace = 0
        diagonal = -np.sort(-np.array([cov[i, i] for i in range(784)]))
        trace = np.sum(diagonal)
        for k in range(500):
            partial_trace = partial_trace + diagonal[k]
            self.tracearray[k] = partial_trace/trace
        print('trace', self.tracearray)

        plt.figure(1)
        plt.plot(list(range(len(self.tracearray))), self.tracearray, '-')
        plt.xlabel("k")
        plt.ylabel("% var explained")
        plt.show()

        #self.resultarray = np.real(np.dot(index.T, self.vec_array))
        return

    # X is a (N x 28 x 28) array where 28x28 is the dimensions of each of the N images. This method should apply PCA to a dataset X.
    def apply(self, X):
        self.reshaped = X.reshape(6000, 784)
        self.pca(self.reshaped)
        #print('resultarray', self.resultarray)
        #print('result shape', self.resultarray.shape)

        plt.plot(list(range(len(self.val_array))), self.val_array, '-')
        plt.xlabel("ith value")
        plt.ylabel("value")
        plt.show()

        #mean image
        plt.imshow(np.mean(X, axis=0), cmap='Greys_r')
        plt.show()

        #first 10 components
        
        #sself.reconstruct = np.zeros()
        for i in range(10):
            weighted_array = np.array([img * np.dot(img, self.vec_array[i]) for img in self.reshaped])
            print(weighted_array.shape)
            img1 = np.mean(np.real(weighted_array), axis=0)
            print(img1)
            #mean image first comp
            plt.imshow(img1.reshape(28,28), cmap='Greys_r')
            plt.show()




PCAfunc = PCA(d=500)
PCAfunc.apply(pics)

# plt.figure(1)
# plt.plot(list(range(len(self.val_array))), self.val_array, '-')
# plt.xlabel("ith value")
# plt.ylabel("value")

# Example of how to plot an image. We ask that images in your writeup be grayscale images, just as in this example.
# plt.figure()
# plt.imshow(pics[0].reshape(28,28), cmap='Greys_r')
# plt.show()
