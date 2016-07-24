#include "nbmutils.h"
#include "spp.h"

void perform_spp_stranger(CSTMARK BIGPOLYARRAY *pIb, CSTMARK int *pRt, int item_size, BIGPOLYARRAY &rib, BIGPOLYARRAY &qtb)
{
    if(NULL == pIb || NULL == pRt || item_size <1 ){
         return;
    }

    int *pBias = new int[item_size](); 
    int qmean = get_mean(pRt, item_size);

    for(int indx=0; indx<item_size; indx++)
    {

    	if(pRt[indx] == 0){
    		continue;
    	}
    	pBias[indx] = pRt[indx] - qmean;
    }

    BIGPOLYARRAY init_zero = enc_bigpoly(init_bigpoly(0));
    BIGPOLY init_one_p = init_bigpoly(1);
    
    rib = init_zero;
    qtb = init_zero;

    for(int indx=0; indx<item_size; indx++)
    {

    	if(pRt[indx]==0){
    		continue;
    	}

    	BIGPOLYARRAY tmp = MUL_P(pIb[indx],init_one_p); //we can use init_one_p here, instead of init_bigpoly(1);

    	if(pBias[indx]!=0)
    	{
    		rib = ADD_C(rib,MUL_P(tmp, init_bigpoly(pBias[indx])));
    	}

    	qtb = ADD_C(tmp,qtb);  //2*qt ?
    }
    
    delete[] pBias;
}


void perform_spp_friend(CSTMARK BIGPOLYARRAY *pIb, CSTMARK int *pRf, CSTMARK BIGPOLYARRAY wuf, int item_size, BIGPOLYARRAY &rib, BIGPOLYARRAY &qfb)
{
	
	perform_spp_stranger(pIb,pRf,item_size,rib,qfb);
	rib =  MUL_C(rib,wuf);
	qfb =  MUL_C(qfb,wuf);

}


void perform_spp_server(CSTMARK BIGPOLYARRAY *pFs, CSTMARK BIGPOLYARRAY *pTs, CSTMARK BIGPOLYARRAY *pQFs, CSTMARK BIGPOLYARRAY *pQTs, \
	 BIGPOLY alpha, BIGPOLY beta, BIGPOLY ab, int f_size, int t_size, BIGPOLYARRAY &x_u , BIGPOLYARRAY &y_u )
{
    if(NULL==pFs || NULL==pTs || NULL==pQFs || NULL==pQTs){
         return;
    }
    
   
    BIGPOLYARRAY init_zero = enc_bigpoly(init_bigpoly(0));

    BIGPOLYARRAY nt = sum_vector(pTs,t_size,init_zero);
    BIGPOLYARRAY dt = sum_vector(pQTs,t_size,init_zero);
    BIGPOLYARRAY nf = sum_vector(pFs,f_size,init_zero);
    BIGPOLYARRAY df = sum_vector(pQFs,f_size,init_zero);
  
    //get X
    BIGPOLYARRAY tmp1 = MUL_P(MUL_C(nt,df),beta);
    BIGPOLYARRAY tmp2 = MUL_P(MUL_C(nf,dt),alpha);

    x_u = ADD_C(tmp1,tmp2);
    //get y
    BIGPOLYARRAY tmp3 = MUL_C(dt,df);
    y_u = MUL_P(tmp3,ab);

}


