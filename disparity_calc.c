#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_THREADS 4

struct args_struct
{
    int t_id;
    int rows;
    int cols;
    int start_row;
    int start_col;
    int end_row;
    int end_col;
    int *imgL;
    int *imgR;
    int block_size;
    int max_disp;
    int *disp_map;
};

typedef struct args_struct ARGS_STRUCT;

// images need to be both grayscale
// int* disparity_calc(int rows, int cols, int *imgL, int *imgR, int block_size, int max_disp) {
//     int *disp_img = malloc(rows * cols * sizeof(int));
//     // intensity on the left img, and on the right img
//     int i_right = 0, i_left = 0;

//     for(int i = block_size/2; i < rows - block_size/2; i++) {
//         for(int j = max_disp + block_size/2; j < cols - block_size/2; j++) {
//             i_left = 0;
//             // compute block intensity in left img
//             for(int k = i - block_size/2; k <= i + block_size/2; k++)
//                 for(int l = j - block_size/2; l <= j + block_size/2; l++)
//                     i_left += imgL[k * cols + l];
//             int disp_px = 0, difference = 0;
//             int best_match = i_left;
            
//             for(int m = 1; m <= max_disp; m++) {
//                 i_right = 0;
//                 // compute block intensity in right img
//                 for(int k = i - block_size/2; k <= i + block_size/2; k++)
//                     for(int l = j - block_size/2 - m; l <= j + block_size/2 - m; l++)
//                         i_right += imgR[k * cols + l];
            
//                 difference = abs(i_right - i_left);
//                 if(difference < best_match) {
//                     best_match = difference;
//                     disp_px = m;
//                 }
//             }
//             // printf("%d\n", disp_px);
//             disp_img[i * cols + j] = (int)((float)disp_px/max_disp * 255);
//         }
//     }
//     return disp_img;
// }

void disp_calc_job(int t_id, int rows, int cols, int start_row, int end_row, int start_col, int end_col, int *imgL, int *imgR, int block_size, int max_disp, int *disp_map) {
    // ARGS_STRUCT *args = arguments;
    // disp_map = (int *) malloc(rows * cols * sizeof(int));

    printf("Starting thread %d\n", t_id);
    // intensity on the left img, and on the right img
    printf("SIZE DISP_IMG: %d bytes\n", sizeof(disp_map[0]));
    int i_right = 0, i_left = 0;
    for(int i = start_row; i < end_row; i++) {
        for(int j = start_col; j < end_col; j++) {
            i_left = 0;
            // compute block intensity in left img
            // for(int k = i - block_size/2; k <= i + block_size/2; k++)
            //     for(int l = j - block_size/2; l <= j + block_size/2; l++)
            //         i_left += imgL[k * cols + l];
            // int disp_px = 0, difference = 0;
            // int best_match = i_left;
            
            // for(int m = 1; m <= max_disp; m++) {
            //     i_right = 0;
            //     // compute block intensity in right img
            //     for(int k = i - block_size/2; k <= i + block_size/2; k++)
            //         for(int l = j - block_size/2 - m; l <= j + block_size/2 - m; l++)
            //             i_right += imgR[k * cols + l];
            
            //     difference = abs(i_right - i_left);
            //     if(difference < best_match) {
            //         best_match = difference;
            //         disp_px = m;
            //     }
            // }
            // printf("%d\n", disp_px);
            disp_map[i * cols + j] = 250;//(int)((float)disp_px/max_disp * 255);
        }
    }
    printf("Finished thread %d\n", t_id);
    return;
}

// int* disp_calc_threaded(int rows, int cols, int *imgL, int *imgR, int block_size, int max_disp) {
//     int *disp_img = malloc(rows * cols * sizeof(int));
//     pthread_t threads[NUM_THREADS];
//     ARGS_STRUCT *args = malloc(sizeof(ARGS_STRUCT) * NUM_THREADS);
//     int status;
//     for(int t=0; t<NUM_THREADS; t++) {
//         // printf("t = %d\n", t);
//         args[t].t_id = t;
//         args[t].block_size = block_size;
//         args[t].cols = cols;
//         args[t].disp_map = disp_img;
//         args[t].imgL = imgL;
//         args[t].imgR = imgR;
//         args[t].rows = rows;
//         args[t].max_disp = max_disp;
//         switch (t) {
//             case 0:
//                 args[t].start_row = block_size/2;
//                 args[t].end_row = rows/2;
//                 args[t].start_col = block_size/2;
//                 args[t].end_col = cols/2;
//                 break;
//             case 1:
//                 args[t].start_row = block_size/2;
//                 args[t].end_row = rows/2;
//                 args[t].start_col = cols/2;
//                 args[t].end_col = cols - block_size/2;
//                 break;
//             case 2:
//                 args[t].start_row = rows/2;
//                 args[t].end_row = rows - block_size/2; 
//                 args[t].start_col = block_size/2;
//                 args[t].end_col = cols/2;
//                 break;
//             case 3:
//                 args[t].start_row = rows/2;
//                 args[t].end_row = rows - block_size/2; 
//                 args[t].start_col = cols/2;
//                 args[t].end_col = cols - block_size/2;
//                 break;
//             default:
//                 break;
//         } 
//         status = pthread_create(&threads[t], NULL, &disp_calc_job, (void *) &args[t]);
//         // if(status) {
//         //  printf("ERROR; return code from pthread_create() is %d\n", status);
//         //  exit(-1);
//         // }
//     }

//     // for(int t=0; t<NUM_THREADS; t++)
//     //     pthread_join(threads[t], NULL);
//     printf("All threads are finished\n");
//     return disp_img;
// }

// void main() {
//     int *imgL = malloc(sizeof(int)*9);
//     int *imgR = malloc(sizeof(int)*9);
//     disp_calc_threaded(9, 9, imgL, imgR, 3, 20);
// }

void foo_func(double* x, int length)
{
    int i;
    for (i = 0; i < length; i++) {
        x[i] = i*i;
    }
}