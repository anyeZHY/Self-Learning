import numpy as np
import util
import matplotlib.pyplot as plt

def main(lr, train_path, eval_path, save_path):
    """Problem: Poisson regression with gradient ascent.

    Args:
        lr: Learning rate for gradient ascent.
        train_path: Path to CSV file containing dataset for training.
        eval_path: Path to CSV file containing dataset for evaluation.
        save_path: Path to save predictions.
    """
    # Load training set
    x_train, y_train = util.load_dataset(train_path, add_intercept=True)

    # *** START CODE HERE ***
    # Fit a Poisson Regression model
    # Run on the validation set, and use np.savetxt to save outputs to save_path
    clf = PoissonRegression(step_size=lr)
    clf.fit(x_train, y_train)
    x_eval, y_eval = util.load_dataset(eval_path, add_intercept=True)
    y_predict = clf.predict(x_eval)
    np.savetxt(save_path, y_predict)

    plt.scatter(y_eval, y_predict)
    plt.xlabel('Predict')
    plt.ylabel('Ground truth')
    tmp = np.append(y_eval,y_eval)
    plt.xlim([-1, max(tmp)+1])
    plt.ylim([-1, max(tmp)+1])
    plt.plot([-1,max(tmp)+1],[-1, max(tmp)+1], '--r')
    plt.savefig(save_path[:-3]+'pdf')
    # *** END CODE HERE ***


class PoissonRegression:
    """Poisson Regression.

    Example usage:
        > clf = PoissonRegression(step_size=lr)
        > clf.fit(x_train, y_train)
        > clf.predict(x_eval)
    """

    def __init__(self, step_size=1e-5, max_iter=10000000, eps=1e-5,
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
        """Run gradient ascent to maximize likelihood for Poisson regression.

        Args:
            x: Training example inputs. Shape (n_examples, dim).
            y: Training example labels. Shape (n_examples,).
        """
        # *** START CODE HERE ***
        N, D = x.shape
        print(x.shape)
        theta = np.zeros(D) if self.theta is None else self.theta
        for i in range(self.max_iter):
            grad = np.sum((y.reshape(N,1) - np.exp(x @ theta.reshape((D,1)))) * x, axis=0)
            if np.sum(np.abs(grad))<self.eps:
                break
            theta += self.step_size * grad
            if self.verbose and i%100==0 :
                prob = np.mean(y * (x @ theta) - np.exp(x @ theta))
                print('iter: {}, prob: {}'.format(i, prob))
            # break
        if self.verbose:
            print('theta: {}'.format(theta))
        self.theta = theta
        # *** END CODE HERE ***

    def predict(self, x):
        """Make a prediction given inputs x.

        Args:
            x: Inputs of shape (n_examples, dim).

        Returns:
            Floating-point prediction for each input, shape (n_examples,).
        """
        # *** START CODE HERE ***
        N, D = x.shape
        return np.exp(x @ self.theta.reshape((D, -1)))
        # *** END CODE HERE ***

if __name__ == '__main__':
    main(lr=1e-5,
        train_path='train.csv',
        eval_path='valid.csv',
        save_path='poisson_pred.txt')
