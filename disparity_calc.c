#include <stdio.h>
#include <stdlib.h>

// images need to be both grayscale
int** disparity_calc(int rows, int cols, int *imgL, int *imgR, int block_size, int max_disp) {
    // allocate memory for disparity matrix
    int *disp_map = (int *) malloc(rows * sizeof(int*));
    for(int i = 0; i < rows; i++) disp_map[i] = (int *) malloc(cols * sizeof(int));
    // intensity on the left img, and on the right img
    int i_right = 0, i_left = 0;

    for(int i = block_size/2; i < rows - block_size/2; i++) {
        for(int j = max_disp + block_size/2; j < cols - block_size/2; j++) {
            i_left = 0;
            // compute block intensity in left img
            for(int k = i - block_size/2; k <= i + block_size/2; k++)
                for(int l = j - block_size/2; l <= j + block_size/2; l++)
                    i_left += imgL[k][l];
            int disp_px = 0, difference = 0;
            int best_match = i_left;
            
            for(int m = 1; m <= max_disp; m++) {
                i_right = 0;
                // compute block intensity in right img
                for(int k = i - block_size/2; k <= i + block_size/2; k++)
                    for(int l = j - block_size/2 - m; l <= j + block_size/2 - m; l++)
                        i_right += imgR[k][l];
            
                difference = abs(i_right - i_left);
                if(difference < best_match) {
                    best_match = difference;
                    disp_px = m;
                }
            }
            disp_map[i][j] = disp_px/max_disp * 255;
        }
    }
    return disp_map;
}