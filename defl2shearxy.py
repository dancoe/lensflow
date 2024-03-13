#from coeio import *
from numpy import *
import pyfits
import os, sys

# shearconv.py
def shear2xy(g1, g2, vert=0):
    """(g1, g2) -> (e, theta) -> (ex, ey)"""
    theta = arctan(g2 / g1) / 2.  # CCW from x-axis
    #
    g1pos = greater(g1,0)
    g2pos = greater(g2,0)
    #
    thetanegg1 = where(g2pos, theta+pi/2., theta-pi/2.)
    theta = where(g1pos, theta, thetanegg1)
    theta = where(g1, theta, where(g2pos, pi/4., -pi/4.))  # / \
    
    # g1 + 0 - 0
    # g2 0 + 0 -
    #    - / | \  (KSB, me usually & above)
    #    | \ - /  (Bridle+, mkstarssheared.py)
    # conversion: Bridle theta = KSB theta + 90
    if vert:
        theta += pi/2.  # | \ - /

    g = hypot(g1, g2)
    e = 2 * g / (g + 1)
    ex = e * cos(theta)
    ey = e * sin(theta)

    return ex, ey

def ddy1(A):
    """Numerical derivative: 1st-order
    output array will have dimentions (N-2, N-2)"""
    dAdy = (A[2:] - A[:-2]) / 2.
    dAdy = dAdy[:,1:-1]
    return dAdy

def ddy(A):
    """Numerical derivative: 2nd-order
    output array will have dimentions (N-2, N-2)"""
    dAdy1 = (A[2:] - A[:-2]) / 2.
    dAdy2 = (-A[4:] + 8*A[3:-1] - 8*A[1:-3] + A[:-4]) / 12.
    dAdy1[1:-1,:] = dAdy2
    dAdy1 = dAdy1[:,1:-1]
    return dAdy1

def ddx(A):
    dAdx = ddy(A.T).T
    return dAdx

def ddx1(A):
    dAdx = ddy1(A.T).T
    return dAdx

def hdusave(hdu, data, outroot):
    hdu[0].data = data
    outfile = outroot + '.fits'
    if os.path.exists(outfile):
        os.remove(outfile)
    hdu.writeto(outfile)

#indir = '/astro/1/frontier/ftp/models/outgoing/abell2744/cats/'
#inxfile = 'hlsp_frontier_model_abell2744_cats_v1_x-pixels-deflect.fits'
#inyfile = 'hlsp_frontier_model_abell2744_cats_v1_y-pixels-deflect.fits'
inxfile = sys.argv[1]
inyfile = sys.argv[2]

hdu = pyfits.open(inxfile)
ax = hdu[0].data

hdu = pyfits.open(inyfile)
ay = hdu[0].data

axx = ddx(ax)
ayy = ddy(ay)

axy = ddy(ax)
ayx = ddx(ay)

kappa  = 0.5 * (axx + ayy)
gamma1 = 0.5 * (axx - ayy)
gamma2 = axy
ex, ey = shear2xy(gamma1, gamma2)

hdusave(hdu, kappa, 'kappa')
hdusave(hdu, gamma1, 'gamma1')
hdusave(hdu, gamma2, 'gamma2')
hdusave(hdu, ex, 'ex')
hdusave(hdu, ey, 'ey')
