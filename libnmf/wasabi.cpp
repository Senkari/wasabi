#include <cstdlib>
#include <stdio.h>
#include <string>
#include <fstream>
#include "toProcessable.h"
#include "nonnegativize.h"

//loaMatrix includes here

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>
#include <time.h>

#include "common.h"
#include "outputtiming.h"
#include "nmfdriver.h"

//

void loadMatrix(const char *fileName, int *m, int *n, double **matrix);

int main(){
	//system("./script-to-convert-soundfile");
	toProcessable("file.dat");
	
	int m, n;
	double* mtrx;
	loadMatrix("file.dat", &m, &n, &mtrx);
	
	nonnegativize(m, n, &mtrx);
	
	//for testing
	
	std::ofstream fileOut("negative.dat");
	fileOut << m << "\n" << n << "\n\n";
	for(int i=0; i<m; i++){
		for (int j=0; j<n; j++){
			fileOut << mtrx[i + j * m] << "\t";
		}
		fileOut << "\n";
	}
	
	// Creating option structure
	options_t opts;
	opts.rep = 1;
	opts.init = nndsvd;
	opts.min_init = 0;
	opts.max_init = 1;
	opts.w_out = "final_w2.matrix";
	opts.h_out = "final_h2.matrix";
	opts.TolX = 2.0E-02;
	opts.TolFun = 2.0E-02;
	opts.nndsvd_maxiter = -1;			//if set to -1 - default value will be set in generateMatrix
	opts.nndsvd_blocksize = 1;
	opts.nndsvd_tol = 2E-08;
	opts.nndsvd_ncv = -1;	
	
	nmfDriver("negative.dat", 3, 100, NULL, NULL, als, &opts);

	return 0;
}

void loadMatrix(const char *fileName, int *m, int *n, double **matrix)
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
