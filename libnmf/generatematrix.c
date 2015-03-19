/**
 * generateMatrix - generates initialization matrices W0 and H0
 *
 * Purpose
 *		Allocating memory for both matrices and initialising them using the method specified by "init"
 *
 * Description
 *		Supports following initialization strategies:
 *			Random		random numbers, min and max can be set in options_t structure "opts" passed to the routine
 *					default-option, if "null" is passed as parameter "opts" (range 0 - 1)
 *					@see options_t in common.h
 *
 *			NNDSVD		non negative double singular value decomposition
 *					option can be set using options_t structure "opts" passed to the routine
 *					@see options_t in common.h
 *
 * Arguments:
 *
 * m		in, 	first dimension of matrix
 *
 * n		in, 	second dimension of matrix 
 *
 * k		in,	approximation factor
 *
 * init		in, 	type of initialization
 *
 * min		in, 	lower bound of random numbers
 *
 * max		in, 	upper bound of random numbers
 *
 * matrixW	in/out, pointer to memory storing the matrix (m x k)
 *
 * matrixH	in/out, pointer to memory storing the matrix (k x n)
 * 
 * matrixA	in,	pointer to matrix which should be factorised
 *
 * opts		in,	pointer to options_t structure to set initialization options, @see "options_t" in common.h
 */


#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>
#include <time.h>

#include "common.h"
#include "blaslapack.h"
#include "outputtiming.h"
#include "randnumber.h"
#include "calculatesvd.h"
#include "storematrix.h"




