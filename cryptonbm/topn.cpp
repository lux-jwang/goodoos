#include "topn.h"

void perform_topn_stranger(const int *pRt, int item_size, BIGPOLY *pIb, BIGPOLY *pBias)
{
	if(NULL == pRt || NULL == pIb || NULL == pQb){
		return;
	}

     int imean = get_mean(pRt);


     for(int indx=0; indx<item_size; indx++)
     {
     	if(pRt[indx]==0){
     		continue;
     	}

     	bias = pRt[indx] - imean;
     	pIb[indx] = init_bigpoly(bias);
     	pBias[indx] = init_bigpoly(1);
     }
	

}

void perform_topn_friend(const int *pRf, const BIGPOLY wuf, int item_size, BIGPOLY *pIb, BIGPOLY *pBias)
{
	perform_topn_stranger(pRf, item_size, pIb, pBias);

	for(int indx=0; indx<item_size; indx++)
	{
		pBias[indx] = MUL_C(pBias[indx], wuf);
	}

}

void perform_topn_server(const BIGPOLY *pFs, int f_num, const BIGPOLY *pTs, int t_num, \
	 const BIGPOLY *pQFs, const BIGPOLY *pQTs, const BIGPOLY **pMx, const BIGPOLY **pMy, const int item_size)
{

	for(int indx=0; indx<item_size; indx++)
	{
		BIGPOLY dt init_bigpoly(0);
		BIGPOLY nt init_bigpoly(0);
		BIGPOLY df init_bigpoly(0);
		BIGPOLY nf init_bigpoly(0);


		for(int itu=0; itu<t_num; itu++)
		{
			nt = MUL_C(pTs[itu][indx],nt);
			dt = MUL_C(pQTs[itu][indx],dt)
		}

		for(int ifu=0; ifu<f_num; ifu++)
		{
			nf = MUL_C(pTs[ifu][indx],nf);
			df = MUL_C(pQTs[ifu][indx],df)

		}

		//get x
		BIGPOLY tmp1 = MUL_P(MUL_C(nt,df),beta);
        BIGPOLY tmp2 = MUL_P(MUL_C(nF,dT),alpha);
        BIGPOLY x_u = ADD_C(tmp1,tmp2);
        pXu[indx] = x_u;

        //get y
        int tmp1 = alpha+beta;
        BIGPOLY tmp2 = MUL_C(dt,df);
        BIGPOLY y_u = ADD_P(tmp2, tmp1);
        pYu[indx] = y_u;
	}


	BIGPOLY *pU = new BIGPOLY[item_size];
	BIGPOLY *pV = new BIGPOLY[item_size];

	for(int indx=0; indx<item_size; indx++)
	{
	     BIGPOLY tmp1 =  dot_vector(pMx[indx],x_u);
	     pU[indx] = tmp1;
	     BIGPOLY tmp2 = dot_vector(pMy[indx],y_u);
	     pV[indx] = tmp2;
	}

	tdsc_rank(pU,PV);

	delete[] Pu;
	delete[] Pv;

}

void perform_topn(UID u_id, int item_size)
{
	int f_num=0, t_num=0;
	int **pFdata = get_friend_data(u_id,f_num);
	int **pTdata = get_stranger_data(u_id, t_num);
	int *pUsim = get_user_sim(u_id);
	BIGPOLY **pMx = get_MX(u_id);
	BIGPOLY **pMy = get_MX(u_id);

	if(NULL==pFdata || NULL==pFdata || NULL==pFdata){
		return;
	}

	BIGPOLY *pTs = new BIGPOLY[t_num];
	BIGPOLY *pFs = new BIGPOLY[f_num];
	BIGPOLY *pBvec = new BIGPOLY[item_size];
	BIGPOLY *pUvec = new BIGPOLY[item_size];
	BIGPOLY *pQTs = new BIGPOLY[t_num];
	BIGPOLY *pQFs = new BIGPOLY[f_num];

    for(int indx=0; indx<t_num; indx++)
    {
    	perform_topn_stranger()

    }

    for(int indx=0; indx<f_num; indx++)
    {
    	perform_topn_friend()
    }

    perform_topn_server()




    //clear mem
	delete[] pTs;
	delete[] pFs;
	delete[] pUsim;
	delete[] pBvec;
	delete[] pIb;
	delete[] pUvec;

	for(int indx=0; indx<item_size; indx++)
	{
		delete[] pMx[indx];
		delete[] pMy[indx];
	}

	for(int indx=0; indx<f_num; indx++)
	{
		delete[] pFdata[indx];
	}

	for(int indx=0; indx<t_num; indx++)
	{
		delete[] pTdata[indx];
	}

}






}