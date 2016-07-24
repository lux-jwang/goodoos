
#include <ctime>
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

	switch(runtype){
		case 1:	
		{
		    int randtgt[3] = {0};
            for(int indx=0; indx<3; indx++)
            {
    	        srand(time(NULL));
	            randtgt[indx] = std::rand()%item_size; //randomly predict one item for u_id
            }
		    cout<<"start spp ..."<<endl;	    
		    perform_spp(u_id, randtgt, 3, f_num, t_num, item_size);
		    cout<<"...complete spp protocol"<<endl; 
		}
		break;
		case 2:
		    cout<<"start topn ..."<<endl;
		    perform_topn(u_id, f_num, t_num, item_size);  
		    cout<<"...complete top protocol"<<endl; 
		break;

		default:
		break;
	}
	return 0;

}