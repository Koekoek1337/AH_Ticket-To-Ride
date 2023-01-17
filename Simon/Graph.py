import networkx as nx
import matplotlib.pyplot as plt


def load_station(filename: str):
    """ Load all stations. """
    G = nx.Graph()
    with open(filename,'r') as file:
        header = file.readline()
        for line in file:
            splits = line.split(',')
            if len(splits)>2:
                station_name = str(splits[0])
                y = float(splits[1])
                x = float(splits[2])

            #print(station_name, y, x)
                G.add_node(station_name, pos=(x, y))
                plt.figure(1,figsize=(12,15))
                nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=50)
            plt.savefig("Graph.png", format="PNG")
            plt.show()

if __name__ == '__main__':
    load_station("StationsNationaal.csv")
