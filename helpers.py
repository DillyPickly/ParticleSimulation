
from PIL import Image

def colormap(x, color0 = (255,0,0), color1 = (0,0,255)) :
    """
    creates a linear colormap between 2 rbg colors
    """
    subtract_tuples = tuple(map(lambda i, j: i - j, color1,color0))
    multiply_tuple = tuple(map(lambda i : i*x, subtract_tuples))
    add_tuples = tuple(map(lambda i,j : int(i+j), multiply_tuple, color0))
    return add_tuples

def make_image( width, height, pixels, name='image.png' ):
    img = Image.new('RGB', (width, height))
    img.putdata(pixels)
    # img.show()
    img.save(name)

if __name__ == "__main__":
    print(colormap(0 ))
    print(colormap(.5))
    print(colormap(1 ))





