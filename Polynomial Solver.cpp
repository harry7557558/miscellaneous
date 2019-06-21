#pragma once

#include <cmath>
using namespace std;

// linear congruence method producing random float value
extern double RAND_LCG_DV = 0.36787944117;	// random number seed
#define RAND_LCG_TMS 13.35717028437795
#define RAND_LCG_ADD 0.841470984807897
inline double pick_random(double max) {
	RAND_LCG_DV = fmod(RAND_LCG_DV * RAND_LCG_TMS + RAND_LCG_ADD, max);
	return RAND_LCG_DV;
}
inline double pick_random(double min, double max) {
	RAND_LCG_DV = fmod(RAND_LCG_DV * RAND_LCG_TMS + RAND_LCG_ADD, max - min);
	return RAND_LCG_DV + min;
}

#define ERR_EPSILON_SN 1e-10
#define ERR_ZETA_SN 1e-8
#define ERR_ETA_SN 1e-6


#include <iostream>
#include <iomanip>
#include <chrono>
typedef chrono::high_resolution_clock NTime;
typedef chrono::duration<double> fsec;

// Solve equation ax^3+bx^2+cx+d=0 with Cardano formula
// return 1: two or three real roots, r, u, v;
// return 0: one real root r and two complex roots u+vi, u-vi;
bool solveCubic(double a, double b, double c, double d, double &r, double &u, double &v) {
	b /= a, c /= a, d /= a;		// now a=1
	double p = c - b * b / 3, q = (b*b / 13.5 - c / 3) * b + d;		// => t^3+pt+q=0, x=t-b/3
	b /= 3, p /= 3, q /= -2; a = q * q + p * p * p;
	if (a > 0) {
		a = sqrt(a);
		//u = cbrt(q + a), v = cbrt(q - a);
		u = q + a; u = u > 0 ? pow(u, 1. / 3) : -pow(-u, 1. / 3);
		v = q - a; v = v > 0 ? pow(v, 1. / 3) : -pow(-v, 1. / 3);
		r = u + v;
		v = sqrt(0.75)*(u - v);
		u = -0.5 * r - b, r -= b;
		return 0;
	}
	else {
		a = -a; c = pow(q*q + a, 1.0 / 6);
		a = sqrt(a); u = atan2(a, q) / 3;
		d = c * sin(u), c *= cos(u);
		r = 2 * c - b;
		c = -c, d *= sqrt(3);
		u = c - d - b, v = u + 2 * d;
		return 1;
	}
}


// Four real roots
void solveQuartic(double a, double b, double c, double d, double e, double &r1, double &r2, double &r3, double &r4) {
	r1 = r2 = r3 = r4 = NAN;
	b /= a, c /= a, d /= a, e /= a;
	double x = 0, dx;
	double a_ = 4, b_ = 3 * b, c_ = 2 * c, d_ = d;
	double r, u, v;
	if (solveCubic(a_, b_, c_, d_, r, u, v)) {
		double mi = u < v ? u : v, ma = u > v ? u : v;
		mi = mi < r ? mi : r, ma = ma > r ? ma : r;	// two minimas
		if ((((mi + b)*mi + c)*mi + d)*mi + e > 0 && (((ma + b)*ma + c)*ma + d)*ma + e > 0) return;
	}
	else {
		if ((((r + b)*r + c)*r + d)*r + e > 0) return;	// one minima with value greate 0
	}
	x = -0.25*b;	// fourth derivative equals to zero (Note that this is not always the best point, sometimes trig extreme point
	unsigned n = 0, lim = 60; do {
		if (n > lim && dx > 0.01) x = pick_random(-2, 2) - 0.25*b, n -= 60, lim++;
		u = (((x + b)*x + c)*x + d)*x + e, v = ((a_*x + b_)*x + c_)*x + d_;
		dx = u / v; x -= dx;
	} while (abs(dx) > ERR_EPSILON_SN && ++n < 120);		// finding one root x using Newton's method
	//if (n >= 120) return;		// test shows this situation mostly occurs when no solution, but its minima shows it has solution (negative number with extreme small absolute value)
	r1 = x;
	c_ = b + x, d_ = x * c_ + c, e = x * d_ + d, d = d_, c = c_, b = 1, a = 0;	// Euclid division
	if (!solveCubic(b, c, d, e, r2, r3, r4)) r3 = r4 = NAN;
	return;
}


