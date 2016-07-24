

#include "topn.h"

void perform_topn_stranger(CSTMARK int *pRt, BIGPOLYARRAY *pIb, BIGPOLYARRAY *pBias, int item_size)
{
	if(NULL == pRt || NULL == pIb || NULL == pBias){
		return;
	}
	clock_t begin_time = clock();
	//BIGPOLYARRAY init_zero = enc_bigpoly(init_bigpoly(0));
	//BIGPOLYARRAY init_one = enc_bigpoly(init_bigpoly(1));
	BIGPOLY init_one_p = init_bigpoly(1);
	BIGPOLY init_zero_p = init_bigpoly(0);
     
    int imean = get_mean(pRt, item_size);
    int bias = 0;
 
    for(int indx=0; indx<item_size; indx++)
    {
    	if(indx%100==0)
    	{
    		cout<<"indx: "<<indx<<endl;
    	}

     	if(pRt[indx]==0){ 
     		//clock_t begin_time = clock();
     		pIb[indx] = enc_bigpoly(init_zero_p);
     		pBias[indx]  = enc_bigpoly(init_zero_p);
     		//cout <<setprecision(5)<<float(clock ()-begin_time )/CLOCKS_PER_SEC <<" xseconds" <<endl;
            
            /**
     		begin_time = clock();
     		BIGPOLYARRAY cx = ADD_P(pIb[indx], init_zero_p);
     		BIGPOLYARRAY cy = ADD_P(pIb[indx], init_zero_p);
     		cout <<setprecision(5)<<float(clock ()-begin_time )/CLOCKS_PER_SEC <<" yseconds" <<endl;
     		**/

     	}
     	else{
     		bias = pRt[indx] - imean;
     		pIb[indx] = enc_bigpoly(init_one_p);
     		if(bias==0){
     			pBias[indx]  = enc_bigpoly(init_zero_p);
     		}
     	    else{
     	    	pBias[indx]  = enc_bigpoly(init_bigpoly(bias)); //ADD_P(enc_bigpoly(init_bigpoly(0)),init_bigpoly(bias)); // faster than enc_bigpoly(init_bigpoly(bias));?????
     	    	//enc_bigpoly(init_bigpoly(bias));
     	    }	
     	}
    }

    cout <<"one stranger: " << setprecision(5)<<float(clock ()-begin_time )/CLOCKS_PER_SEC <<" seconds" <<endl;	
}

void perform_topn_friend(CSTMARK int *pRf, CSTMARK BIGPOLYARRAY wuf, BIGPOLYARRAY *pIb, BIGPOLYARRAY *pBias, int item_size)
{

   if(NULL == pRf || NULL == pIb || NULL == pBias){
		return;
	}
	//BIGPOLYARRAY init_zero = enc_bigpoly(init_bigpoly(0));
	//BIGPOLYARRAY init_one = enc_bigpoly(init_bigpoly(1)); // can not
	BIGPOLY init_one_p = init_bigpoly(1);
	BIGPOLY init_zero_p = init_bigpoly(0);
 
    int imean = get_mean(pRf, item_size);
    int bias = 0;
 
    for(int indx=0; indx<item_size; indx++)
    {
     	if(pRf[indx]==0){
     		
     		pIb[indx] = enc_bigpoly(init_zero_p);
     		pBias[indx]  = enc_bigpoly(init_zero_p);
     	}
     	else{
     		bias = pRf[indx] - imean;
     		pIb[indx] = MUL_P(wuf,init_one_p); //init_one;
     		if(bias == 0){
     			pBias[indx]  = enc_bigpoly(init_zero_p);
     		}
     		else{
     			pBias[indx] = MUL_P(wuf,init_bigpoly(bias));
     		}    		
     	}
    }	
}

void perform_topn_server(CSTMARK BIGPOLYARRAY **pFs, CSTMARK BIGPOLYARRAY **pTs, CSTMARK BIGPOLYARRAY **pQFs, \
	 CSTMARK BIGPOLYARRAY **pQTs, int alpha, int beta, int item_size, int f_num, int t_num, BIGPOLYARRAY *pXu, BIGPOLYARRAY *pYu)
{
	if(NULL==pFs || NULL==pTs || NULL==pQFs || NULL==pQTs || NULL==pXu || NULL==pYu){
		return;
	}

	//BIGPOLYARRAY *pXu = new BIGPOLYARRAY[item_size]; //output the result, it's good for testing without affecting the logical
	//BIGPOLYARRAY *pYu = new BIGPOLYARRAY[item_size];

	BIGPOLY ab = init_bigpoly(alpha+beta); //alpha+beta === 10;
	BIGPOLY bp_alpha = init_bigpoly(alpha); 
	BIGPOLY bp_beta = init_bigpoly(beta);

	BIGPOLYARRAY init_zero = enc_bigpoly(init_bigpoly(0));


	for(int indx=0; indx<item_size; indx++)
	{
		BIGPOLYARRAY dt = init_zero;
		BIGPOLYARRAY nt = init_zero;
		BIGPOLYARRAY df = init_zero;
		BIGPOLYARRAY nf = init_zero;

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
        BIGPOLYARRAY y_u = MUL_P(MUL_C(dt,df), ab);
        pYu[indx] = y_u;
	}

    /*
     * Rank results
    **/

     //delete[] pXu;
     //delete[] pYu;
}

