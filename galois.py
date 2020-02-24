def add(a, b):
    return a ^ b


def mult(a, b, irp=int("100011011", 2)):
    k = irp.bit_length() - 1
    irp_mult = irp - (1 << k)
    p = 0
    while a > 0 and b > 0:
        c = 0
        if b & 1:
            p ^= a
        b >>= 1
        a <<= 1
        if a & 1 << k:
            c = 1
            a -= 1 << k
        if c & 1:
            a ^= irp_mult
    return p


def dumb_exp(a, e, irp=int("100011011", 2)):
    c = 1
    for i in range(e):
        c = mult(c, a, irp)
    return c


def exp(a, e, irp=int("100011011", 2)):
    c = 1
    r = a
    while e > 0:
        if e & 1:
            c = mult(c, r, irp)
        e >>= 1
        if e > 0:
            r = mult(r, r, irp)
    return c


def exp_ltor(a, e, irp=int("100011011", 2)):
    c = 1
    for i in range(e.bit_length()-1, -1, -1):
        c = mult(c, c, irp)
        if e & 1 << i:
            c = mult(c, a, irp)
    return c


def gf2divmod(avec, bvec):
    na = avec[0].bit_length()
    nd = bvec[0].bit_length()
    i = na - nd
    q = 0
    test = 1 << (na - 1)
    while i >= 0:
        if (avec[0] & test) != 0:
            avec = [a ^ (d << i) for (a, d) in zip(avec, bvec)]
            q |= (1 << i)
        i -= 1
        test >>= 1
    r = avec
    return q, r


def blankinship(a, b):
    arow = [a, 1, 0]
    brow = [b, 0, 1]
    while True:
        (_, rrow) = gf2divmod(arow, brow)
        if rrow[0] == 0:
            break
        arow = brow
        brow = rrow
    return tuple(brow)


def inv(a, irp=int("100011011", 2)):
    _, u, _ = blankinship(a, irp)
    return u


def mon_redc(a, irp=int("100011011", 2)):
    r = 1 << irp.bit_length() - 1
    _, irp_tick, r_inv = blankinship(irp, r)
    m = (mult((a & (r - 1)), irp_tick, irp) & (r - 1))
    t = mult((a ^ mult(m, irp, irp)), r_inv)
    if t > irp:
        return t ^ irp
    else:
        return t


def dumb_mon_mult(a, b, irp=int("100011011", 2)):
    t = mult(a, b, irp)
    return mon_redc(t, irp)


def mon_mult(a, b, irp=int("100011011", 2)):
    c = 0
    for i in range(0, irp.bit_length() - 1):
        if (1 << i) & a:
            c = c ^ b
        if 1 & c:
            c = c ^ irp
        c >>= 1
    return c


def mon_square(a, irp=int("100011011", 2)):
    c = 0
    k = irp.bit_length()
    for i in range(k-1):
        c += (a & 1) << 2 * i
        a >>= 1
    for i in range(k-1):
        if c & 1:
            c ^= irp
        c >>= 1
    return c


def mon_exp(a, e, irp=int("100011011", 2)):
    k = irp.bit_length() - 1
    r = 1 << k
    rt = r ^ irp
    r_sq = mult(rt, rt, irp)
    c = mon_mult(1, r_sq, irp)
    m = mon_mult(a, r_sq, irp)
    for i in range(k):
        if e & (1 << i):
            c = mon_mult(c, m, irp)
        m = mon_square(m, irp)
    return mon_mult(c, 1, irp)


def mon_mult_and_square(m, c, irp=int("100011011", 2)):
    t = m
    mul = 0
    sqr = 0
    for i in range(irp.bit_length() - 2, -1, -1):
        if t & 1:
            t = t ^ irp
        t >>= 1
        if c & (1 << i):
            mul ^= t
        if m & (1 << i):
            sqr ^= t
    return sqr, mul


def mon_exp_kor(a, e, irp=int("100011011", 2)):
    k = irp.bit_length() - 1
    r = 1 << k
    rt = r ^ irp
    r_sq = mult(rt, rt, irp)
    c = mon_mult(1, r_sq, irp)
    m = mon_mult(a, r_sq, irp)
    for i in range(k):
        if e & (1 << i):
            m, c = mon_mult_and_square(m, c, irp)
        else:
            m = mon_square(m, irp)
    return mon_mult(c, 1, irp)
