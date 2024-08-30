import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class MDP_Data:
    # Number of states
    M: int = 2
    # Number of assets
    N: int = 4
    # transition probabilities matrix
    PROB_MC: np.ndarray = field(default_factory=lambda: np.array([
        [0.7, 0.3],
        [0.4, 0.6]
    ]))
    # quarterly mean excess return for each state
    MU: np.ndarray = field(default_factory=lambda: np.array([
        [0.167, 0.157, 0.057, 0.1470],
        [-0.193, -0.063, -0.073, -0.113]
    ]))
    # covariance matrices for each state
    SIGMA: np.ndarray = field(default_factory=lambda: np.array([
        0.01 * np.array([
            [3.06, 0.12, 0.15, 0.47],
            [0.12, 3.19, 0.32, 0.27],
            [0.15, 0.32, 1.30, 0.41],
            [0.47, 0.27, 0.41, 2.22]
        ]),
        0.01 * np.array([
            [4.88, 0.36, 1.16, 1.94],
            [0.36, 3.69, 0.69, 0.64],
            [1.16, 0.69, 2.57, 1.41],
            [1.94, 0.64, 1.41, 5.80]
        ])
    ]))
    # quarterly risk-free rate
    RF: float = 1.003

    def __post_init__(self):
        self._validate_shapes()

    def _validate_shapes(self):
        assert len(self.PROB_MC) == len(self.MU) == len(self.SIGMA) == self.M
        assert len(self.MU[0]) == len(self.SIGMA[0]) == self.N


@dataclass
class FF_Data:
    # data paths
    factor_data_path = './data/six_factors.csv'
    return_data_path = './data/returns.csv'
    # factors used to describe the market states
    factors: List[str] = field(default_factory=lambda: ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'Mom'])
    # 10 industry portfolios
    assets: List[str] = field(
        default_factory=lambda: ['NoDur', 'Durbl', 'Manuf', 'Enrgy', 'HiTec', 'Telcm', 'Shops', 'Hlth', 'Utils',
                                 'Other'])
    # the time period for the data
    begin_date: str = '1964-01-01'
    end_date: str = '2024-5-31'

    # the dimension of states
    M: int = field(init=False)
    # the number of assets
    N: int = field(init=False)
    # Alpha vector (intercept term for the excess returns regression model)
    alpha: np.ndarray = None
    # B matrix (factor loadings matrix, mapping factors to excess returns)
    B: np.ndarray = None
    # Phi matrix (mean-reversion coefficients matrix for the state variables)
    Phi: np.ndarray = None
    # Sigma_return matrix (covariance matrix for the noise term in the excess returns model)
    Sigma_return: np.ndarray = None
    # Sigma_state matrix (covariance matrix for the noise term in the state variables model)
    Sigma_state: np.ndarray = None
    # Define the quarterly risk-free rate
    RF: float = None

    def __post_init__(self):
        self.M = len(self.factors)
        self.N = len(self.assets)
        self.get_params_from_real_data()
        self._validate_shapes()

    def _validate_shapes(self):
        assert self.Phi.shape == (self.M, self.M)
        assert self.alpha.shape == (self.N,)
        assert self.B.shape == (self.N, self.M)
        assert self.Sigma_return.shape == (self.N, self.N)
        assert self.Sigma_state.shape == (self.M, self.M)

    def get_params_from_real_data(self):
        factor_data, s_t = self._load_factor_data()
        self.RF = np.mean(factor_data['RF'].values) * 0.01
        self.Phi, self.Sigma_state = self._fit_factor_model(s_t)

        return_data, r_t = self._load_return_data()
        self.alpha, self.B, self.Sigma_return = self._fit_return_model(s_t, r_t)

    def _load_factor_data(self) -> Tuple[pd.DataFrame, np.ndarray]:
        factor_data = pd.read_csv(self.factor_data_path)
        factor_data['Date'] = pd.to_datetime(factor_data['index'].astype(str), format='%Y%m')
        data_subset = factor_data[(factor_data['Date'] >= self.begin_date) & (factor_data['Date'] <= self.end_date)]
        return data_subset, data_subset[self.factors].values * 0.01

    def _load_return_data(self) -> Tuple[pd.DataFrame, np.ndarray]:
        return_data = pd.read_csv(self.return_data_path, sep='\t')
        return_data['Date'] = pd.to_datetime(return_data['index'].astype(str), format='%Y%m')
        data_subset = return_data[(return_data['Date'] >= self.begin_date) & (return_data['Date'] <= self.end_date)]
        return data_subset, data_subset[self.assets].values * 0.01

    def _fit_factor_model(self, s_t: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        X, Y = s_t[:-1], s_t[1:]
        model = LinearRegression(fit_intercept=False).fit(X, Y)
        Phi = np.eye(self.M) - model.coef_
        residuals = Y - model.predict(X)
        Sigma_epsilon = np.cov(residuals.T)
        return Phi, Sigma_epsilon

    def _fit_return_model(self, s_t: np.ndarray, r_t: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        model = LinearRegression(fit_intercept=True).fit(s_t, r_t)
        residuals = r_t - model.predict(s_t)
        Sigma_epsilon = np.cov(residuals.T)
        return model.intercept_, model.coef_, Sigma_epsilon


if __name__ == '__main__':
    mdp_data = MDP_Data()
    print("\n------------MDP Data----------------")
    print("The number of states:", mdp_data.M)
    print("The number of assets:", mdp_data.N)
    print("Transition probabilities matrix:")
    print(mdp_data.PROB_MC)
    print("Mean excess return for each state:")
    print(mdp_data.MU)
    print("Covariance matrices for each state:")
    print(mdp_data.SIGMA)
    print("Risk-free rate:", mdp_data.RF)

    ff_data = FF_Data()
    print("\n------------Factor Model Data----------------")
    print("The number of states:", ff_data.M)
    print("The number of assets:", ff_data.N)
    print("Alpha vector (intercept term for the excess returns regression model):")
    print(ff_data.alpha)
    print("B matrix (factor loadings matrix, mapping factors to excess returns):")
    print(ff_data.B)
    print("Phi matrix (mean-reversion coefficients matrix for the state variables):")
    print(ff_data.Phi)
    print("Sigma_return matrix (covariance matrix for the noise term in the excess returns model):")
    print(ff_data.Sigma_return)
    print("Sigma_state matrix (covariance matrix for the noise term in the state variables model):")
    print(ff_data.Sigma_state)
    print("Risk-free rate:", ff_data.RF)
