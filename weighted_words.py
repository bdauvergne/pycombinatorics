'''

Author: Benjamin Dauvergne <benjamin.dauvergne@gmail.com>

Enumerate or index words containing exactly d 1-bits or less thant d 1-bits

'''

def weight(i):
    '''Return the number of 1 bits in the integer i'''
    c = 0
    while i:
        if i & 1:
            c += 1
        i >>= 1
    return c

def counting_d_weight(k, n):
    '''Return the number of words with exactly d 1-bits.

       It's the same as the binomial coefficient C(k, n).
    '''
    if not (0 <= k <= n):
        raise ValueError
    if k == 0:
        return 1
    elif k <= n:
        return (counting_d_weight(k-1,n)*(n-k+1))/k
    return 0

def counting_less_d_weight(d, n):
    '''Return the number of words with at most d 1-bits.
    '''
    assert 0 <= d <= n
    if d == 0:
        return 1
    elif d < n:
        return counting_less_d_weight(d-1,n) + counting_d_weight(d, n)
    else:
        return 2**n

def enumerate_d_weight(d, n):
    '''Enumerate all words with d 1-bits.
    '''
    assert 0 <= d <= n
    if n == 0:
        yield 0
    elif d == 0 and n == 1:
        yield 0
    elif d == 1 and n == 1:
        yield 1
    else:
        j, k = (n/2, n/2+1) if n & 1 == 1 else (n/2, n/2)
        for i in range(max(0, d-k), min(j+1,d+1)):
            l1 = list(enumerate_d_weight(i, j))
            l2 = list(enumerate_d_weight(d-i, k))
            for u in ((x<<k)+y for x in l1 for y in l2):
                yield u

def enumerate_less_d_weight(d, n):
    '''Enumerate all words with at most d 1-bits.
    '''
    assert 0 <= d <= n
    for less_d in range(d+1):
        for u in enumerate_d_weight(less_d, n):
            yield u

def idx_d_weight(i, d, n):
    '''Compute the i-th word with d 1-bits.

       The following assertion is True:

          >>> list(enumerate(enumerate_d_weight(d, n))) == [(i, idx_d_weight(i, d, n)) for i in range(counting_d_weight(d, n))]
    '''
    #print 'idx_d_weight', i, d, n
    assert i < counting_d_weight(d, n), "i is out of bound"
    if d == 0 and n == 1:
        #print '0,1'
        return 0
    elif d == 1 and n == 1:
        #print '1,1'
        return 1
    else:
        j, k = (n/2, n/2+1) if n & 1 == 1 else (n/2, n/2)
        c = 0
        #print 'range', max(0, d-k), min(j+1,d+1)
        for h in range(max(0, d-k), min(j+1,d+1)):
            #print 'c', c
            #print 'i', i
            c1 = counting_d_weight(h, j)
            c2 = counting_d_weight(d-h, k)
            #print 'c1', c1, (h, j), 'c2', c2, (d-h, k)
            count = c1*c2 if c1 and c2 else c1+c2
            #print 'count', count
            if i >= c+count:
                c += count
                #print 'incr c', c
                continue
            elif c1 and not c2:
                #print '1', i-c
                return idx_d_weight(i-c, h, j) << k
            elif c2 and not c1:
                #print '2', i-c
                return idx_d_weight(i-c, d-h, k)
            else:
                x1 = (i-c) / c2
                x2 = (i-c) % c2
                #print '3_<<k', x1, h, j
                #print '3_<<1', x2, d-h, k
                return (idx_d_weight(x1, h, j) << k) + idx_d_weight(x2, d-h, k)

def idx_less_d_weight(i, d, n):
    '''Compute the i-th word with at most d 1-bits.

       The following assertion is True:

          >>> list(enumerate(enumerate_less_d_weight(d, n))) == [(i, idx_less_d_weight(i, d, n)) for i in range(counting_less_d_weight(d, n))]
    '''
    assert i < counting_less_d_weight(d, n)
    if d == 0:
        return 0
    c = counting_less_d_weight(d-1, n)
    if i < c:
        return idx_less_d_weight(i, d-1, n)
    else:
        return idx_d_weight(i-c, d, n)
