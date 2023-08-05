import collections
from typing import Union

import numpy as np
from numpy.random import Generator, RandomState
from scipy.integrate import solve_ivp

from ..utils.random import rand_generator
from ..utils.validation import check_vector
from ._seed import get_seed


def _mg_eq(xt, xtau, a=0.2, b=0.1, n=10):
    """
    Mackey-Glass time delay diffential equation, at values x(t) and x(t-tau).
    """
    return -b * xt + a * xtau / (1 + xtau**n)


def _mg_rk4(xt, xtau, a, b, n, h=1.0):
    """
    Runge-Kuta method (RK4) for Mackey-Glass timeseries discretization.
    """
    k1 = h * _mg_eq(xt, xtau, a, b, n)
    k2 = h * _mg_eq(xt + 0.5 * k1, xtau, a, b, n)
    k3 = h * _mg_eq(xt + 0.5 * k2, xtau, a, b, n)
    k4 = h * _mg_eq(xt + k3, xtau, a, b, n)

    return xt + k1 / 6 + k2 / 3 + k3 / 3 + k4 / 6


def henon_map(
    n_timesteps: int,
    a: float = 1.4,
    b: float = 0.3,
    x0: Union[list, np.ndarray] = [0.0, 0.0],
) -> np.ndarray:
    """Hénon map discrete timeseries [2]_ [3]_:

    .. math::

        x(n+1) &= 1 - ax(n)^2 + y(n)\\\\
        y(n+1) &= bx(n)

    Parameters
    ----------
    n_timesteps : int
        Number of timesteps to generate.
    a : float, default to 1.4
        :math:`a` parameter of the system.
    b : float, default to 0.3
        :math:`b` parameter of the system.
    x0 : array-like of shape (2,), default to [0.0, 0.0]
        Initial conditions of the system.

    Returns
    -------
    array of shape (n_timesteps, 2)
        Hénon map discrete timeseries.

    References
    ----------
    .. [2] M. Hénon, ‘A two-dimensional mapping with a strange
           attractor’, Comm. Math. Phys., vol. 50, no. 1, pp. 69–77, 1976.

    .. [3] `Hénon map <https://en.wikipedia.org/wiki/H%C3%A9non_map>`_
           on Wikipédia

    """
    states = np.zeros((n_timesteps, 2))
    states[0] = np.asarray(x0)

    for i in range(1, n_timesteps):
        states[i][0] = 1 - a * states[i - 1][0] ** 2 + states[i - 1][1]
        states[i][1] = b * states[i - 1][0]

    return states


def logistic_map(n_timesteps: int, r: float = 3.9, x0: float = 0.5) -> np.ndarray:
    """Logistic map discrete timeseries [4]_ [5]_:

    .. math::

        x(n+1) = rx(n)(1-x(n))

    Parameters
    ----------
    n_timesteps : int
        Number of timesteps to generate.
    r : float, default to 3.9
        :math:`r` parameter of the system.
    x0 : float, default to 0.5
        Initial condition of the system.

    Returns
    -------
    array of shape (n_timesteps, 1)
        Logistic map discrete timeseries.

    References
    ----------
    .. [4] R. M. May, ‘Simple mathematical models with very
           complicated dynamics’, Nature, vol. 261, no. 5560,
           Art. no. 5560, Jun. 1976, doi: 10.1038/261459a0.

    .. [5] `Logistic map <https://en.wikipedia.org/wiki/Logistic_map>`_
           on Wikipédia
    """
    if r > 0 and 0 < x0 < 1:
        X = np.zeros(n_timesteps)
        X[0] = x0

        for i in range(1, n_timesteps):
            X[i] = r * X[i - 1] * (1 - X[i - 1])

        return X.reshape(-1, 1)
    elif r <= 0:
        raise ValueError("r should be positive.")
    else:
        raise ValueError("Initial condition x0 should be in ]0;1[.")


