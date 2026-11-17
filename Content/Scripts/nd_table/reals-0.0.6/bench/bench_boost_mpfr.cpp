// bench_boost_mpfr.cpp
//
// Speed benchmark: arbitrary-precision math via Boost.Multiprecision with the
// MPFR backend. Matches the operations in bench_python.py so timings can be
// pasted into the same table.
//
// ──────────────────────────────────────────────────────────────────────────
// Build (Linux/macOS):
//   sudo apt install libmpfr-dev libgmp-dev libboost-all-dev   # or brew
//   g++ -O3 -DNDEBUG -std=c++17 -o bench_boost_mpfr bench_boost_mpfr.cpp \
//       -lmpfr -lgmp
//
// Build (Windows with vcpkg + MSVC):
//   vcpkg install boost-multiprecision mpfr
//   "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
//   cl /O2 /EHsc /std:c++17 /MD /I C:\vcpkg\installed\x64-windows\include ^
//      bench_boost_mpfr.cpp ^
//      /link /LIBPATH:C:\vcpkg\installed\x64-windows\lib mpfr.lib gmp.lib
//
// Build (Windows with MSYS2):
//   pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-boost \
//             mingw-w64-x86_64-mpfr mingw-w64-x86_64-gmp
//   g++ -O3 -DNDEBUG -std=c++17 -o bench_boost_mpfr.exe bench_boost_mpfr.cpp \
//       -lmpfr -lgmp
//
// Run:
//   ./bench_boost_mpfr
// ──────────────────────────────────────────────────────────────────────────

#include <boost/multiprecision/mpfr.hpp>
#include <boost/math/constants/constants.hpp>

#include <algorithm>
#include <chrono>
#include <functional>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

// Dynamic-precision MPFR-backed float. Each instance can have its own
// precision set at runtime via ``::default_precision`` or per-object init.
using HPFloat = boost::multiprecision::number<
    boost::multiprecision::mpfr_float_backend<0>>;

namespace bp = boost::multiprecision;

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

// MPFR precision is in bits; convert from desired decimal digits.
int bits_for_digits(int digits) {
    return static_cast<int>(digits * 3.3219280948873626) + 64;  // log2(10) + slack
}

std::string to_fixed(const HPFloat& x, int n) {
    std::ostringstream oss;
    oss << std::setprecision(n) << std::fixed << x;
    return oss.str();
}

int main() {
    std::vector<int> precisions = {50, 100, 500, 1000, 5000};

    std::cout << "# C++ benchmark — Boost.Multiprecision + MPFR\n\n";
    std::cout << "Boost.Multiprecision " << BOOST_VERSION / 100000 << "."
              << (BOOST_VERSION / 100) % 1000 << "." << BOOST_VERSION % 100
              << " with MPFR backend.\n\n";
    std::cout << "Times are minimum of 3 runs (post-warmup), in milliseconds.\n\n";
    std::cout << "| Operation | digits | Boost+MPFR (ms) |\n";
    std::cout << "|-----------|--------|-----------------|\n";

    for (int n : precisions) {
        int bits = bits_for_digits(n);
        HPFloat::default_precision(bits);

        double t_pi = timeit([&] {
            HPFloat::default_precision(bits);
            HPFloat pi = boost::math::constants::pi<HPFloat>();
            volatile auto s = to_fixed(pi, n);
            (void)s;
        });

        double t_e = timeit([&] {
            HPFloat::default_precision(bits);
            HPFloat e_val = exp(HPFloat(1));
            volatile auto s = to_fixed(e_val, n);
            (void)s;
        });

        double t_sqrt2 = timeit([&] {
            HPFloat::default_precision(bits);
            HPFloat r = sqrt(HPFloat(2));
            volatile auto s = to_fixed(r, n);
            (void)s;
        });

        double t_sin1 = timeit([&] {
            HPFloat::default_precision(bits);
            HPFloat r = sin(HPFloat(1));
            volatile auto s = to_fixed(r, n);
            (void)s;
        });

        double t_ln2 = timeit([&] {
            HPFloat::default_precision(bits);
            HPFloat r = log(HPFloat(2));
            volatile auto s = to_fixed(r, n);
            (void)s;
        });

        double t_compound = timeit([&] {
            HPFloat::default_precision(bits);
            HPFloat pi    = boost::math::constants::pi<HPFloat>();
            HPFloat e_val = exp(HPFloat(1));
            HPFloat r     = HPFloat(100000) *
                        (HPFloat(22873) * e_val - HPFloat(19791) * pi);
            volatile auto s = to_fixed(r, n);
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

    std::cout << "\nDone. Paste alongside the Python table for comparison.\n";
    return 0;
}
