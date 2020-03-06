#!/usr/bin/python3
import time
import random
import primitive_polynomials_GF2
import galois_math


def hexprint(arr):
    for el in arr:
        print(hex(el)[2:], ' ', end='')
    print()


def benchmark(irp):
    len = 10000
    field = galois_math.Galois(irp)
    res_file = open("results.txt", "a+")
    k = irp.bit_length() - 1
    r = 1 << k
    nums = [random.randint(r >> 1, r - 1) for _ in range(len)]
    e = random.randint(r >> 1, r - 1)

    def exp(num):
        return field.exp(num, e)

    t0 = time.perf_counter()
    res = list(map(exp, nums))
    t1 = time.perf_counter()
    print(k, 0, t1 - t0, file=res_file)

    def mon_exp(num):
        return field.mon_exp(num, e)

    t0 = time.perf_counter()
    res = list(map(mon_exp, nums))
    t1 = time.perf_counter()
    print(k, 1, t1 - t0, file=res_file)

    def mon_exp_kor(num):
        return field.mon_exp_kor(num, e)

    t0 = time.perf_counter()
    res = list(map(mon_exp_kor, nums))
    t1 = time.perf_counter()
    print(k, 2, t1 - t0, file=res_file)


open("results.txt", "w+")
for irp in primitive_polynomials_GF2.irp_list:
    benchmark(irp)
