import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import SIR
import os

def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

os.chdir("./Images")

Each_city = True
Show_graph = False
Save_graph_t = False

beta, gamma = 0.35, 1/14

I, R = [1], [0]
t = [0]


cities_pop = {'Rio de Janeiro' : 16460000,
            'São Paulo' : 44040000,
            'Minas gerais' : 20870000}
cities_locations = {'Rio de Janeiro' : (1,0.3),
                    'São Paulo' : (0,0),
                    'Minas gerais' : (0.2,1.5)}



corr_cities = np.array([[0,100,50],[100,0,50],[50,50,0]])

cities_travels = pd.DataFrame(corr_cities)
cities_travels.index = cities_pop.keys()
cities_travels.columns = cities_pop.keys()
cities_SIR = {}
n = len(cities_pop)
total_pop = 0


##Declaring SIR for each city in city list
for i in cities_pop.keys():
    cities_SIR[i] = SIR.SIR(cities_pop[i], I[0], R[0], beta, gamma)
    total_pop += cities_pop[i]


c1='green' #blue
c2='red' #green
##Looping through days
for days in range(1, 200):
    t.append(days)
    for keys in cities_pop.keys():
        cities_SIR[keys].Evolve()
    if Save_graph_t:
        g=nx.DiGraph()

        for keys in cities_pop.keys():
            g.add_node(keys)

        # Build your graph
        for i in cities_travels:
            for j in range(len(cities_pop.keys())):
                if cities_travels[i][j] > 0:
                    g.add_edge(i,list(cities_pop.keys())[j])
        colormap = []
        for j in cities_pop.keys():
            ratio = cities_SIR[j].I / (cities_SIR[j].S + cities_SIR[j].R)
            if ratio > 1:
                ratio = 1.
            colormap.append(colorFader(c1, c2, mix = ratio ))
        # Plot it
        nx.draw(g, with_labels = True, edge_color = 'black', \
                node_color = colormap, arrows = True, \
                arrowsize = 10,  connectionstyle='arc3,rad=0.05', \
                pos = cities_locations)
        plt.savefig(fname = str(days))
        plt.clf()


if Each_city:
    for i in cities_pop.keys():
        fig = plt.figure(facecolor = 'w')
        ax = fig.add_subplot(111)
        ax.plot(t, cities_SIR[i].hist_S, 'b', alpha = 0.5, lw = 2, label = 'Susceptible')
        ax.plot(t, cities_SIR[i].hist_I, 'r', alpha = 0.5, lw = 2, label = 'Infected')
        ax.plot(t, cities_SIR[i].hist_R, 'g', alpha = 0.5, lw = 2, label = 'Recovered')
        ax.set_xlabel('Time /days')
        ax.set_ylabel('Number')
        ax.set_ylim(0,cities_pop[i]*1.01)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
        plt.title(i)
        plt.show()
