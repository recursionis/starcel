// CR.java — Hans Boehm's Constructive Reals, the canonical reference
// implementation. Copied verbatim from the source the user provided
// earlier in this session. Licensed under SGI / HP terms (see header).
//
// This file is identical to com.hp.creals.CR upstream. The package
// declaration is dropped so we can compile and run it standalone here
// without a directory hierarchy.

import java.math.BigInteger;

public abstract class CR extends Number {
      static final BigInteger big0 = BigInteger.valueOf(0);
      static final BigInteger big1 = BigInteger.valueOf(1);
      static final BigInteger bigm1 = BigInteger.valueOf(-1);
      static final BigInteger big2 = BigInteger.valueOf(2);
      static final BigInteger big3 = BigInteger.valueOf(3);
      static final BigInteger big6 = BigInteger.valueOf(6);
      static final BigInteger big8 = BigInteger.valueOf(8);
      static final BigInteger big10 = BigInteger.valueOf(10);

public volatile static boolean please_stop = false;

      protected abstract BigInteger approximate(int precision);
      transient int min_prec;
      transient BigInteger max_appr;
      transient boolean appr_valid = false;

      static int bound_log2(int n) {
        int abs_n = Math.abs(n);
        return (int)Math.ceil(Math.log((double)(abs_n + 1))/Math.log(2.0));
      }

      static void check_prec(int n) {
        int high = n >> 28;
        int high_shifted = n >> 29;
        if (0 != (high ^ high_shifted)) {
            throw new ArithmeticException("precision overflow");
        }
      }

      public static CR valueOf(BigInteger n) { return new int_CR(n); }
      public static CR valueOf(int n) { return valueOf(BigInteger.valueOf(n)); }
      public static CR valueOf(long n) { return valueOf(BigInteger.valueOf(n)); }

      static CR one = valueOf(1);

      static BigInteger shift(BigInteger k, int n) {
        if (n == 0) return k;
        if (n < 0) return k.shiftRight(-n);
        return k.shiftLeft(n);
      }

      static BigInteger scale(BigInteger k, int n) {
        if (n >= 0) return k.shiftLeft(n);
        BigInteger adj_k = shift(k, n+1).add(big1);
        return adj_k.shiftRight(1);
      }

      public BigInteger get_appr(int precision) {
        check_prec(precision);
        if (appr_valid && precision >= min_prec) {
            return scale(max_appr, min_prec - precision);
        } else {
            BigInteger result = approximate(precision);
            min_prec = precision;
            max_appr = result;
            appr_valid = true;
            return result;
        }
      }

      int known_msd() {
        int length;
        if (max_appr.signum() >= 0) length = max_appr.bitLength();
        else length = max_appr.negate().bitLength();
        return min_prec + length - 1;
      }

      int msd(int n) {
        if (!appr_valid ||
            max_appr.compareTo(big1) <= 0
            && max_appr.compareTo(bigm1) >= 0) {
            get_appr(n - 1);
            if (max_appr.abs().compareTo(big1) <= 0) return Integer.MIN_VALUE;
        }
        return known_msd();
      }

      int iter_msd(int n) {
        int prec = 0;
        for (;prec > n + 30; prec = (prec * 3)/2 - 16) {
            int msd = msd(prec);
            if (msd != Integer.MIN_VALUE) return msd;
            check_prec(prec);
        }
        return msd(n);
      }

      int msd() { return iter_msd(Integer.MIN_VALUE); }

      private static String zeroes(int n) {
        char[] a = new char[n];
        for (int i = 0; i < n; ++i) a[i] = '0';
        return new String(a);
      }

      CR simple_ln() { return new prescaled_ln_CR(this.subtract(one)); }
      static CR ten_ninths = valueOf(10).divide(valueOf(9));
      static CR twentyfive_twentyfourths = valueOf(25).divide(valueOf(24));
      static CR eightyone_eightyeths = valueOf(81).divide(valueOf(80));
      static CR ln2_1 = valueOf(7).multiply(ten_ninths.simple_ln());
      static CR ln2_2 = valueOf(2).multiply(twentyfive_twentyfourths.simple_ln());
      static CR ln2_3 = valueOf(3).multiply(eightyone_eightyeths.simple_ln());
      static CR ln2 = ln2_1.subtract(ln2_2).add(ln2_3);

      static CR atan_reciprocal(int n) { return new integral_atan_CR(n); }
      static CR four = valueOf(4);

