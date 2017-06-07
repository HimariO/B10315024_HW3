import math
import random
import sympy as sp
import threading
from queue import Queue


def SqMut(base, p, n):
    H = [int(i) for i in bin(p)[2:]]
    y = base
    for h in H[1:]:
        y = y**2 % n
        if h == 1:
            y *= base
            y %= n
    return y


def gcd(a, b, d):
    i_ = 1
    j_ = 0
    c = a

    i = 0
    j = 1
    d = b

    while True:
        q = c // d
        r = c % d
        t = 0
        if r == 0:
            break
        c = d
        d = r
        t = i_
        i_ = i
        i = t - q * i
        t = j_
        j_ = j
        j = t - q * j
    return i, j


class MRtester:
    def __init__(self):
        self.threads = []
        self.thread_start = []

        for _ in range(20):
            thr = threading.Thread(target=self.run_test, name="testThread[%d]" % _)
            thr.daemon = True
            # thr.start()
            self.threads.append(thr)
            self.thread_start.append(False)

        self.task_queue = Queue()
        self.task_result = []

    @staticmethod
    def posttest(u, n, t):
        a = random.randrange(2, n)
        x = pow(a, u, n)
        # print('value')
        if x == 1 or x == n - 1:
            return True
        for i in range(0, t - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                return True
            # elif x == 1:
            #     return False
        return False

    def run_test(self):
        while True:
            u, n, t = self.task_queue.get()
            self.task_result.append(MRtester.posttest(u, n, t))
            # sp.ntheory.isprime(n)
            self.task_queue.task_done()
            # print('I RUN onece.')
        # print('Im done.')

    def test(self, n):
        if n < 2 or n % 2 == 0:
            return False
        u = n - 1
        t = 0

        while (u % 2) == 0:
            u = u // 2
            t += 1
        # print(a, ' ', u, ' ', t)

        self.task_result.clear()

        for i in range(20):
            self.task_queue.put((u, n, t))

        for ID, thr in zip(range(len(self.threads)), self.threads):
            if not self.thread_start[ID]:
                thr.start()
                self.thread_start[ID] = True

        self.task_queue.join()
        # print(self.task_result)
        return all(self.task_result) and len(self.task_result) != 0


class RSA:
    def __init__(self, key_len=1024):
        print("RSA Init...")

        self.key_bits = key_len
        self.p = self._prime(2**(self.key_bits // 2), 2**((self.key_bits // 2) + 1))
        print('Got p')
        self.q = self._prime(2**(self.key_bits // 2), 2**((self.key_bits // 2) + 1))
        print('Got q')
        self.e = self._get_e()
        print('Got e')
        self.d = self._get_d()
        print('Got d')
        self.n = self.p * self.q

    def _prime(self, start, end):
        range_size = end - start
        # times = int(range_size / (math.log(range_size) ** 2))
        times = int(math.log(range_size)) ** 2
        # step = int(range_size / times)

        tester = MRtester()
        counter = 0

        while True:
            N = random.randint(start, end)
            counter += 1
            if tester.test(N):
                return N
            else:
                if counter > times:
                    break
                # print("%d / %d" % (counter, times))
        raise ValueError("Seen like there is no prime in range[%d, %d]!" % (start, end))

    def _relatively_prime(self, a, b):
        for n in range(2, min(a, b) + 1):
            if a % n == b % n == 0:
                return False
        return True

    def _CRTpow(self, X):
        q_inv, _ = gcd(self.q, self.p, 1)
        q_inv %= self.p

        m1 = SqMut(X, self.d, self.p)
        m2 = SqMut(X, self.d, self.q)
        h = (q_inv * (m1 - m2)) % self.p
        m = m2 + h * self.q
        return m

    def _get_e(self):
        assert self.p is not None and self.q is not None
        return 17
        pq = (self.p - 1) * (self.q - 1)

        e = 3
        while True:
            if self._relatively_prime(e, pq):
                return e
            e += 2
            if e > pq:
                break
        raise ValueError("Seen like there is no relative prime to (p-1)(q-1) in range[%d, %d]!" % (3, pq))

    def _get_d(self):
        assert self.p is not None and self.q is not None and self.e is not None

        pq = (self.p - 1) * (self.q - 1)
        i, j = gcd(self.e, pq, 1)
        return i % pq

    def encrpy(self, x):
        y = SqMut(x, self.e, self.n)
        return y

    def decrpy(self, y):
        return self._CRTpow(y)


# if __name__ == "__main__":
#     error_n = 0
#     test_n = 1000
#
#     for _ in range(test_n):
#         a = random.randrange(3, 10000)
#         A = all([MRtest(a) for __ in range(10)])
#         B = sp.ntheory.isprime(a)
#         print(_, ' ', A, ', ', B)
#         if A != B:
#             error_n += 1
#
#     print('Error rate: %f' % (error_n / test_n))
