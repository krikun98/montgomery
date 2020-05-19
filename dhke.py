import galois_math
import rfc_polynomials
import primitive_polynomials_GF2
import random
import time


def benchmark(prime_list):
    test_length = 10
    for prime in prime_list:
        field = galois_math.Galois(prime)
        field.__mon_init__()
        g = 2
        for i in range(test_length):
            print(field.k)
            res_file = open("results_dhke.txt", "a+")
            a = random.randint(field.r >> 1, field.r - 1)
            b = random.randint(field.r >> 1, field.r - 1)
            t0 = time.perf_counter()
            g_a = field.exp_ltor(g, a)
            g_b = field.exp_ltor(g, b)
            k_a = field.exp_ltor(g_b, a)
            k_b = field.exp_ltor(g_a, b)
            t1 = time.perf_counter()
            if k_a != k_b:
                print("ERROR0", field.k)
                print(a)
                print(b)
            k_sta_a = k_a
            k_sta_b = k_b
            print(field.k, '0', t1 - t0, file=res_file)
            t0 = time.perf_counter()
            g_a = field.mon_exp(g, a)
            g_b = field.mon_exp(g, b)
            k_a = field.mon_exp(g_b, a)
            k_b = field.mon_exp(g_a, b)
            t1 = time.perf_counter()
            if k_a != k_b:
                print("ERROR1", field.k)
                print(a)
                print(b)
                print(g_a)
                print(g_b)
                print(k_a)
                print(k_b)
            k_mon_a = k_a
            k_mon_b = k_b
            print(field.k, '1', t1 - t0, file=res_file)
            t0 = time.perf_counter()
            g_a = field.mon_exp_kor(g, a)
            g_b = field.mon_exp_kor(g, b)
            k_a = field.mon_exp_kor(g_b, a)
            k_b = field.mon_exp_kor(g_a, b)
            t1 = time.perf_counter()
            if k_a != k_b:
                print("ERROR2", field.k)
                print(a)
                print(b)
                print(g_a)
                print(g_b)
                print(k_a)
                print(k_b)
            k_acc_a = k_a
            k_acc_b = k_b
            print(field.k, '2', t1 - t0, file=res_file)
            if (k_acc_a != k_mon_a) | (k_sta_a != k_acc_a):
                print("ERROR3", field.k)
                print(a)
                print(b)
                print("Differing k:")
                print(k_sta_a)
                print(k_sta_b)
                print(k_mon_a)
                print(k_mon_b)
                print(k_acc_a)
                print(k_acc_b)


benchmark(rfc_polynomials.irp_list[6:])
