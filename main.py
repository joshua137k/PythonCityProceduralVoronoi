import pygame
import numpy as np
from scipy.spatial import Voronoi
from areaQuad import *

# Constantes
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voronoi Diagram")

def draw_point(screen, position, color, radius=2):
    pygame.draw.circle(screen, color, position, radius)

def draw_voronoi_line(screen, start_point, end_point, color):
    pygame.draw.line(screen, color, start_point, end_point)


def generate_random_points_in_region(vertices, num_points):
    """ Gera pontos aleatórios dentro de uma região delimitada. """
    points = []
    min_x = min(vertices, key=lambda x: x[0])[0]
    max_x = max(vertices, key=lambda x: x[0])[0]
    min_y = min(vertices, key=lambda x: x[1])[1]
    max_y = max(vertices, key=lambda x: x[1])[1]

    while len(points) < num_points:
        x = np.random.randint(min_x, max_x)
        y = np.random.randint(min_y, max_y)
        if is_inside_polygon(x, y, vertices):
            points.append([x, y])
    return points

def getroads(vor,region):
    roads=[]
    c=0
    for line in vor.ridge_vertices:
        start_idx, end_idx = line
        if start_idx != -1 and end_idx != -1:
            point1 = vor.vertices[start_idx]
            point2 = vor.vertices[end_idx]
            if is_inside_polygon(point1[0], point1[1], region) and is_inside_polygon(point2[0], point2[1], region):
                roads.append((point1, point2))
                if c<3:
                    line = find_closest_line_to_point(point1,region)
                    roads.append((point1, closest_point_on_line(point1,line)))
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
            roads+=getroads(v,region_points)
            
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
    points = np.random.rand(50, 2) * (WIDTH, HEIGHT)
    vor = Voronoi(points)

    roads = []
    casas = []
    for line in vor.ridge_vertices:
        start_idx, end_idx = line
        if start_idx != -1 and end_idx != -1:
            start_point = vor.vertices[start_idx]
            end_point = vor.vertices[end_idx]
            
            roads.append((start_point, end_point))
    r,casas = create_sub_voronoi(vor,40)
    roads+=r
    
    

    return roads, casas

# Gerando diagrama de Voronoi
roads, casas = generate_voronoi_diagram()
l = str(roads)
l=l.replace("array","")
f = open("roads.txt","w")
f.write(l)
f.close()
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenhando estradas
    for road in roads:
        draw_voronoi_line(screen, road[0], road[1], BLACK)

    # Desenhando casas
    for casa in casas:
        if casa is not None:
            pygame.draw.polygon(screen, RED, casa)

    pygame.display.flip()

pygame.quit()