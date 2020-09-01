// Polynomial Regression
// Designed to fit functions that are expensive to calculate
// It is not recommended to fit a polynomial with a degree higher than 6 since they often have high computing error


#include <cmath>
#include <stdio.h>

#define PI 3.1415926535897932384626


// highest degree term comes first (where the highest term is P[0] and the constant term is P[n])
double evalPolynomial(const double *P, int N, double x) {
	double r = P[0];
	for (int i = 1; i <= N; i++) r = r * x + P[i];
	return r;
}


// translate a polynomial by (x,y) (x right y up)
void translatePolynomial(double *P, int N, double x, double y) {
	int L = N + 1;
	double *xn = new double[L]; xn[0] = 1;
	for (int i = 1; i < L; i++) xn[i] = -xn[i - 1] * x;
	double *M = new double[L*L];
	for (int i = 0; i < L; i++) M[N*L + i] = M[i*L + i] = 1.0;
	for (int i = N - 1; i > 0; i--) for (int j = N; j > i; j--)
		M[(j - 1)*L + (i - 1)] = M[j*L + i] + M[(j - 1)*L + i];  // Pascal triangle
	for (int i = 0; i < L; i++) for (int j = i; j < L; j++) M[j*L + i] *= xn[j - i] * P[i];
	for (int j = 0; j < L; j++) {
		P[j] = 0;
		for (int i = 0; i <= j; i++) P[j] += M[j*L + i];
	}
	P[N] += y;
	delete xn; delete M;
}

// Gaussian elimination in non-degenerated case
void Eliminate(double* M, double *X, int N) {
	for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++) {
		double d = M[j*N + i] / M[i*N + i];
		for (int k = i; k < N; k++) M[j*N + k] -= M[i*N + k] * d;
		X[j] -= X[i] * d;
	}
	for (int i = N - 1; i >= 0; i--) for (int j = i - 1; j >= 0; j--) {
		double d = M[j*N + i] / M[i*N + i];
		for (int k = N - 1; k >= i; k--) M[j*N + k] -= M[i*N + k] * d;
		X[j] -= X[i] * d;
	}
	for (int i = 0; i < N; i++) X[i] /= M[i*N + i];
}



// repeated parts of the regression function

#define IntVector(intvec, vec_N, x_d_, f_x_) \
	for (int i = 0; i <= vec_N; i++) intvec[i] = 0; \
	for (int d = 0; d <= n; d++) { \
		x = x_d_; xp = (d == 0 || d == n ? 1.0 : d & 1 ? 4.0 : 2.0) * f_x_; \
		for (int i = 0; i <= vec_N; i++) intvec[i] += xp, xp *= x; \
	} \
	for (int i = 0; i <= vec_N; i++) intvec[i] *= u / 3;

#define InitMat \
	double *Mat = new double[L*L]; \
	for (int i = 0; i < L; i++) for (int j = 0; j < L; j++) Mat[i*L + j] = sumxn[2 * N - i - j]; \
	for (int i = 0; i < L; i++) P[i] = sumxny[N - i]; \
	delete sumxn, sumxny;

#define CalcError(x_i_, dif_x_) \
	double E = 0, MaxE = 0; \
	for (int i = 0; i <= n; i++) { \
		x = x_i_; xp = dif_x_; xp *= xp; \
		E += (i == 0 || i == n ? 1.0 : i & 1 ? 4.0 : 2.0) * xp; \
		if (xp > MaxE) MaxE = xp; \
	} \
	if (RMSE) *RMSE = sqrt(E / (3 * n)); \
	if (ERR) *ERR = sqrt(MaxE);



// fit to a data set
void fitDataSet(double *x, double *y, int n, double *P, int N) {
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
	Eliminate(Mat, P, L); delete Mat;
}


// fit a function in interval [x0,x1], where dif is the number of samples in numerical integration
void fitFunction(double(*f)(double), double x0, double x1, int dif, double *P, int N, double *RMSE, double *ERR) {
	int L = N + 1, n = dif * 2;
	double u = (x1 - x0) / n, x, xp;
	double *sumxn = new double[2 * N + 1], *sumxny = new double[L];  // or intxn, intxny

	// sumxn[i] = Integral[xⁱ,x0,x1]
	for (int i = 0; i <= 2 * N; i++) sumxn[i] = (pow(x1, i + 1) - pow(x0, i + 1)) / (i + 1);

	// sumxny[i] = Integral[xⁱ·f(x),x0,x1]
	IntVector(sumxny, N, x0 + u * d, f(x));

	InitMat;
	Eliminate(Mat, P, L); delete Mat;

	// calculate error - spend time!
	if (RMSE || ERR) { CalcError(x0 + u * i, evalPolynomial(P, N, x) - f(x)); }
}

// fit a function in interval [x0,x1] where P(x0)=y0
void fitFunction(double(*f)(double), double x0, double x1, double y0, int dif, double *P, int N, double *RMSE, double *ERR) {
	// transform interval to [0,x1-x0] with P(0)=0
	int L = N + 1, n = dif * 2; x1 -= x0;
	double u = x1 / n, x, xp;
	double *sumxn = new double[2 * N + 1], *sumxny = new double[L];
	for (int i = 0; i <= 2 * N; i++) sumxn[i] = pow(x1, i + 1) / (i + 1);
	IntVector(sumxny, N, u * d, (f(x + x0) - y0));

	// a lazy approach
	InitMat;
	for (int i = 0; i < N; i++) Mat[i*L + N] = Mat[N*L + i] = 0;
	P[N] = 1;
	Eliminate(Mat, P, L); delete Mat;
	translatePolynomial(P, N, x0, y0 - P[N]);

	// calculate error
	if (RMSE || ERR) { CalcError(x0 + u * i, evalPolynomial(P, N, x) - f(x)); }
}


