#include "nbmutils.h"
#include "spp.h"

void perform_spp_stranger(CSTMARK BIGPOLYARRAY *pIb, CSTMARK int *pRt, int item_size, BIGPOLYARRAY &rib, BIGPOLYARRAY &qtb)
{
    if(NULL == pIb || NULL == pRt || item_size <1 ){
         return;
    }

    int *pBias = new int[item_size]();
    int qmean = 0;

    for(int indx=0; indx<item_size; indx++){
    	qmean += pRt[indx];
    }
    qmean /= item_size;


    for(int indx=0; indx<item_size; indx++)
    {

    	if(pRt[indx] == 0){
    		continue;
    	}
    	pBias[indx] = pRt[indx] - qmean;
    }


    rib = enc_bigpoly(init_bigpoly(0));
    qtb = enc_bigpoly(init_bigpoly(0));

    for(int indx=0; indx<item_size; indx++)
    {

    	if(pRt[indx]==0){
    		continue;
    	}
    	BIGPOLY tmp = MUL_P(pIb[indx],init_bigpoly(1));
    	rib = ADD_C(rib,tmp);
    	qtb = ADD_C(MUL_P(pIb[indx],init_bigpoly(1)),qtb);  //2*qt
    }

    delete[] pBias;
}


void perform_spp_friend(CSTMARK BIGPOLYARRAY *pIb, CSTMARK int *pRf, CSTMARK BIGPOLYARRAY wuf, int item_size, BIGPOLYARRAY &rib, BIGPOLYARRAY &qfb)
{
	perform_spp_stranger(pIb,pRf,item_size,rib,qfb);
	rib =  MUL_C(rib,wuf);
	qfb = MUL_C(qfb,wuf);	
}


void perform_spp_server(CSTMARK BIGPOLYARRAY *pFs, CSTMARK BIGPOLYARRAY *pTs, CSTMARK BIGPOLYARRAY *pQFs, CSTMARK BIGPOLYARRAY *pQTs, \
	 BIGPOLY alpha, BIGPOLY beta, BIGPOLY ab, int f_size, int t_size, BIGPOLYARRAY x_u , BIGPOLYARRAY &y_u )
{
    if(NULL == pFs || NULL == pTs){
         return;
    }

    BIGPOLY nt = sum_vector(pTs,t_size);
    BIGPOLY dt = sum_vector(pQTs,t_size);

    BIGPOLY nf = sum_vector(pFs,f_size);
    BIGPOLY df = sum_vector(pQFs,f_size);

    //get X
    BIGPOLY tmp1 = MUL_P(MUL_C(nt,df),beta);
    BIGPOLY tmp2 = MUL_P(MUL_C(nf,dt),alpha);
    x_u = ADD_C(tmp1,tmp2);

    //get y
    BIGPOLY tmp3 = MUL_C(dt,df);
    y_u = MUL_P(tmp3,ab);

}


void perform_spp(UID u_id, int *pTgt, int tgt_size)
{

	int f_num=0, t_num=0, item_size=1682;
	int** pFdata = get_friend_data(u_id, f_num, item_size);
	int** pTdata = get_stranger_data(u_id, t_num, item_size);
	int* pUsim = get_user_sim(u_id);

	if(NULL==pFdata || NULL==pFdata || NULL==pFdata || NULL==pUsim ){
		return;
	}

	BIGPOLY ab = init_bigpoly(10); //alpha+beta === 10;
	BIGPOLY bp_alpha = init_bigpoly(8); 
	BIGPOLY bp_beta = init_bigpoly(2);

	BIGPOLYARRAY *pTs = new BIGPOLYARRAY[t_num];
	BIGPOLYARRAY *pFs = new BIGPOLYARRAY[f_num];
	BIGPOLY *pBvec = new BIGPOLY[item_size];
	BIGPOLYARRAY *pBavec = new BIGPOLYARRAY[item_size];
    BIGPOLY *pUvec = new BIGPOLY[f_num];
	BIGPOLYARRAY *pUavec = new BIGPOLYARRAY[f_num];
	BIGPOLYARRAY *pQTs = new BIGPOLYARRAY[t_num];
	BIGPOLYARRAY *pQFs = new BIGPOLYARRAY[f_num];

	int *pIb = new int[item_size]();
	init_bigpoly_vec(pIb,pBvec,item_size);
	enc_bigpoly_vec(pBvec,pBavec, item_size);

	init_bigpoly_vec(pUsim,pUvec,f_num);
	enc_bigpoly_vec(pUvec,pUavec, f_num);
	
	for(int tidx=0; tidx<tgt_size; tidx++)
	{ 
		pBavec[pTgt[tidx]] = enc_bigpoly(init_bigpoly(1));

		for(int indx=0; indx<t_num; t_num++)
	    {
	       BIGPOLYARRAY rib;
	       BIGPOLYARRAY qb;
		   perform_spp_stranger(pBavec, pTdata[indx], item_size, rib, qb);
		   pTs[indx] = rib;
		   pQTs[indx] = qb;
	    }

	    for(int indx=0; indx<f_num; f_num++)
	    {
	       BIGPOLYARRAY rib;
	       BIGPOLYARRAY qb;
		   perform_spp_friend(pBavec, pFdata[indx], pUavec[indx], item_size, rib, qb);
		   pFs[indx] = rib;
		   pQFs[indx] = qb;
	    }

	    BIGPOLYARRAY xu;
	    BIGPOLYARRAY yu;

	    perform_spp_server(pFs, pTs, pQTs, pQFs,  bp_alpha, bp_beta, ab, f_num, t_num, xu, yu);
	    pBavec[pTgt[tidx]]  = enc_bigpoly(init_bigpoly(0));

	}

	delete[] pTs;
	delete[] pFs;
	delete[] pUsim;
	delete[] pBvec;
	delete[] pIb;
	delete[] pUvec;
	delete[] pBavec;

    for(int indx=0; indx<f_num; indx++){
		delete[] pFdata[indx];
	}
	
	for(int indx=0; indx<t_num; indx++){
		delete[] pTdata[indx];
	}
	delete[] pFdata;
	delete[] pTdata;
}


