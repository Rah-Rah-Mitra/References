import numpy
from sklearn import linear_model
from sklearn.metrics import mean_squared_error

filename = ".vscode\References\Machine Learning Tutorials\My_Projects\Weight Predictor App\weight-height.csv"
raw_data = open(filename, 'rt')
data = numpy.loadtxt(raw_data, delimiter=',') #(10000,2) Shape

# Seperate out the indepnedent variables height into X
# and dependent variable weight into y
X = data[:,1]
y = data[:,0]

#Split the data into training / testing sets
X_train = X[:9000]
X_test = X[9000:]
#Split the targets into training / testing sets
y_train = y[:9000]
y_test = y[9000:]

#Modify the data to input to scikit learn convert to nparray
X_train = X_train.reshape(-1,1)
X_test = X_test.reshape(-1,1)

#Create linear regression object
regr = linear_model.LinearRegression()

#Train model using training sets
regr.fit(X_train, y_train)

def Predict_Value(Value):
    Pred_value = numpy.array([Value])
    Pred_value = Pred_value.reshape(-1,1)
    return str(regr.predict(Pred_value))