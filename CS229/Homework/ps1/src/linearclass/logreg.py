import numpy as np
import util


def main(train_path, valid_path, save_path):
    """Problem: Logistic regression with Newton's Method.

    Args:
        train_path: Path to CSV file containing dataset for training.
        valid_path: Path to CSV file containing dataset for validation.
        save_path: Path to save predicted probabilities using np.savetxt().
    """
    x_train, y_train = util.load_dataset(train_path, add_intercept=True)

    # *** START CODE HERE ***
    # Train a logistic regression classifier
    # Plot decision boundary on top of validation set
    # Use np.savetxt to save predictions on eval set to save_path
    clf = LogisticRegression(theta_0=np.zeros_like(x_train[0]))
    clf.fit(x_train,y_train)
    x_vad, y_vad = util.load_dataset(valid_path, add_intercept=True)
    y_predict = clf.predict(x_vad)
    np.savetxt(save_path, y_predict)
    util.plot(x_vad, y_vad, clf.theta, save_path=train_path[:3]+'.pdf', correction=1)
    # print(np.mean(y_predict == y_vad))
    # *** END CODE HERE ***

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class LogisticRegression:
    """Logistic regression with Newton's Method as the solver.

    Example usage:
        > clf = LogisticRegression()
        > clf.fit(x_train, y_train)
        > clf.predict(x_eval)
    """
    def __init__(self, step_size=0.01, max_iter=1000000, eps=1e-5,
                 theta_0=None, verbose=True):
        """
        Args:
            step_size: Step size for iterative solvers only.
            max_iter: Maximum number of iterations for the solver.
            eps: Threshold for determining convergence.
            theta_0: Initial guess for theta. If None, use the zero vector.
            verbose: Print loss values during training.
        """
        self.theta = theta_0
        self.step_size = step_size
        self.max_iter = max_iter
        self.eps = eps
        self.verbose = verbose

    def fit(self, x, y):
        """Run Newton's Method to minimize J(theta) for logistic regression.

        Args:
            x: Training example inputs. Shape (n_examples, dim).
            y: Training example labels. Shape (n_examples,).
        """
        # *** START CODE HERE ***
        N, D = x.shape
        theta = self.theta
        if theta is None:
            theta = np.zeros(D)
        i = 0
        for i in range(self.max_iter):
            mu = theta.dot(x.T)
            dJ = - np.sum((y-sigmoid(mu)).reshape(N, -1) * x, axis=0) / N
            if np.sum(np.abs(dJ)) <= self.eps:
                break
            if i%1000 == 0:
                if self.verbose:
                    # print(sigmoid(mu))
                    loss = -np.mean(y * np.log(sigmoid(mu)+1e-6) + (1-y) * np.log(1-sigmoid(mu)+1e-6))
                    print('iter: {}, loss: {}'.format(i,loss))
            theta = theta - self.step_size * dJ
        if self.verbose:
            print('total iter: {}, theta: {}'.format(i+1, theta))
        self.theta = theta
        # H = np.sum(sigmoid(mu) * (1 - sigmoid(mu))) * (x.T @ x) / N
        # print(H.shape)
        # *** END CODE HERE ***

    def predict(self, x):
        """Return predicted probabilities given new inputs x.

        Args:
            x: Inputs of shape (n_examples, dim).

        Returns:
            Outputs of shape (n_examples,).
        """
        # *** START CODE HERE ***
        return sigmoid(x.dot(self.theta))
        # *** END CODE HERE ***

if __name__ == '__main__':
    main(train_path='ds1_train.csv',
         valid_path='ds1_valid.csv',
         save_path='logreg_pred_1.txt')

    main(train_path='ds2_train.csv',
         valid_path='ds2_valid.csv',
         save_path='logreg_pred_2.txt')