void perform_topn(UID u_id, int f_num=70, int t_num=10, int item_size=1682)
{
	//int f_num=70, t_num=10, item_size=1682;
	int **pFdata = get_friend_data(u_id,f_num,item_size);
	int **pTdata = get_stranger_data(u_id, t_num,item_size);
	int *pUsim = get_user_sim(u_id, f_num);

	if(NULL==pFdata || NULL==pTdata || NULL==pUsim){
		return;
	}

	clock_t begin_time = clock();

    BIGPOLY *pUvec = new BIGPOLY[f_num];
	BIGPOLYARRAY *pUavec = new BIGPOLYARRAY[f_num];
	init_bigpoly_vec(pUsim,pUvec,f_num);
	enc_bigpoly_vec(pUvec,pUavec, f_num);

	cout <<"user stage >> u_id: "<<u_id<<"->  "<<  setprecision(5)<<float(clock ()-begin_time )/CLOCKS_PER_SEC <<" seconds" <<endl;

	BIGPOLYARRAY** pQTs = new BIGPOLYARRAY*[t_num];
	BIGPOLYARRAY** pBATs = new BIGPOLYARRAY*[t_num];
	BIGPOLYARRAY** pQFs = new BIGPOLYARRAY*[f_num];
	BIGPOLYARRAY** pBAFs = new BIGPOLYARRAY*[f_num];

    begin_time = clock();
    for(int indx=0; indx<t_num; indx++)
    {
    	BIGPOLYARRAY *pBavec = new BIGPOLYARRAY[item_size];
    	BIGPOLYARRAY *pIb = new BIGPOLYARRAY[item_size];

    	perform_topn_stranger(pTdata[indx], pIb, pBavec, item_size);
    	pQTs[indx] = pIb;
    	pBATs[indx] = pBavec;
    	cout<<"one stranger done...."<<endl;
    }

    cout <<"stranger stage >> u_id: "<<u_id<<"->  "<<  setprecision(5)<<float(clock ()-begin_time )/CLOCKS_PER_SEC <<" seconds" <<endl;
    begin_time = clock();
    for(int indx=0; indx<f_num; indx++)
    {
    	BIGPOLYARRAY *pBavec = new BIGPOLYARRAY[item_size];
    	BIGPOLYARRAY *pIb = new BIGPOLYARRAY[item_size];
    	perform_topn_friend(pFdata[indx],pUavec[indx],pIb,pBavec,item_size);

    	pQFs[indx] = pIb;
    	pBAFs[indx] = pBavec;
    	cout<<"one friend done...."<<endl;
    }
    cout <<"friend stage >> u_id: "<<u_id<<"->  "<<  setprecision(5)<<float(clock ()-begin_time )/CLOCKS_PER_SEC <<" seconds" <<endl;

    BIGPOLYARRAY *pXu = new BIGPOLYARRAY[item_size]; 
	BIGPOLYARRAY *pYu = new BIGPOLYARRAY[item_size];

    begin_time = clock();
    perform_topn_server(pBAFs,pBATs,pQFs,pBATs,8, 2,item_size,f_num,t_num,pXu,pYu);
    cout <<"server stage >> u_id: "<<u_id<<"->  "<<  setprecision(5)<<float(clock ()-begin_time )/CLOCKS_PER_SEC <<" seconds" <<endl;
    //clear mem
    delete_p2p<int>(pFdata,f_num);
    delete_p2p<BIGPOLYARRAY>(pQFs,f_num);
    delete_p2p<BIGPOLYARRAY>(pBAFs,f_num);

    delete_p2p<int>(pTdata,t_num);
    delete_p2p<BIGPOLYARRAY>(pQTs,t_num);
    delete_p2p<BIGPOLYARRAY>(pBATs,t_num);

	delete[] pXu;
	delete[] pYu;
	cout<<"complete topn protocol..."<<endl;
}

