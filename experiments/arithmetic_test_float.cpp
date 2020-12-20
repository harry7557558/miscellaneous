// test floating point arithmetic

#pragma GCC optimize "O0"

#include <stdio.h>
#include <math.h>
#include <stdint.h>


// random integer
uint64_t seed = 1;
uint32_t randu() {
    return (uint32_t)((seed = seed*(uint64_t)6364136223846793005+(uint64_t)1442695040888963407) >> 32);
}

// bitwise random floating point
float randf() {
    uint32_t x = randu();
    return *(float*)&x;
}
double randd() {
    uint64_t x = (uint64_t)randu() | ((uint64_t)randu() << 32);
    return *(double*)&x;
}

// bitwise random floating point with absolute value within a range
float randf_c(float _min, float _max) {
    float x;
    do {
        x = randf();
    } while (!(abs(x)>=_min && abs(x)<=_max));
    return x;
}
double randd_c(double _min, double _max) {
    double x;
    do {
        x = randf();
    } while (!(abs(x)>=_min && abs(x)<=_max));
    return x;
}

// test loop
#define LOOP_N 1000000
#define TEST(msg, cnt) \
    bad_count = 0; \
    for (int _=0;_<LOOP_N;_++) { cnt } \
    printf("%-32s %s (%d/%d)\n", msg, bad_count==0?"true":"false", bad_count, LOOP_N);

