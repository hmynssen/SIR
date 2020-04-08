import numpy as np

class SIR():
    def __init__(self, N = 1, I = 1, Immunes = 0, Deaths = 0, beta = 0.2, gamma = 1/10, death_ratio = 0):
        # Total population, N.
        self.N, self.I, self.Immunes, self.Deaths, self.beta, self.gamma = N, I, Immunes, Deaths, beta, gamma

        # Everyone else, S0, is susceptible to infection initially.
        self.S = self.N - self.I - self.Immunes - self.Deaths

        self.gamma1 = (1 - death_ratio) * gamma ##constant to calculate Survivors
        self.gamma2 = death_ratio * gamma ##constant for the deads
        self.death_ratio = death_ratio ##need to store curent death_ratio in order
                                        ## to update it if asked

        ##Historical Variables
        self.hist_S = [self.S]
        self.hist_I = [self.I]
        self.hist_Immunes = [self.Immunes]
        self.hist_Deaths = [self.Deaths]


    ##setting new variables on the go
    def SetSEIR(**variables):
        varlist = ["N", "S", "I0", "I1", "I2", "Immunes", "Deaths", "beta", "gamma"]
        for i, value in variables.items():
            if i in varlist:
                setattr(self, i, value)
            else:
                print("Could not set " + str(i) + "=" + str(value) + " to any attribute\nWorng attribute name " + str(i))


    ## Increase or decrease variables by a certain ammount
    def AddSEIR(**variables):
        varlist = ["N", "S", "I0", "I1", "I2", "Immunes", "Deaths", "beta", "gamma"]
        for i, value in variables.items():
            if i in varlist:
                add = value + getattr(self, i)
                setattr(self, i, add)
            else:
                print("Could not add " + str(i) + "=" + str(value) + " to any attribute\nWorng attribute name " + str(i))


    # The SIR model differential equations.
    def Evolve(self):
        ##Evolve the system by the following rules/EDO
        dS = - self.S * self.beta * self.I / self.N


        ##  The I0 population, since it is assymptomatic,
        ##doesn't die, they will spread the desease and get immune
        dI = self.beta * self.S * self.I / self.N - \
            self.gamma1 * self.I

        dR1 = self.gamma1 * self.I
        dR2 = self.gamma2 * self.I

        ## Next number
        self.S += dS
        self.I += dI
        self.Immunes += dR1
        self.Deaths += dR2
        self.hist_S.append(self.S)
        self.hist_I.append(self.I)
        self.hist_Immunes.append(self.Immunes)
        self.hist_Deaths.append(self.Deaths)




class SEIR3():
    def __init__(self, N = 1, I0 = 1, I1 = 1, I2 = 1, Immunes = 0, Deaths = 0, beta = 0.8, \
                gammaI0_I1 = 1/6, gammaI0_R1 = 1/10, gammaI1_I2 = 1/3, gammaI1_R1 = 1/9, gammaI2_R1 = 1/14, gammaI2_R2 = 1/5):
        # Initial Parameters
        self.N, self.I0, self.I1, self.I2, self.Immunes, self.Deaths, self.beta = \
            N,  I0 ,     I1,      I2,      Immunes,      Deaths,      beta

        # All the gammas transitions
        self.gammaI0_I1, self.gammaI0_R1, self.gammaI1_I2, self.gammaI1_R1, self.gammaI2_R1, self.gammaI2_R2 = \
        gammaI0_I1,      gammaI0_R1,      gammaI1_I2,       gammaI1_R1,     gammaI2_R1,      gammaI2_R2


        # Everyone else, S0, is susceptible to infection initially.
        self.S = self.N - self.I0 - self.I1 - self.I2 - self.Immunes - self.Deaths


        ##Historical Variables
        self.hist_S = [self.S]
        self.hist_I0 = [self.I0]
        self.hist_I1 = [self.I1]
        self.hist_I2 = [self.I2]
        self.hist_Immunes = [self.Immunes]
        self.hist_Deaths = [self.Deaths]

        ##Aux Historical variables for each recovered
        self.hist_I0Im = [0]
        self.hist_I1Im = [0]
        self.hist_I2Im = [0]



    ##setting new variables on the go

    def SetSEIR(**variables):
        varlist = ["N", "S", "I0", "I1", "I2", "Immunes", "Deaths", "beta", \
                    "gammaI0_I1", "gammaI0_R2", "gammaI1_I2", "gammaI1_R2", "gammaI2_R1", "gammaI2_R2"]
        for i, value in variables.items():
            if i in varlist:
                setattr(self, i, value)
            else:
                print("Could not set " + str(i) + "=" + str(value) + " to any attribute\nWorng attribute name " + str(i))


    ## Increase or decrease variables by a certain ammount
    def AddSEIR(**variables):
        varlist = ["N", "S", "I0", "I1", "I2", "Immunes", "Deaths", "beta", \
                    "gammaI0_I1", "gammaI0_R2", "gammaI1_I2", "gammaI1_R2", "gammaI2_R1", "gammaI2_R2"]
        for i, value in variables.items():
            if i in varlist:
                add = value + getattr(self, i)
                setattr(self, i, add)
            else:
                print("Could not add " + str(i) + "=" + str(value) + " to any attribute\nWorng attribute name " + str(i))



    # The SEIR model differential equations.
    def Evolve(self):
        ##Evolve the system by the following rules/EDO
        dS = - self.beta * self.S * (self.I0 + self.I1 + self.I2) / self.N


        ##  The I0 population, since it is assymptomatic,
        ##doesn't die, they will spread the desease and get immune
        dI0 = self.beta * self.S * self.I0 / self.N - \
            self.gammaI0_I1 * self.I0 -\
            self.gammaI0_R1 * self.I0

        ## Minor health issues
        dI1 = self.gammaI0_I1 * self.I0 - \
            self.gammaI1_I2 * self.I1 - \
            self.gammaI1_R1 * self.I2

        dI2 = self.gammaI1_I2 * self.I1 - \
            self.gammaI2_R1 * self.I2 - \
            self.gammaI2_R2 * self.I2

        ## R1 = Immunes
        dR1 = self.gammaI2_R1 * self.I2 + \
                self.gammaI1_R1 * self.I1 + \
                self.gammaI0_R1 * self.I0

        ## R2 = Dead
        dR2 = self.gammaI2_R2 * self.I2

        ## Next number
        self.S += dS
        self.I0 += dI0
        self.I1 += dI1
        self.I2 += dI2
        self.Immunes += dR1
        self.Deaths += dR2

        ##History
        self.hist_S.append(self.S)
        self.hist_I0.append(self.I0)
        self.hist_I1.append(self.I1)
        self.hist_I2.append(self.I2)
        self.hist_Immunes.append(self.Immunes)
        self.hist_Deaths.append(self.Deaths)
        self.hist_I0Im.append(self.hist_I0Im[len(self.hist_I0Im) - 1] + self.gammaI0_R1 * self.I0)
        self.hist_I1Im.append(self.hist_I1Im[len(self.hist_I1Im) - 1] + self.gammaI1_R1 * self.I1)
        self.hist_I2Im.append(self.hist_I2Im[len(self.hist_I2Im) - 1] + self.gammaI2_R1 * self.I2)
