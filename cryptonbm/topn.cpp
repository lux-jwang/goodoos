

#include "topn.h"

void perform_topn_stranger(CSTMARK int *pRt, BIGPOLYARRAY *pIb, BIGPOLYARRAY *pBias, int item_size)
{
	if(NULL == pRt || NULL == pIb || NULL == pBias){
		return;
	}
     
     int imean = get_mean(pRt, item_size);
     int bias = 0;
     int idct = 0;

     for(int indx=0; indx<item_size; indx++)
     {
     	if(pRt[indx]==0){
     		bias = 0;
     		idct = 0;
     	}
     	else{
     		bias = pRt[indx] - imean;
     		idct = 1;
     	}
    	
     	pBias[indx]  = enc_bigpoly(init_bigpoly(bias));
     	pIb[indx] = enc_bigpoly(init_bigpoly(idct));

     }	
}

void perform_topn_friend(CSTMARK int *pRf, CSTMARK BIGPOLYARRAY wuf, BIGPOLYARRAY *pIb, BIGPOLYARRAY *pBias, int item_size)
{
	perform_topn_stranger(pRf, pIb, pBias,item_size);

	for(int indx=0; indx<item_size; indx++)
	{
		pBias[indx] = MUL_C(pBias[indx], wuf);
	}
}

void perform_topn_server(CSTMARK BIGPOLYARRAY **pFs, CSTMARK BIGPOLYARRAY **pTs, CSTMARK BIGPOLYARRAY **pQFs, \
	 CSTMARK BIGPOLYARRAY **pQTs, int alpha, int beta, int item_size, int f_num, int t_num)
{
	if(NULL==pFs || NULL==pTs || NULL==pQFs || NULL==pQTs){
		return;
	}

	BIGPOLYARRAY *pXu = new BIGPOLYARRAY[item_size];
	BIGPOLYARRAY *pYu = new BIGPOLYARRAY[item_size];


	BIGPOLY ab = init_bigpoly(alpha+beta); //alpha+beta === 10;
	BIGPOLY bp_alpha = init_bigpoly(alpha); 
	BIGPOLY bp_beta = init_bigpoly(beta);

	for(int indx=0; indx<item_size; indx++)
	{
		BIGPOLYARRAY dt = enc_bigpoly(init_bigpoly(0));
		BIGPOLYARRAY nt = enc_bigpoly(init_bigpoly(0));
		BIGPOLYARRAY df = enc_bigpoly(init_bigpoly(0));
		BIGPOLYARRAY nf = enc_bigpoly(init_bigpoly(0));


		for(int itu=0; itu<t_num; itu++)
		{
			nt = ADD_C(pTs[itu][indx],nt);
			dt = ADD_C(pQTs[itu][indx],dt);
		}

		for(int ifu=0; ifu<f_num; ifu++)
		{
			nf = ADD_C(pFs[ifu][indx],nf);
			df = ADD_C(pQFs[ifu][indx],df);
		}

		//get x
		BIGPOLYARRAY tmp1 = MUL_P(MUL_C(nt,df),bp_beta);
        BIGPOLYARRAY tmp2 = MUL_P(MUL_C(nf,dt),bp_alpha);
        BIGPOLYARRAY x_u = ADD_C(tmp1,tmp2);
        pXu[indx] = x_u;

        //get y
        //int tmp1 = alpha+beta;  alpha+beta = 10;
        BIGPOLYARRAY tmp3 = MUL_C(dt,df);
        BIGPOLYARRAY y_u = ADD_P(tmp3, ab);
        pYu[indx] = y_u;
	}

    /*
     * Rank results
    **/

     delete[] pXu;
     delete[] pYu;
}


void perform_topn(UID u_id)
{
	int f_num=0, t_num=0, item_size=0;
	int **pFdata = get_friend_data(u_id,f_num,item_size);
	int **pTdata = get_stranger_data(u_id, t_num,item_size);
	int *pUsim = get_user_sim(u_id);

	if(NULL==pFdata || NULL==pFdata || NULL==pFdata){
		return;
	}

    BIGPOLY *pUvec = new BIGPOLY[f_num];
	BIGPOLYARRAY *pUavec = new BIGPOLYARRAY[f_num];
	init_bigpoly_vec(pUsim,pUvec,f_num);
	enc_bigpoly_vec(pUvec,pUavec, f_num);


	BIGPOLYARRAY** pQTs = new BIGPOLYARRAY*[t_num];
	BIGPOLYARRAY** pBATs = new BIGPOLYARRAY*[t_num];
	BIGPOLYARRAY** pQFs = new BIGPOLYARRAY*[f_num];
	BIGPOLYARRAY** pBAFs = new BIGPOLYARRAY*[f_num];



    for(int indx=0; indx<t_num; indx++)
    {
    	BIGPOLYARRAY *pBavec = new BIGPOLYARRAY[item_size];
    	BIGPOLYARRAY *pIb = new BIGPOLYARRAY[item_size];
    	perform_topn_stranger(pTdata[indx], pIb, pBavec, item_size);

    	pQTs[indx] = pIb;
    	pBATs[indx] = pBavec;
    }

    for(int indx=0; indx<f_num; indx++)
    {
    	BIGPOLYARRAY *pBavec = new BIGPOLYARRAY[item_size];
    	BIGPOLYARRAY *pIb = new BIGPOLYARRAY[item_size];
    	perform_topn_friend(pTdata[indx],pUavec[indx],pIb,pBavec,item_size);

    	pQFs[indx] = pIb;
    	pBAFs[indx] = pBavec;
    }

    perform_topn_server(pBAFs,pBATs,pQFs,pBATs,8, 2,item_size,f_num,t_num);

    //clear mem
	for(int indx=0; indx<f_num; indx++){
		delete[] pFdata[indx];
		delete[] pQFs[indx];
		delete[] pBAFs[indx];
	}

	for(int indx=0; indx<t_num; indx++){
		delete[] pTdata[indx];
		delete[] pQTs[indx];
		delete[] pBATs[indx];
	}

	delete[] pFdata;
	delete[] pTdata;
	delete[] pQFs;
	delete[] pBAFs;
	delete[] pQTs;
	delete[] pBATs;
}

