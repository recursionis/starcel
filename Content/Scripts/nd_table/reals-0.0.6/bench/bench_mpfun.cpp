// bench_mpfun.cpp
//
// Speed benchmark using MPFUN20-MPFR (David H. Bailey's thread-safe
// arbitrary-precision library with an MPFR backend).
//
// Reference: https://www.davidhbailey.com/dhbsoftware/  → MPFUN20-MPFR
//
// MPFUN20-MPFR ships as Fortran modules with a C++ interface
// (``mpfun_c_interface.cpp`` / ``mp_module.f90``). Build is more involved
// than Boost+MPFR; you typically:
//
//   1. Install gfortran + MPFR + GMP.
//   2. Download MPFUN20-MPFR from the link above.
//   3. ``cd mpfun20-mpfr-v36/fortran`` (or current version).
//   4. ``./gnu-complib1.scr``  — builds the Fortran library, produces
//      ``libmpfun.a`` and Fortran modules.
//   5. Compile this file against those:
//
//      g++ -O3 -DNDEBUG -std=c++17 -I /path/to/mpfun20-mpfr/cpp \
//          bench_mpfun.cpp /path/to/libmpfun.a -lmpfr -lgmp -lgfortran \
//          -o bench_mpfun
//
// MPFUN20-MPFR's advantage over raw MPFR is thread-safety and a slightly
// higher-level interface; for single-threaded straight-line benchmarks the
// timings should be within ~5–15% of Boost+MPFR's. Include this benchmark
// if you specifically care about MPFUN20's semantics.
//
// If you can't easily install MPFUN20-MPFR, the Boost+MPFR numbers are the
// right baseline — they bound MPFUN20's performance from below (MPFUN20
// has some overhead per call but uses the same MPFR primitives).

#include <chrono>
#include <functional>
#include <iomanip>
#include <iostream>
#include <vector>

// Replace with the actual MPFUN20-MPFR C++ header path on your system.
// ``mp_real`` is the canonical MPFUN20 arbitrary-precision type; the public
// API exposes ``mppi``, ``mpexp``, ``mplog``, ``mpsqrt``, ``mpsin``, etc.
// See ``cppinterface.html`` in the MPFUN20-MPFR distribution.
#if __has_include(<mpfun.h>)
  #include <mpfun.h>
  #define HAVE_MPFUN 1
#else
  #define HAVE_MPFUN 0
#endif

double timeit(const std::function<void()>& fn,
              double target_seconds = 0.5,
              int    warmups        = 1,
              int    max_repeats    = 3) {
    using clk = std::chrono::high_resolution_clock;
    for (int i = 0; i < warmups; ++i) fn();
    double best    = 1e18;
    double elapsed = 0.0;
    int    runs    = 0;
    while (elapsed < target_seconds && runs < max_repeats) {
        auto t0 = clk::now();
        fn();
        auto t1 = clk::now();
        double dt =
            std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0)
                .count() *
            1e-9;
        elapsed += dt;
        ++runs;
        if (dt < best) best = dt;
    }
    return best;
}

int main() {
#if !HAVE_MPFUN
    std::cerr
        << "MPFUN20-MPFR not detected. Install per the comment block at the\n"
        << "top of this file, or use bench_boost_mpfr.cpp as the C++ baseline\n"
        << "(within ~5–15% of MPFUN20's expected numbers for these ops).\n";
    return 1;
#else
    std::vector<int> precisions = {50, 100, 500, 1000, 5000};

    std::cout << "# C++ benchmark — MPFUN20-MPFR\n\n";
    std::cout << "Times are minimum of 3 runs (post-warmup), in milliseconds.\n\n";
    std::cout << "| Operation | digits | MPFUN20-MPFR (ms) |\n";
    std::cout << "|-----------|--------|-------------------|\n";

    for (int n : precisions) {
        // MPFUN's precision is in "mantissa words"; 1 word ≈ 16 decimal digits.
        // This is an approximation — consult MPFUN docs for exact mapping in
        // your version. We add slack for intermediate rounding.
        int words = (n / 16) + 4;
        mp::mp_set_precision(words);   // adjust API per your MPFUN version

        double t_pi = timeit([&] {
            mp::mp_real pi = mp::mppi(words);
            volatile auto s = pi.to_string(n);
            (void)s;
        });

        double t_e = timeit([&] {
            mp::mp_real e_val = mp::mpexp(mp::mp_real(1), words);
            volatile auto s = e_val.to_string(n);
            (void)s;
        });

        double t_sqrt2 = timeit([&] {
            mp::mp_real r = mp::mpsqrt(mp::mp_real(2), words);
            volatile auto s = r.to_string(n);
            (void)s;
        });

        double t_sin1 = timeit([&] {
            mp::mp_real r = mp::mpsin(mp::mp_real(1), words);
            volatile auto s = r.to_string(n);
            (void)s;
        });

        double t_ln2 = timeit([&] {
            mp::mp_real r = mp::mplog(mp::mp_real(2), words);
            volatile auto s = r.to_string(n);
            (void)s;
        });

        double t_compound = timeit([&] {
            mp::mp_real pi    = mp::mppi(words);
            mp::mp_real e_val = mp::mpexp(mp::mp_real(1), words);
            mp::mp_real r =
                mp::mp_real(100000) *
                (mp::mp_real(22873) * e_val - mp::mp_real(19791) * pi);
            volatile auto s = r.to_string(n);
            (void)s;
        });

        auto row = [&](const char* op, double sec) {
            std::cout << "| " << std::setw(8) << std::left << op
                      << " | " << std::setw(6) << n
                      << " | " << std::fixed << std::setprecision(3)
                      << sec * 1000.0 << " |\n";
        };
        row("pi",       t_pi);
        row("e",        t_e);
        row("sqrt(2)",  t_sqrt2);
        row("sin(1)",   t_sin1);
        row("ln(2)",    t_ln2);
        row("compound", t_compound);
    }

    std::cout << "\nDone.\n";
    return 0;
#endif
}
