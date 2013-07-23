from PIL import Image
image = Image.open('images/input/TokyoPanoramaShredded.png')
data = image.getdata() # This gets pixel data

# Access an arbitrary pixel. Data is stored as a 2d array where rows are
# sequential. Each element in the array is a RGBA tuple (red, green, blue,
# alpha).

x, y = 20, 90
def get_pixel_value(x, y):
   width, height = image.size
   pixel = data[y * width + x]
   return pixel
print get_pixel_value(20, 30)
def get_distance_of_2_pixel(pixel1, pixel2):
    return  (pixel1[0] - pixel2[0])**2 + \
            (pixel1[1] - pixel2[1])**2 + \
            (pixel1[2] - pixel2[2])**2

point1 = get_pixel_value(19,30)
point2 = get_pixel_value(20,30)
print get_distance_of_2_pixel(point1,point2)

# Create a new image of the same size as the original
# and copy a region into the new image
width, height = image.size
NUMBER_OF_COLUMNS = 20
unshredded = Image.new("RGBA", image.size)
shred_width = unshredded.size[0]/NUMBER_OF_COLUMNS
shred_number = 1
x1, y1 = shred_width * shred_number, 0
x2, y2 = x1 + shred_width, height
source_region_rectangle = (x1, y1, x2, y2)
source_region = image.crop(source_region_rectangle)
destination_point = (0, 0)
unshredded.paste(source_region, destination_point)
# Output the new image
unshredded.save("images/output/TokyoPanoramaShredded-unshredded.png", "PNG")
