import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import EpidemicModel
import os

def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

Each_city = True
Show_graph = False
Save_graph_t = False

beta, gamma = 0.35, 1/14

I, R = [1], [0]
t = [0]

with open("ListaCapitaiscsv.csv") as Lista:
    cities = pd.read_csv(Lista, delimiter = ";", decimal = ",")

cities = cities.sort_values(by = ['Capital'], ascending = True)
cities_number = len(list(cities['Capital']))

cities_locations = {}
for i in list(cities['Capital']):
    x = cities.loc[cities['Capital'] == i, 'x'].item()*10
    y = cities.loc[cities['Capital'] == i, 'y'].item()*10
    cities_locations[i] = (x,y)


corr_cities = np.array( [[1] * cities_number] * cities_number )

for i in range(cities_number):
    for j in range(cities_number):
        if i == j:
            corr_cities[i][j] = 0

cities_travels = pd.DataFrame(corr_cities)
cities_travels.index = cities['Capital']
cities_travels.columns = cities['Capital']
cities_SIR = {}
total_pop = 0


##Declaring SIR for each city in city list
for i in list(cities['Capital']):
    pop = cities.loc[cities['Capital'] == i, 'Populacao'].item()
    cities_SIR[i] = EpidemicModel.SEIR3(N = pop)#, I = I[0], Immunes = 0, Deaths = 0, beta = beta, gamma = gamma, death_ratio = 3/100)
    total_pop += pop


c1='#14de32' #blue
c2='#e81005' #green

if Save_graph_t:
    os.chdir("./Images")

##Looping through days
for days in range(1, 200):
    t.append(days)
    for keys in list(cities['Capital']):
        cities_SIR[keys].Evolve()

    if Save_graph_t:
        g=nx.DiGraph()

        for keys in list(cities['Capital']):
            g.add_node(keys)

        # Build your graph
        for i in cities_travels:
            for j in range(cities_number):
                if cities_travels[i][j] > 0:
                    g.add_edge(i,list(cities['Capital'])[j])
                    a = 0
        colormap = []
        for j in list(cities['Capital']):
            ratio = cities_SIR[j].I / (cities_SIR[j].S + cities_SIR[j].Immune + cities_SIR[j].Deaths)
            if ratio > 1:
                ratio = 1.
            colormap.append(colorFader(c1, c2, mix = ratio ))
        # Plot it
        fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (11, 11))# dpi = 100)
        nx.draw(g, with_labels = True, edge_color = '#747678', width = 0.5, \
                node_color = colormap, arrows = True, \
                arrowsize = 10,  connectionstyle='arc', \
                pos = cities_locations, font_size = 14)
        ax.set_facecolor("#c9ddff")
        plt.savefig(fname = str(days))
        plt.clf()


if Each_city:
    for i in list(cities['Capital']):
        m = len(cities_SIR[i].hist_S)
        fig = plt.figure(facecolor = 'w')
        ax = fig.add_subplot(111)
        ax.plot(t, cities_SIR[i].hist_S, 'b', alpha = 0.5, lw = 2, label = 'Susceptible')
        try:
            ax.plot(t, cities_SIR[i].hist_I, 'r', alpha = 0.5, lw = 2, label = 'Infected')
        except:
            ax.plot(t, cities_SIR[i].hist_I0, '#730909', alpha = 0.5, lw = 2, label = 'I0')
            ax.plot(t, cities_SIR[i].hist_I1, '#c41616', alpha = 0.5, lw = 2, label = 'I1')
            ax.plot(t, cities_SIR[i].hist_I2, '#ff0000', alpha = 0.5, lw = 2, label = 'I2')
        ax.plot(t, cities_SIR[i].hist_Immunes, 'g', alpha = 0.5, lw = 2, label = 'Immunes')
        ax.plot(t, cities_SIR[i].hist_Deaths, 'black', alpha = 0.5, lw = 2, label = 'Deaths')
        ax.set_xlabel('Time(#days)')
        ax.set_ylabel('Number')
        ax.set_ylim(0,cities.loc[cities['Capital'] == i, 'Populacao'].item()*1.01)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
        plt.title(i)
        plt.show()