void perform_spp(UID u_id, int *pTgt, int tgt_size, int f_num=70, int t_num=10, int item_size=1682)
{

	int** pFdata = get_friend_data(u_id, f_num, item_size);
	int** pTdata = get_stranger_data(u_id, t_num, item_size);
	int* pUsim = get_user_sim(u_id, f_num);

	if(NULL==pFdata || NULL==pFdata || NULL==pFdata || NULL==pUsim ){
		return;
	}

	BIGPOLY ab = init_bigpoly(10); //alpha+beta === 10;
	BIGPOLY bp_alpha = init_bigpoly(8); 
	BIGPOLY bp_beta = init_bigpoly(2);
	BIGPOLYARRAY init_zero = enc_bigpoly(init_bigpoly(0));

	BIGPOLYARRAY *pTs = new BIGPOLYARRAY[t_num];
	BIGPOLYARRAY *pFs = new BIGPOLYARRAY[f_num];
	BIGPOLY *pBvec = new BIGPOLY[item_size];
	BIGPOLYARRAY *pBavec = new BIGPOLYARRAY[item_size];
    BIGPOLY *pUvec = new BIGPOLY[f_num];
	BIGPOLYARRAY *pUavec = new BIGPOLYARRAY[f_num];
	BIGPOLYARRAY *pQTs = new BIGPOLYARRAY[t_num];
	BIGPOLYARRAY *pQFs = new BIGPOLYARRAY[f_num];


	int *pIb = new int[item_size]();
	clock_t begin_time = clock();
	init_bigpoly_vec(pIb,pBvec,item_size);
	//cout<<"start spp 10..."<<endl;
	enc_bigpoly_vec(pBvec,pBavec, item_size);
	init_bigpoly_vec(pUsim,pUvec,f_num);
	enc_bigpoly_vec(pUvec,pUavec, f_num);
	//cout<<"start spp 2..."<<endl;
	cout <<"user stage >> u_id: "<<u_id<<"->  "<<  setprecision(5)<<float(clock ()-begin_time )/CLOCKS_PER_SEC <<" seconds" <<endl;
	
	for(int tidx=0; tidx<tgt_size; tidx++)
	{ 
		pBavec[pTgt[tidx]] = enc_bigpoly(init_bigpoly(1));

		begin_time = clock();
		for(int indx=0; indx<t_num; indx++)
	    {
	       BIGPOLYARRAY rib;
	       BIGPOLYARRAY qb;
		   perform_spp_stranger(pBavec, pTdata[indx], item_size, rib, qb);
		   //cout<<"f1: rib: "<<get_plain_int(rib)<<" qb1: "<< get_plain_int(qb)<<endl;
		   pTs[indx] = rib;
		   pQTs[indx] = qb;
	    }
	    cout <<"stranger stage >> u_id: "<<u_id<<" predict: "<<pTgt[tidx]<<"->  "<<  setprecision(5)<<float(clock ()-begin_time )/CLOCKS_PER_SEC <<" seconds" <<endl;

	    begin_time = clock();
	    for(int indx=0; indx<f_num; indx++)
	    {
	       BIGPOLYARRAY rib;
	       BIGPOLYARRAY qb;
		   perform_spp_friend(pBavec, pFdata[indx], pUavec[indx], item_size, rib, qb);

		   //cout<<"f: rib: "<<get_plain_int(rib)<<"qb: "<< get_plain_int(qb)<<endl;
		   pFs[indx] = rib;
		   pQFs[indx] = qb;
	    }
	    cout <<"friend stage >> u_id: "<<u_id<<" predict: "<<pTgt[tidx]<<"->  "<<  setprecision(5)<<float(clock ()-begin_time )/CLOCKS_PER_SEC <<" seconds" <<endl;

	    BIGPOLYARRAY xu;
	    BIGPOLYARRAY yu;

	    begin_time = clock();
	    perform_spp_server(pFs, pTs, pQFs,pQTs, bp_alpha, bp_beta, ab, f_num, t_num, xu, yu);
	    cout <<"server stage >> u_id: "<<u_id<<" predict: "<<pTgt[tidx]<<"->  "<< setprecision(5)<<float(clock ()-begin_time )/CLOCKS_PER_SEC <<" seconds" <<endl;

	    //reset
	    pBavec[pTgt[tidx]]  = init_zero;

	}

	delete[] pTs;
	delete[] pFs;
	delete[] pUsim;
	delete[] pBvec;
	delete[] pIb;
	delete[] pUvec;
	delete[] pBavec;

	delete_p2p<int>(pFdata,f_num);
	delete_p2p<int>(pTdata,t_num);

}


