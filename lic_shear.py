#from coeio import savefits, loadfits
from numpy import *
import pyfits

import pyximport
pyximport.install()
import lic_internal

#indir = ''
inxfile = 'ex.fits'
inyfile = 'ey.fits'

hdu = pyfits.open(inxfile)
ax = hdu[0].data

hdu = pyfits.open(inyfile)
ay = hdu[0].data

ny, nx = ay.shape

vectors = zeros((ny,nx,2),dtype=float32)
vectors[...,0] = ax
vectors[...,1] = ay

texture = random.rand(ny,nx).astype(float32)

kernellen=31
kernel = sin(arange(kernellen)*pi/kernellen)
kernel = kernel.astype(float32)

image = lic_internal.line_integral_convolution(vectors, texture, kernel)

hdu[0].data = image
hdu.writeto('lic_shear.fits')
