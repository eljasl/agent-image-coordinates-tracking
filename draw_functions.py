import pyautogui
from PIL import Image, ImageDraw, ImageFont

def get_grid_spacing(w, h, max_lines=20):
    """
    w: Width of image that will be processed later
    h: Height of image that will be processed later
    max_lines: The amount of coordinate lines to include on the larger dimension
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Define the step size between grid lines based on the larger dimension
    step_pixels = int(max(w, h) / max_lines)

    # Define corresponding alphabetical and numeric coordinates for grid lines on X and Y axes
    x_alph = {alphabet[i]:step_pixels*i for i in range(int(w/step_pixels))}
    y_alph = {alphabet[i]:step_pixels*i for i in range(int(h/step_pixels))}
    return {"x":x_alph, "y":y_alph}

def img_add_grid(img, grid_spacing=None, line_color=(40,200,40,100)):
    """
    img: PIL.Image.Image type image on which the grid will be drawn
    grid_spacing: Nested dictionary that defines coordinates and spacing for X and Y axes
    line_color: RGBA used for grid and text

    Draws alphabetical coordinate grid and labels on the given image.
    """
    # Define grid spacing if not provided
    if not grid_spacing:
        grid_spacing = get_grid_spacing(img.width, img.height)

    # Define font
    font = ImageFont.truetype("arial.ttf", size=12)

    # Initiate drawing
    draw = ImageDraw.Draw(img, "RGBA")
    
    # Draw vertical lines and write X axis labels
    for x_letter, x in grid_spacing["x"].items():
        draw.line([(x, 0), (x, img.height-15)], fill=line_color, width=3)
        draw.text((x-3, img.height-12), x_letter, fill=line_color, font=font)
    # Draw horizontal lines and write Y axis labels
    for y_letter, y in grid_spacing["y"].items():
        draw.line([(0, y), (img.width-15, y)], fill=line_color, width=3)
        draw.text((img.width-12, y-6), y_letter, fill=line_color, font=font)

    # Write coordinates on each point in the grid
    for x_letter, x in grid_spacing["x"].items():
        for y_letter, y in grid_spacing["y"].items():
            c = f"{x_letter},{y_letter}"
            draw.text((x+2,y+2), c, fill=line_color, font=font)
    return img
    
def img_add_cursor(img, cursor_img, coords):
    """
    img: PIL.Image.Image type image on which the cursor will be overlaid
    cursor_img: PIL.Image.Image type image which will be overlaid to indicate current cursor location
    coords: Tuple for the top-left corner where the cursor image will be placed, e.g. (120,100)

    Overlays a mouse cursor on top of the provided image to indicate the current location of the cursor.
    """
    img.paste(cursor_img, coords, cursor_img)
    return img

def img_add_path(img, actions):
    """
    img: PIL.Image.Image type image on which the actions will be drawn
    actions: list(dict) for actions and their locations, e.g. [{"type":"move", "coords":(300,280)}, {"type":"move", "coords":(100,180)}, {"type":"click", "coords":(100,180)}]
    """
    # Initiate drawing
    draw = ImageDraw.Draw(img, 'RGBA')

    # Loop through each action
    for i, action in enumerate(actions):
        # If action is click, add a circle on the click location
        if action["type"]=="click":
            draw.ellipse([action["coords"][0]-8, action["coords"][1]-8, action["coords"][0]+8, action["coords"][1]+8], outline=(200,50,50,150), width=4)  # Set outline color and width
        # If action is mouse movement, draw line from previous point to new point
        elif action["type"]=="move":
            if i == 0: continue
            start = actions[i-1]["coords"]
            end = actions[i]["coords"]
            draw.line([start, end], fill=(200, 50, 50, 150), width=4)
    return img
