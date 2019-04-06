# CS 181, Spring 2019
# Homework 3: Max-Margin, Ethics, Clustering
# Name: Miles Wang
# Email: mileswang@college.harvard.edu

import numpy as np 
import matplotlib.pyplot as plt
import random

# This line loads the images for you. Don't change it! 
pics = np.load("images.npy", allow_pickle=False)

# You are welcome to change anything below this line. This is just an example of how your code may look.
# Keep in mind you may add more public methods for things like the visualization.
# Also, you must cluster all of the images in the provided dataset, so your code should be fast enough to do that.

# Use L2 norm
# Step 1: Start at random initialization, some choice of K, plot the K means objective function as a 
# function of 

class KMeans(object):
    # K is the K in KMeans
    def __init__(self, K):
        self.K = K
        self.centroid_list = np.zeros((self.K, 28, 28))

    def random_start(self, data):
        randomlist = random.sample(range(data.shape[0]), self.K)
        #self.centroid_list = list(random.sample(list(mod_data), self.K))
        self.class_list = np.zeros(data.shape[0])
        for i in range(len(randomlist)):
            self.centroid_list[i] = data[randomlist[i]]
            self.class_list[randomlist[i]] = i 
        #print('randomlist', randomlist)
        #print("random start")
        return

    def iteration_start(self, centroids, data):
        self.class_list = np.zeros(data.shape[0])
        self.centroid_list = centroids
        self.sort(data)
        #print("iteration start")
        return 

    def norm_diff_array(self, point):
        temp_array = []
        for index in self.centroid_list:
            temp_array.append(np.linalg.norm(np.subtract(index, point)))
        return np.array(temp_array)

    def sort(self, data):
        self.class_list = np.zeros(data.shape[0])
        for i in range(data.shape[0]): 
            varmin = np.argmin(self.norm_diff_array(data[i]))
            self.class_list[i] = varmin
        #print("sort")
        return 

    def loss(self, data):
        iter_sum = 0
        for index in range(len(self.class_list)):
                iter_sum = iter_sum + np.amin(self.norm_diff_array(data[index]))
        #print("loss")
        return iter_sum

    # X is a (N x 28 x 28) array where 28x28 is the dimensions of each of the N images.
    def fit(self, X):
        losslist = []

        #standardize the data
        for index in range(X.shape[0]): 
            X[index] = (X[index] - np.mean(X[index])) / np.std(X[index])

        self.random_start(X)
        self.sort(X)
        self.oldloss = self.loss(X)
        losslist.append(self.oldloss)
        #print("fit")
        self.losscheck = False
        #counter = 0 
        while self.losscheck != True:
            meanimages = self.get_mean_images(X, False)
            self.iteration_start(meanimages, X)
            self.newloss = self.loss(X)
            #print('losslist', losslist)
            #print('oldloss', self.oldloss)
            print('newloss', self.newloss)
            losslist.append(self.newloss)
            #counter = counter + 1

            if (self.oldloss - self.newloss) < 50:
                self.losscheck = True
                #print('losslist', losslist)
                self.get_mean_images(X, True)
            else:
                self.oldloss = self.newloss
        return losslist, self.newloss

    # This should return the arrays for K images. Each image should represent the mean of each of the fitted clusters.
    def get_mean_images(self, data, boolcheck):
        meanarray = np.zeros((self.K, 28, 28))
        
        for k in range(self.K):
            counter = 0
            innersum = np.zeros((28, 28))
            for i in range(data.shape[0]):
                if self.class_list[i] == k:
                    innersum = np.add(data[i], innersum)
                    counter = counter + 1
            avg = np.divide(innersum, counter)
            meanarray[k] = avg
        #print("get mean images")

        if boolcheck == True:
            for i in range(self.K):
                plt.figure()
                plt.imshow(meanarray[i], cmap='Greys_r')
                #plt.show()
                plt.savefig('run4std_' + str(i) + '.png')

        return meanarray


KMeansClassifier = KMeans(K=10)
KMeansClassifier.fit(pics)

    
#meanlist = [np.mean(list3),np.mean(list7),np.mean(list10),np.mean(list15),np.mean(list25),np.mean(list50)]
#stdlist = [np.std(list3),np.std(list7),np.std(list10),np.std(list15),np.std(list25),np.std(list50)]

#print('stdlist', stdlist)

#loss_list = KMeansClassifier.fit(pics)[0]

# This is how to plot an image. We ask that any images in your writeup be grayscale images, just as in this example.

#plt.figure(1)
#plt.plot(list(range(len(loss_list))), loss_list, '-')
#plt.xlabel("Iterations")
#plt.ylabel("K means Objective Function")

# fig, ax = plt.subplots()
# ax.bar(np.arange(6), meanlist, yerr=stdlist, align='center', alpha=0.5, ecolor='black', capsize=10)
# ax.set_ylabel('final losses for K classes')
# ax.set_xticks(np.arange(6))
# ax.set_xticklabels(K)
# ax.set_title('Loss Mean and STD based on K value')
# ax.yaxis.grid(True)

# # Save the figure and show
# plt.tight_layout()

# plt.show()


