from typing import Optional

import numpy as np  # type: ignore
from scipy import linalg  # type: ignore

from d3m.container import ndarray
from d3m.primitive_interfaces.base import CallResult
from d3m.primitive_interfaces.unsupervised_learning import UnsupervisedLearnerPrimitiveBase
from d3m.metadata import base as metadata_base, hyperparams, params
import d3m.metadata.base as metadata_module
from d3m import exceptions

from . import __author__, __version__

from sklearn.preprocessing import OneHotEncoder

Inputs = ndarray
Outputs = ndarray


class Params(params.Params):
    transformation: Optional[np.ndarray]
    mean: Optional[np.ndarray]


class Hyperparams(hyperparams.Hyperparams):
    n_components = hyperparams.Hyperparameter[int](
        semantic_types=[
            'https://metadata.datadrivendiscovery.org/types/ControlParameter',
        ],
        default=1,
        description="Target rank, i.e., number of sparse components to be computed.",
    )
    max_iter = hyperparams.Hyperparameter[int](
        semantic_types=[
            'https://metadata.datadrivendiscovery.org/types/TuningParameter',
            'https://metadata.datadrivendiscovery.org/types/ResourcesUseParameter',
        ],
        default=100,
        description="Maximum number of iterations to perform before exiting."
    )
    max_tol = hyperparams.Hyperparameter[float](
        semantic_types=[
            'https://metadata.datadrivendiscovery.org/types/TuningParameter',
            'https://metadata.datadrivendiscovery.org/types/ResourcesUseParameter',
        ],
        default=1e-5,
        description="Stopping tolerance for reconstruction error."
    )

    # search over these hyperparameters to tune performance
    alpha = hyperparams.Uniform(
        default=1e-1, lower=0.0, upper=1.0,
        description="Sparsity controlling parameter. Higher values lead to sparser components",
        semantic_types=['https://metadata.datadrivendiscovery.org/types/TuningParameter'],
    )
    beta = hyperparams.Uniform(
        default=1e-6, lower=0.0, upper=1e-1,
        description="Amount of ridge shrinkage to apply in order to improve conditionin.",
        semantic_types=['https://metadata.datadrivendiscovery.org/types/TuningParameter'],
    )
    gamma = hyperparams.Uniform(
        default=1.0, lower=0.1, upper=5,
        description="Parameter to control the amount of grossly corrupted entries that should be pulled out.",
        semantic_types=['https://metadata.datadrivendiscovery.org/types/TuningParameter'],
    )    


