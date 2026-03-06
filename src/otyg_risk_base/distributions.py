import numpy as np
import math
from otyg_risk_base.montecarlo import MonteCarloRange


class PertDistribution:
    def __init__(self, range: MonteCarloRange, samples: int = 100000):
        rng = np.random.default_rng()
        delta_min_max = range.max - range.min
        alpha = 1 + ((range.probable - range.min) * 4) / delta_min_max
        beta = 1 + ((range.max - range.probable) * 4) / delta_min_max
        self.__samples = float(range.min) + rng.beta(alpha, beta, samples) * float(
            delta_min_max
        )

    def get(self):
        return self.__samples.copy()


class LogLogisticDistribution:
    def __init__(
        self,
        range: MonteCarloRange,
        samples: int = 100000,
        upper_quantile: float = 0.99,
    ):
        rng = np.random.default_rng()

        min_value = float(range.min)
        probable_value = float(range.probable)
        max_value = float(range.max)

        eps = np.finfo(float).eps

        if max_value <= min_value:
            self.__samples = np.full(samples, min_value, dtype=float)
            return

        # Shifted log-logistic:
        # X = min_value + Y
        # Y ~ LogLogistic(alpha, beta)
        #
        # Median(X) = min_value + alpha
        alpha = probable_value - min_value
        if alpha <= eps:
            alpha = max((max_value - min_value) * 0.1, eps)

        span_ratio = (max_value - min_value) / alpha

        if span_ratio <= 1.0 + eps:
            beta = 10.0
        else:
            # Q(u) = min_value + alpha * (u / (1-u)) ** (1/beta)
            # Solve Q(upper_quantile) = max_value for beta
            logit_q = math.log(upper_quantile / (1.0 - upper_quantile))
            beta = logit_q / math.log(span_ratio)
            if not np.isfinite(beta) or beta <= 0:
                beta = 10.0

        # Truncate distribution to [min_value, max_value]
        # CDF(max_value) for shifted log-logistic
        f_max = 1.0 / (1.0 + (alpha / (max_value - min_value)) ** beta)

        # Sample uniformly in truncated CDF interval
        u = rng.uniform(low=eps, high=max(f_max - eps, eps), size=samples)

        # Inverse CDF
        self.__samples = min_value + alpha * (u / (1.0 - u)) ** (1.0 / beta)

    def get(self):
        return self.__samples.copy()
