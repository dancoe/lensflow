#from coeio import *
#from mycolormaps import *
from PIL import Image
import sys
import pyfits
from numpy import clip, zeros, log10, newaxis, uint8
from pylab import cm

def loadfits(inroot):
    infile = inroot
    if infile[-5:] <> '.fits':
        infile += '.fits'
    return pyfits.open(infile)[0].data

def zeropad(a, n=1, val=0):
    ny, nx = a.shape
    bny = ny + 2 * n
    bnx = nx + 2 * n
    dtype = type(a[0,0])
    b = zeros((bny, bnx), dtype=dtype) + val
    b[n:-n,n:-n] = a
    return b

def log10clip(x, loexp, hiexp):
    return log10(clip(x, 10.**loexp, 10.**hiexp))

#inmagnif = 'hlsp_frontier_model_abell2744_cats_v1_z09-magnif'
inmagnif = sys.argv[1]

if len(sys.argv) > 2:
    kernellen = int(sys.argv[2])
else:
    kernellen = 31

if len(sys.argv) > 3:
    kfac = int(sys.argv[3])
else:
    kfac = 1/30.
    
lic = loadfits('lic_shear')
mid = kernellen / 2.
lo = (1-kfac) * mid
hi = (1+kfac) * mid 
lic = clip(lic, lo, hi)
lic = (lic - lo) / float(hi - lo)
lic = 0.42 * lic + 0.58
lic = zeropad(lic)

magnif = loadfits(inmagnif)
loexp, hiexp = 0, 2
loexp, hiexp = 0.1, 1.5
data = log10clip(magnif, loexp, hiexp)
data = (data - loexp) / float(hiexp - loexp)
data = 0.95 * data + 0.05
data = 1 - data
rgba = cm.RdYlBu(data)
rgba = rgba * lic[:,:,newaxis]
rgba[:,:,-1] = 1
rgba = 255 * rgba
rgba = rgba.astype(uint8)
im = Image.fromarray(rgba)
im = im.transpose(Image.FLIP_TOP_BOTTOM)
im.show()
im.save('lensflow.png')
