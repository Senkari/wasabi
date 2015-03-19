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


void toProcessable(const char* fileName)
{
	
	int i, j, matches, beginning, rowAmnt;
	
	char* tmpName = new char[strlen(fileName) + 7 + 1];
	char* oldName = new char[strlen(fileName) + 1];
	strcpy(tmpName, fileName);
	strcat(tmpName, ".wasabi");
	strcpy(oldName, fileName);
	//
	//const char[] oldName = *fileName;
	//const char tmpName = oldName + ".wasabi"
	//const char tmpName = oldName + ".wasabi"
	rename(oldName, tmpName);

	//FILE *file = fopen(fileName, "r");
	
	std::ifstream fileIn(tmpName);
	
#ifdef ERROR_CHECKING
	if (errno) {
	  perror(tmpName);
	  return;
	}
#endif

	std::ofstream fileOut(oldName);
		
#ifdef ERROR_CHECKING
	if (errno) {
	  perror(oldName);
	  return;
	}
#endif
	
	string line;
	string firstline, secondline
	getline(fileIn, firstline); //sample rate line
	getline(fileIn, secondline); //channel amount line
	beginning = 2;
	rowAmnt = 0;
	while (getline(fileIn, line)){
		rowAmnt++;
	}
	beginning = fileIn.tellg();
	
	fileOut << std::to_String(rowAmnt)+"\n"; 
	fileOut << split(secondline, ' ')[1]+"\n";
	for(i=0; i<rowAmnt; i++){
		fileOut << getline(fileIn, line);
	}
	
	//remove(tmpName);
	
}
