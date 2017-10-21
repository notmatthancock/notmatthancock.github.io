#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include "region_growing.c"

int main() {
    int m,n,p;
    m = 5; n = 5; p = 1;
    double img[m*n*p];
    bool seg[m*n*p];

    for(int i=0; i < m; i++) {
        for(int j=0; j < n; j++) {
            img[5*i+j] = 0.0;
        }
    }

    img[5*2+2] = 1.0;
    img[5*2+1] = 1.0;
    img[5*2+3] = 1.0;
    img[5*1+2] = 1.0;
    img[5*3+2] = 1.0;

    grow(m,n,p, img, seg, 2, 2, 0, 5);

    for(int i=0; i < m; i++) {
        for(int j=0; j < n; j++) {
            printf("%d ", seg[5*i+j] ? 1 : 0);
        }
        printf("\n");
    }

    return 0;
}