// Five real roots
void solveQuintic(double a, double b, double c, double d, double e, double f, double &r1, double &r2, double &r3, double &r4, double &r5) {
	// Note: try Halley's method https://en.wikipedia.org/wiki/Halley%27s_method  Cubic convergence, but more ratio of failture  Also https://en.wikipedia.org/wiki/Householder%27s_method
	r1 = r2 = r3 = r4 = r5 = NAN;
	b /= a, c /= a, d /= a, e /= a, f /= a, a = 1;
	double x = -0.2*b, u, v, dx;
	double a_ = 5, b_ = 4 * b, c_ = 3 * c, d_ = 2 * d, e_ = e;
	unsigned n = 0, lim = 1000; do {
		if (n > lim && dx > 0.01) x = pick_random(-2, 2) - 0.2*b, n -= 60, lim++;	// In random-value test: 0.008% fail, average 1.4μs elapsed; switch 1000/2000 to 60/120 reaches an average elapsed time of 1.1μs but 0.10% fail
		// Failture mostly occurs on functions with a root with extreme large absolute value and an extremum with small absolute value. Its solution would be the large root and two small numbers. I don't know why. (There're a few exceptions)
		u = ((((a*x + b)*x + c)*x + d)*x + e)*x + f, v = (((a_*x + b_)*x + c_)*x + d_)*x + e_;
		dx = u / v; x -= dx;
	} while (abs(dx) > ERR_EPSILON_SN && ++n < 2000);
	//if (n >= 2000) return;
	r1 = x;
	c_ = b + x, d_ = x * c_ + c, e_ = x * d_ + d, f = x * e_ + e, e = e_, d = d_, c = c_, b = 1, a = 0;
	solveQuartic(b, c, d, e, f, r2, r3, r4, r5);
}


// All real roots, may be low efficiency
void solvePolynomial(const double* C, double* r, unsigned N) {
	cout << noshowpos << C[0] << "*x^" << N;
	for (int i = 1; i < N - 1; i++) cout << showpos << C[i] << "*x^" << (N - i);
	cout << C[N - 1] << "*x" << C[N] << endl << endl;

	for (int i = 0; i < N; i++) r[i] = NAN;
	double *c = new double[N + 1];
	for (int i = 0; i <= N; i++) c[i] = C[i];
	while (c[0] == 0 && N != 0) {
		for (int i = 0; i < N; i++) c[i] = c[i + 1]; N--;
	}

	// solve analytically
	if (N == 0) return;
	if (N == 1) {
		r[0] = -c[1] / c[0]; return;
	}
	if (N == 2) {
		double delta = c[1] * c[1] - 4 * c[0] * c[2];
		if (delta < 0) return;
		delta = sqrt(delta); r[0] = (delta - c[1]) / (2 * c[0]), r[1] = (-delta - c[1]) / (2 * c[0]);
		return;
	}
	if (N == 3) {
		if (solveCubic(c[0], c[1], c[2], c[3], r[0], r[1], r[2])) return;
		else { r[1] = r[2] = NAN; return; }
	}

	for (int i = 1; i <= N; i++) c[N] /= c[0]; c[0] = 1;
	double x = c[1] / N, u, v, dx;
	double *c_ = new double[N]; for (int i = 0; i < N; i++) c_[i] = (N - i) * c[i];
	auto eval = [](double *c, unsigned N, double x) -> double {
		double r = 0;
		for (int i = 0; i <= N; i++) r *= x, r += c[i];
		return r;
	};
	if (!(N & 1)) {	// probably no solution
		unsigned n = 0, lim = 20; do {
			if (++n > lim && dx > 0.01) {
				// check the existence of solutions
				solvePolynomial(c_, r, N - 1);	// extremes
				for (int i = 0; i < N; i++) {
					if (!isnan(r[i])) r[i] = eval(c, N, r[i]);
					if (r[i] < 0) {		// at least 2 solutions exist
						for (int j = 0; j < N; j++) r[j] = NAN;
						break;
					}
					if (i + 1 == N) {	// no real solution
						for (int j = 0; j < N; j++) r[j] = NAN;
						return;
					}
				}
			}
			u = eval(c, N, x), v = eval(c_, N - 1, x);
			dx = u / v; x -= dx;
		} while (abs(dx) > ERR_EPSILON_SN);
	}
	unsigned n = 0, lim = 1000; do {
		if (n > lim && dx > 0.01) x = pick_random(-2, 2) - c[1] / N, n -= 60, lim++;
		u = eval(c, N, x), v = eval(c_, N - 1, x);
		dx = u / v; x -= dx;
	} while (abs(dx) > ERR_EPSILON_SN && ++n < 2000);
	r[0] = x;

	// Euclid division
	N--;
	c_[2] = c[1] + x;
	for (int i = 2; i < N; i++) c_[i + 1] = x * c_[i] + c[i];
	c[N + 1] = x * c_[N] + c[N];
	for (int i = N; i > 1; i--) c[i] = c_[i];
	c[1] = 1, c[0] = 0;
	solvePolynomial(c + 1, r + 1, N);
}


