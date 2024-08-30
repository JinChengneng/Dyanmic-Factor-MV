# Data Description

This file contains the data used in the paper *"Dynamic Factor Model-Based Multiperiod Mean-Variance Portfolio Selection with Portfolio Constraints"*. The data is divided into two main sections: Markov Decision Process (MDP) data, and Factor Model data.

## MDP data 
This data is used to illustrate the solution procedure outlined in Algorithm 1 for solving cone-constrained multi-period MV portfolio optimization under the Markov regime setting.

### Model Parameters
- Number of states (M): 2
- Number of assets (N): 4 (IBM, Altria Group, Exxon Mobil, UTC from the Dow Jones Index)
- Time periods (T): 12 quarters

### transition probabilities matrix
The market state evolves according to a Markov Chain model with the following transition probabilities:

$$
P = 
\begin{pmatrix}
0.7 & 0.3 \\
0.4 & 0.6
\end{pmatrix},
$$

where $P(s_{t+1} = S_1 | s_t = S_1) = 0.7$ and $P(s_{t+1} = S_2 | s_t = S_2) = 0.6$.

### quarterly mean excess return for each state
$$\mu = 
\begin{pmatrix}
0.167 & 0.157 & 0.057 & 0.1470 \\
-0.193 & -0.063 & -0.073 & -0.113
\end{pmatrix},
$$

where each row corresponds to a market state (S_1 and S_2 respectively), and each column represents an asset.

### covariance matrices for each state 
$$
\Sigma_{S_1} = \begin{pmatrix}
0.0306 & 0.0012 & 0.0015 & 0.0047 \\
0.0012 & 0.0319 & 0.0032 & 0.0027 \\
0.0015 & 0.0032 & 0.0130 & 0.0041 \\
0.0047 & 0.0027 & 0.0041 & 0.0222
\end{pmatrix},
$$

$$
\Sigma_{S_2} = \begin{pmatrix}
0.0488 & 0.0036 & 0.0116 & 0.0194 \\
0.0036 & 0.0369 & 0.0069 & 0.0064 \\
0.0116 & 0.0069 & 0.0257 & 0.0141 \\
0.0194 & 0.0064 & 0.0141 & 0.0580
\end{pmatrix}.
$$

### quarterly risk-free rate
RF = 1.003


## Factor Model Data
This data is used to illustrate the solution procedure outlined in Algorithm 2 for solving cone-constrained multi-period MV portfolio optimization within the context of a market featuring the Fama-French factor model.

### Model Parameters

- Factors: ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'Mom']
- Assets (Industry Portfolios): ['NoDur', 'Durbl', 'Manuf', 'Enrgy', 'HiTec', 'Telcm', 'Shops', 'Hlth', 'Utils', 'Other']
- Dimension of states (M): 6
- Number of assets (N): 10
- Time period: July 1963 to May 2024 (over 60 years of monthly data)

### Alpha vector (intercept term for the excess returns regression model)
$$\alpha = 10^{-3}\cdot\begin{pmatrix}
2.69 \\
3.15 \\
1.91 \\
2.02 \\
8.10 \\
4.16 \\
4.03 \\
4.83 \\
2.87 \\
2.11
\end{pmatrix}$$

### B matrix (factor loadings matrix, mapping factors to excess returns)
$$ B = \begin{pmatrix}
0.864 & 0.071 & -0.047 & 0.544 & 0.395 & -0.011 \\
1.190 & 0.219 & 0.172 & 0.162 & 0.040 & -0.301 \\
1.073 & 0.117 & 0.080 & 0.325 & 0.166 & -0.035 \\
0.999 & -0.053 & 0.373 & 0.147 & 0.342 & 0.063 \\
1.049 & 0.078 & -0.348 & -0.338 & -0.440 & -0.050 \\
0.823 & -0.247 & 0.079 & -0.209 & 0.164 & -0.086 \\
0.978 & 0.200 & -0.106 & 0.424 & 0.045 & -0.069 \\
0.871 & -0.107 & -0.372 & 0.270 & 0.317 & 0.061 \\
0.654 & -0.174 & 0.208 & 0.125 & 0.315 & 0.046 \\
1.110 & 0.088 & 0.462 & 0.113 & -0.206 & -0.033
\end{pmatrix}$$

### Phi matrix (mean-reversion coefficients matrix for the state variables)
$$\Phi = 10^{-2} \cdot \begin{pmatrix}
97.09 & -5.64 & 2.83 & 4.05 & 7.22 & -0.44 \\
-12.32 & 97.92 & -4.08 & -3.88 & 8.00 & 1.97 \\
-5.91 & 1.17 & 84.92 & 1.88 & -9.63 & -1.72 \\
-0.79 & -8.45 & 0.86 & 78.39 & -4.86 & -0.54 \\
-3.78 & -0.37 & -2.95 & -2.90 & 84.96 & -0.68 \\
4.75 & -9.20 & 6.93 & -4.08 & -7.17 & 95.58
\end{pmatrix}$$

### Sigma_return matrix (covariance matrix for the noise term in the excess returns model)
$$\Sigma_{\epsilon} =  10^{-4}\cdot \begin{pmatrix}
4.41 & -1.90 & 0.04 & -2.04 & -1.50 & 0.47 & 1.42 & 1.95 & 1.55 & 0.68 \\
-1.90 & 19.39 & 0.67 & -2.93 & 0.49 & -1.61 & 1.27 & -2.43 & -2.25 & -0.53 \\
0.04 & 0.67 & 2.43 & -0.24 & 0.04 & -1.01 & -0.21 & -0.05 & -0.70 & 0.16 \\
-2.04 & -2.93 & -0.24 & 19.28 & -1.81 & -1.45 & -3.90 & -1.48 & 1.54 & -1.33 \\
-1.50 & 0.49 & 0.04 & -1.81 & 6.67 & -0.31 & -0.51 & -1.50 & -2.17 & -1.24 \\
0.47 & -1.61 & -1.01 & -1.45 & -0.31 & 9.03 & 0.20 & -0.22 & 0.72 & -0.53 \\
1.42 & 1.27 & -0.21 & -3.90 & -0.51 & 0.20 & 5.75 & 0.07 & -0.57 & 0.41 \\
1.95 & -2.43 & -0.05 & -1.48 & -1.50 & -0.22 & 0.07 & 8.28 & 0.52 & 1.01 \\
1.55 & -2.25 & -0.70 & 1.54 & -2.17 & 0.72 & -0.57 & 0.52 & 9.45 & -0.24 \\
0.68 & -0.53 & 0.16 & -1.33 & -1.24 & -0.53 & 0.41 & 1.01 & -0.24 & 2.61
\end{pmatrix}$$

### Sigma_state matrix (covariance matrix for the noise term in the state variables model)
$$\Sigma_{\varepsilon} =  10^{-3}\cdot \begin{pmatrix}
2.02 & 0.38 & -0.26 & -0.18 & -0.33 & -0.32 \\
0.38 & 0.89 & -0.01 & -0.24 & -0.05 & -0.08 \\
-0.26 & -0.01 & 0.87 & 0.06 & 0.41 & -0.23 \\
-0.18 & -0.24 & 0.06 & 0.48 & -0.01 & 0.08 \\
-0.33 & -0.05 & 0.41 & -0.01 & 0.42 & 0.00 \\
-0.32 & -0.08 & -0.23 & 0.08 & 0.00 & 1.77
\end{pmatrix}$$

### monthly risk-free rate
RF = 1.0036