class RobustSparsePCA(UnsupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    """
    Given a mean centered rectangular matrix `A` with shape `(m, n)`, SPCA
    computes a set of sparse components that can optimally reconstruct the
    input data.  The amount of sparseness is controllable by the coefficient
    of the L1 penalty, given by the parameter alpha. In addition, some ridge
    shrinkage can be applied in order to improve conditioning.
    """

    __author__ = "ICSI" # a la directions on https://gitlab.datadrivendiscovery.org/jpl/primitives_repo
    metadata = metadata_base.PrimitiveMetadata({
        'id': '3ed8e16e-1d5f-45c8-90f7-fe3c4ce2e758',
        'version': __version__,
        'name': 'Robust Sparse Principal Component Analysis',
        'description': "Given a mean centered rectangular matrix `A` with shape `(m, n)`, Robust SPCA computes a set of robust sparse components that can optimally reconstruct the input data.  The amount of sparseness is controllable by the coefficient of the L1 penalty, given by the parameter alpha. In addition, some ridge shrinkage can be applied in order to improve conditioning.",
        'python_path': 'd3m.primitives.feature_extraction.sparse_pca.RobustSparsePCA',
        'primitive_family': metadata_base.PrimitiveFamily.FEATURE_EXTRACTION,
        'algorithm_types' : [
            'LOW_RANK_MATRIX_APPROXIMATIONS'
        ],
        'keywords' : ['low rank approximation', 'sparse PCA'],
        'source' : {
            'name': __author__,
            'contact': 'mailto:erichson@berkeley.edu',
            'uris' : [
                'https://gitlab.com/datadrivendiscovery/contrib/realML',
            ],
        },
        'installation': [
            {
                'type': metadata_base.PrimitiveInstallationType.PIP,
                'package': 'realML',
                'version': '3.0.3',
            }
        ],
        'location_uris': [ # NEED TO REF SPECIFIC COMMIT
            'https://gitlab.com/datadrivendiscovery/contrib/realML/-/blob/master/realML/matrix/robustsparsepca.py',
            ],
        'preconditions': [
            'NO_MISSING_VALUES',
            'NO_CATEGORICAL_VALUES'
        ],
    })    
    
    
    def __init__(self, *, hyperparams: Hyperparams) -> None:
        super().__init__(hyperparams=hyperparams)

        self._training_inputs: Inputs = None
        self._fitted = False
        self._transformation = None
        self._mean = None
        # Used only for testing.
        self._invtransformation = None

    def fit(self, *, timeout: float = None, iterations: int = None) -> CallResult[None]:
        # If already fitted with current training data, this call is a noop.
        if self._fitted:
            return CallResult(None)
        if self._training_inputs is None:
            raise exceptions.InvalidStateError("Missing training data.")

        # Do some preprocessing to pass CI
        #enc = OneHotEncoder(handle_unknown='ignore')
        #enc.fit(self._training_inputs)
        #self._training_inputs = enc.transform(self._training_inputs).toarray()
        
        self._training_inputs = np.array(self._training_inputs)
        self._training_inputs[np.isnan(self._training_inputs)] = 1
        
        # Center data
        self._mean = self._training_inputs.mean(axis=0)
        
        
        X = self._training_inputs - self._mean
        
        
        # Initialization of Variable Projection Solver
        U, D, Vt = linalg.svd(X, full_matrices=False, overwrite_a=False)
        Dmax = D[0]  # l2 norm
        A = Vt[:self.hyperparams['n_components']].T
        B = Vt[:self.hyperparams['n_components']].T

        U = U[:, :self.hyperparams['n_components']]
        Vt = Vt[:self.hyperparams['n_components']]
        S = np.zeros_like(X)


        # Set Tuning Parameters
        alpha = self.hyperparams['alpha']
        beta = self.hyperparams['beta']
        gamma = self.hyperparams['gamma']
        alpha *= Dmax**2
        beta *= Dmax**2
        nu = 1.0 / (Dmax**2 + beta)
        kappa = nu * alpha
        obj = []  # values of objective function
        n_iter = 0

        #   Apply Variable Projection Solver
        while self.hyperparams['max_iter'] > n_iter:
            # Update A:
            # X'XB = UDV'
            # Compute X'XB via SVD of X

            XS = X - S
            XB = X.dot(B)
            Z = (XS).T.dot(XB)

            Utilde, Dtilde, Vttilde = linalg.svd(Z, full_matrices=False, overwrite_a=True)
            A = Utilde.dot(Vttilde)
            
            # Proximal Gradient Descent to Update B
            R = XS - XB.dot(A.T)
            G = X.T.dot(R.dot(A)) - beta * B            
            arr = B + nu * G
            B = np.sign(arr) * np.maximum(np.abs(arr) - kappa, 0)
            
            # Compute residuals
            R = X - X.dot(B).dot(A.T)
            S = np.sign(R) * np.maximum(np.abs(R) - gamma, 0)
            R -= S
            
            
            
            # Calculate objective
            obj.append(0.5 * np.sum(R**2) + alpha * np.sum(np.abs(B)) + 0.5 * beta * np.sum(B**2) + gamma * np.sum(np.abs(S)))
            # Break if obj is not improving anymore
            if n_iter > 0 and abs(obj[-2] - obj[-1]) / obj[-1] < self.hyperparams['max_tol']:
                break
            # Next iter
            n_iter += 1

        # Construct transformation matrix with eigenvectors
        self._invtransformation = A
        self._transformation = B

        self._fitted = True
        return CallResult(None)

    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> CallResult[Outputs]:
        "Returns the latent matrix"
        if not self._fitted:
            raise exceptions.PrimitiveNotFittedError("Primitive not fitted.")
        comps = (inputs - self._mean).dot(self._transformation)
        return CallResult(ndarray(comps, generate_metadata=True))

    def set_training_data(self, *, inputs: Inputs) -> None:  # type: ignore
        self._training_inputs = inputs
        self._fitted = False

    def get_params(self) -> Params:
        if self._fitted:
            return Params(
                transformation=self._transformation,
                mean=self._mean,
            )
        else:
            return Params(
                transformation=None,
                mean=None,
            )

    def set_params(self, *, params: Params) -> None:
        self._transformation = params['transformation']
        self._mean = params['mean']
        self._fitted = all(param is not None for param in params.values())