
#include <cstdlib>
#include "spp.h"
#include "topn.h"

int main ( int argc, char *argv[] )
{

	if(argc < 6){
		return 0;
	}

	//cout<<atoi(argv[1])<<atoi(argv[2])<<atoi(argv[3])<<atoi(argv[4])<<atoi(argv[5])<<endl;
	int runtype = atoi(argv[1]);
	int u_id = atoi(argv[2]);
	int f_num = atoi(argv[3]);
	int t_num = atoi(argv[4]);
	int item_size = atoi(argv[5]);

	if(runtype!=1 && runtype!=2)
	{
		return 0;
	}

	

	int randtgt = std::rand()%item_size; //randomly predict one item for u_id
	switch(runtype){
		case 1:	
		    cout<<"start spp ..."<<endl;	    
		    perform_spp(u_id, &randtgt, 1, f_num, t_num, item_size);    
		break;
		case 2:
		    cout<<"start topn ..."<<endl;
		    perform_topn(u_id, f_num, t_num, item_size);   
		break;

		default:
		break;
	}
	return 0;

}