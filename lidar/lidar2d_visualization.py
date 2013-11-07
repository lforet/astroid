

#from lidar_faker_class import *
from lidar3d_class import *
import time
from visual import *
from visual.text import *

lidarData = [[] for i in range(360)] #A list of 360 elements Angle, Distance , quality

offset = 140
fps_rate = 60
angle_correction = 10
					

#lidar = lidar_faker(resolution)
lidar = mobot_lidar3d("/dev/ttyUSB0", 115200, 3)


#setup the window, view, etc
scene =  display(title='PROTOX1 LIDAR Data',
     x=0, y=0, width=1200, height=800,
     center=(5,0,0), background=(0,1,1))

scene.forward = (1, -.5,0)
scene.background = (0.1, 0.1, 0.2)
scene.title = "ProtoX1 Lidar Distance"
scene.show_rendertime = 1


point = points(pos=[(0,0,0) for i in range(360)], size=5, color=(0 , 1, 0))
#pointb = points(pos=[(0,0,0) for i in range(360)], size=5, color=(0.4, 0, 0))
point2 = points(pos=[(0,0,0) for i in range(360)], size=3, color=(1 , 1, 0))
#point2b = points(pos=[(0,0,0) for i in range(360)], size=3, color=(0.4, 0.4, 0))
#lines
outer_line= curve (pos=[(0,0,0) for i in range(360)], size=5, color=(1 , 0, 0))
lines=[curve(pos=[(offset*cos(i* pi / 180.0),0,offset*-sin(i* pi / 180.0)),(offset*cos(i* pi / 180.0),0,offset*-sin(i* pi / 180.0))], color=[(0.1, 0.1, 0.2),(1,0,0)]) for i in range(360)]

class grid:
    """A graphical grid, with two level of subdivision.

    The grid can be manipulated (moved, showed/hidden...) by acting on self.frame.
    """
    
    def __init__(self, size=100, small_interval=10, big_interval=50):
        self.frame = frame(pos=(0,0,0))
        for i in range(-size, size+small_interval, small_interval):
            if i %big_interval == 0:
                c = color.gray(0.65)
            else:
                c = color.gray(0.25)
            curve(frame=self.frame, pos=[(i,0,size),(i,0,-size)], color=c)
            curve(frame=self.frame, pos=[(size,0,i),(-size,0,i)], color=c)

#grid where major intervals are 1m, minor intervals are 10cm
my_grid = grid(size=4000, small_interval = 100, big_interval=1000)
my_grid.frame.pos.y=-5

use_points = True
use_outer_line = False
use_lines = True
use_intensity = False

def adjust_angle(x):
	global angle_correction 
	temp_angle = x + angle_correction

	#if (x >= 90 and x <= 270):
	#	temp_angle = x + 180 
	if (temp_angle > 360):
		temp_angle = temp_angle - 360
	if (temp_angle == 360): temp_angle = 359
	#if (temp_angle < 0):
	#	temp_angle = temp_angle + 360
	#if (temp_angle == 360): temp_angle = 359
	return temp_angle

def reset_data():
	for i in range(360):
		#reset the point display
		point.pos[i] = vector( 0, 0, 0 )
		#pointb.pos[i] = vector( 0, 0, 0 )
		point2.pos[i] = vector( 0, 0, 0 )
		#point2b.pos[i] = vector( 0, 0, 0 )

def update_view( y_degree, dist, quality ):


	global offset, use_outer_line, use_line
	
	if (y_degree >= 0 and y_degree <= 360):
		#reset_data()
		#print "raw:" , x_degree
		y_degree = adjust_angle(y_degree)
		#print "adjusted:" , x_degree
		
		y_degree_rad = y_degree * math.pi / 180.0
		c = math.cos(y_degree_rad)
		s = -math.sin(y_degree_rad)
		dist_mm = dist
		dist_x = dist_mm*c
		dist_y = dist_mm*s

		#reset the point display
		point.pos[y_degree] = vector( 0, 0, 0 )
		#pointb.pos[x_degree] = vector( 0, 0, 0 )
		point2.pos[y_degree] = vector( 0, 0, 0 )
		#point2b.pos[x_degree] = vector( 0, 0, 0 )

		if not use_lines : lines[angle].pos[1]=(offset*c,0,offset*s)
		if not use_outer_line :
			outer_line.pos[y_degree]=(offset*c,0,offset*s)
			outer_line.color[y_degree] = (0.1, 0.1, 0.2)

		if use_points : point.pos[y_degree] = vector( dist_x,0, dist_y)
		if use_intensity : point2.pos[y_degree] = vector( (quality + offset)*c,0, (quality + offset)*s)
		if use_lines : lines[y_degree].color[1] = (1,0,0)
		if use_outer_line : outer_line.color[y_degree] = (1,0,0)

		if use_lines : lines[y_degree].pos[1]=( dist_x, 0, dist_y)
		if use_outer_line : outer_line.pos[y_degree]=( dist_x, 0, dist_y)

#message = text(pos=(0,0,0), string='PROTOX180 DATA', justify='center',
#               color=color.yellow, axis=(0,0,1), height=100,
#                depth=0.3, up=(10,10,-0.3))
#time.sleep(2)

while True:
	lidar_data = lidar.read_lidar()
	print lidar_data

	if (len(lidar_data) > 0):
		try:
			x_degree = int(lidar_data[1])
			x_degree = 0
			#print self.y_degree 
		except:
			x_degree = 0
			pass
		try:
			y_degree = int(lidar_data[2])
			#y_degree = y_degree #+ 90
			#print x_degree
		except:
			y_degree = 0
			pass
		try:
			dist = int(lidar_data[3])
			#print dist
		except:
			dist = 0 
			pass
		try:
			quality = int(lidar_data[4])
			#print dist
		except:
			quality = 0 
			pass
		#reset_dist_data()
		if quality > 0:
			update_view (y_degree, dist, 0 )
		#time.sleep(0.1)
		#reset_data()
	else:
		#time.sleep(3)
		print "no data"
		#print lidar.x_degree, lidar.y_degree, lidar.dist, lidar.quality
 		
	#rate(60) # synchonous repaint at 60fps
	if scene.kb.keys: # event waiting to be processed?
		s = scene.kb.getkey() # get keyboard info
		print s
		#if s == "q": 
		#	sys.exit(-1)
