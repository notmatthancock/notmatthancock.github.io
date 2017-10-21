import sys
import numpy as np

def get_nbhd(pt, checked, dims):
    nbhds = []

    if (pt[0] > 0) and not checked[pt[0]-1, pt[1], pt[2]]:
        nbhds.append((pt[0]-1, pt[1], pt[2]))
    if (pt[1] > 0) and not checked[pt[0], pt[1]-1, pt[2]]:
        nbhds.append((pt[0], pt[1]-1, pt[2]))
    if (pt[2] > 0) and not checked[pt[0], pt[1], pt[2]-1]:
        nbhds.append((pt[0], pt[1], pt[2]-1))

    if (pt[0] < dims[0]-1) and not checked[pt[0]+1, pt[1], pt[2]]:
        nbhds.append((pt[0]+1, pt[1], pt[2]))
    if (pt[1] < dims[1]-1) and not checked[pt[0], pt[1]+1, pt[2]]:
        nbhds.append((pt[0], pt[1]+1, pt[2]))
    if (pt[2] < dims[2]-1) and not checked[pt[0], pt[1], pt[2]+1]:
        nbhds.append((pt[0], pt[1], pt[2]+1))

    return nbhds

def grow(img, seed, t, verbose=True):
    seg = np.zeros(img.shape, dtype=np.bool)
    checked = np.zeros_like(seg)

    seg[seed] = True
    checked[seed] = True
    needs_check = get_nbhd(seed, checked, img.shape)

    while len(needs_check) > 0:
        pt = needs_check.pop()

        # Its possible that the point was already checked and was
        # put in the needs_check stack twice.
        if checked[pt]: continue

        checked[pt] = True

        # Handle borders.
        imin = max(pt[0]-t, 0)
        imax = min(pt[0]+t, img.shape[0]-1)
        jmin = max(pt[1]-t, 0)
        jmax = min(pt[1]+t, img.shape[1]-1)
        kmin = max(pt[2]-t, 0)
        kmax = min(pt[2]+t, img.shape[2]-1)

        if img[pt] >= img[imin:imax+1, jmin:jmax+1, kmin:kmax+1].mean():
            # Include the voxel in the segmentation and
            # add its neighbors to be checked.
            seg[pt] = True
            needs_check += get_nbhd(pt, checked, img.shape)

    return seg
