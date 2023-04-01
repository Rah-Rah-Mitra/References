import matplotlib.pyplot as plt
import numpy
from sklearn import linear_model
from sklearn.metrics import mean_squared_error

filename = "weight-height.csv"
raw_data = open(filename, 'rt')
data = numpy.loadtxt(raw_data, delimiter=',') #10000 Lines of Weight-Height

# Seperate out the indepnedent variables height into X
# and dependent variable weight into y
X = data[:,1]
y = data[:,0]

X_20 = X[:20]
y_20 = y[:20]