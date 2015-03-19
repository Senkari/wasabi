/**
 * 
    Create one dataset with all negative numbers zeroed.
    Create another dataset with all positive numbers zeroed and the signs of all negative numbers removed.
    Merge the two (eg. by concatenation), resulting in a dataset twice as large as the original, but with positive values only and zeros, hence appropriate for NMF.

 * 
 **/

#include "loadmatrix.h"

void nonnegativize(const char *fileName){
	int m, n;
	double *mtrx
	loadMatrix(fileName, &m, &n, &mtrx);
	double copy = (double) malloc(sizeof(double) * m * n);
#ifdef ERROR_CHECKING
	if (errno) {
	  perror("Allocating memory in nonnegativize failed");
	  return;
	}
#endif
	copy = *mtrx;
	
	for(int i=0; i<m; i++){
		for (int j=0; j<n; j++){
			if (copy[i + j*m] < 0) copy[i + j*m] = 0;
			if ((*mtrx)[i + j*m > 0) (*mtrx)[i + j*m] = 0;
		}
	}
	
	//TODO: Merge copy and *mtrx
}