// find the polynomial of best fit P(x) such that P[k(x)] ≈ f(x)
void fitFunctionComp(double(*f)(double), double(*k)(double), double x0, double x1, int dif, double *P, int N, double *RMSE, double *ERR) {
	// It is best to integrate analytically if the interval contains indifferentiable point
	int L = N + 1, n = dif * 2;
	double u = (x1 - x0) / n, x, kx, xp;
	double *sumxn = new double[2 * N + 1], *sumxny = new double[L];

	// sumxn[i] = Integral[k(x)ⁱ,x0,x1]
	IntVector(sumxn, 2 * N, x = k(x0 + u * d), 1.0);

	// sumxny[i] = Integral[f(x)·k(x)ⁱ,x0,x1]
	IntVector(sumxny, N, x = x0 + u * d; kx = k(x), f(x); x = kx);

	InitMat;
	Eliminate(Mat, P, L); delete Mat;

	if (RMSE || ERR) { CalcError(x0 + u * i, evalPolynomial(P, N, k(x)) - f(x)); }
}

// debugging
void fitFunctionComp(double(*f)(double), double(*k)(double), double x0, double x1, double y0, int dif, double *P, int N, double *RMSE, double *ERR) {
	int L = N + 1, n = dif * 2; x1 -= x0;
	double u = x1 / n, x, kx, xp;
	double *sumxn = new double[2 * N + 1], *sumxny = new double[L];

	// sumxn[i] = Integral[k(x)ⁱ,x0,x1]
	IntVector(sumxn, 2 * N, x = k(x0 + u * d), 1.0);

	// sumxny[i] = Integral[f(x)·k(x)ⁱ,x0,x1]
	IntVector(sumxny, N, x = u * d; kx = k(x + x0), (f(x + x0) - y0); x = kx);

	InitMat;
	for (int i = 0; i < N; i++) Mat[i*L + N] = Mat[N*L + i] = 0;
	P[N] = 1;
	Eliminate(Mat, P, L); delete Mat;
	//translatePolynomial(P, N, x0, y0 - P[N]);
	//P[N] += y0 - evalPolynomial(P, N, x0);

	if (RMSE || ERR) { CalcError(x0 + u * i, evalPolynomial(P, N, k(x)) - f(x)); }
}



#undef IntVector
#undef InitMat
#undef CalcError






// ================================== testing code ==================================


#include <chrono>

void printPolynomial(const double *P, int N, const char var[] = "x") {
	if (N < 1) { printf("%.12lf\n", P[0]); return; }
	for (int i = 1; i < N; i++) putchar('(');
	printf("%.12lf*%s", P[0], var);
	for (int i = 1; i < N; i++) printf("%+.12lf)*%s", P[i], var);
	if (P[N] != 0.0) printf("%+.12lf", P[N]);
	printf("\n");
}



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
	for (int N = 1; N <= 8; N++) {
		double RMSE, ERR;
		//fitFunctionComp([](double x) {return cos(acos(x) / 3); }, [](double x) {return sqrt(x + 1); }, -1, 1, 0.5, 1000000, c, N, &RMSE, &ERR);
		fitFunctionComp([](double x) {return sin(acos(x) / 3); }, [](double x) {return sqrt(1 - x) - sqrt(1 + x); }, -1, 1, 0.5*sqrt(3), 1000000, c, N, &RMSE, &ERR);
		printf("deg = %d, RMSE = %.2le, ERR = %.2le\n", N, RMSE, ERR); printPolynomial(c, N, "u(x)");

		//fitFunction([](double x) { return (x + 2)*sqrt(x*x + 1) / sqrt(2); }, -1, 1, 1, 1000000, c, N, &RMSE, &ERR);
		//printf("deg = %d, RMSE = %.2le, ERR = %.2le\np(x)=", N, RMSE, ERR); printPolynomial(c, N);
		//fitFunction(F, 0, 2, 0, 100000, c, N, &RMSE, &ERR);
		//printf("deg = %d, RMSE = %.2le, ERR = %.2le\n", N, RMSE, ERR); printPolynomial(c, N);
		//fitFunction(F, 0, PI / 2, 100000, c, N, &RMSE, &ERR);
		//printf("deg = %d, RMSE = %.2le, ERR = %.2le\n", N, RMSE, ERR); printPolynomial(c, N);
		//fitFunctionComp([](double x) {return cos(acos(x) / 3); }, [](double x) {return sqrt(x + 1); }, -1, 1, 1000000, c, N, &RMSE, &ERR);
		//printf("deg = %d, RMSE = %.2le, ERR = %.2le\n", N, RMSE, ERR); printPolynomial(c, N, "u(x)");
	}
	auto t1 = std::chrono::high_resolution_clock::now();
	double time_elapsed = std::chrono::duration<double>(t1 - t0).count();
	printf("\nTime Elapsed: %.3lfs\n", time_elapsed);

	return 0;
}