void generateMatrix(const int m, const int n, const int k, init_t init, const int min, const int max, double **matrixW, double **matrixH, double * matrixA, options_t * opts)
{

#ifdef PROFILE_GENERATE_MATRIX
	struct timeval start, end;
	gettimeofday(&start, 0);
#endif
#if DEBUG_LEVEL >= 2
	printf("Entering generateMatrix\n");
#endif


  //if *matrix is NULL, memory has to be allocated
  if ( !(*matrixW) )
    *matrixW = (double*) malloc(sizeof(double)*m*k);
  if ( !(*matrixH) )      
    *matrixH = (double*) malloc(sizeof(double)*k*n);

#ifdef ERROR_CHECKING
  if (errno) {
    perror("Failed to allocate memory in generateMatrix");
    return;
  }
#endif

  //random initialization
  if (init == ran) {
    int i;
    for(i = 0; i < m*k; ++i)
      (*matrixW)[i] = randnumber(min, max);
    for(i = 0; i < k*n; ++i)
      (*matrixH)[i] = randnumber(min, max);
  }
  if (init == nndsvd) {
    double * U, *S, *V;
    
    int mindim = (m > n) ? n : m;
    int vcols, ucols;
    
    if (opts->nndsvd_maxiter < 0)
      opts->nndsvd_maxiter = 300;
    if (opts->nndsvd_ncv < 0) {
      if ( k > 10) {
        opts->nndsvd_ncv = 2 * k;
      }
      else {
	opts->nndsvd_ncv = 20;
      }
    }
    if (opts->nndsvd_ncv > mindim)
      opts->nndsvd_ncv = mindim;
    if (opts->nndsvd_ncv <= k)
      opts->nndsvd_ncv = k + 1;
   

    if (m >= n) {
      vcols = opts->nndsvd_ncv;
      ucols = k;
    }
    else {
      vcols = k;
      ucols = opts->nndsvd_ncv;
    }
    double *uup, *uun, *vvp, *vvn;
    U = (double*) malloc(sizeof(double) * m * ucols);
    S = (double*) malloc(sizeof(double) * k);
    V = (double*) malloc(sizeof(double) * n * vcols);
    uup = (double*) malloc(sizeof(double) * m);
    uun = (double*) malloc(sizeof(double) * m);
    vvp = (double*) malloc(sizeof(double) * n);
    vvn = (double*) malloc(sizeof(double) * n);
    double n_uup, n_uun, n_vvp, n_vvn, termp, termn;
    
    

    //calculate svd
    int errcode = 0;
    errcode = calculateSVD(matrixA, U, S, V, m, n, k, opts->nndsvd_maxiter, opts->nndsvd_tol, opts->nndsvd_ncv, 1);

#ifdef ERROR_CHECKING

    if (errcode < 0) {
	    errno = errcode;
	    free(U);
	    free(S);
	    free(V);
	    free(uup);
	    free(uun);
	    free(vvp);
	    free(vvn);
	    perror("Error in calculateSVD. Aborting.");
	    return;
    }
#endif

    if (errcode < k)
	printf("Warning: Only %d singular values of %d calculated converged\n", errcode, k);
    

    
    //fill outputmatrices with zeros
    dlaset('A', m, k, 0., 0., *matrixW, m);
    dlaset('A', k, n, 0., 0., *matrixH, k);
    
    //setting first column of W and first row of H
    double sqrt_sv = sqrt(S[0]);
    daxpy(m, sqrt_sv, U, 1, *matrixW, 1);
    daxpy(n, sqrt_sv, V, 1, *matrixH, k);

    
    
    //setting remaining columns of W and rows of H
    int i, j;
    for(i = 1; i < k; ++i) {

	for (j = 0; j < m; ++j) {
		if (U[j + i*m] < 0.) {
			uup[j] = 0.0;
			uun[j] = fabs(U[j + i*m]);
		}
		else {
			uun[j] = 0.0;
			uup[j] = U[j + i*m];
		}
	}

	for (j = 0; j < n; ++j) {
		if (V[j + i*n] < 0.) {
			vvp[j] = 0.0;
			vvn[j] = fabs(V[j + i*n]);
		}
		else {
			vvn[j] = 0.0;
			vvp[j] = V[j + i*n];
		}
	}

	n_uup = dnrm2(m, uup, 1);
	n_uun = dnrm2(m, uun, 1);
	n_vvp = dnrm2(n, vvp, 1);
	n_vvn = dnrm2(n, vvn, 1);
	termp = n_uup * n_vvp;
	termn = n_uun * n_vvn;

	if (termp >= termn) {
		double factorw = sqrt(S[i] * termp) / n_uup;
		double factorh = sqrt(S[i] * termp) / n_vvp;
		daxpy(m, factorw, uup, 1, *matrixW + i*m, 1);
		daxpy(n, factorh, vvp, 1, *matrixH + i, k); 
	}
	else {
		double factorw = sqrt(S[i] * termn) / n_uun;
		double factorh = sqrt(S[i] * termn) / n_vvn;
		daxpy(m, factorw, uun, 1, *matrixW + i*m, 1);
		daxpy(n, factorh, vvn, 1, *matrixH + i, k);

	}
	
      
    }
    
    //set negative elements to absolute value or zero if absolute value is smaller than ZERO_THRESHOLD from common.h
    for(i = 0; i < m*k; ++i) {
      double tmp_abs = 0.0;
      tmp_abs = fabs((*matrixW)[i]);
      if (tmp_abs < ZERO_THRESHOLD) {
 	tmp_abs = 0.0;
      }
      (*matrixW)[i] = tmp_abs;
    }
    
    //set negative elements to absolute value or zero if absolute value is smaller than ZERO_THRESHOLD from common.h
    for(i = 0; i < k*n ; ++i) {
      double tmp_abs = 0.0;
      tmp_abs = fabs((*matrixH)[i]);
      if (tmp_abs < ZERO_THRESHOLD) {
 	tmp_abs = 0.0;
      }
      (*matrixH)[i] = tmp_abs;    
    }

    
    free(U);
    free(S);
    free(V);
    free(uup);
    free(uun);
    free(vvp);
    free(vvn);
  }


#if DEBUG_LEVEL >= 2
	printf("Exiting generateMatrix\n");
#endif
#ifdef PROFILE_GENERATE_MATRIX
	gettimeofday(&end, 0);
	outputTiming("", start, end);
#endif
  return;
}
//end of generateMatrix
//---------------------
