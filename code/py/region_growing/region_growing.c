#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "stack.h"

// Map the index (i,j,k) to an index l, the "flat" index
// into the row-major 3D array of dimensions, (m,n,p).
inline int map_index(int i, int j, int k, int m, int n, int p) {
    return n*p*i + p*j + k;
}

// Add voxels coordinates in the 6-voxel neighborhood of (i,j,k)
// to the stack, S, if the coordinate is not in `checked`.
void add_neighbors(int i, int j, int k, int m, int n, int p,
                   stack * needs_check, bool * checked) {
    int l;
    element * el;

    if (i >= 1) {
        l = map_index(i-1,j,k,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i-1, j, k);
            stack_push(needs_check, el);
        }
    }

    if (j >= 1) {
        l = map_index(i,j-1,k,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i, j-1, k);
            stack_push(needs_check, el);
        }
    }

    if (k >= 1) {
        l = map_index(i,j,k-1,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i, j, k-1);
            stack_push(needs_check, el);
        }
    }

    if (i < m-1) {
        l = map_index(i+1,j,k,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i+1, j, k);
            stack_push(needs_check, el);
        }
    }

    if (j < n-1) {
        l = map_index(i,j+1,k,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i, j+1, k);
            stack_push(needs_check, el);
        }
    }

    if (k < p-1) {
        l = map_index(i,j,k+1,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i, j, k+1);
            stack_push(needs_check, el);
        }
    }
}

// Here we check if the coordinate (i,j,k) is included in the foreground
// of the segmentation by computing the average image value in the
// neighborhood of (i,j,k) and check whether the image value at (i,j,k)
// is greater than or equal to the neighborhood average.
//
// The neighborhood is defined as {i-t, ... , i+t} and similarly
// for j and k where `t` is supplied. Points beyond the border 
// are not considered.
bool check_inclusion(int i, int j, int k,
                     int m, int n, int p,
                     double * img, int t) {
    double sum;
    int imin, imax, jmin, jmax, kmin, kmax;
    int count,l;
    
    // Handle lower borders.
    imin = i-t; imin = imin < 0 ? 0 : imin;
    jmin = j-t; jmin = jmin < 0 ? 0 : jmin;
    kmin = k-t; kmin = kmin < 0 ? 0 : kmin;

    // Handle upper borders.
    imax = i+t; imax = imax > m-1 ? m-1 : imax;
    jmax = j+t; jmax = jmax > n-1 ? n-1 : jmax;
    kmax = k+t; kmax = kmax > p-1 ? p-1 : kmax;

    sum = 0.0;
    count = 0;

    // Compute the neighborhood average.
    for(int ii=imin; ii <= imax; ii++) {
        for(int jj=jmin; jj <= jmax; jj++) {
            for(int kk=kmin; kk <= kmax; kk++) {
                l = map_index(ii,jj,kk,m,n,p);
                sum += img[l];
                count += 1;
            }
        }
    }

    l = map_index(i,j,k,m,n,p);

    return (img[l] >= (sum / count));
}

void grow(int m, int n, int p,
          double * img, bool * seg,
          int si, int sj, int sk, int t) {
    int l, i, j, k;
    bool checked[m*n*p]; // indicator of coordinates already checked.
    stack needs_check;   // stack of coordinates to check.
    element * el;

    // Initialize the segmentation and `checked` indicator boolean arrays.
    for(int ii=0; ii < m*n*p; ii++) {
   //     printf("%d\n",ii);
        seg[ii]     = false;
        checked[ii] = false;
    }

  //  printf("..............................\n\n\n");

    // Initialize the stack.
    stack_init(&needs_check);

    // The segmentation and `checked` arrays are `true` at the seed voxel.
    l = map_index(si,sj,sk,m,n,p);
    seg[l]     = true;
    checked[l] = true;

    // Add the neighbors of the seed point to the stack.
    add_neighbors(si, sj, sk, m, n, p, &needs_check, checked);

    while (needs_check.n_elements > 0) {
        // Pop a coordinate from the stack.
        el = stack_pop(&needs_check);
        // Record the coordinate data from the stack element.
        i = el->i; j = el->j; k = el->k;
        // Free the stack element.
        free(el);

        l = map_index(i, j, k, m, n, p);

        // Check if the coordinate was placed in the stack twice
        // and continue to the next iteration if so.
        if (checked[l]) continue;

        // Otherwise marked the voxel as checked and proceed.
        checked[l] = true;

        // Set segmentation to true if neighborhood criteria satisfied.
        if (check_inclusion(i, j, k, m, n, p, img, t)) {
            // Mark the segmentation voxel as included.
            seg[l] = true;
            // Add potential neighbors to the stack.
            add_neighbors(i, j, k, m, n, p, &needs_check, checked);
        }
    }
}
