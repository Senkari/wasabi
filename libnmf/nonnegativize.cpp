/**
 * 
    Create one dataset with all negative numbers zeroed.
    Create another dataset with all positive numbers zeroed and the signs of all negative numbers removed.
    Merge the two (eg. by concatenation), resulting in a dataset twice as large as the original, but with positive values only and zeros, hence appropriate for NMF.

 * 
 **/


#include <string>
#include <cstdlib>
#include "nonnegativize.h"
//#include "loadMatrix.h"

/**loaMatrix includes here

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>
#include <time.h>

#include "common.h"
#include "outputtiming.h"
**/

//void loadMatrix(const char *fileName, int *m, int *n, double **matrix);

void nonnegativize(int m, int n, double **matrix){
/**	
	int m, n;
	double* mtrx;
	loadMatrix(fileName.c_str(), &m, &n, &mtrx);
**/	
	//double* copy = (double*) malloc(sizeof(double) * m * n);
	
	double* min=matrix[0];
	for(int i=0; i<m; i++){
		for (int j=0; j<n; j++){
			if ((*matrix)[i + j*m] < *min) *min = (*matrix)[i + j*m];
		}
	}
	if (*min >=0) *min = 0;
	else *min = -1* *min;	
	for(int i=0; i<m; i++){
		for (int j=0; j<n; j++){
			(*matrix)[i + j*m] = (*matrix)[i + j*m] + *min;
		}
	}
	
	
/**	for(int i=0; i<m; i++){
		for (int j=0; j<n; j++){
			if (mtrx[i + j*m] < 0) copy[i + j*m] = 0;
			else copy[i + j*m] = mtrx[i + j*m];
			if (mtrx[i + j*m] > 0) mtrx[i + j*m] = 0;
		}
	}
**/	
	
	
}

/**void loadMatrix(const char *fileName, int *m, int *n, double **matrix)
{
#ifdef PROFILE_LOAD_MATRIX
	struct timeval start, end;
	gettimeofday(&start, 0);
#endif
#if DEBUG_LEVEL >= 2
	printf("Exiting loadMatrix\n");
#endif

#ifdef ERROR_CHECKING	
	errno = 0;		//no error occured so far
#endif

	int i, j, matches;
	FILE *file = fopen(fileName, "r");

#ifdef ERROR_CHECKING
	if (errno) {
	  perror(fileName);
	  return;
	}
#endif

	matches = fscanf(file, "%d", m);
	matches = fscanf(file, "%d", n);

	(*matrix) = (double*) malloc(sizeof(double) * (*m) * (*n));

#ifdef ERROR_CHECKING
	if (errno) {
	  perror("Allocating memory in loadMatrix failed");
	  return;
	}
#endif

	double tmp;
	for(i = 0; i < *m; i++)
	{
		for(j = 0; j < *n; j++)
		{
			matches = fscanf(file, "%lf", &tmp);
			(*matrix)[i + j * (*m)] = tmp;
		}
	}
	fclose(file);
#if DEBUG_LEVEL >= 2
	printf("Exiting loadMatrix\n");
#endif
#ifdef PROFILE_LOAD_MATRIX
	gettimeofday(&end, 0);
	outputTiming("Timing:", start, end);
#endif
}
**/
