#!/usr/bin/python3
import time
import random
import primitive_polynomials_GF2
import rfc_polynomials
import galois


def htoi(n):
    return int(n, 16)


def btoi(n):
    return int(n, 2)


def hexprint(arr):
    for el in arr:
        print(hex(el)[2:], ' ', end='')
    print()


def benchmark(irp):
    res_file = open("results.txt", "a+")
    k = irp.bit_length()
    r = 1 << (k - 1)
    nums = [random.randint(r >> 1, r) for _ in range(1000000)]
    e = random.randint(r >> 1, r)

    def exp(num):
        return galois.exp_ltor(num, e, irp)

    t0 = time.perf_counter()
    res = map(exp, nums)
    t1 = time.perf_counter()
    t_stan = t1 - t0
    print(k, 0, t_stan, file=res_file)

    def mon_exp(num):
        return galois.mon_exp(num, e, irp)

    t0 = time.perf_counter()
    res = map(mon_exp, nums)
    t1 = time.perf_counter()
    t_mont = t1 - t0
    print(k, 1, t_mont, file=res_file)

    def mon_exp_kor(num):
        return galois.mon_exp_kor(num, e, irp)

    t0 = time.perf_counter()
    res = map(mon_exp_kor, nums)
    t1 = time.perf_counter()
    t_par_mont = t1 - t0
    print(k, 2, t_par_mont, file=res_file)
    print("Percentages:", "%0.2f" % (100 - (t_par_mont/t_stan*100)), "percent to standard and", "%0.2f" % (100 - (t_par_mont/t_mont*100)), "percent to ordinary Montgomery")
    print("Also:", "%0.2f" % (100 - (t_mont/t_stan*100)), "percent Montgomery to standard")


# irp = (1 << 984) + (1 << 24) + (1 << 9) + (1 << 3) + 1
open("results.txt", "w+")
for irp in rfc_polynomials.irp_list:
    benchmark(irp)

# a_mont = galois.mon_mult(a, r_sq)
# b_mont = galois.mon_mult(b, r_sq)
# c_mont = galois.mon_mult(a_mont, b_mont)
# a_sq_mont = galois.mon_square(a_mont)
# c_mont_par, a_sq_mont_par = galois.mon_mult_and_square(a_mont, b_mont)
# print('c_mont', bin(c_mont)[2:])
# print('c_mont_par', bin(c_mont_par)[2:])
# print('a_sq_mont', bin(a_sq_mont)[2:])
# print('a_sq_mont_par', bin(a_sq_mont_par)[2:])
# c = galois.mon_redc(c_mont)
# print('c', bin(c)[2:])
# a_sq = galois.mon_redc(a_sq_mont)
# print('a_sq', bin(a_sq)[2:])
# print('dumb_exp', bin(galois.dumb_exp(a, e, irp))[2:])
# print('exp', bin(galois.exp(a, e, irp))[2:])
# print('exp_ltor', bin(galois.exp_ltor(a, e, irp))[2:])
# print('mont_exp', bin(galois.mon_exp(a, e, irp))[2:])
# print('mont_exp_kor', bin(galois.mon_exp_kor(a, e, irp))[2:])


'''
a = 10
b = 13
n = 255
k = n.bit_length()
r = 1 << k
_, n_inv, _ = xgcd(n, r)
n_tick = n_inv * -1 if n_inv < 0 else r - n_inv
r_sq_mont = r * r % n
a_mont = mon_mult(a, r_sq_mont, n, n_tick, k)
b_mont = mon_mult(b, r_sq_mont, n, n_tick, k)
c = mon_redc(mon_mult(a_mont, b_mont, n, n_tick, k), n, n_tick, k)
print(c)
print(mon_mult_bit(mon_mult_bit(a, b, n), 1, n))

print("exp test")
a = 4
e = 7
n = 11
print(pow(a, e, n))
print(mon_exp(a, e, n))
print(mon_exp_bit(a, e, n))


# multiplication speed test
# Example:
# Native Python: 0.0030524000000000037
# Montgomery: 0.021069899999999996
bitnum = 16
print("MULTIPLICATION")
nums = [random.randint(1 << bitnum - 1, 1 << bitnum) for _ in range(10000)]
multiplier = random.randint(1 << bitnum - 1, 1 << bitnum)
n = (1 << bitnum) + 1


def default_mod_mult(num):
    s = (num * multiplier) % n
    return s


t0 = time.perf_counter()
res_dumb = list(map(default_mod_mult, nums))
t1 = time.perf_counter()
print("Native Python:", t1 - t0)

k = n.bit_length()
r = 1 << k
_, n_inv, _ = xgcd(n, r)
n_tick = n_inv * -1 if n_inv < 0 else r - n_inv
multiplier_mont = multiplier * r % n
r_sq_mont = r * r % n


def mont_mod_mult(num):
    num_mont = decimal.mon_mult(num, r_sq_mont, n, n_tick, k)
    t = decimal.mon_mult(num_mont, multiplier_mont, n, n_tick, k)
    s = decimal.mon_redc(t, n, n_tick, k)
    return s


t0 = time.perf_counter()
res_mont = list(map(mont_mod_mult, nums))
t1 = time.perf_counter()
print("Montgomery:", t1 - t0)

def dumb_mod_mult(a, e, n):
    x = 1
    for i in range(e):
        x *= a
        x %= n
    return x

# Exponentiation speed test
# Example
# Native Python: 0.00011579999999999924
# Montgomery: 5.1999999999996493e-05
print("EXPONENTIATION")
print(nums[0]," to the power of ", multiplier)
t0 = time.perf_counter()
res_dumb = dumb_mod_mult(nums[0],multiplier,n)
t1 = time.perf_counter()
print("Native Python:", t1 - t0)
t0 = time.perf_counter()
res_mont = decimal.mon_exp(nums[0], multiplier, n)
t1 = time.perf_counter()
print("Montgomery:", t1 - t0)
print(res_mont == res_dumb)
'''
