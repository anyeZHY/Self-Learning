import util
import numpy as np
import matplotlib.pyplot as plt

np.seterr(all='raise')


factor = 2.0

class LinearModel(object):
    """Base class for linear models."""

    def __init__(self, theta=None):
        """
        Args:
            theta: Weights vector for the model.
        """
        self.theta = theta

    def fit(self, X, y):
        """Run solver to fit linear model. You have to update the value of
        self.theta using the normal equations.

        Args:
            X: Training example inputs. Shape (n_examples, dim).
            y: Training example labels. Shape (n_examples,).
        """
        # *** START CODE HERE ***
        self.theta = np.linalg.solve(X.T@X,X.T@y)
        # *** END CODE HERE ***

    def create_poly(self, k, X):
        """
        Generates a polynomial feature map using the data x.
        The polynomial map should have powers from 0 to k
        Output should be a numpy array whose shape is (n_examples, k+1)

        Args:
            X: Training example inputs. Shape (n_examples, 2).
        """
        # *** START CODE HERE ***
        if k==0:
            return
        if k==1:
            return X[:,0].reshape(len(X[:,0]), -1)
        if k==2:
            return X
        feature = X[:,-1]
        N, D = X.shape
        pow_idx = [np.full(N, i) for i in range(2,int(k+1))]
        attribute = np.power(feature, np.array(pow_idx)).T
        X = np.concatenate([X, attribute], axis=1)
        return X
        # *** END CODE HERE ***

    def create_sin(self, k, X):
        """
        Generates a sin with polynomial featuremap to the data x.
        Output should be a numpy array whose shape is (n_examples, k+2)

        Args:
            X: Training example inputs. Shape (n_examples, 2).
        """
        # *** START CODE HERE ***
        sin = np.sin(X[:,1]).reshape(len(X[:,1]), -1)
        self.create_poly(k, X)
        result = np.concatenate([X, sin], axis=1) if k>0 else sin
        return result
        # *** END CODE HERE ***

    def predict(self, X):
        """
        Make a prediction given new inputs x.
        Returns the numpy array of the predictions.

        Args:
            X: Inputs of shape (n_examples, dim).

        Returns:
            Outputs of shape (n_examples,).
        """
        # *** START CODE HERE ***
        # *** END CODE HERE ***


def run_exp(train_path, sine=False, ks=None, filename='plot.png'):
    if ks is None:
        ks = [1, 2, 3, 5, 10, 20]
    train_x,train_y=util.load_dataset(train_path,add_intercept=True)
    plot_x = np.ones([1000, 2])
    plot_x[:, 1] = np.linspace(-factor*np.pi, factor*np.pi, 1000)
    plt.figure()
    plt.scatter(train_x[:, 1], train_y)

    for k in ks:
        '''
        Our objective is to train models and perform predictions on plot_x data
        '''
        # *** START CODE HERE ***
        clf = LinearModel()
        x_new = clf.create_poly(k, train_x) if not sine else clf.create_sin(k, train_x)
        clf.fit(x_new, train_y)
        plot_y = clf.theta * clf.create_poly(k, plot_x.reshape(len(plot_x), -1)) if not sine \
            else clf.theta * clf.create_sin(k, plot_x.reshape(len(plot_x), -1))
        plot_y = np.sum(plot_y, axis=1)
        # *** END CODE HERE ***
        '''
        Here plot_y are the predictions of the linear model on the plot_x data
        '''
        plt.ylim(-2, 2)
        plt.plot(plot_x[:, 1], plot_y, label='k=%d' % k)

    plt.legend()
    plt.savefig(filename)
    plt.clf()


def main(train_path, small_path, eval_path):
    '''
    Run all expetriments
    '''
    # *** START CODE HERE ***
    x_train, y_train = util.load_dataset(train_path, label_col='y', add_intercept=True)
    x_small, y_small = util.load_dataset(small_path, label_col='y', add_intercept=True)
    x_eval, y_eval = util.load_dataset(eval_path, label_col='y', add_intercept=True)
    # ========== Poly: 3 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    clf = LinearModel()
    x_new = clf.create_poly(3, x_train)
    clf.fit(x_new, y_train)
    #### Visualization
    plt.scatter(x_train[:,1], y_train)
    x_lim_max = max(x_train[:,1])
    x_lim_min = min(x_train[:,1])
    x = np.arange(x_lim_min, x_lim_max, (x_lim_max-x_lim_min)/1000)
    y = clf.theta * clf.create_poly(3, util.add_intercept(x.reshape(len(x),-1)))
    y = np.sum(y, axis=1)
    plt.plot(x, y, '--')
    plt.savefig('degree3.pdf')
    # ========== Poly: k >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    run_exp(train_path, ks=[3, 5, 10, 20], filename='degreek.pdf')
    run_exp(train_path, ks=[0, 1, 2, 3, 5, 10, 20], filename='sine.pdf', sine=True)
    run_exp(small_path, ks=[1, 2, 5, 10, 20], filename='overfitting.pdf')
    # *** END CODE HERE ***

if __name__ == '__main__':
    main(train_path='train.csv',
        small_path='small.csv',
        eval_path='test.csv')