      public int compareTo(CR x, int r, int a) {
        int this_msd = iter_msd(a);
        int x_msd = x.iter_msd(this_msd > a ? this_msd : a);
        int max_msd = (x_msd > this_msd ? x_msd : this_msd);
        int rel = max_msd + r;
        int abs_prec = (rel > a ? rel : a);
        return compareTo(x, abs_prec);
      }

      public int compareTo(CR x, int a) {
        int needed_prec = a - 1;
        BigInteger this_appr = get_appr(needed_prec);
        BigInteger x_appr = x.get_appr(needed_prec);
        int comp1 = this_appr.compareTo(x_appr.add(big1));
        if (comp1 > 0) return 1;
        int comp2 = this_appr.compareTo(x_appr.subtract(big1));
        if (comp2 < 0) return -1;
        return 0;
      }

      public int compareTo(CR x) {
        for (int a = -20; ; a *= 2) {
            check_prec(a);
            int result = compareTo(x, a);
            if (0 != result) return result;
        }
      }

      public int signum(int a) {
        if (appr_valid) {
            int quick_try = max_appr.signum();
            if (0 != quick_try) return quick_try;
        }
        int needed_prec = a - 1;
        BigInteger this_appr = get_appr(needed_prec);
        return this_appr.signum();
      }

      public int signum() {
        for (int a = -20; ; a *= 2) {
            check_prec(a);
            int result = signum(a);
            if (0 != result) return result;
        }
      }

      public String toString(int n, int radix) {
        CR scaled_CR;
        if (16 == radix) scaled_CR = shiftLeft(4*n);
        else {
            BigInteger scale_factor = BigInteger.valueOf(radix).pow(n);
            scaled_CR = multiply(new int_CR(scale_factor));
        }
        BigInteger scaled_int = scaled_CR.get_appr(0);
        String scaled_string = scaled_int.abs().toString(radix);
        String result;
        if (0 == n) result = scaled_string;
        else {
            int len = scaled_string.length();
            if (len <= n) {
                String z = zeroes(n + 1 - len);
                scaled_string = z + scaled_string;
                len = n + 1;
            }
            String whole = scaled_string.substring(0, len - n);
            String fraction = scaled_string.substring(len - n);
            result = whole + "." + fraction;
        }
        if (scaled_int.signum() < 0) result = "-" + result;
        return result;
      }

      public String toString(int n) { return toString(n, 10); }
      public String toString() { return toString(10); }

      public BigInteger BigIntegerValue() { return get_appr(0); }
      public int intValue() { return BigIntegerValue().intValue(); }
      public byte byteValue() { return BigIntegerValue().byteValue(); }
      public long longValue() { return BigIntegerValue().longValue(); }

      public double doubleValue() {
        int my_msd = iter_msd(-1080);
        if (Integer.MIN_VALUE == my_msd) return 0.0;
        int needed_prec = my_msd - 60;
        double scaled_int = get_appr(needed_prec).doubleValue();
        boolean may_underflow = (needed_prec < -1000);
        long scaled_int_rep = Double.doubleToLongBits(scaled_int);
        long exp_adj = may_underflow ? needed_prec + 96 : needed_prec;
        long orig_exp = (scaled_int_rep >> 52) & 0x7ff;
        if (((orig_exp + exp_adj) & ~0x7ff) != 0) {
            if (scaled_int < 0.0) return Double.NEGATIVE_INFINITY;
            else return Double.POSITIVE_INFINITY;
        }
        scaled_int_rep += exp_adj << 52;
        double result = Double.longBitsToDouble(scaled_int_rep);
        if (may_underflow) {
            double two48 = (double)(1 << 48);
            return result/two48/two48;
        } else {
            return result;
        }
      }

      public float floatValue() { return (float)doubleValue(); }

      public CR add(CR x) { return new add_CR(this, x); }
      public CR shiftLeft(int n) { check_prec(n); return new shifted_CR(this, n); }
      public CR shiftRight(int n) { check_prec(n); return new shifted_CR(this, -n); }
      public CR assumeInt() { return new assumed_int_CR(this); }
      public CR negate() { return new neg_CR(this); }
      public CR subtract(CR x) { return new add_CR(this, x.negate()); }
      public CR multiply(CR x) { return new mult_CR(this, x); }
      public CR inverse() { return new inv_CR(this); }
      public CR divide(CR x) { return new mult_CR(this, x.inverse()); }
      public CR select(CR x, CR y) { return new select_CR(this, x, y); }
      public CR max(CR x) { return subtract(x).select(x, this); }
      public CR min(CR x) { return subtract(x).select(this, x); }
      public CR abs() { return select(negate(), this); }

