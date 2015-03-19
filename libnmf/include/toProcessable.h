/** toProcessable
 *	Changes the first two lines from a .dat file created by sox to row amount
 *  and column amount.
 */


#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>
#include <time.h>

#include "common.h"
#include "outputtiming.h"


void toProcessable(const char *fileName);
