#include "spp.h"


void perform_spp_stranger(const BIGPOLY *pIb, const int *pRt, int item_size, BIGPOLY &rib, BIGPOLY &qtb)
{
    if(NULL == pIb || NULL == pRt || item_size <1 ){
         return;
    }

    int *pBias = new int[item_size]

    int qmean = 0;

    for(int indx=0; indx<item_size; indx++)
    {
    	qmean += pRt[indx];
    }
    qmean \= item_size;


    for(int indx=0; indx<item_size; indx++)
    {
    	if{pBias[indx] == 0}{
    		continue;
    	}
    	pBias[indx] = pRt[indx] - qmean;
    }


    rib = init_bigpoly(0);
    qtb = init_bigpoly(0);

    for(int indx=0; idx<item_size; idx++)
    {

    	if(pRt[indx]==0){
    		continue
    	}
    	BIGPOLY tmp = MUL_P(pIb[idx],pRt[idx]);
    	rib = ADD_C(rib,tmp);
    	qtb = ADD_C(MUL_P(pIb[idx],1),qtb);
    }

    delete[] pBias;

}

void perform_spp_friend(const BIGPOLY *pIb, const int *pRf, const BIGPOLY wuf, int item_size, BIGPOLY &rib, BIGPOLY &qfb)
{

	perform_stranger(pIb,pRf,rib,qfb);
	rib =  MUL_C(rib,wuf);
	qfb = MUL_C(qfb,wuf);
	
}


void perform_spp_server(BIGPOLY *pFs, int f_size, BIGPOLY *pTs, int t_size, BIGPOLY *pQFs, int qf_size, BIGPOLY *pQTs, int qt_size, BIGPOLY x_u , BIGPOLY &y_u )
{
    if(NULL == pFs || NULL == pTs){
         return NULL;
    }

    BIGPOLY nt = sum_vec(pTs,t_size);
    BIGPOLY dt = sum_vec(pQTs,qt_size);

    BIGPOLY nf = sum_vec(pFs,f_size);
    BIGPOLY dt = sum_vec(pQGs,qf_size);

    //get X
    BIGPOLY tmp1 = MUL_P(MUL_C(nt,df),beta);
    BIGPOLY tmp2 = MUL_P(MUL_C(nF,dT),alpha);
    x_u = tmp1 + tmp2;

    //get y
    int tmp1 = alpha+beta;
    BIGPOLY tmp2 = MUL_C(dt,df);
    y_u = MUL_P(tmp2,tmp1);

}


void perform_spp(UID u_id, int *pTgt, int tgt_size)
{
	int f_num=0, t_num=0, item_size;
	int **pFdata = get_friend_data(u_id,f_num, item_size);
	int **pTdata = get_stranger_data(u_id, t_num);
	int *pUsim = get_user_sim(u_id);

	if(NULL==pFdata || NULL==pFdata || NULL==pFdata){
		return;
	}

	BIGPOLY *pTs = new BIGPOLY[t_num];
	BIGPOLY *pFs = new BIGPOLY[f_num];
	BIGPOLY *pBvec = new BIGPOLY[item_size];
	BIGPOLY *pUvec = new BIGPOLY[item_size];
	BIGPOLY *pQTs = new BIGPOLY[t_num];
	BIGPOLY *pQFs = new BIGPOLY[f_num];

	int *pIb = new int[item_size]();
	
	for(int tidx=0; tidx<tgt_size; tidx++)
	{ 
		mytgt = pTgt[tidx];
		pIb[mytgt] = 1;
		get_bigpoly_vec(pIb,pBvec,item_size);

		for(int indx=0; indx<t_num; t_num++)
	    {
	       BIGPOLY &rib = NULL;
	       BIGPOLY &qb = NULL;
		   perform_stranger(pBvec, pTdata[indx],rib, qb);
		   pTs[indx] = rib;
		   pQTs[indx] = qb;
	    }

	    for(int indx=0; indx<t_num; t_num++)
	    {
	       BIGPOLY &rib = NULL;
	       BIGPOLY &qb = NULL;
		   perform_stranger(pBvec, pFdata[indx], rib, qb);
		   pFs[indx] = rib;
		   pQFs[indx] = qb;
	    }

	    perform_spp_server(pFs, f_num, pTs, t_num, pQTs, t_num, pQFs, f_num, xu, yu)

	}

	delete[] pTs;
	delete[] pFs;
	delete[] pUsim;
	delete[] pBvec;
	delete[] pIb;
	delete[] pUvec;

	for(int indx=0; indx<f_num; indx++)
	{
		delete[] pFdata[indx];
	}

	for(int indx=0; indx<t_num; indx++)
	{
		delete[] pTdata[indx];
	}
}


