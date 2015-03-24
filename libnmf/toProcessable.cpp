/** toProcessable
 *	Changes the first two lines from a .dat file created by sox to row amount
 *  and column amount.
 */


#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string>
#include <errno.h>
#include <sys/time.h>
#include <time.h>
#include <fstream>
#include <vector>
#include <sstream>
#include <iostream>

std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems);
std::vector<std::string> split(const std::string &s, char delim);

void toProcessable(std::string fileName)
{
	
	//char* tmpName = new char[strlen(fileName) + 7 + 1];
	//char* oldName = new char[strlen(fileName) + 1];
	//strcpy(tmpName, fileName);
	//strcat(tmpName, ".wasabi");
	//strcpy(oldName, fileName);
	
	std::string oldName = fileName;
	std::string tmpName = oldName + ".wasabi";
	rename(oldName.c_str(), tmpName.c_str());

	//FILE *file = fopen(fileName, "r");
	
	std::ifstream fileIn(tmpName);
	if(!fileIn.is_open()){
		std::cout << "Error: Opening " << tmpName << "failed!\n";
		return;
	}

	std::ofstream fileOut(oldName);
	if(!fileOut.is_open()){
		std::cout << "Error: Opening " << oldName << "failed!\n";
		return;
	}

	int i, j, matches, beginning, rowAmnt;	
	std::string line, firstline, secondline;
	
	getline(fileIn, firstline); //sample rate line
	getline(fileIn, secondline); //channel amount line
	beginning = fileIn.tellg();
	rowAmnt = 0;
	while (getline(fileIn, line)){
		rowAmnt++;
	}
	fileIn.clear();
	fileIn.seekg(beginning, fileIn.beg);
	
	fileOut << std::to_string(rowAmnt)+"\n"; 
	fileOut << split(secondline, ' ')[2]+"\n";
	for(i=0; i<rowAmnt; i++){
		getline(fileIn, line);
		fileOut << line << "\n";
	}
	
	//remove(tmpName);
	
}


//http://stackoverflow.com/questions/236129/split-a-string-in-c
std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}

std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, elems);
    return elems;
}