      public CR exp() {
        final int low_prec = -10;
        BigInteger rough_appr = get_appr(low_prec);
        if (rough_appr.signum() < 0) return negate().exp().inverse();
        if (rough_appr.compareTo(big2) > 0) {
            CR square_root = shiftRight(1).exp();
            return square_root.multiply(square_root);
        }
        return new prescaled_exp_CR(this);
      }

      static CR two = valueOf(2);

      public static CR PI = four.multiply(four.multiply(atan_reciprocal(5))
                                              .subtract(atan_reciprocal(239)));
      static CR half_pi = PI.shiftRight(1);

      public CR cos() {
        BigInteger rough_appr = get_appr(-1);
        BigInteger abs_rough_appr = rough_appr.abs();
        if (abs_rough_appr.compareTo(big6) >= 0) {
            BigInteger multiplier = rough_appr.divide(big6);
            CR adjustment = PI.multiply(CR.valueOf(multiplier));
            if (multiplier.and(big1).signum() != 0)
                return subtract(adjustment).cos().negate();
            return subtract(adjustment).cos();
        } else if (abs_rough_appr.compareTo(big2) >= 0) {
            CR cos_half = shiftRight(1).cos();
            return cos_half.multiply(cos_half).shiftLeft(1).subtract(one);
        }
        return new prescaled_cos_CR(this);
      }

      public CR sin() { return half_pi.subtract(this).cos(); }

      static final BigInteger low_ln_limit = big8;
      static final BigInteger high_ln_limit = BigInteger.valueOf(16 + 8);
      static final BigInteger scaled_4 = BigInteger.valueOf(4*16);

      public CR ln() {
        final int low_prec = -4;
        BigInteger rough_appr = get_appr(low_prec);
        if (rough_appr.compareTo(big0) < 0) throw new ArithmeticException();
        if (rough_appr.compareTo(low_ln_limit) <= 0) return inverse().ln().negate();
        if (rough_appr.compareTo(high_ln_limit) >= 0) {
            if (rough_appr.compareTo(scaled_4) <= 0) {
                CR quarter = sqrt().sqrt().ln();
                return quarter.shiftLeft(2);
            } else {
                int extra_bits = rough_appr.bitLength() - 3;
                CR scaled_result = shiftRight(extra_bits).ln();
                return scaled_result.add(CR.valueOf(extra_bits).multiply(ln2));
            }
        }
        return simple_ln();
      }

      public CR sqrt() { return new sqrt_CR(this); }
}

abstract class slow_CR extends CR {
    static int max_prec = -64;
    static int prec_incr = 32;
    public BigInteger get_appr(int precision) {
        check_prec(precision);
        if (appr_valid && precision >= min_prec) return scale(max_appr, min_prec - precision);
        int eval_prec = (precision >= max_prec ? max_prec :
                         (precision - prec_incr + 1) & ~(prec_incr - 1));
        BigInteger result = approximate(eval_prec);
        min_prec = eval_prec;
        max_appr = result;
        appr_valid = true;
        return scale(result, eval_prec - precision);
    }
}

class int_CR extends CR {
    BigInteger value;
    int_CR(BigInteger n) { value = n; }
    protected BigInteger approximate(int p) { return scale(value, -p); }
}

class assumed_int_CR extends CR {
    CR value;
    assumed_int_CR(CR x) { value = x; }
    protected BigInteger approximate(int p) {
        if (p >= 0) return value.get_appr(p);
        return scale(value.get_appr(0), -p);
    }
}

class add_CR extends CR {
    CR op1, op2;
    add_CR(CR x, CR y) { op1 = x; op2 = y; }
    protected BigInteger approximate(int p) {
        return scale(op1.get_appr(p-2).add(op2.get_appr(p-2)), -2);
    }
}

class shifted_CR extends CR {
    CR op; int count;
    shifted_CR(CR x, int n) { op = x; count = n; }
    protected BigInteger approximate(int p) { return op.get_appr(p - count); }
}

class neg_CR extends CR {
    CR op;
    neg_CR(CR x) { op = x; }
    protected BigInteger approximate(int p) { return op.get_appr(p).negate(); }
}