def lorenz(
    n_timesteps: int,
    rho: float = 28.0,
    sigma: float = 10.0,
    beta: float = 8.0 / 3.0,
    x0: Union[list, np.ndarray] = [1.0, 1.0, 1.0],
    h: float = 0.03,
    **kwargs,
) -> np.ndarray:
    """Lorenz attractor timeseries [6]_ [7]_:

    .. math::

        \\frac{dx}{dt} &= \\sigma (y-x) \\\\
        \\frac{dy}{dt} &= x(\\rho - z) - y \\\\
        \\frac{dz}{dt} &= xy - \\beta z

    Parameters
    ----------
    n_timesteps : int
        Number of timesteps to generate.
    rho : float, default to 28.0
        :math:`\\rho` parameter of the system.
    sigma : float, default to 10.0
        :math:`\\sigma` parameter of the system.
    beta : float, default to 8/3
        :math:`\\beta` parameter of the system.
    x0 : array-like of shape (3,), default to [1.0, 1.0, 1.0]
        Initial conditions of the system.
    h : float, default to 0.03
        Time delta between two discrete timesteps.
    **kwargs:
        Other parameters to pass to the `scipy.integrate.solve_ivp`
        solver.

    Returns
    -------
    array of shape (n_timesteps, 3)
        Lorenz attractor timeseries.

    References
    ----------
    .. [6] E. N. Lorenz, ‘Deterministic Nonperiodic Flow’,
           Journal of the Atmospheric Sciences, vol. 20, no. 2,
           pp. 130–141, Mar. 1963,
           doi: 10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2.

    .. [7] `Lorenz system <https://en.wikipedia.org/wiki/Lorenz_system>`_
           on Wikipedia.
    """

    def lorenz_diff(t, state):
        x, y, z = state
        return sigma * (y - x), x * (rho - z) - y, x * y - beta * z

    t_eval = np.arange(0.0, n_timesteps * h, h)

    sol = solve_ivp(
        lorenz_diff, y0=x0, t_span=(0.0, n_timesteps * h), t_eval=t_eval, **kwargs
    )

    return sol.y.T


def mackey_glass(
    n_timesteps: int,
    tau: int = 17,
    a: float = 0.2,
    b: float = 0.1,
    n: int = 10,
    x0: float = 1.2,
    h: float = 1.0,
    seed: Union[int, RandomState, Generator] = None,
) -> np.ndarray:
    """Mackey-Glass timeseries [8]_ [9]_, computed from the Mackey-Glass
    delayed differential equation:

    .. math::

        \\frac{x}{t} = \\frac{ax(t-\\tau)}{1+x(t-\\tau)^n} - bx(t)

    Parameters
    ----------
    n_timesteps : int
        Number of timesteps to compute.
    tau : int, default to 17
        Time delay :math:`\\tau` of Mackey-Glass equation.
        By defaults, equals to 17. Other values can
        change the choatic behaviour of the timeseries.
    a : float, default to 0.2
        :math:`a` parameter of the equation.
    b : float, default to 0.1
        :math:`b` parameter of the equation.
    n : int, default to 10
        :math:`n` parameter of the equation.
    x0 : float, optional, default to 1.2
        Initial condition of the timeseries.
    h : float, default to 1.0
        Time delta between two discrete timesteps.
    seed : int or :py:class:`numpy.random.Generator`, optional
        Random state seed for reproducibility.

    Returns
    -------
    array of shape (n_timesteps, 1)
        Mackey-Glass timeseries.

    Note
    ----
        As Mackey-Glass is defined by delayed time differential equations,
        the first timesteps of the timeseries can't be initialized at 0
        (otherwise, the first steps of computation involving these
        not-computed-yet-timesteps would yield inconsistent results).
        A random number generator is therefore used to produce random
        initial timesteps based on the value of the initial condition
        passed as parameter. A default seed is hard-coded to ensure
        reproducibility in any case. It can be changed with the
        :py:func:`set_seed` function.

    References
    ----------
    .. [8] M. C. Mackey and L. Glass, ‘Oscillation and chaos in
           physiological
           control systems’, Science, vol. 197, no. 4300, pp. 287–289,
           Jul. 1977,
           doi: 10.1126/science.267326.

    .. [9] `Mackey-Glass equations
            <https://en.wikipedia.org/wiki/Mackey-Glass_equations>`_
            on Wikipedia.

    """
    # a random state is needed as the method used to discretize
    # the timeseries needs to use randomly generated initial steps
    # based on the initial condition passed as parameter.
    if seed is None:
        seed = get_seed()

    rs = rand_generator(seed)

    # generate random first step based on the value
    # of the initial condition
    history_length = int(np.floor(tau / h))
    history = collections.deque(
        x0 * np.ones(history_length) + 0.2 * (rs.random(history_length) - 0.5)
    )
    xt = x0

    X = np.zeros(n_timesteps)

    for i in range(0, n_timesteps):
        X[i] = xt

        if tau == 0:
            xtau = 0.0
        else:
            xtau = history.popleft()
            history.append(xt)

        xth = _mg_rk4(xt, xtau, a=a, b=b, n=n)

        xt = xth

    return X.reshape(-1, 1)


