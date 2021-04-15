// problem statement: https://uwaterloo.ca/entangler/fall-2019/sin-bin/sin-bin

#include "numerical/geometry.h"
#include "numerical/ode.h"
#include <stdio.h>

int main() {
	vec2 v0 = vec2(8, 0);

	const double dt = 0.01;
	double temp0[2], temp1[2], temp2[2];
	for (double t = 0.0; t <= 20.0; t += dt) {
		RungeKuttaMethod([](double* x, double t, double* dxdt) {
			vec2 v = *(vec2*)x;
			const double theta = 0.2*PI, g = 9.80665;
			vec2 a = vec2(0, -g * sin(theta)) - normalize(v) * g*cos(theta)*tan(theta);
			*(vec2*)dxdt = a;
		}, (double*)&v0, 2, t, dt, temp0, temp1, temp2);
		if (abs(t - int(t + 0.5)) < 1e-6)
			printf("(%lf,%lf) %lf\n", v0.x, v0.y, length(v0));
	}

}

// result: 4.000000
