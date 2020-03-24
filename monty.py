#!/usr/bin/python3
import time
import random
import primitive_polynomials_GF2
import galois_math
import rfc_polynomials


def hexprint(arr):
    for el in arr:
        print(hex(el)[2:], ' ', end='')
    print()


def benchmark(irp):
    field = galois_math.Galois(irp)
    length = 10
    res_file = open("results.txt", "a+")
    k = irp.bit_length()
    r = 1 << (k - 1)
    nums = [random.randint(r >> 1, r - 1) for _ in range(length)]
    e = random.randint(r >> 1, r - 1)

    def exp(num):
        return field.exp(num, e)

    t0 = time.perf_counter()
    res = list(map(exp, nums))
    t1 = time.perf_counter()
    t_stan = t1 - t0
    print(k, 0, t_stan, file=res_file)
    print(res[0])

    def mon_exp(num):
        return field.mon_exp(num, e)

    t0 = time.perf_counter()
    res = list(map(mon_exp, nums))
    t1 = time.perf_counter()
    t_mont = t1 - t0
    print(k, 1, t_mont, file=res_file)
    print(res[0])

    def mon_exp_kor(num):
        return field.mon_exp_kor(num, e)

    t0 = time.perf_counter()
    res = list(map(mon_exp_kor, nums))
    t1 = time.perf_counter()
    t_par_mont = t1 - t0
    print(k, 2, t_par_mont, file=res_file)
    print(res[0])

    print("Percentages:", "%0.2f" % (100 - (t_par_mont/t_stan*100)), "percent to standard and", "%0.2f" % (100 - (t_par_mont/t_mont*100)), "percent to ordinary Montgomery")
    print("Also:", "%0.2f" % (100 - (t_mont/t_stan*100)), "percent Montgomery to standard")


open("results.txt", "w+")
for irp in rfc_polynomials.irp_list:
    benchmark(irp)
