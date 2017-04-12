from sklearn.datasets import load_iris

iris = load_iris()

print iris.feature_names  # metadata: names of the features
print iris.target_names  # metadata: names of the different types of flowers

print iris.data[0]  # first flower
print iris.target[0]  # contains the labels

import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree

iris = load_iris()
# here, we remove the first example of each flower
# found at indices: 0, 50, 100
test_idx = [0, 50, 100]

# create 2 new sets of variables, for training and testing
# training data
# remove the entires from the data and target variables
train_target = np.delete(iris.target, test_idx)
train_data = np.delete(iris.data, test_idx, axis=0)

# testing data
test_target = iris.target[test_idx]
test_data = iris.data[test_idx]

# create new classifier
clf = tree.DecisionTreeClassifier()
# train on training data
clf.fit(train_data, train_target)

# what we expect
print test_target
# what tree predicts
print clf.predict(test_data)

# Visualize
from sklearn.externals.six import StringIO
import pydotplus

dot_data = StringIO()
tree.export_graphviz(clf, out_file=dot_data,
                     feature_names=iris.feature_names,
                     class_names=iris.target_names,
                     filled=True, rounded=True,
                     impurity=False)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("iris.pdf")
