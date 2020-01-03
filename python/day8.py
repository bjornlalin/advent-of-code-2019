import sys

# Read input from stdin
raw = sys.stdin.readline()

# Convert raw input to integer values
pixels = list(map(int, raw))

# State
size = 25 * 6
layers = []
n_layers = int(len(pixels)/size)

# Create layers
for i in range(0, n_layers):
    layers.append(pixels[(i*size):((i+1)*size)])

# Part 1: Find layer with fewest '0' and calculate #('1') * #('2') in that layer
layer_fewest_num_0 = None
fewest_num_0 = size

for layer in layers:
    if layer.count(0) < fewest_num_0:
        fewest_num_0 = layer.count(0)
        layer_fewest_num_0 = layer

print("Part 1: {}".format(layer_fewest_num_0.count(1) * layer_fewest_num_0.count(2)))

# Part 2: Render the image from first to last layer, only
#         rendering layers below if all layers above are transparent
img = layers[0]
for layer in layers[1:]:
    for i in range(0, size):
        if img[i] == 2:
            img[i] = layer[i]

# Print image
print("Part 2:")
for row in range(0, 6):
    print(''.join(map(lambda p: "X" if p == 1 else " ", img[(row*25):((row+1)*25)])))
    