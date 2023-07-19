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
instance_names = ('PART-1-1', 'GRAFT-1')  # Don't include assembly
material_prefix = "PMGS"
list_of_material_suffixes = ("_GRAFT_FOR_H2_12MM_GS", "_FEMUR_GS", "_TIBIA_GS")
# -----------PARTS TO CHANGE------------


# can't get materials as easily in ODB files as you can in CAE so have to go through this process through section assignments.
myodb = session.openOdb(name=os.path.split(session.viewports[session.currentViewportName].displayedObject.path)[1])
root_assembly = myodb.rootAssembly
sections = myodb.sections

materials = []
for inst in instance_names:
    section_assignments = root_assembly.instances[inst].sectionAssignments
    materials += [sections[section_assignment.sectionName].material for section_assignment in section_assignments]



for matName in list_of_material_suffixes:
    for matName in list_of_material_suffixes:
        num_colours = 0
        for mat in materials:
            if mat.endswith(matName): num_colours +=1
    

    # A nice coincidence (?) that the hue value from HSV is red at 0 and blue at 255,
    # with the standard color wheel bit in between
    hue_inc_size = 1
    count = num_colours

    for i in range(num_colours):
        name = material_prefix + str(i) + matName
       
        # You can change the colorMappings bit from Materials to Sections or anything else,
        # obviously that makes the above loop pointless in this case
        cmap = session.viewports['Viewport: 1'].colorMappings['Material']
        hue = int(count * hue_inc_size)
        cmap.updateOverrides(
            overrides={name: (True, hsv_to_hex(hue, 100, 100), 'Default', hsv_to_hex(hue, 100, 100))}
        )
        count -= 1

    # Apply color scheme
    session.viewports['Viewport: 1'].setColor(colorMapping=cmap)

    # Very important to prevent Abaqus from crashing
    session.viewports['Viewport: 1'].disableMultipleColors()