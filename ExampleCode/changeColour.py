def hsv_to_hex(h, s, v):
    # Ensure valid input range for hue, saturation, and value
    h = max(0, min(360, h))
    s = max(0, min(100, s))
    v = max(0, min(100, v))

    # Convert percentage values to ratios
    s /= 100
    v /= 100

    # Convert HSV to RGB
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    # Convert RGB to hexadecimal color code
    r = round((r + m) * 255)
    g = round((g + m) * 255)
    b = round((b + m) * 255)

    hex_code = "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b))
    return hex_code

# -----------PARTS TO CHANGE------------
# The full or last part of the names of the materials we want to change the color of
list_of_materials = ("MM_GS", "FEMUR_GS", "TIBIA_GS")
model_name = "Knee"
# -----------PARTS TO CHANGE------------


for matName in list_of_materials:
    num_colours = sum(mat.endswith(matName) for mat in mdb.models[model_name].materials.keys())

    # A nice coincidence (?) that the hue value from HSV is red at 0 and blue at 255,
    # with the standard color wheel bit in between
    hue_inc_size = 255 / num_colours
    count = num_colours

    for mat in mdb.models[model_name].materials.keys():
        if mat.endswith(matName):
            # You can hange the colorMappings bit from Materials to Sections or anything else,
            # obviously that makes the above loop pointless in this case
            cmap = session.viewports['Viewport: 1'].colorMappings['Material']
            hue = int(count * hue_inc_size)
            cmap.updateOverrides(
                overrides={mat: (True, hsv_to_hex(hue, 100, 100), 'Default', hsv_to_hex(hue, 100, 100))}
            )
            count -= 1

    # Apply color scheme
    session.viewports['Viewport: 1'].setColor(colorMapping=cmap)

    # Very important to prevent Abaqus from crashing
    session.viewports['Viewport: 1'].disableMultipleColors()