def multiscroll(
    n_timesteps: int,
    a: float = 40.0,
    b: float = 3.0,
    c: float = 28.0,
    x0: Union[list, np.ndarray] = [-0.1, 0.5, -0.6],
    h: float = 0.01,
) -> np.ndarray:
    """Double scroll attractor timeseries [10]_ [11]_,
    a particular case of multiscroll attractor timeseries.

    .. math::

        \\frac{dx}{dt} &= a(y - x) \\\\
        \\frac{dy}{dt} &= (c - a)x - xz + cy \\\\
        \\frac{dz}{dt} &= xy - bz

    Parameters
    ----------
    n_timesteps : int
        Number of timesteps to generate.
    a : float, default to 40.0
        :math:`a` parameter of the system.
    b : float, default to 3.0
        :math:`b` parameter of the system.
    c : float, default to 28.0
        :math:`c` parameter of the system.
    x0 : array-like of shape (3,), default to [-0.1, 0.5, -0.6]
        Initial conditions of the system.
    h : float, default to 0.01
        Time delta between two discrete timesteps.

    Returns
    -------
    array of shape (n_timesteps, 3)
        Multiscroll attractor timeseries.

    References
    ----------
    .. [10] G. Chen and T. Ueta, ‘Yet another chaotic attractor’,
           Int. J. Bifurcation Chaos, vol. 09, no. 07, pp. 1465–1466,
           Jul. 1999, doi: 10.1142/S0218127499001024.

    .. [11] `Chen double scroll attractor
           <https://en.wikipedia.org/wiki/Multiscroll_attractor
           #Chen_attractor>`_
           on Wikipedia.

    """

    def multiscroll_diff(t, state):
        x, y, z = state
        dx = a * (y - x)
        dy = (c - a) * x - x * z + c * y
        dz = x * y - b * z
        return dx, dy, dz

    t = np.arange(0.0, n_timesteps * h, h)

    sol = solve_ivp(
        multiscroll_diff, y0=x0, t_span=(0.0, n_timesteps * h), dense_output=True
    )

    return sol.sol(t).T


def doublescroll(
    n_timesteps: int,
    r1: float = 1.2,
    r2: float = 3.44,
    r4: float = 0.193,
    ir: float = 2 * 2.25e-5,
    beta: float = 11.6,
    x0: Union[list, np.ndarray] = [0.37926545, 0.058339, -0.08167691],
    h: float = 0.25,
    **kwargs,
) -> np.ndarray:
    """Double scroll attractor timeseries [10]_ [11]_,
    a particular case of multiscroll attractor timeseries.

    .. math::

        \\frac{dV_1}{dt} &= \\frac{V_1}{R_1} - \\frac{\\Delta V}{R_2} -
        2I_r \\sinh(\\beta\\Delta V) \\\\
        \\frac{dV_2}{dt} &= \\frac{\\Delta V}{R_2} +2I_r \\sinh(\\beta\\Delta V) - I\\\\
        \\frac{dI}{dt} &= V_2 - R_4 I

    where :math:`\\Delta V = V_1 - V_2`.

    Parameters
    ----------
    n_timesteps : int
        Number of timesteps to generate.
    r1 : float, default to 1.2
        :math:`R_1` parameter of the system.
    r2 : float, default to 3.44
        :math:`R_2` parameter of the system.
    r4 : float, default to 0.193
        :math:`R_4` parameter of the system.
    ir : float, default to 2*2e.25e-5
        :math:`I_r` parameter of the system.
    beta : float, default to 11.6
        :math:`\\beta` parameter of the system.
    x0 : array-like of shape (3,), default to [0.37926545, 0.058339, -0.08167691]
        Initial conditions of the system.
    h : float, default to 0.01
        Time delta between two discrete timesteps.

    Returns
    -------
    array of shape (n_timesteps, 3)
        Multiscroll attractor timeseries.

    References
    ----------
    .. [10] G. Chen and T. Ueta, ‘Yet another chaotic attractor’,
           Int. J. Bifurcation Chaos, vol. 09, no. 07, pp. 1465–1466,
           Jul. 1999, doi: 10.1142/S0218127499001024.

    .. [11] `Chen double scroll attractor
           <https://en.wikipedia.org/wiki/Multiscroll_attractor
           #Chen_attractor>`_
           on Wikipedia.
    """

    def doublescroll(t, state):
        V1, V2, i = state

        dV = V1 - V2
        factor = (dV / r2) + ir * np.sinh(beta * dV)
        dV1 = (V1 / r1) - factor
        dV2 = factor - i
        dI = V2 - r4 * i

        return dV1, dV2, dI

    t_eval = np.arange(0.0, n_timesteps * h, h)

    sol = solve_ivp(
        doublescroll, y0=x0, t_span=(0.0, n_timesteps * h), t_eval=t_eval, **kwargs
    )

    return sol.y.T


