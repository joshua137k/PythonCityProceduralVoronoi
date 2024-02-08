import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from areaQuad import *
# As funções auxiliares fornecidas no script original serão mantidas com modificações mínimas necessárias.
WIDTH, HEIGHT = 1200, 800

reg = [(0,0),(WIDTH,0),(0,HEIGHT),(WIDTH,HEIGHT)]






def getroads(vor,region):
    roads=[]
    c=0
    for line in vor.ridge_vertices:
        start_idx, end_idx = line
        if start_idx != -1 and end_idx != -1:
            point1 = vor.vertices[start_idx]
            point2 = vor.vertices[end_idx]
            if is_inside_polygon(point1[0], point1[1], region):
                if is_inside_polygon(point2[0], point2[1], region):
                    roads.append([list(point1), list(point2)])
                    if c<3:
                        line = find_closest_line_to_point(point1,region)
                        roads.append([list(point1), list(closest_point_on_line(point1,line))])
                        c+=1


    return roads


def create_sub_voronoi(vor, num_points):
    """ Cria sub-diagramas de Voronoi e calcula centróides. """
    roads = []
    casas = []

    for region in vor.regions:
        if -1 not in region and region:
            region_points = [list(vor.vertices[i]) for i in region]
            random_points = generate_random_points_in_region(region_points, num_points)
            
            v = Voronoi(random_points)
            roads+=[getroads(v,region_points)]
            
            for i in v.regions:
                if not -1 in i:
                    reg_points = [list(v.vertices[t]) for t in i]
                    
                    if reg_points!=[]:
                        
                        centroid = grow_square_in_polygon(reg_points)
                        if centroid==None:
                            continue
                        if all (is_inside_polygon(x,y,region_points) for x,y in centroid) :
                            casas.append(centroid)


                

    return roads,casas
 

#função para gerar as estradas e casas
def generate_voronoi_diagram():
    points = generate_random_points_in_region(reg,20)
    vor = Voronoi(points)

    roads = []
    casas = []
    r = []
    limit=20


    for line in vor.ridge_vertices:
        start_idx, end_idx = line
        if start_idx != -1 and end_idx != -1:
            point1 = vor.vertices[start_idx]
            point2 = vor.vertices[end_idx]

            r.append([list(point1), list(point2)])


    roads.append(r)
    r,casas = create_sub_voronoi(vor,20)
    roads+=r
    
    

    return roads, casas



# Funções modificadas ou adicionais para trabalhar com Matplotlib
def plot_voronoi_diagram(roads, casas):
    fig, ax = plt.subplots(figsize=(12, 8))
    # Desenhando estradas
    for road in roads:
        for r in road:
            ax.plot([r[0][0], r[1][0]], [r[0][1], r[1][1]], color='black')
    # Desenhando casas
    for casa in casas:
        if casa is not None:
            polygon = plt.Polygon(casa, color='red', fill=None, edgecolor='red')
            ax.add_patch(polygon)
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    plt.show()

# Gerando diagrama de Voronoi
roads, casas = generate_voronoi_diagram()
exportGodot(roads)
# Plotando o diagrama de Voronoi com Matplotlib
plot_voronoi_diagram(roads, casas)
