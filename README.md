# Particle Simulation by vote

There will be two types of particles. The particles will have an affinity for other particles of the same type and an aversion to particles of the other type. The particles will be organized in partitions of a 2 dimensional grid. Box.py takes care of interacting the partitions. At each step an image of the box is saved and a properties.txt file holds the parameters for the run. runner.py allows setting parameters. For example: `python runner.py 32 10` does 10 iterations of a 32x32 grid. The results of `runner.py` are saved in the `data` directory.

## Examples:


## Usage
Move this project to a remote computer
``` 
rsync -av -e ssh --exclude="data" ~/Projects/particle-simulation-by-vote 192.168.1.172:~/Projects/ 
```

Run the project on a remote server
```
python runner.py 512 150 <optional_name_arg>
```

Move the data directory to local machine to see results
```
rsync -av -e ssh ~/Projects/particle-simulation-by-vote/data/ 192.168.1.159:~/Projects/particle-simulation-by-vote/data/
```

Convert images to video from the directory with the images
```
ffmpeg -framerate 10 -i "%03d.png" -vf "scale=2*trunc(iw):-2,setsar=1,format=yuv420p" -c:v libx264 -preset medium -tune stillimage -crf 18 -c:a aac -shortest "outputVideo.mp4"
```

# Structure

## Particle
#### Members
- `affinity` (attraction to same particle type)
- `aversion` (repulsion to particles of other type)
- `interaction_chance`
- `cramming_chance`
- `movement` 
- `type`
- `stay`
#### Functions
- `is_type(type)`
- `reset`
*** ***

## Partition
#### Members
- `threshold` (number of particles allowed in each partition)
- `index`
- `particle list`
#### Functions
- `num_particles`
- `add_particle(particle)`
- `add_new_particle(type)`
- `count_particle_type(type)`
*** ***

## Box
#### Members
- `shape`
- `partitions`
#### Functions
- `partition_interaction()`
- `add_new_particles(int,int)`
- `new_box()`
- `image_out(name)`
*** ***

## helpers
#### Functions
- `colormap(x,color0,color1)`
- `make_image( width, height, pixels, name )`