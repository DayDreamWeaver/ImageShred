import sys
from PIL import Image
image = Image.open('images/input/TokyoPanoramaShredded.png')
data = image.getdata() # This gets pixel data

# Access an arbitrary pixel. Data is stored as a 2d array where rows are
# sequential. Each element in the array is a RGBA tuple (red, green, blue,
# alpha).

x, y = 20, 90
width, height = image.size
def get_pixel_value(x, y):
    global width,height
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
def get_image_column(x):
    global width,height
    tmp_image_column = []
    for i in range(height):
        tmp_image_column.append(get_pixel_value(x, i))

    return tmp_image_column


# Create a new image of the same size as the original
# and copy a region into the new image
NUMBER_OF_COLUMNS = 20
unshredded = Image.new("RGBA", image.size)
shred_width = unshredded.size[0]/NUMBER_OF_COLUMNS

image_shred_left_edges = []
image_shred_right_edges = []
for i in range(20):
    image_shred_left_edges.append(get_image_column(i*shred_width))
    image_shred_right_edges.append(get_image_column((i+1)*shred_width - 1))


def get_distance_of_2_column(col1, col2):
    height = len(col1)
    sum = 0
    for i in range(height):
        sum = sum + get_distance_of_2_pixel(col1[i], col2[i])
    return sum

#print len(image_shred_left_edges)
#print len(image_shred_right_edges)
min_col_distance_pair = []
print "distance :"
for i in range(20):
    print "col "+ str(i)
    tmp_min_col_distance = sys.maxint
    tmp_left = 0
    tmp_right = 0
    for j in range(20):
        left = image_shred_left_edges[i]
        right = image_shred_right_edges[j]
        tmp_distance = get_distance_of_2_column(left,right)
        print "%2d->%2d:%s" % (j,i,str(tmp_distance))
        if tmp_distance < tmp_min_col_distance and i != j:
            tmp_min_col_distance = tmp_distance
            tmp_left = i
            tmp_right = j
    tmp_col_dis_pair = (tmp_right,tmp_left,tmp_min_col_distance)
    min_col_distance_pair.append(tmp_col_dis_pair)

print "min col distance pair:   right -> left"
max_col_pair_dis = 0
max_left_index = -1
max_right_index = -1
pair_col_dict = dict()
for i, v in enumerate(min_col_distance_pair):
    #print i,v
    tmp_right, tmp_left, tmp_dis = v
    print "%2d -> %2d:%s" % (tmp_right, tmp_left, tmp_dis)
    pair_col_dict[tmp_right] = tmp_left
    if tmp_dis > max_col_pair_dis:
        max_col_pair_dis = tmp_dis
        max_right_index = tmp_right
        max_left_index = tmp_left




cur = max_left_index
for i in range(20):
    shred_number = cur
    x1, y1 = shred_width * shred_number, 0
    x2, y2 = x1 + shred_width, height
    source_region_rectangle = (x1, y1, x2, y2)
    source_region = image.crop(source_region_rectangle)
    destination_point = (i * shred_width, 0)
    unshredded.paste(source_region, destination_point)
    cur = pair_col_dict[cur]
# Output the new image
unshredded.save("images/output/TokyoPanoramaShredded-unshredded.png", "PNG")
