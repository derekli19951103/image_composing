# smart_removal

In smart removal

1. Triangulation matting 

Here is an example run, with the output images stored in tif format:

viscomp.py --matting --backA ../test-images/large/flowers-backA.jpg --backB ../test-images/large/flowers-backB.jpg --compA ../test-images/large/flowers-compA.jpg --compB ../test-images/large/flowers-compB.jpg --alphaOut alpha.tif --colOut col.tif

2. Image compositing 

Here is an example run, with the output images stored in tif format.
Assuming you've already ran the command above, you can use the
following

viscomp.py --compositing --alphaIn alpha.tif --colIn col.tif --backIn ../test-images/tiny/window.jpg --compOut comp.jpg