class select_CR extends CR {
    CR selector; int selector_sign; CR op1, op2;
    select_CR(CR s, CR x, CR y) {
        selector = s;
        selector_sign = selector.get_appr(-20).signum();
        op1 = x; op2 = y;
    }
    protected BigInteger approximate(int p) {
        if (selector_sign < 0) return op1.get_appr(p);
        if (selector_sign > 0) return op2.get_appr(p);
        BigInteger op1_appr = op1.get_appr(p-1);
        BigInteger op2_appr = op2.get_appr(p-1);
        BigInteger diff = op1_appr.subtract(op2_appr).abs();
        if (diff.compareTo(big1) <= 0) return scale(op1_appr, -1);
        if (selector.signum() < 0) { selector_sign = -1; return scale(op1_appr, -1); }
        selector_sign = 1;
        return scale(op2_appr, -1);
    }
}

class mult_CR extends CR {
    CR op1, op2;
    mult_CR(CR x, CR y) { op1 = x; op2 = y; }
    protected BigInteger approximate(int p) {
        int half_prec = (p >> 1) - 1;
        int msd_op1 = op1.msd(half_prec);
        int msd_op2;
        if (msd_op1 == Integer.MIN_VALUE) {
            msd_op2 = op2.msd(half_prec);
            if (msd_op2 == Integer.MIN_VALUE) return big0;
            CR tmp = op1; op1 = op2; op2 = tmp;
            msd_op1 = msd_op2;
        }
        int prec2 = p - msd_op1 - 3;
        BigInteger appr2 = op2.get_appr(prec2);
        if (appr2.signum() == 0) return big0;
        msd_op2 = op2.known_msd();
        int prec1 = p - msd_op2 - 3;
        BigInteger appr1 = op1.get_appr(prec1);
        int scale_digits = prec1 + prec2 - p;
        return scale(appr1.multiply(appr2), scale_digits);
    }
}

class inv_CR extends CR {
    CR op;
    inv_CR(CR x) { op = x; }
    protected BigInteger approximate(int p) {
        int msd = op.msd();
        int inv_msd = 1 - msd;
        int digits_needed = inv_msd - p + 3;
        int prec_needed = msd - digits_needed;
        int log_scale_factor = -p - prec_needed;
        if (log_scale_factor < 0) return big0;
        BigInteger dividend = big1.shiftLeft(log_scale_factor);
        BigInteger scaled_divisor = op.get_appr(prec_needed);
        BigInteger abs_scaled_divisor = scaled_divisor.abs();
        BigInteger adj_dividend = dividend.add(abs_scaled_divisor.shiftRight(1));
        BigInteger result = adj_dividend.divide(abs_scaled_divisor);
        return scaled_divisor.signum() < 0 ? result.negate() : result;
    }
}

class prescaled_exp_CR extends CR {
    CR op;
    prescaled_exp_CR(CR x) { op = x; }
    protected BigInteger approximate(int p) {
        if (p >= 1) return big0;
        int iterations_needed = -p/2 + 2;
        int calc_precision = p - bound_log2(2*iterations_needed) - 4;
        int op_prec = p - 3;
        BigInteger op_appr = op.get_appr(op_prec);
        BigInteger scaled_1 = big1.shiftLeft(-calc_precision);
        BigInteger current_term = scaled_1;
        BigInteger current_sum = scaled_1;
        int n = 0;
        BigInteger max_trunc_error = big1.shiftLeft(p - 4 - calc_precision);
        while (current_term.abs().compareTo(max_trunc_error) >= 0) {
            n += 1;
            current_term = scale(current_term.multiply(op_appr), op_prec);
            current_term = current_term.divide(BigInteger.valueOf(n));
            current_sum = current_sum.add(current_term);
        }
        return scale(current_sum, calc_precision - p);
    }
}

class prescaled_cos_CR extends slow_CR {
    CR op;
    prescaled_cos_CR(CR x) { op = x; }
    protected BigInteger approximate(int p) {
        if (p >= 1) return big0;
        int iterations_needed = -p/2 + 4;
        int calc_precision = p - bound_log2(2*iterations_needed) - 4;
        int op_prec = p - 2;
        BigInteger op_appr = op.get_appr(op_prec);
        BigInteger current_term;
        int n;
        BigInteger max_trunc_error = big1.shiftLeft(p - 4 - calc_precision);
        n = 0;
        current_term = big1.shiftLeft(-calc_precision);
        BigInteger current_sum = current_term;
        while (current_term.abs().compareTo(max_trunc_error) >= 0) {
            n += 2;
            current_term = scale(current_term.multiply(op_appr), op_prec);
            current_term = scale(current_term.multiply(op_appr), op_prec);
            BigInteger divisor = BigInteger.valueOf(-n).multiply(BigInteger.valueOf(n-1));
            current_term = current_term.divide(divisor);
            current_sum = current_sum.add(current_term);
        }
        return scale(current_sum, calc_precision - p);
    }
}

