#include <cmath>
#include <stdio.h>

#define PI 3.1415926535897932384626




// highest degree term comes first (where the highest term is c[0] and constant term is c[n])
double evalPolynomial(const double *c, int N, double t) {
	double r = c[0];
	for (int i = 1; i <= N; i++) r = r * t + c[i];
	return r;
}



// Polynomial Regression
// It is not recommand to fit a polynomial with degree higher than 8 since they often have high computing error

#pragma region Polynomial Fitting Macros

// Try to study the property of the matrix and find a better way to solve
// M[i][j] = 1/k (bᵏ-aᵏ), k = 2N-(i+j)+1, zero-indexed
// M[i][j] = ∑ᵢ xᵢ^(2N-i-j)

#define InitMat \
	double *Mat = new double[L*L]; \
	for (int i = 0; i < L; i++) for (int j = 0; j < L; j++) Mat[i*L + j] = sumxn[2 * N - i - j]; \
	for (int i = 0; i < L; i++) c[i] = sumxny[N - i]; \
	delete sumxn, sumxny;

#define Eliminate \
	for (int i = 0; i < L; i++) for (int j = i + 1; j < L; j++) { \
		double d = Mat[j*L + i] / Mat[i*L + i]; \
		for (int k = i; k < L; k++) Mat[j*L + k] -= Mat[i*L + k] * d; \
		c[j] -= c[i] * d; \
	} \
	for (int i = L - 1; i >= 0; i--) for (int j = i - 1; j >= 0; j--) { \
		double d = Mat[j*L + i] / Mat[i*L + i]; \
		for (int k = L - 1; k >= i; k--) Mat[j*L + k] -= Mat[i*L + k] * d; \
		c[j] -= c[i] * d; \
	} \
	for (int i = 0; i < L; i++) c[i] /= Mat[i*L + i]; \
	delete Mat;

#define CalcError(x_i_, dif_x_) \
	double E = 0, MaxE = 0; \
	for (int i = 0; i <= n; i++) { \
		x = x_i_, xp = i & 1 ? 4.0 : 2.0; \
		xp = dif_x_; xp *= xp; \
		E += (i == 0 || i == n ? 1.0 : i & 1 ? 4.0 : 2.0) * xp; \
		if (xp > MaxE) MaxE = xp; \
	} \
	if (RMSE) *RMSE = sqrt(E / (3 * n)); \
	if (ERR) *ERR = sqrt(MaxE);

#pragma endregion Repeated part of fitPolynomial functions

// fit to data set
void fitPolynomial(double *x, double *y, int n, double *c, int N) {
	int L = N + 1;
	double *sumxn = new double[2 * N + 1], *sumxny = new double[L];
	for (int i = 0; i <= 2 * N; i++) sumxn[i] = 0;
	for (int i = 0; i < L; i++) sumxny[i] = 0;
	for (int i = 0, j; i < n; i++) {
		double t;
		for (j = 0, t = 1.0; j <= 2 * N; j++) sumxn[j] += t, t *= x[i];
		for (j = 0, t = 1.0; j <= N; j++) sumxny[j] += t * y[i], t *= x[i];
	}
	InitMat;
	Eliminate;
}

// fit a function in interval [x0,x1], where dif is the sample in numerical integration
void fitPolynomial(double(*f)(double), double x0, double x1, int dif, double *c, int N, double *RMSE, double *ERR) {
	int L = N + 1;
	double *sumxn = new double[2 * N + 1], *sumxny = new double[L];  // or intxn, intxny
	for (int d = 0; d <= 2 * N; d++) sumxn[d] = (pow(x1, d + 1) - pow(x0, d + 1)) / (d + 1);

	// numerical integration
	int n = dif * 2;
	double u = (x1 - x0) / n, x, xp;
	for (int d = 0; d < L; d++) sumxny[d] = 0;
	for (int i = 0; i <= n; i++) {
		x = x0 + u * i, xp = i == 0 || i == n ? 1.0 : i & 1 ? 4.0 : 2.0;
		for (int d = 0; d < L; d++) sumxny[d] += xp * f(x), xp *= x;
	}
	for (int d = 0; d < L; d++) sumxny[d] *= u / 3;

	InitMat;
	Eliminate;

	// calculate error - spend time!
	if (RMSE || ERR) { CalcError(x0 + u * i, evalPolynomial(c, N, x) - f(x)); }
}

