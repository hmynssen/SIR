class SIR():
    def __init__(self, N, S, I, R, beta, gamma):
        # Total population, N.
        self.N, self.I, self.R, self.beta, self.gamma = N, I, R, beta, gamma

        # Everyone else, S0, is susceptible to infection initially.
        self.S = N - self.I - self.R


    def SetN(self, N):
        self.N = N
    def SetS(self, S):
        self.S = S
    def SetI(self, I):
        self.I = I
    def SetR(self, R):
        self.R = R
    def SetNSIR(self, N, S, I, R):
        self.N = N
        self.S = S
        self.I = I
        self.R = R
    def SetSIR(self, S, I, R):
        self.S = S
        self.I = I
        self.R = R
    def Setbeta(self, beta):
        self.beta = beta
    def Setgamma(self, gamma):
        self.gamma = gamma

    def AddN(self, N):
        self.N += N
    def AddS(self, S):
        self.S += S
    def AddI(self, I):
        self.I += I
    def AddR(self, R):
        self.R += R
    def AddNSIR(self, N, S, I, R):
        self.N += N
        self.S += S
        self.I += I
        self.R += R
    def AddSIR(self, S, I, R):
        self.S += S
        self.I += I
        self.R += R
    # The SIR model differential equations.
    def Evolve(self):
        dSdt = -self.beta * self.S * self.I / self.N
        dIdt = self.beta * self.S * self.I / self.N - self.gamma * self.I
        dRdt = self.gamma * self.I
        self.S += dSdt
        self.I += dIdt
        self.R += dRdt
        return self.S, self.I, self.R
