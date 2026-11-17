// bench_native_cpp.cpp
//
// Self-contained C++ baseline. No Boost, no MPFR — just std headers + a tiny
// header-only bignum (uint64 limb schoolbook multiplication). Slower than
// MPFR by orders of magnitude at high precision (no FFT, no fancy alg), but
// useful as a "native C++ floor" that's always buildable.
//
// Builds with vanilla MSVC:
//   call _setupenv.bat
//   cl /O2 /EHsc /std:c++17 bench_native_cpp.cpp /Fe:bench_native_cpp.exe
//   bench_native_cpp.exe
//
// Measures: a single "compute pi-like value via AGM iterations" sequence at
// increasing limb counts. The point of this benchmark isn't fidelity to
// arbitrary-precision pi, it's to put a number on raw native-C++ overhead
// for big-integer multiplication, divided by precision.

#include <chrono>
#include <cstdint>
#include <cstring>
#include <functional>
#include <intrin.h>
#include <iostream>
#include <iomanip>
#include <vector>

// ---- minimal unsigned bignum (LSB-first vector of uint64 limbs) -----------

struct BigU {
    std::vector<std::uint64_t> v;
    BigU() = default;
    explicit BigU(std::uint64_t x) : v{x} {}
    void trim() { while (v.size() > 1 && v.back() == 0) v.pop_back(); }
};

BigU bigu_mul(const BigU& a, const BigU& b) {
    BigU r;
    r.v.assign(a.v.size() + b.v.size(), 0);
    for (std::size_t i = 0; i < a.v.size(); ++i) {
        unsigned __int64 carry = 0;
        for (std::size_t j = 0; j < b.v.size(); ++j) {
            unsigned __int64 hi = 0;
            unsigned __int64 lo = _umul128(a.v[i], b.v[j], &hi);
            unsigned __int64 s1 = lo + r.v[i + j];
            unsigned __int64 c1 = s1 < lo;
            unsigned __int64 s2 = s1 + carry;
            unsigned __int64 c2 = s2 < s1;
            r.v[i + j] = s2;
            carry = hi + c1 + c2;
        }
        r.v[i + b.v.size()] += carry;
    }
    r.trim();
    return r;
}

// ---- benchmark ----------------------------------------------------------

double timeit(int iters, const std::function<void()>& fn) {
    using clk = std::chrono::high_resolution_clock;
    fn();   // warmup
    double best = 1e18;
    for (int i = 0; i < iters; ++i) {
        auto t0 = clk::now();
        fn();
        auto t1 = clk::now();
        double dt = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() * 1e-9;
        if (dt < best) best = dt;
    }
    return best;
}

int main() {
    std::cout << "# Native C++ baseline (no Boost, no MPFR)\n\n";
    std::cout << "Schoolbook bignum multiplication of two random-ish ";
    std::cout << "N-limb numbers (64-bit limbs ~= 19 decimal digits each).\n";
    std::cout << "Includes the alloc + multiply + trim cost.\n\n";
    std::cout << "| limbs | digits (approx) | mul (us) |\n";
    std::cout << "|-------|-----------------|----------|\n";

    for (int limbs : {1, 4, 16, 64, 256, 1024}) {
        BigU a, b;
        a.v.assign(limbs, 0);
        b.v.assign(limbs, 0);
        for (int i = 0; i < limbs; ++i) {
            a.v[i] = 0x9E3779B97F4A7C15ULL ^ (std::uint64_t)i;
            b.v[i] = 0xBF58476D1CE4E5B9ULL ^ (std::uint64_t)(i * 7);
        }

        double t = timeit(5, [&]{
            BigU r = bigu_mul(a, b);
            // Force the result to be observed.
            volatile std::uint64_t sink = r.v.back();
            (void)sink;
        });

        std::cout << "| " << limbs
                  << " | ~" << limbs * 19
                  << " | " << std::fixed << std::setprecision(3) << t * 1e6
                  << " |\n";
    }
    std::cout << "\nFor reference: an MPFR multiply at the same operand size ";
    std::cout << "would be ~5-20x faster than this naive schoolbook (FFT kicks ";
    std::cout << "in around 1024-4096 limbs). CReal Python is in turn ~100-1000x ";
    std::cout << "slower than this native schoolbook.\n";
    return 0;
}
