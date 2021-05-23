from Partition import Partition
import os
import sys
import cv2
from Box import Box
import os
import time
from Particle import Particle

start_time = time.time()
### Input Parameters
height = int(sys.argv[1])
width = int(sys.argv[1])
num_of_frames = int(sys.argv[2])
outer_folder = 'data'

try:
    inner_folder = 'sim_{}x{}_{}'.format(height,width,sys.argv[3])
except:
    inner_folder = 'sim_{}x{}'.format(height,width)

### Setting up Simulation
Particle.affinity = 0.5
Particle.aversion = 0.5
Particle.interaction_chance = 0.1
Particle.cramming_chance = 1
Partition.threshold = 2

shape = (height,width)
box = Box(shape)

particles_per_box = 4
particles_0 = int(particles_per_box*shape[0]*shape[1]/2)
particles_1 = int(particles_per_box*shape[0]*shape[1]/2)
box.add_new_particles(particles_0,particles_1)

### Initialize data dir
if not os.path.exists(outer_folder):
    os.makedirs(outer_folder)

partial_path = os.path.join(outer_folder,inner_folder)
if not os.path.exists(partial_path):
    os.makedirs(partial_path)

# Add the simulation properties to 'properties.txt'
properties_path = os.path.join(partial_path, 'properties.txt')
properties = open(properties_path,"w")
properties.write('Particle.affinity = {}\n'.format(Particle.affinity))
properties.write('Particle.aversion = {}\n'.format(Particle.aversion))
properties.write('Particle.interaction_chance = {}\n'.format(Particle.interaction_chance))
properties.write('Particle.cramming_chance = {}\n'.format(Particle.cramming_chance))
properties.write('Partition.threshold = {}\n'.format(Partition.threshold))
properties.write('particles_per_box = {}\n'.format(particles_per_box))
properties.write('height = {}\n'.format(height))
properties.write('width = {}\n'.format(width))
properties.write('num_of_frames = {}\n'.format(num_of_frames))
properties.close()

### Initial Box
path = os.path.join(partial_path,'{:03d}.png'.format(0))
box.image_out(path)
initialize_time = time.time() - start_time
print('Setup Complete')
print('Saved: {} in {:.3f}s'.format(path, initialize_time))

### Run simulation
for i in range(num_of_frames):

    time1 = time.time()

    box.partition_interaction()
    path = os.path.join(partial_path,'{:03d}.png'.format(i+1))
    box.image_out(path)
    
    time2 = time.time()
    print('Saved: {} in {:.3f}s'.format(path, time2-time1))

end_time = time.time()
print('SIMULATION COMPLETE: {:.3f}s'.format(end_time-start_time))



# image_folder = 'test'
# video_name = 'video.avi'

# images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
# frame = cv2.imread(os.path.join(image_folder, images[0]))
# height, width, layers = frame.shape

# video = cv2.VideoWriter(video_name, 0, 1, (width,height))

# for image in images:
#     video.write(cv2.imread(os.path.join(image_folder, image)))

# cv2.destroyAllWindows()
# video.release()
