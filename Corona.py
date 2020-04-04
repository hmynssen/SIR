import numpy as np
import matplotlib.pyplot as plt
import SIR

beta, gamma = 0.2, 1./10
N = 210000000
S, I, R = [N], [1], [0]
t = [0]


sirVariables = SIR.SIR(N, S[0], I[0], R[0], beta, gamma)

for i in range(1, 200):
    t.append(i)
    aS, aI, aR = sirVariables.Evolve()
    beta = beta*(1 + 0.5*np.sin((i/50)*2*np.pi))
    sirVariables.Setbeta(beta)
    S.append(aS)
    I.append(aI)
    R.append(aR)



if True:
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111)#, axis_bgcolor='#dddddd', axisbelow=True)
    ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
    ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
    ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    ax.set_xlabel('Time /days')
    ax.set_ylabel('Number (1000s)')
    ax.set_ylim(0,N*1.01)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.show()
