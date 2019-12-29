import numpy as np
import matplotlib.pyplot as plt
def hypothesis(X, theta):
	return 1/(1+np.exp(-(X@theta)))

def cost_function(theta, X, y):
	m = len(y)
	cost = -np.multiply(y.T, np.log(hypothesis(X,theta))) - np.multiply((1 - y).T,np.log(1-hypothesis(X,theta)))
	cost = cost.sum()/m
	return cost

def gradient(theta, X, y):
	m = len(y)
	derivatives = np.multiply(X.T,np.subtract(hypothesis(X,theta),y.T).T)
	derivatives = derivatives.sum(axis=1)/(m)
	return derivatives
	
def gradient_Reg(theta, X, y, lamb):
	m = len(y)
	derivatives = gradient(theta, X, y)
	derivatives[1:] = theta[1:]*lamb/m
	return derivatives

def cost_function_Reg(theta, X, y, lamb):
	m = len(y)
	cost = -np.multiply(y.T,np.log(hypothesis(X,theta))) - np.multiply((1 - y).T,np.log(1-hypothesis(X,theta)))
	cost[1:] += np.square(theta[1:]).sum()*lamb/(2*m)
	cost = cost.sum()/m
	return cost

def mapFeature(X1, X2):
	X1.shape = (X1.size, 1)
	X2.shape = (X2.size, 1)
	degree = 6
	m, _ = X1.shape
	out = np.ones((m, 1))
	for i in range(1, degree+1):
		for j in range(0,i+1):
			out = np.concatenate((out,np.multiply(np.power(X1, i-j), np.power(X2, j)).reshape(m,1)), axis=1)
	return out

'''
Plot Decision Boundary is capable of plotting boundaries x2 = f(x1)
where each row in X is [xo, x1, x2, H.O.F]
where H.O.F are polynomial combinations of x1, x2
'''
def plotDecisionBoundary(theta, X, y):
	#X is a Mx(n+1) matrix of features x0 x1 x2 x3 ... xn
	#Plotting the normal graph of points
	mask = y == 1.0
	#Only extract x1, x2
	positives = X[mask,1:3]
	negatives = X[~mask, 1:3]
	plt.scatter(positives[:,0], positives[:,1], marker = 'x')
	plt.scatter(negatives[:,0], negatives[:,1], marker = 'o')
	m, n = X.shape
	if n <= 3:
		#This is just basically ploting a line
		x_vals = np.array([min(X[:, 1])-2, max(X[:, 1])+2]) # Plotting x1
		y_vals = np.multiply(-1/theta[2],np.multiply(theta[1],x_vals) + theta[0])
		plt.plot(x_vals, y_vals, color = 'y')
	else:
		#Creating an evenly spcaed grid of 50x50
		u = np.linspace(min(X[:,1]),max(X[:,1]), 50)
		v = np.linspace(min(X[:,2]),max(X[:,2]), 50)
		z = np.zeros((len(u), len(v)))
		for i in range(len(u)):
			for j in range(len(v)):
				z[i, j] = mapFeature(np.array(u[i]),np.array(v[j])).dot(theta)
		#plot z = 0
		z = z.T
		plt.contour(u, v, z, cmap = 'Reds')
	plt.legend(['Decision Boundary', 'y = 1', 'y = 0'])
	plt.show()