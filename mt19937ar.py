class MT19937ar:
    
    def __init__(self):
        self._mt = [0] * 624
        self._mti = 625
    
    def init_genrand(self, s):
        self._mt[0] = s & 0xffffffff
        for i in range(1, 624):
            self._mt[i] = 1812433253 * (self._mt[i - 1] ^ (self._mt[i - 1] >> 30)) + i
            self._mt[i] &= 0xffffffff
        self._mti = 624
        
    def init_by_array(self, RTseed):
        self.init_genrand(19650218)
        i, j, l = 1, 0, len(RTseed)
        for _ in range(max(624, l)):
            self._mt[i] = (self._mt[i] ^ ((self._mt[i - 1] ^ (self._mt[i - 1] >> 30)) * 1664525)) + RTseed[j] + j
            self._mt[i] &= 0xffffffff
            i += 1
            if i >= 624:
                self._mt[0] = self._mt[623]
                i = 1
            j += 1
            if j >= l:
                j = 0
    
        for _ in range(623):
            self._mt[i] = (self._mt[i] ^ ((self._mt[i - 1] ^ (self._mt[i - 1] >> 30)) * 1566083941)) - i
            self._mt[i] &= 0xffffffff
            i += 1
            if i >= 624:
                self._mt[0] = self._mt[623]
                i = 1
        self._mt[0] = 0x80000000
    
    def genrand_int32(self):
        y = 0
        mag01 = [0x0, 0x9908b0df]
        if self._mti >= 624:
            if self._mti == 625:
                self.init_genrand(5489)
            
            for kk in range(227):
                y = (self._mt[kk] & 0x80000000) | (self._mt[kk + 1] & 0x7fffffff)
                self._mt[kk] = self._mt[kk + 397] ^ (y >> 1) ^ mag01[y & 1]
            
            for kk in range(227, 623):
                y = (self._mt[kk] & 0x80000000) | (self._mt[kk + 1] & 0x7fffffff)
                self._mt[kk] = self._mt[kk - 227] ^ (y >> 1) ^ mag01[y & 1]
            
            y = (self._mt[623] & 0x80000000) | (self._mt[0] & 0x7fffffff)
            self._mt[623] = self._mt[396] ^ (y >> 1) ^ mag01[y & 1]
            self._mti = 0
        
        y = self._mt[self._mti]
        self._mti += 1
        
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        y ^= (y >> 18)
        
        return y
    
    def genrand_int31(self):
        return self.genrand_int32() >> 1
    
    def genrand_real1(self):
        # [0, 1]
        return self.genrand_int32() * 1.0 / 4294967295.0
    
    def genrand_real2(self):
        # [0, 1)
        return self.genrand_int32() * 1.0 / 4294967296.0
    
    def genrand_real3(self):
        # (0, 1)
        return (self.genrand_int32() + 0.5) * 1.0 / 4294967295.0
    
    def genrand_res53(self):
        a = genrand_int32() >> 5
        b = genrand_int32() >> 6
        return (a * 67108864.0 + b) * 1.0 / 9007199254740992.0