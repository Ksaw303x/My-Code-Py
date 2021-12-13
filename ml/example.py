from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

url = "iris.csv"
csv_names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = read_csv(url, names=csv_names)

array = dataset.values
X = array[:, 0:4]
y = array[:, 4]
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1, shuffle=True)

print(X_train)
print(X_validation)


def visualization():
    print(dataset.groupby('class').size())

    # box and whisker plots
    dataset.plot(kind='box', subplots=True, layout=(2, 2), sharex=False, sharey=False)
    pyplot.show()

    # histograms
    dataset.hist()
    pyplot.show()

    scatter_matrix(dataset)
    pyplot.show()
    

def build_models():
    # Spot Check Algorithms
    models = [
        ('LR', LogisticRegression(solver='liblinear', multi_class='ovr')),
        ('LDA', LinearDiscriminantAnalysis()),
        ('KNN', KNeighborsClassifier()),
        ('CART', DecisionTreeClassifier()),
        ('NB', GaussianNB()),
        ('SVM', SVC(gamma='auto'))
    ]
    # evaluate each model in turn
    results = []
    names = []
    for name, model in models:
        kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
        results.append(cv_results)
        names.append(name)
        print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
    # Compare Algorithms
    pyplot.boxplot(results, labels=names)
    pyplot.title('Algorithm Comparison')
    pyplot.show()
    
    
def make_predictions():
    model = SVC(gamma='auto')
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    
    # Evaluate predictions
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))


if __name__ == '__main__':
    # visualization()
    build_models()
    # make_predictions()
