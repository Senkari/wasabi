/**
 * 
    Create one dataset with all negative numbers zeroed.
    Create another dataset with all positive numbers zeroed and the signs of all negative numbers removed.
    Merge the two (eg. by concatenation), resulting in a dataset twice as large as the original, but with positive values only and zeros, hence appropriate for NMF.

 * 
 **/

#include <string>

void nonnegativize(int m, int n, double **matrix);