// fit a function in interval [0,x1], force the constant term of the polynomial to be 0
void fitPolynomial(double(*f)(double), double x1, int dif, double *c, int N, double *RMSE, double *ERR) {
	// much copied from the previous function
	int L = N + 1, n = dif * 2;
	double *sumxn = new double[2 * N + 1], *sumxny = new double[L];
	for (int d = 0; d <= 2 * N; d++) sumxn[d] = pow(x1, d + 1) / (d + 1);
	double u = x1 / n, x, xp;
	for (int d = 0; d < L; d++) sumxny[d] = 0;
	for (int i = 0; i <= n; i++) {
		x = u * i, xp = i == 0 || i == n ? 1.0 : i & 1 ? 4.0 : 2.0;
		for (int d = 0; d < L; d++) sumxny[d] += xp * f(x), xp *= x;
	}
	for (int d = 0; d < L; d++) sumxny[d] *= u / 3;

	// a lazy approach, only this part is different from the previous function
	InitMat;
	for (int i = 0; i < N; i++) Mat[i*L + N] = Mat[N*L + i] = 0;
	c[N] = 1;
	Eliminate;
	c[N] = 0;

	// calculate error - spend time!
	if (RMSE || ERR) { CalcError(u * i, evalPolynomial(c, N, x) - f(x)); }
}


// find the polynomial of best fit c(x) such that c[k(x)] ≈ f(x)
void fitPolynomial(double(*f)(double), double(*k)(double), double x0, double x1, int dif, double *c, int N, double *RMSE, double *ERR) {
	// It is best to integrate analytically if the interval contains indifferentiable point
	int L = N + 1, n = dif * 2;
	double u = (x1 - x0) / n, x, kx, xp;
	double *sumxn = new double[2 * N + 1], *sumxny = new double[L];

	// sumxn[i] = Integral[u(x)ⁱ,x0,x1]
	for (int d = 0; d <= 2 * N; d++) sumxn[d] = 0;
	for (int i = 0; i <= n; i++) {
		x = x0 + u * i, kx = k(x), xp = i == 0 || i == n ? 1.0 : i & 1 ? 4.0 : 2.0;
		for (int d = 0; d <= 2 * N; d++) sumxn[d] += xp, xp *= kx;
	}
	for (int d = 0; d <= 2 * N; d++) sumxn[d] *= u / 3;

	// sumxny[i] = Integral[f(x)·u(x)ⁱ,x0,x1]
	for (int d = 0; d < L; d++) sumxny[d] = 0;
	for (int i = 0; i <= n; i++) {
		x = x0 + u * i, kx = k(x), xp = (i == 0 || i == n ? 1.0 : i & 1 ? 4.0 : 2.0) * f(x);
		for (int d = 0; d < L; d++) sumxny[d] += xp, xp *= kx;
	}
	for (int d = 0; d < L; d++) sumxny[d] *= u / 3;

	InitMat;
	Eliminate;

	// calculate error - spend time!
	if (RMSE || ERR) { CalcError(x0 + u * i, evalPolynomial(c, N, k(x)) - f(x)); }
}


#undef InitMat
#undef Eliminate
#undef CalcError




void printPolynomial(const double *c, int N, const char var[] = "x") {
	if (N < 1) { printf("%.12lf\n", c[0]); return; }
	for (int i = 1; i < N; i++) putchar('(');
	printf("%.12lf*%s", c[0], var);
	for (int i = 1; i < N; i++) printf("%+.12lf)*%s", c[i], var);
	if (c[N] != 0.0) printf("%+.12lf", c[N]);
	printf("\n");
}


#include <chrono>


double F(double a) {
	double S = sin(a), C = cos(a);
	double s2 = S * S, c2 = C * C, sc2 = s2 + c2, sc22 = sc2 * sc2;
	a = 1. / (756.*(sc22 + 1.) + 810.*s2 - 1890.*(sc2 + 1.)*C + 2430.*c2);
	double c = (2520.*sc22 + 2736.*s2 + (-507.*sc2 - 6600.*C + 7215.)*C - 2628.) * a,
		b = (3996.*(sc2 + 1.) - 6750.*C)*S * a, d = (3439.*sc2 + 4276.*C - 7715.)*S * a;
	double p = (c - b * b / 3.) / 3., q = -0.5 * ((b*b / 13.5 - c / 3.) * b + d);
	return (a = q * q + p * p * p) > 0.0 ? cbrt(q + sqrt(a)) + cbrt(q - sqrt(a)) - b / 3.
		: 2.0 * pow(q*q - a, 1. / 6.) * cos(atan2(sqrt(-a), q) / 3.) - b / 3.;
}

int main() {
	double c[11];

	auto t0 = std::chrono::high_resolution_clock::now();
	for (int N = 1; N <= 10; N++) {
		double RMSE, ERR;
		fitPolynomial(F, PI / 2, 100000, c, N, &RMSE, &ERR);
		//fitPolynomial([](double x) {return cos(acos(x) / 3); }, [](double x) {return sqrt(x + 1); }, -1, 1, 1000000, c, N, &RMSE, &ERR);
		printf("deg = %d, RMSE = %.2le, ERR = %.2le\n", N, RMSE, ERR);
		printPolynomial(c, N, "u(x)");
	}
	auto t1 = std::chrono::high_resolution_clock::now();
	double time_elapsed = std::chrono::duration<double>(t1 - t0).count();
	printf("\nTime Elapsed: %.3lfs\n", time_elapsed);

	return 0;
}