int main(int argc, char* argv[]){

    // may be needed because compiler is smart
    #define min(a,b) ((a)<(b)?(a):(b))
    float zero_f = min((float)argc, 0.0f);
    double zero_d = min((double)argc, 0.0);

    // a counter
    int bad_count = 0;

    // test if A+B==B+A
    TEST("A+B==B+A (float)",
        float A = randf_c(1e-6f,1e+6f);
        float B = randf_c(1e-6f,1e+6f);
        float c1 = A+B;
        float c2 = B+A;
        if (c1!=c2) bad_count++;
    );
    TEST("A+B==B+A (double)",
        double A = randd_c(1e-12,1e+12);
        double B = randd_c(1e-12,1e+12);
        double c1 = A+B;
        double c2 = B+A;
        if (c1!=c2) bad_count++;
    );

    // test if A*B==B*A
    TEST("A*B==B*A (float)",
        float A = randf_c(1e-6f,1e+6f);
        float B = randf_c(1e-6f,1e+6f);
        float c1 = A*B;
        float c2 = B*A;
        if (c1!=c2) bad_count++;
    );
    TEST("A*B==B*A (double)",
        double A = randd_c(1e-12,1e+12);
        double B = randd_c(1e-12,1e+12);
        double c1 = A*B;
        double c2 = B*A;
        if (c1!=c2) bad_count++;
    );

    // test if X-X==0
    TEST("X-X==0 (float)",
        float X = randf_c(1e-6f,1e+6f);
        float c1 = X-X;
        float c2 = 0.0f;
        if (c1!=c2) bad_count++;
    );
    TEST("X-X==0 (double)",
        double X = randd_c(1e-12,1e+12);
        double c1 = X-X;
        double c2 = 0.0;
        if (c1!=c2) bad_count++;
    );

    // test if X/X==1
    // some people say no but my answer is yes
    TEST("X/X==1 (float)",
        float X = randf_c(1e-6f,1e+6f);
        float c1 = X/X;
        float c2 = 1.0f;
        if (c1!=c2) bad_count++;
    );
    TEST("X/X==1 (float)",
        double X = randd_c(1e-12,1e+12);
        double c1 = X/X;
        double c2 = 1.0;
        if (c1!=c2) bad_count++;
    );

    printf("\n");

    // test exponential/logarithm/power functions
    TEST("expf(logf(x))==x",
        float x = abs(randf_c(1e-20f,1e+20f));
        float c1 = expf(logf(x));
        float c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("exp(log(x))==x",
        double x = abs(randd_c(1e-100,1e+100));
        double c1 = exp(log(x));
        double c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("logf(expf(x))==x",
        float x = randf_c(-50.0f,50.0f);
        float c1 = logf(expf(x));
        float c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("log(exp(x))==x",
        double x = randd_c(-200.0,200.0);
        double c1 = log(exp(x));
        double c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("powf(x,2)==x*x",
        float x = randf_c(1e-6f,1e+6f);
        float c1 = powf(x,2.0f+zero_f);
        float c2 = x*x;
        if (c1!=c2) bad_count++;
    );
    TEST("pow(x,2)==x*x",
        double x = randd_c(1e-6,1e+6);
        double c1 = pow(x,2.0+zero_d);
        double c2 = x*x;
        if (c1!=c2) bad_count++;
    );
    TEST("powf(x,3)==x*x*x",
        float x = randf_c(1e-6f,1e+6f);
        float c1 = powf(x,3.0f+zero_f);
        float c2 = x*x*x;
        if (c1!=c2) bad_count++;
    );
    TEST("pow(x,3)==x*x*x",
        double x = randd_c(1e-6,1e+6);
        double c1 = pow(x,3.0+zero_d);
        double c2 = x*x*x;
        if (c1!=c2) bad_count++;
    );
    TEST("powf(x,0.5)==sqrtf(x)",
        float x = abs(randf_c(1e-6f,1e+6f));
        float c1 = powf(x,0.5f+zero_f);
        float c2 = sqrtf(x);
        if (c1!=c2) bad_count++;
    );
    TEST("pow(x,0.5)==sqrt(x)",
        double x = abs(randd_c(1e-6,1e+6));
        double c1 = pow(x,0.5+zero_d);
        double c2 = sqrt(x);
        if (c1!=c2) bad_count++;
    );
    TEST("powf(x,1/3)==cbrtf(x)",
        float x = abs(randf_c(1e-12f,1e+12f));
        float c1 = powf(x,1.0f/3.0f+zero_f);
        float c2 = cbrtf(x);
        if (c1!=c2) bad_count++;
    );
    TEST("pow(x,1/3)==cbrt(x)",
        double x = abs(randd_c(1e-12,1e+12));
        double c1 = pow(x,1.0/3.0+zero_d);
        double c2 = cbrt(x);
        if (c1!=c2) bad_count++;
    );
    TEST("expf(0.5*logf(x))==sqrtf(x)",
        float x = abs(randf_c(1e-6f,1e+6f));
        float c1 = expf(0.5f*logf(x));
        float c2 = sqrtf(x);
        if (c1!=c2) bad_count++;
    );
    TEST("exp(0.5*log(x))==sqrt(x)",
        double x = abs(randd_c(1e-6,1e+6));
        double c1 = exp(0.5*log(x));
        double c2 = sqrt(x);
        if (c1!=c2) bad_count++;
    );
    TEST("sqrtf(x*x)==abs(x)",
        float x = randf_c(1e-6f,1e+6f);
        float c1 = sqrtf(x*x);
        float c2 = abs(x);
        if (c1!=c2) bad_count++;
    );
    TEST("sqrt(x*x)==abs(x)",
        double x = abs(randd_c(1e-6,1e+6));
        double c1 = sqrt(x*x);
        double c2 = abs(x);
        if (c1!=c2) bad_count++;
    );

    printf("\n");

    // test trigonometric/hyperbolic functions
    TEST("sinf(asinf(x))==x",
        float x = randf_c(1e-6f,1.0f);
        float c1 = sinf(asinf(x));
        float c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("sin(asin(x))==x",
        double x = randd_c(1e-6,1.0);
        double c1 = sin(asin(x));
        double c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("cosf(acosf(x))==x",
        float x = randf_c(1e-6f,1.0f);
        float c1 = cosf(acosf(x));
        float c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("cos(acos(x))==x",
        double x = randd_c(1e-6,1.0);
        double c1 = cos(acos(x));
        double c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("tanf(atanf(x))==x",
        float x = randf_c(1e-6f,1e+6f);
        float c1 = tanf(atanf(x));
        float c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("tan(atan(x))==x",
        double x = randd_c(1e-6,1e+6);
        double c1 = tan(atan(x));
        double c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("sinhf(asinhf(x))==x",
        float x = randf_c(1e-6f,1e+6f);
        float c1 = sinhf(asinhf(x));
        float c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("sinh(asinh(x))==x",
        double x = randd_c(1e-6,1e+6);
        double c1 = sinh(asinh(x));
        double c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("coshf(acoshf(x))==x",
        float x = abs(randf_c(1.0f,1e+6f));
        float c1 = coshf(acoshf(x));
        float c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("cosh(acosh(x))==x",
        double x = randd_c(1.0,1e+6);
        double c1 = cosh(acosh(x));
        double c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("tanhf(atanhf(x))==x",
        float x = randf_c(1e-6f,1.0f);
        float c1 = tanhf(atanhf(x));
        float c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("tanh(atanh(x))==x",
        double x = randd_c(1e-6,1.0);
        double c1 = tanh(atanh(x));
        double c2 = x;
        if (c1!=c2) bad_count++;
    );
    TEST("tanf(x)==sinf(x)/cosf(x)",
        float x = randf_c(1e-6f,12.0f);
        float c1 = tanf(x);
        float c2 = sinf(x)/cosf(x);
        if (c1!=c2) bad_count++;
    );
    TEST("tan(x)==sin(x)/cos(x)",
        double x = randd_c(1e-6,12.0);
        double c1 = tan(x);
        double c2 = sin(x)/cos(x);
        if (c1!=c2) bad_count++;
    );
    TEST("tanhf(x)==sinhf(x)/coshf(x)",
        float x = randf_c(1e-6f,12.0f);
        float c1 = tanhf(x);
        float c2 = sinhf(x)/coshf(x);
        if (c1!=c2) bad_count++;
    );
    TEST("tanh(x)==sinh(x)/cosh(x)",
        double x = randd_c(1e-6,12.0);
        double c1 = tanh(x);
        double c2 = sinh(x)/cosh(x);
        if (c1!=c2) bad_count++;
    );
    TEST("sinhf(x)==0.5*(expf(x)-expf(-x))",
        float x = randf_c(1e-6f,50.0f);
        float c1 = sinhf(x);
        float c2 = 0.5f*(expf(x)+expf(-x));
        if (c1!=c2) bad_count++;
    );
    TEST("sinh(x)==0.5*(exp(x)-exp(-x))",
        double x = randd_c(1e-6,200.0);
        double c1 = sinh(x);
        double c2 = 0.5*(exp(x)-exp(-x));
        if (c1!=c2) bad_count++;
    );
    TEST("asinhf(x)==logf(x+sqrtf(x*x+1))",
        float x = randf_c(1e-6f,50.0f);
        float c1 = asinhf(x);
        float c2 = logf(x+sqrtf(x*x+1.0f));
        if (c1!=c2) bad_count++;
    );
    TEST("asinh(x)==log(x+sqrt(x*x+1))",
        double x = randd_c(1e-6,200.0);
        double c1 = asinh(x);
        double c2 = log(x+sqrt(x*x+1.0));
        if (c1!=c2) bad_count++;
    );
    TEST("sinf(x)**2+cosf(x)**2==1",
        float x = randf_c(1e-6f,12.57f);
        float c1 = sinf(x)*sinf(x)+cosf(x)*cosf(x);
        float c2 = 1.0f;
        if (c1!=c2) bad_count++;
    );
    TEST("sin(x)**2+cos(x)**2==1",
        double x = randd_c(1e-6,12.57);
        double c1 = sin(x)*sin(x)+cos(x)*cos(x);
        double c2 = 1.0;
        if (c1!=c2) bad_count++;
    );
    TEST("coshf(x)**2-sinhf(x)**2==1",
        float x = randf_c(1e-6f,10.0f);
        float c1 = coshf(x)*coshf(x)-sinhf(x)*sinhf(x);
        float c2 = 1.0f;
        if (c1!=c2) bad_count++;
    );
    TEST("cosh(x)**2-sinh(x)**2==1",
        double x = randd_c(1e-6,10.0);
        double c1 = cosh(x)*cosh(x)-sinh(x)*sinh(x);
        double c2 = 1.0;
        if (c1!=c2) bad_count++;
    );
    TEST("sinf(acosf(x))==sqrtf(1-x*x)",
        float x = randf_c(1e-6f,1.0f);
        float c1 = sinf(acosf(x));
        float c2 = sqrtf(1.0f-x*x);
        if (c1!=c2) bad_count++;
    );
    TEST("sin(acos(x))==sqrt(1-x*x)",
        double x = randd_c(1e-6,1.0);
        double c1 = sin(acos(x));
        double c2 = sqrt(1.0-x*x);
        if (c1!=c2) bad_count++;
    );
    TEST("coshf(asinhf(x))==sqrtf(1+x*x)",
        float x = randf_c(1e-6f,1.0f);
        float c1 = coshf(asinhf(x));
        float c2 = sqrtf(1.0f+x*x);
        if (c1!=c2) bad_count++;
    );
    TEST("cosh(asinh(x))==sqrt(1+x*x)",
        double x = randd_c(1e-6,1.0);
        double c1 = cosh(asinh(x));
        double c2 = sqrt(1.0+x*x);
        if (c1!=c2) bad_count++;
    );

    printf("\n");

    return 0;
}
