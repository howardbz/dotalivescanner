import numpy as np

# code up dataset

x1 = np.array([0, 0, 0, .5, .5, .5, 1, 1, 1])
x2 = np.array([0, .5, 1, 0, .5, 1, 0, .5, 1])
y = np.array([0, 0, 0, .5, .5, .5, 1, 1, 1])

data_x = np.vstack((x1, x2)).T
data_y = y.T

# code up kernels
alpha = 10

W1 = alpha * np.array([[1, 0], [0, 1]])
W2 = alpha * np.array([[.1, 0], [0, 1]])
W3 = alpha * np.array([[1, 0], [0, .1]])

# functions

def kernel(x, xprime, W): 
	#return np.exp(-np.dot((x-xprime), np.dot(W, (x-xprime).T)))
	return np.exp(-np.dot(np.dot((x-xprime), W), (x-xprime).T))

def yhat(pos, W):
	top_sum = 0.
	bot_sum = 0.
	
	# predicted yhat for xprime = index2 
	for index2 in range(len(y)):
		value = kernel(data_x[index2], data_x[pos], W)
		top_sum = top_sum + (value * data_y[index2])
		bot_sum = bot_sum + value
	return top_sum/bot_sum

def loss(W):
	loss_sum = 0.
	for index1 in range(len(y)):
		individual_loss = data_y[index1] - yhat(index1, W)
		loss_sum = loss_sum + (individual_loss)**2
	return loss_sum/2

print("W1", loss(W1))
print("W2", loss(W2))
print("W3", loss(W3))
