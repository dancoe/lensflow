# lensflow

These scripts date back to 2017. And here's what I wrote about them:

Right now my scripts are in three steps which:
- Produce shear x & y components
- Perform the Line Integral Convolution
- Produce the pretty picture

The commands are below (you'll insert your own file names).  The second step is the one that doesn't work on my laptop.  Someday when I have more time I'll package this up a bit nicer and figure out the C dependencies better.

<pre>
python defl2shearxy.py \
hlsp_frontier_model_abell2744_cats_v1_x-pixels-deflect.fits \
hlsp_frontier_model_abell2744_cats_v1_y-pixels-deflect.fits

python lic_shear.py

python lensflow.py hlsp_frontier_model_abell2744_cats_v1_z09-magnif.fits
</pre>
