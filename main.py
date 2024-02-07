import pygame
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
    points = generate_random_points_in_region(reg,60)
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
            if is_inside_polygon(point1[0], point1[1], reg):
                if is_inside_polygon(point2[0], point2[1], reg):

                    r.append([list(point1), list(point2)])
                else:
                    if point2[0]<0:
                        point2[0]=limit
                    elif point2[0]>WIDTH:
                        point2[0]=WIDTH-limit

                    if point2[1]<0:
                        point2[1]=limit
                    elif point2[1]>HEIGHT:
                        point2[1]=HEIGHT-limit

                    r.append([list(point1), list(point2)])
            else:
                if point1[0]<0:
                    point1[0]=limit
                elif point1[0]>WIDTH:
                    point1[0]=WIDTH-limit

                if point1[1]<0:
                    point1[1]=limit
                elif point1[1]>HEIGHT:
                    point1[1]=HEIGHT-limit

                r.append([list(point1), list(point2)])

    roads.append(r)
    r,casas = create_sub_voronoi(vor,80)
    roads+=r
    
    

    return roads, casas

# Gerando diagrama de Voronoi
roads, casas = generate_voronoi_diagram()



l = "{"
for i,road in enumerate(roads):
    l +=str(i)+":["
    for r in road:
        a = "'Vector2({},{})'".format(r[0][0], r[0][1])
        b = "'Vector2({},{})'".format(r[1][0], r[1][1])
        c = "[{},{}]".format(a, b)
        l += c + ","
    l = l[:-1]
    l +="],"
l = l[:-1]
l+="}"
with open("teste/ro.txt", "w") as f:
    f.write(l)

'''
l = str(roads)
f = open("roads.txt","w")
f.write(l)
f.close()
'''
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenhando estradas
    for road in roads:
        for r in road:
            pygame.draw.line(screen, BLACK, r[0], r[1])

    # Desenhando casas
    for casa in casas:
        if casa is not None:
            pygame.draw.polygon(screen, RED, casa)

    pygame.display.flip()

pygame.quit()