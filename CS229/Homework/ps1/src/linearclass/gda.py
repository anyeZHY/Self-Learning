import numpy as np
import util


def main(train_path, valid_path, save_path):
    """Problem: Gaussian discriminant analysis (GDA)

    Args:
        train_path: Path to CSV file containing dataset for training.
        valid_path: Path to CSV file containing dataset for validation.
        save_path: Path to save predicted probabilities using np.savetxt().
    """
    # Load dataset
    x_train, y_train = util.load_dataset(train_path, add_intercept=True)

    # *** START CODE HERE ***
    # Train a GDA classifier
    # Plot decision boundary on validation set
    # Use np.savetxt to save outputs from validation set to save_path
    clf = GDA()
    clf.fit(x_train,y_train)
    x_vad, y_vad = util.load_dataset(valid_path, add_intercept=True)
    y_predict = clf.predict(x_vad)
    np.savetxt(save_path, y_predict.astype(int))

    util.plot(x_vad, y_vad, clf.theta, save_path=train_path[:3]+'_gda.pdf', correction=1)
    print(np.mean(y_predict==y_vad))
    # *** END CODE HERE ***


class GDA:
    """Gaussian Discriminant Analysis.

    Example usage:
        > clf = GDA()
        > clf.fit(x_train, y_train)
        > clf.predict(x_eval)
    """
    def __init__(self, step_size=0.01, max_iter=10000, eps=1e-5,
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
        """Fit a GDA model to training set given by x and y by updating
        self.theta.

        Args:
            x: Training example inputs. Shape (n_examples, dim).
            y: Training example labels. Shape (n_examples,).
        """
        # *** START CODE HERE ***
        # Find phi, mu_0, mu_1, and sigma
        # Write theta in terms of the parameters
        N, D = x.shape
        D = D - 1
        x = x[:,1:]
        phi = np.mean(y)
        mu1 = np.mean(x[y==1], axis=0)
        mu0 = np.mean(x[y==0], axis=0)
        sigma = (x[y==1] - mu1).T @ (x[y==1] - mu1) + (x[y==0] - mu0).T @ (x[y==0] - mu0)
        sigma /= N
        sigma_inv = np.linalg.inv(sigma)
        mu1 = mu1.reshape(D, -1)
        mu0 = mu0.reshape(D, -1)

        theta = sigma_inv @ (mu1 - mu0)
        theta = theta.reshape(-1)
        b = np.log(phi/(1-phi)) + mu0.T @ sigma_inv @ mu0 / 2 - mu1.T @ sigma_inv @ mu1 / 2
        theta = np.append(b, theta)
        if self.verbose:
            print('theta: {}'.format(theta))
        self.theta = theta
        # *** END CODE HERE ***

    def predict(self, x):
        """Make a prediction given new inputs x.

        Args:
            x: Inputs of shape (n_examples, dim).

        Returns:
            Outputs of shape (n_examples,).
        """
        # *** START CODE HERE ***
        r = np.sum(self.theta * x, axis=1)
        return (1 / (1 + np.exp(-r)))>0.5
        # *** END CODE HERE

if __name__ == '__main__':
    main(train_path='ds1_train.csv',
         valid_path='ds1_valid.csv',
         save_path='gda_pred_1.txt')

    main(train_path='ds2_train.csv',
         valid_path='ds2_valid.csv',
         save_path='gda_pred_2.txt')