def rabinovich_fabrikant(
    n_timesteps: int,
    alpha: float = 1.1,
    gamma: float = 0.89,
    x0: Union[list, np.ndarray] = [-1, 0, 0.5],
    h: float = 0.05,
    **kwargs,
) -> np.ndarray:
    """Rabinovitch-Fabrikant system [12]_ [13]_ timeseries.

    .. math::

        \\frac{dx}{dt} &= y(z - 1 + x^2) + \\gamma x \\\\
        \\frac{dy}{dt} &= x(3z + 1 - x^2) + \\gamma y \\\\
        \\frac{dz}{dt} &= -2z(\\alpha + xy)

    Parameters
    ----------
    n_timesteps : int
        Number of timesteps to generate.
    alpha : float, default to 1.1
        :math:`\\alpha` parameter of the system.
    gamma : float, default to 0.89
        :math:`\\gamma` parameter of the system.
    x0 : array-like of shape (3,), default to [-1, 0, 0.5]
        Initial conditions of the system.
    h : float, default to 0.05
        Time delta between two discrete timesteps.
    **kwargs:
        Other parameters to pass to the `scipy.integrate.solve_ivp`
        solver.

    Returns
    -------
    array of shape (n_timesteps, 3)
        Rabinovitch-Fabrikant system timeseries.

    References
    ----------
    .. [12] M. I. Rabinovich and A. L. Fabrikant,
           ‘Stochastic self-modulation of waves in
           nonequilibrium media’, p. 8, 1979.

    .. [13] `Rabinovich-Fabrikant equations
           <https://en.wikipedia.org/wiki/Rabinovich%E2%80
           %93Fabrikant_equations>`_
           on Wikipedia.

    """

    def rabinovich_fabrikant_diff(t, state):
        x, y, z = state
        dx = y * (z - 1 + x**2) + gamma * x
        dy = x * (3 * z + 1 - x**2) + gamma * y
        dz = -2 * z * (alpha + x * y)
        return dx, dy, dz

    t_eval = np.arange(0.0, n_timesteps * h, h)

    sol = solve_ivp(
        rabinovich_fabrikant_diff,
        y0=x0,
        t_span=(0.0, n_timesteps * h),
        t_eval=t_eval,
        **kwargs,
    )

    return sol.y.T


def narma(
    n_timesteps: int,
    order: int = 30,
    a1: float = 0.2,
    a2: float = 0.04,
    b: float = 1.5,
    c: float = 0.001,
    x0: Union[list, np.ndarray] = [0.0],
    seed: Union[int, RandomState] = None,
):
    """Non-linear Autoregressive Moving Average (NARMA) timeseries,
    as first defined in [14]_, and as used in [15]_.

    NARMA n-th order dynamical system is defined by the recurrent relation:

    .. math::

        y[t+1] = a_1 y[t] + a_2 y[t] (\\sum_{i=0}^{n-1} y[t-i]) + b u[t-(
        n-1)]u[t] + c

    where :math:`u[t]` are sampled following a uniform distribution in
    :math:`[0, 0.5]`.

    Parameters
    ----------
    n_timesteps : int
        Number of timesteps to generate.
    order: int, default to 30
        Order of the system.
    a1 : float, default to 0.2
        :math:`a_1` parameter of the system.
    a2 : float, default ot 0.04
        :math:`a_2` parameter of the system.
    b : float, default to 1.5
        :math:`b` parameter of the system.
    c : float, default to 0.001
        :math:`c` parameter of the system.
    x0 : array-like of shape (init_steps,), default to [0.0]
        Initial conditions of the system.
    seed : int or :py:class:`numpy.random.Generator`, optional
        Random state seed for reproducibility.

    Returns
    -------
    array of shape (n_timesteps, 1)
        NARMA timeseries.

    References
    ----------
    .. [14] A. F. Atiya and A. G. Parlos, ‘New results on recurrent
           network training: unifying the algorithms and accelerating
           convergence,‘ in IEEE Transactions on Neural Networks,
           vol. 11, no. 3, pp. 697-709, May 2000,
           doi: 10.1109/72.846741.

    .. [15] B.Schrauwen, M. Wardermann, D. Verstraeten, J. Steil,
           D. Stroobandt, ‘Improving reservoirs using intrinsic
           plasticity‘,
           Neurocomputing, 71. 1159-1171, 2008,
           doi: 10.1016/j.neucom.2007.12.020.
    """
    if seed is None:
        seed = get_seed()
    rs = rand_generator(seed)

    y = np.zeros((n_timesteps + order, 1))

    x0 = check_vector(np.atleast_2d(np.asarray(x0)))
    y[: x0.shape[0], :] = x0

    noise = rs.uniform(0, 0.5, size=(n_timesteps + order, 1))
    for t in range(order, n_timesteps + order - 1):
        y[t + 1] = (
            a1 * y[t]
            + a2 * y[t] * np.sum(y[t - order : t])
            + b * noise[t - order] * noise[t]
            + c
        )
    return y[order:, :]
