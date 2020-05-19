#!/usr/bin/python3
import time
import random
import primitive_polynomials_GF2
import galois_math
import rfc_polynomials

mode = "num"

filename = "results.txt"
irp_list = primitive_polynomials_GF2.irp_list
if mode == "bignum":
    filename = "results_bignum.txt"
    irp_list = rfc_polynomials.irp_list


def hexprint(arr):
    for el in arr:
        print(hex(el)[2:], ' ', end='')
    print()


def benchmark(irp):
    field = galois_math.Galois(irp)
    field.__mon_init__()
    length = 10000
    res_file = open(filename, "a+")
    k = irp.bit_length()
    print(k)
    r = 1 << (k - 1)
    nums = [random.randint(r >> 1, r - 1) for _ in range(length)]
    e = random.randint(r >> 1, r - 1)

    res = []
    t0 = time.perf_counter()
    for num in nums:
        res.append(field.exp_ltor(num, e))
    t1 = time.perf_counter()
    t_stan = t1 - t0
    print(k, 0, t_stan, file=res_file)
    res_sta = res[0]

    res = []
    t0 = time.perf_counter()
    for num in nums:
        res.append(field.mon_exp(num, e))
    t1 = time.perf_counter()
    t_mont = t1 - t0
    print(k, 1, t_mont, file=res_file)
    res_mon = res[0]

    res = []
    t0 = time.perf_counter()
    for num in nums:
        res.append(field.mon_exp_kor(num, e))
    t1 = time.perf_counter()
    t_par_mont = t1 - t0
    print(k, 2, t_par_mont, file=res_file)
    res_acc = res[0]

    if (res_sta != res_mon) | (res_sta != res_acc):
        print("ERROR")
        print(res_sta)
        print(res_mon)
        print(res_acc)

    print("Percentages:", "%0.2f" % (100 - (t_par_mont/t_stan*100)), "percent to standard and",
          "%0.2f" % (100 - (t_par_mont/t_mont*100)), "percent to ordinary Montgomery")
    print("Also:", "%0.2f" % (100 - (t_mont/t_stan*100)), "percent Montgomery to standard")


for irp in irp_list:
    benchmark(irp)
