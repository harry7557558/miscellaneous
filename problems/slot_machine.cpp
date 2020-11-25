// problem statement: ?!

#include <stdio.h>
#include <cmath>
#include <stdint.h>

uint32_t seed = 1234567890;  // random number seed
double rand01() { return (seed = seed * 1664525u + 1013904223u) / 4294967295.; }  // generate a random number between 0 and 1

int main() {
	double P[100];  // average money earned in each day, in billions of dollars
	const int TRY = 10000000;  // number of Monte-Carlo samples

	for (int i = 0; i < 100; i++) P[i] = 0.;
	for (int T = 0; T < TRY; T++) {
		bool ppl[99];  // other people
		for (int i = 0; i < 99; i++) ppl[i] = true;  // everyone are alive initially
		for (int i = 0; i < 100; i++) {  // 0-indexed days
			// calculate how many people will roll
			int ppl_roll = 0;
			for (int i = 0; i < 99; i++) if (ppl[i]) {
				if (rand01() < 0.5) {  // each person has 1/2 probability to roll
					ppl_roll++;
					ppl[i] = false;
				}
			}
			double pe = 0.01*(i + 1);  // probability of winning per each roll at this day
			double pw = 1.0 - pow(1.0 - pe, ppl_roll);  // probability of at least one person hits the "jackpot"
			double random = rand01();
			if (random < pw) {  // game over
				break;
			}
			// if you roll at this day...
			pw = 1.0 - pow(1.0 - pe, ppl_roll + 1);
			if (random < pw) {  // wow!
				P[i] += 1.0 / (ppl_roll + 1);  // share the money
				break;
			}
		}
	}

	printf("[");
	for (int i = 0; i < 100; i++) {
		printf("(%d,%lf),", i + 1, P[i] / TRY);
	}
	printf("\b]\n");
	return 0;
}
