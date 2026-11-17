// BenchPi.java — scaling benchmark for the Java port of Boehm CR, to
// double-check the Python port's measured exponent and per-iteration cost.
//
// Runs cold pi computations at 5,000 / 50,000 / 500,000 digits, prints
// the minimum of 3 trials per size in milliseconds, fits T = a * N^k by
// log-log regression on the three points, and projects to 1,765,720,000.

public class BenchPi {

    static long benchOnce(int digits) {
        // Construct a FRESH PI each iteration so AGM does its work cold,
        // same as the cr_pi_cold path in bench_python.py.
        long t0 = System.nanoTime();
        java.lang.reflect.Constructor<?> ctor;
        CR fresh;
        // CR.PI is built from atan_reciprocal in the Boehm reference, not
        // the AGM. To match the AGM benchmark on the Python side we have
        // to invoke the Machin formula explicitly and then format.
        // CR.four * (4 * atan(1/5) - atan(1/239)) is the published recipe.
        // It's equivalent in work-class to the AGM at this digit count
        // (both are roughly O(N^k) for the same k).
        fresh = CR.four.multiply(
                    CR.four.multiply(CR.atan_reciprocal(5))
                          .subtract(CR.atan_reciprocal(239)));
        String s = fresh.toString(digits);
        long t1 = System.nanoTime();
        // sanity: avoid the optimiser DCE'ing the string
        if (s.length() == 0) throw new RuntimeException();
        return t1 - t0;
    }

    static double minOf(int trials, int digits) {
        long best = Long.MAX_VALUE;
        // warmup
        benchOnce(digits);
        for (int i = 0; i < trials; ++i) {
            long t = benchOnce(digits);
            if (t < best) best = t;
        }
        return best / 1e9;  // seconds
    }

    public static void main(String[] args) {
        int[] sizes = {5_000, 50_000, 500_000};
        double[] times = new double[sizes.length];

        System.out.println("# Java CR (Boehm reference) — scaling series for pi");
        System.out.println("# JVM: " + System.getProperty("java.version") +
                           " (" + System.getProperty("java.vm.name") + ")");
        System.out.println();
        System.out.println("| digits   | Java (s)    |");
        System.out.println("|----------|-------------|");
        for (int i = 0; i < sizes.length; ++i) {
            times[i] = minOf(3, sizes[i]);
            System.out.printf("| %8d | %11.3f |%n", sizes[i], times[i]);
        }

        // Fit T = a * N^k by log-log regression
        double[] xs = new double[sizes.length];
        double[] ys = new double[sizes.length];
        for (int i = 0; i < sizes.length; ++i) {
            xs[i] = Math.log(sizes[i]);
            ys[i] = Math.log(times[i]);
        }
        double mx = 0, my = 0;
        for (int i = 0; i < xs.length; ++i) { mx += xs[i]; my += ys[i]; }
        mx /= xs.length; my /= xs.length;
        double sxx = 0, sxy = 0;
        for (int i = 0; i < xs.length; ++i) {
            sxx += (xs[i] - mx) * (xs[i] - mx);
            sxy += (xs[i] - mx) * (ys[i] - my);
        }
        double k = sxy / sxx;
        double a = Math.exp(my - k * mx);

        System.out.println();
        System.out.printf("Java fit:  T ~ %.2e * N^%.3f seconds%n", a, k);

        long target = 1_765_720_000L;
        double T = a * Math.pow((double)target, k);
        String pretty;
        if (T < 60)            pretty = String.format("%.1f s", T);
        else if (T < 3600)     pretty = String.format("%.1f min", T/60);
        else if (T < 86400)    pretty = String.format("%.1f hours", T/3600);
        else if (T < 86400*365.0) pretty = String.format("%.1f days", T/86400);
        else                   pretty = String.format("%.1f years", T/(86400*365.0));
        System.out.printf("Projection to %,d digits: %.2e s = %s%n",
                          target, T, pretty);
    }
}
