# Abaqus Visualisation Colour Change

## Changing the element colours

Scripts for ODB files and cae based visualisation to change the element colours into "standard" colour map varients.

The scripts change the colours of either materials or sections based on the material name, useful for anyone with more than a few different materials, especially if they’re CT intensity based material properties as you can get an idea of the material property distribution similarly to how you can in ScanIP.

Currently the scripts are pretty tuned to my work, where I have 255 material properties and want the materials with names containing high numbers to be red and low numbers to be blue. It’s a kind of handy coincidence that in HSV colour space, a hue value of 0 is red and a hue value of 255 is blue. So doing anything with fancier colour gradients might require different modules to do the hard work for you.

Even though the scripts are pretty specific to my models, the snippets of code within them might be useful for others to adapt. The two versions are for CAE and for the ODB viewer, because of the way materials are accessed (or not accessed) in ODB scripting – so that’s also a nice code snippet to have.

https://github.com/mngad/abq_colour_change/ 

Code for CAE: [changeColour.py](ExampleCode/changeColour.py)
Code for ODB: [changeColourODB.py](ExampleCode/changeColourODB.py)