class integral_atan_CR extends slow_CR {
    int op;
    integral_atan_CR(int x) { op = x; }
    protected BigInteger approximate(int p) {
        if (p >= 1) return big0;
        int iterations_needed = -p/2 + 2;
        int calc_precision = p - bound_log2(2*iterations_needed) - 2;
        BigInteger scaled_1 = big1.shiftLeft(-calc_precision);
        BigInteger big_op = BigInteger.valueOf(op);
        BigInteger big_op_squared = BigInteger.valueOf(op*op);
        BigInteger op_inverse = scaled_1.divide(big_op);
        BigInteger current_power = op_inverse;
        BigInteger current_term = op_inverse;
        BigInteger current_sum = op_inverse;
        int current_sign = 1;
        int n = 1;
        BigInteger max_trunc_error = big1.shiftLeft(p - 2 - calc_precision);
        while (current_term.abs().compareTo(max_trunc_error) >= 0) {
            n += 2;
            current_power = current_power.divide(big_op_squared);
            current_sign = -current_sign;
            current_term = current_power.divide(BigInteger.valueOf(current_sign*n));
            current_sum = current_sum.add(current_term);
        }
        return scale(current_sum, calc_precision - p);
    }
}

class prescaled_ln_CR extends slow_CR {
    CR op;
    prescaled_ln_CR(CR x) { op = x; }
    protected BigInteger approximate(int p) {
        if (p >= 0) return big0;
        int iterations_needed = -p;
        int calc_precision = p - bound_log2(2*iterations_needed) - 4;
        int op_prec = p - 3;
        BigInteger op_appr = op.get_appr(op_prec);
        BigInteger scaled_1 = big1.shiftLeft(-calc_precision);
        BigInteger x_nth = scale(op_appr, op_prec - calc_precision);
        BigInteger current_term = x_nth;
        BigInteger current_sum = current_term;
        int n = 1;
        int current_sign = 1;
        BigInteger max_trunc_error = big1.shiftLeft(p - 4 - calc_precision);
        while (current_term.abs().compareTo(max_trunc_error) >= 0) {
            n += 1;
            current_sign = -current_sign;
            x_nth = scale(x_nth.multiply(op_appr), op_prec);
            current_term = x_nth.divide(BigInteger.valueOf(n * current_sign));
            current_sum = current_sum.add(current_term);
        }
        return scale(current_sum, calc_precision - p);
    }
}

class sqrt_CR extends CR {
    CR op;
    sqrt_CR(CR x) { op = x; }
    final int fp_prec = 50;
    final int fp_op_prec = 60;
    protected BigInteger approximate(int p) {
        int max_prec_needed = 2*p - 1;
        int msd = op.msd(max_prec_needed);
        if (msd <= max_prec_needed) return big0;
        int result_msd = msd/2;
        int result_digits = result_msd - p;
        if (result_digits > fp_prec) {
            int appr_digits = result_digits/2 + 6;
            int appr_prec = result_msd - appr_digits;
            BigInteger last_appr = get_appr(appr_prec);
            int prod_prec = 2*appr_prec;
            BigInteger op_appr = op.get_appr(prod_prec);
            BigInteger prod_prec_scaled_numerator = last_appr.multiply(last_appr).add(op_appr);
            BigInteger scaled_numerator = scale(prod_prec_scaled_numerator, appr_prec - p);
            BigInteger shifted_result = scaled_numerator.divide(last_appr);
            return shifted_result.add(big1).shiftRight(1);
        } else {
            int op_prec = (msd - fp_op_prec) & ~1;
            int working_prec = op_prec - fp_op_prec;
            BigInteger scaled_bi_appr = op.get_appr(op_prec).shiftLeft(fp_op_prec);
            double scaled_appr = scaled_bi_appr.doubleValue();
            if (scaled_appr < 0.0) throw new ArithmeticException();
            double scaled_fp_sqrt = Math.sqrt(scaled_appr);
            BigInteger scaled_sqrt = BigInteger.valueOf((long)scaled_fp_sqrt);
            int shift_count = working_prec/2 - p;
            return shift(scaled_sqrt, shift_count);
        }
    }
}
