
#include "spp.h"
#include "topn.h"

int main ( int argc, char *argv[] )
{
	if(argc < 3)
	{
		return;

	}

	int runt = int(argv[1]);
	UID u_id = argv[2];

	switch(runt){
		case 1:
		    perform_spp();
		case 2:
		    perform_topn(u_id);
	}

}