// Find all real roots, available for any continuous function with finite roots, may be low efficiency
#include <vector>
void findRoots(double(*fun)(double), vector<double> &r) {
	auto f = [](double(*f)(double), vector<double> &d, double x)->double {
		double r = f(x);
		for (int i = 0; i < d.size(); i++) r /= x - d[i];
		return r;
	};
	double u, v, x = 0.001, dx = 1;
	unsigned n = 0, lim = 1000; do {
		if (n > lim && dx > 0.01) x = pick_random(-2, 2), n -= 1000, lim++;
		if (isnan(dx)) x = pick_random(-1, 1);
		u = f(fun, r, x), v = (f(fun, r, x + ERR_ZETA_SN) - f(fun, r, x)) / ERR_ZETA_SN;
		dx = u / v; x -= dx;
	} while (!(abs(dx) < ERR_EPSILON_SN) && ++n < 2000);
	if (n >= 2000) return;

	bool inc = (fun(x + ERR_ZETA_SN) - fun(x)) / ERR_ZETA_SN > 0;
	u = x - ERR_ETA_SN, v = x + ERR_ETA_SN;
	if (inc) {
		n = 0; while (v - u > 0.0001 * ERR_EPSILON_SN) {
			if (fun(x) < 0) u = x, x = 0.5*(u + v);
			else v = x, x = 0.5*(u + v);
			if (++n > lim) break;
		}
	}
	else {
		n = 0; while (v - u > 0.0001 * ERR_EPSILON_SN) {
			if (fun(x) < 0) v = x, x = 0.5*(u + v);
			else u = x, x = 0.5*(u + v);
			if (++n > lim) break;
		}
	}
	r.push_back(x);
	findRoots(fun, r);
}


int main() {
	vector<double> r;
	//findRoots([](double x) -> double { return exp(x) + sin(x) - pow(x, 3); }, r);
	//findRoots([](double x) -> double { return exp(exp(-x - 4)) + 1 / tgamma(x); }, r);
	//findRoots([](double x) -> double { return acos(erf(x)) - 1; }, r);
	findRoots([](double x) -> double { \
		double w = cos(2 * x) + 2 * sin(2 * x) + cos(4 * x) - 2 * sin(4 * x) + cos(6 * x) + 2 * sin(6 * x) + cos(8 * x) - 2 * sin(8 * x); \
		double r = exp(-pow(0.1*x, 10)); \
		return w * r - 0.01; \
	}, r);	// This function has 58 real roots! Try to graph it and see what it looks like. 
	for (int i = 0; i < r.size(); i++) cout << noshowpos << setprecision(15) << r[i] << endl;
	//for (int i = 0; i < r.size(); i++) cout << "(x" << showpos << setprecision(18) << -r[i] << ")*"; cout << "\b \n";
	cout << "\nTotal " << r.size() << " real roots. " << endl << endl;
	system("pause");
}
