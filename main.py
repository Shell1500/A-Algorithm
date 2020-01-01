import pygame, random, math


pygame.init()
width, height = 600, 600
screen=pygame.display.set_mode((width, height))


# function to calculate euclidean distance
def distance(first_cord, second_cord):
    return math.sqrt(abs(((first_cord[0]-second_cord[0])^2) + ((first_cord[1]-second_cord[1])^2)))

# box class with for each obstace and path
class box:
    
    def __init__(self, size, x, y, color):
        self.size=size
        self.x=x
        self.y=y
        self.color=color
        # g => distance of box from the starting node
        self.g=distance((self.x, self.y), (0, 0))
        # h => heuristic or the manhattan distance between the box and ending node
        self.h= abs(self.x - width-25) + abs (self.y - height-25)
        self.f=self.g+self.h
        self.parent= None       
    def create(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))





x=25
y=0

boxes=[]
grid_running=True

while grid_running:
    
    screen.fill((240, 245, 250))
    
    # creating the starting and goal boxes
    pygame.draw.rect(screen, (255, 10, 10), (0, 0, 25, 25))
    pygame.draw.rect(screen, (10, 255, 10), (width-25, height-25, 25, 25))
    
    
    boxes.append(box(25, x, y, (10, 10, 10)))
    
    for event in pygame.event.get():        
        # checking if quit button pressed
        if event.type == pygame.QUIT:
            grid_running=False
    
    for i in boxes:
        i.create()
        
    x+=25
    
    if x>=width:
        x=0
        y+=25
        
    if y>=height-25 and x>=width-25:
        grid_running=False
    
    
    pygame.display.update()




start_pos=(0, 0)
end_pos=(width, height)

obstacles=[]
obstacle_loop=True

while obstacle_loop:
    screen.fill((240, 245, 250))
    mouse_position=pygame.mouse.get_pos()
    
    
    # creating the starting and goal boxes
    pygame.draw.rect(screen, (255, 10, 10), (0, 0, 25, 25))
    pygame.draw.rect(screen, (10, 255, 10), (width-25, height-25, 25, 25))
    
    
    for event in pygame.event.get():        
        # checking if quit button pressed
        if event.type == pygame.QUIT:
            obstacle_loop=False
        
        if event.type== pygame.KEYDOWN:
            if event.key == pygame.K_c:
                obstacle_loop=False
            
            
            
    for i in boxes:
        i.create()
        if mouse_position[0]>=i.x and mouse_position[0]<=i.x+25:
            if mouse_position[1]>=i.y and mouse_position[1]<=i.y+25:
                if pygame.mouse.get_pressed()[0]==1:
                    i.color=(60, 60, 60)
                    obstacles.append(i)
    
    
    pygame.display.update()
    



# ________________________________________________________________________________________________ #
#                                           Main A* Loop

open_list=[]
closed_list=[]


obstacles=[i for i in set(obstacles)]
paths=[i for i in boxes if i not in obstacles]
boxes=paths


start_node=box(25, 0, 0, (255, 10, 10))
end_node=box(25, width-25, height-25, (255, 10, 10))
start_node.g=0
start_node.parent=None

open_list.append(start_node)


path=None
draws=[]
paths=[]
main_loop=True
while main_loop:
    successors=[]
    q=min(open_list, key=lambda x: x.f)  
    open_list.remove(q)      
    closed_list.append(q)
    pygame.draw.rect(screen, (255, 10, 10), (q.x, q.y, 25, 25))
    draws.append(q)
    

    if (q.x==575 and q.y==550) or (q.x==550 and q.y==575):    
        
        temp=q
        paths.append(q)
        while temp.parent != None:
            paths.append(temp.parent)
            temp=temp.parent
            
        
        
        main_loop=False
    
    for i in boxes:
        # north
        if i.x==q.x and i.y==q.y-25:
            successors.append(i)
        # south    
        if i.x==q.x and i.y==q.y+25:
            successors.append(i)         
        # east
        if i.x==q.x+25 and i.y==q.y:
            successors.append(i)
        # west
        if i.x==q.x-25 and i.y==q.y:
            successors.append(i)
        # north-east    
        if i.x==q.x+25 and i.y==q.y-25:
            successors.append(i)
        # north-west
        if i.x==q.x-25 and i.y==q.y-25:
            successors.append(i) 
        # south-east       
        if i.x==q.x+25 and i.y==q.y+25:
            successors.append(i)
        # south-west
        if i.x==q.x-25 and i.y==q.y+25:
            successors.append(i)           
            
            
    for successor in successors:
        if successor not in obstacles:
            if successor not in closed_list:
                if successor not in open_list:
                    successor.parent=q
                    open_list.append(successor)
                    

    
        
        
    pygame.display.update()



end_loop=True
while end_loop:


    for event in pygame.event.get():        
        # checking if quit button pressed
        if event.type == pygame.QUIT:
            end_loop=False

    for q in draws:
        pygame.draw.rect(screen, (200, 10, 10), (q.x, q.y, 25, 25))
    for i in paths:
        pygame.draw.rect(screen, (10, 10, 200), (i.x, i.y, 25, 25))

        
    pygame.display.update()