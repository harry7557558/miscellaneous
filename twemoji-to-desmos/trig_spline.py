from pygame import Vector2
import math
import numpy as np
import re


class TrigSpline():
    """Parametric curve defined by trigonometric series"""

    def __init__(self, control_points: list[Vector2]):
        """Calculate the coefficients of the spline based on a list of control points
        Additional info:
            Calculated using the Fast Fourier Transform (FFT) algorithm via NumPy.
            If the number of control points is odd,
            the spline is guaranteed to go through all control points.
        Args:
            control_points: a list of control points
        """
        if len(control_points) == 0:
            control_points = [Vector2(0, 0)]
        n_points = len(control_points)
        x_coords = [p.x for p in control_points]
        y_coords = [p.y for p in control_points]
        x_freqs = np.fft.fft(x_coords)[:(n_points+1)//2] * (2.0/n_points)
        x_freqs[0] = np.real(x_freqs[0]) * 0.5
        y_freqs = np.fft.fft(y_coords)[:(n_points+1)//2] * (2.0/n_points)
        y_freqs[0] = np.real(y_freqs[0]) * 0.5
        self._x_cos = np.real(x_freqs)
        self._x_sin = np.imag(x_freqs)
        self._y_cos = np.real(y_freqs)
        self._y_sin = np.imag(y_freqs)

    def evaluate(self, t: float) -> Vector2:
        """Evaluate the curve at a given parameter value"""
        x_cos = self._x_cos * np.cos(2.0*math.pi*np.arange(len(self._x_cos))*t)
        x_sin = self._x_sin * np.sin(2.0*math.pi*np.arange(len(self._x_sin))*t)
        y_cos = self._y_cos * np.cos(2.0*math.pi*np.arange(len(self._y_cos))*t)
        y_sin = self._y_sin * np.sin(2.0*math.pi*np.arange(len(self._y_sin))*t)
        return Vector2(sum(x_cos)+sum(x_sin), sum(y_cos)+sum(y_sin))

    def evaluate_n(self, n: int) -> list[Vector2]:
        """Evaluate the curve at n points with evenly-spaced parameter values"""
        if n < max(len(self._x_cos), len(self._x_sin), len(self._y_cos), len(self._y_sin)):
            return super().evaluate_n(n)  # O(MN), should be affordable for up to 2000
        # O(NlogN) using FFT
        x_cos = np.zeros(n)
        x_cos[:len(self._x_cos)] = self._x_cos
        x_sin = np.zeros(n)
        x_sin[:len(self._x_sin)] = self._x_sin
        xs = np.real(np.fft.ifft(x_cos+x_sin*1j)) * n
        y_cos = np.zeros(n)
        y_cos[:len(self._y_cos)] = self._y_cos
        y_sin = np.zeros(n)
        y_sin[:len(self._y_sin)] = self._y_sin
        ys = np.real(np.fft.ifft(y_cos+y_sin*1j)) * n
        result = []
        for i in range(n):
            result.append(Vector2(xs[i], ys[i]))
        return result

    def get_magnitude(self) -> float:
        """Return a float number that estimates the size of the shape"""
        x_sum = np.sum(self._x_cos[1:]**2) + np.sum(self._x_sin[1:]**2)
        y_sum = np.sum(self._y_cos[1:]**2) + np.sum(self._y_sin[1:]**2)
        return math.sqrt(0.5*(x_sum+y_sum))

    def count_nonzero(self, epsilon: float = 1e-8) -> int:
        """Count the number of sinusoidal basis with non-zero amplitudes
        Additional info:
            Calculates the number of non-zero sinusoidal basis for each dimension
            and choose the maximum one.
        Args:
            epsilon: a number is considered zero if its absolute value is less than this number.
        Returns:
            the number of non-zero sinusoidal basis.
        """
        x_cos_n = np.count_nonzero(abs(self._x_cos) >= epsilon)
        x_sin_n = np.count_nonzero(abs(self._x_sin) >= epsilon)
        y_cos_n = np.count_nonzero(abs(self._y_cos) >= epsilon)
        y_sin_n = np.count_nonzero(abs(self._y_sin) >= epsilon)
        return max(x_cos_n+x_sin_n, y_cos_n+y_sin_n)

    def is_degenerated(self, epsilon: float = 1e-8) -> bool:
        """Test if this curve is degenerated, or, shrinks at one point
        Args:
            epsilon: two values will be considered equal if their difference is less than this
        Returns:
            True if it is degenerated, False if not
        """
        for arr in [self._x_cos, self._x_sin, self._y_cos, self._y_sin]:
            if len(arr) > 0 and np.any(abs(arr[1:]) >= epsilon):
                return True
        return False

    def filter_lowest(self, n_waves: int) -> "TrigSpline":
        """Filter frequencies, keep lowest frequencies
        Args:
            n_waves: the number of sinusoidal basis to keep, same for both dimensions
        Returns:
            a trigonometric spline that keeps waves of the lowest n_waves frequencies
        """
        if not n_waves > 0:
            raise ValueError("Number of waves must be positive.")
        result = TrigSpline([Vector2(0, 0)])
        result._x_cos, result._x_sin = self._filter_lowest_dim(
            self._x_cos, self._x_sin, n_waves)
        result._y_cos, result._y_sin = self._filter_lowest_dim(
            self._y_cos, self._y_sin, n_waves)
        return result

    def filter_greatest(self, n_waves: int) -> "TrigSpline":
        """Filter frequencies, keep greatest amplitudes
        Args:
            n_waves: the number of sinusoidal waves to keep, same for both dimensions
        Returns:
            a trigonometric spline that keeps waves of the greatest n_waves amplitudes
        """
        if not n_waves > 0:
            raise ValueError("Number of waves must be positive.")
        result = TrigSpline([Vector2(0, 0)])
        result._x_cos, result._x_sin = self._filter_greatest_dim(
            self._x_cos, self._x_sin, n_waves)
        result._y_cos, result._y_sin = self._filter_greatest_dim(
            self._y_cos, self._y_sin, n_waves)
        return result

    @staticmethod
    def _filter_lowest_dim(a_cos: list[float], a_sin: list[float], n_waves: int) -> tuple[list[float], list[float]]:
        """Filter frequencies in one dimension, keep lowest frequencies
        Args:
            a_cos: the amplitudes of cosine waves of frequencies
            a_sin: the amplitudes of sine waves of frequencies, frequency 0 must be zero
            n_waves: the number of sinusoidal basis to keep
        Returns:
            a tuple of filtered cosine and sine waves
        """
        r_cos = [a_cos[0]]
        r_sin = [0.0]
        for i in range(1, n_waves):
            k = (i - 1) // 2 + 1
            if i % 2 == 1:
                r_cos.append(a_cos[k] if k < len(a_cos) else 0.0)
            else:
                r_sin.append(a_sin[k] if k < len(a_sin) else 0.0)
        return (np.array(r_cos), np.array(r_sin))

    @staticmethod
    def _filter_greatest_dim(a_cos: list[float], a_sin: list[float], n_waves: int) -> tuple[list[float], list[float]]:
        """Filter frequencies in one dimension, keep greatest amplitudes
        Args:
            a_cos: the amplitudes of cosine waves of frequencies
            a_sin: the amplitudes of sine waves of frequencies
            n_waves: the number of sinusoidal basis to keep
        Returns:
            a tuple of filtered cosine and sine waves
        """
        if n_waves >= len(a_cos) + len(a_sin) - 1:
            return (a_cos[:], a_sin[:])
        # convert waves to a list of tuples of indices and amplitudes
        # non-negative indices for cosine, negative indices for sine
        waves = []
        for k in range(len(a_cos)):
            waves.append((k, a_cos[k]))
        for k in range(1, len(a_sin)):
            waves.append((-k, a_sin[k]))
        # selection sort, terminate when finds n greatest amplitudes
        for j in range(n_waves):
            largest_i = j
            for i in range(j+1, len(waves)):
                if abs(waves[i][1]) > abs(waves[largest_i][1]):
                    largest_i = i
            temp = waves[j]
            waves[j] = waves[largest_i]
            waves[largest_i] = temp
        # convert them back to arrays
        r_cos = []
        r_sin = []
        for i in range(n_waves):
            k, amp = waves[i]
            if k >= 0:
                while len(r_cos) <= k:
                    r_cos.append(0.0)
                r_cos[k] = amp
            else:
                while len(r_sin) <= -k:
                    r_sin.append(0.0)
                r_sin[-k] = amp
        return (np.array(r_cos), np.array(r_sin))

    def get_latex(self, digits=4, optimize=False) -> str:
        """Get the LateX of the curve to be exported to Desmos
        Args:
            digits: the number of significant digits of the greatest amplitude,
                    if it has a decimal point.
                    (each amplitude has equal number of decimal places)
            minimize: whether minimize the latex string
        Returns:
            a string of LaTeX that is compatible with Desmos
        """
        latex_x = TrigSpline._get_latex_dim(
            self._x_cos, self._x_sin, digits, optimize)
        latex_y = TrigSpline._get_latex_dim(
            self._y_cos, self._y_sin, digits, optimize)
        bracket_l = "(" if optimize else "\\left("
        bracket_r = ")" if optimize else "\\right)"
        return bracket_l + latex_x + ',' + latex_y + bracket_r

    @staticmethod
    def _get_latex_dim(a_cos: list[float], a_sin: list[float], digits, optimize) -> str:
        """Get the LateX of the curve to be exported to Desmos, in one dimension"""
        max_val = max(
            0.0 if len(a_cos) <= 1 else max(np.abs(a_cos[1:])),
            0.0 if len(a_sin) <= 1 else max(np.abs(a_sin[1:]))
        )
        if max_val == 0.0:
            return "0"
        decimals = max(digits - (int(math.ceil(math.log10(max_val)))), 0)
        bracket_l = "(" if optimize else "\\left("
        bracket_r = ")" if optimize else "\\right)"
        s = ""
        for k in range(max(len(a_cos), len(a_sin))):
            kt = str(k) + 't'
            a = a_cos[k] if k < len(a_cos) else 0.0
            b = a_sin[k] if k < len(a_sin) else 0.0
            a = TrigSpline._float_to_str(a, decimals, optimize)
            b = TrigSpline._float_to_str(b, decimals, optimize)
            if kt == "0t":
                if a != "+0":
                    s += a
            else:
                if kt == "1t":
                    kt = "t"
                if a in ["+1", "-1"]:
                    a = a[0]
                if b in ["+1", "-1"]:
                    b = b[0]
                if float(a) != 0.0:
                    s += a + "\\cos" + bracket_l + kt + bracket_r
                if float(b) != 0.0:
                    s += b + "\\sin" + bracket_l + kt + bracket_r
        return s.lstrip('+')
