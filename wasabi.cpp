#include <cstdlib>
#include <stdio.h>
#include "toProcessable.h"
#include "nonnegativize.h"

void main(){
	//system("./script-to-convert-soundfile");
	toProcessable("file.dat");
	nonnegativize("file.dat");
}
