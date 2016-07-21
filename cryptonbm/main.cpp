
#include "spp.h"
#include "topn.h"

int main ( int argc, char *argv[] )
{
	if(argc < 3){
		return 0;
	}

	//int runt = int(*argv[1]);
	//UID u_id = int(*argv[2]);
	int runt=1;

	switch(runt){
		case 1:
		cout << "1..." << endl; 
		break;
		case 2:
		cout << "2.." << endl;	
		break;
	}

	return 0;

}