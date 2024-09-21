import pyautogui
from PIL import Image, ImageDraw, ImageFont
from draw_functions import *

# Define screenshot area by top-left corner and dimensions
image_dims={"x":0, "y":0, "w":500, "h":500}

# Snap screenshot
img = pyautogui.screenshot(region=(image_dims["x"], image_dims["y"], image_dims["w"], image_dims["h"]))

# Define grid spacing
grid_spacing = get_grid_spacing(img.width, img.height, 10)

# Draw grid on the image
img = img_add_grid(img, grid_spacing)

# Draw mock-actions on the image
img = img_add_path(img, [{"type":"move","coords":(300,290)},
                         {"type":"move","coords":(200,150)},
                         {"type":"click","coords":(200,150)},
                         {"type":"move","coords":(100,100)}])

# Draw cursor on the image
img = img_add_cursor(img, cursor_img, (100,100))
img.save("output.png")
