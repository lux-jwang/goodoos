#include "nbmutils.h"
#include "spp.h"
#include "topn.h"


#include "nbmutils.h"
#include "spp.h"
#include "topn.h"
#include "cnut.h"


CPPUNIT_TEST_SUITE_REGISTRATION( CryptonbmTest );


void CryptonbmTest::Test_math_op(void)
{
	BIGPOLY a = init_bigpoly(2);
	BIGPOLYARRAY a_c = enc_bigpoly(a);

	BIGPOLY b = init_bigpoly(3);
	BIGPOLYARRAY b_c = enc_bigpoly(b);

	BIGPOLYARRAY r_add = enc_bigpoly(init_bigpoly(5));
	BIGPOLYARRAY r_sub1 = enc_bigpoly(init_bigpoly(1));
	BIGPOLYARRAY r_sub2 = enc_bigpoly(init_bigpoly(-1));
	BIGPOLYARRAY r_mul = enc_bigpoly(init_bigpoly(6));

	BIGPOLYARRAY vres;
	bool bres = false;

    //+
	vres = ADD_P(a_c, b);
	bres = equal_c(r_add, vres);
	CPPUNIT_ASSERT(bres);
	vres = ADD_C(a_c, b_c);
	bres = equal_c(r_add, vres);
	CPPUNIT_ASSERT(bres);
     
    // -
	vres = SUB_P(b_c, a);
	bres = equal_c(r_sub1, vres);
	CPPUNIT_ASSERT(bres);
	vres = SUB_P(a_c, b);
	bres = equal_c(r_sub2, vres);
	CPPUNIT_ASSERT(bres);
	vres = SUB_C(b_c, a_c);
	bres = equal_c(r_sub1, vres);
	CPPUNIT_ASSERT(bres);
	vres = SUB_C(a_c, b_c);
	bres = equal_c(r_sub2, vres);
	CPPUNIT_ASSERT(bres);

	//*
	vres = MUL_P(a_c, b);
	bres = equal_c(r_mul, vres);
	CPPUNIT_ASSERT(bres);
	vres = MUL_C(a_c, b_c);
	bres = equal_c(r_mul, vres);
	CPPUNIT_ASSERT(bres);

}

//void perform_spp_stranger(CSTMARK BIGPOLYARRAY *pIb, CSTMARK int *pRt, int item_size, BIGPOLYARRAY &rib, BIGPOLYARRAY &qtb);
void CryptonbmTest::Test_perform_spp_stranger(void)
{
	int pibv[5] = {0,1,0,0,0};
	int pRt[5] = {32000000,48000001,0,0,16000000};

	BIGPOLYARRAY *pIba = new BIGPOLYARRAY[5];
	BIGPOLY *pIb = new BIGPOLY[5];
	init_bigpoly_vec(pibv,pIb,5);
	enc_bigpoly_vec(pIb,pIba,5);
	

	BIGPOLYARRAY r_qtb = enc_bigpoly(init_bigpoly(1));
	BIGPOLYARRAY r_rib = enc_bigpoly(init_bigpoly(16000001));

	BIGPOLYARRAY rib, qtb;


	perform_spp_stranger(pIba, pRt, 5, rib, qtb);

	bool bres = false;
	bres = equal_c(r_rib, rib);
	CPPUNIT_ASSERT(bres);
	bres = equal_c(r_qtb, qtb);
	CPPUNIT_ASSERT(bres);

	delete[] pIba;
	delete[] pIb;
}

// void perform_spp_friend(CSTMARK BIGPOLYARRAY *pIb, CSTMARK int *pRf, CSTMARK BIGPOLYARRAY wuf, int item_size, BIGPOLYARRAY &rib, BIGPOLYARRAY &qfb)
void CryptonbmTest::Test_perform_spp_friend(void)
{
	int pibv[5] = {0,1,0,0,0};
	int pRt[5] = {32000000,48000001,0,0,16000000};

	BIGPOLYARRAY *pIba = new BIGPOLYARRAY[5];
	BIGPOLY *pIb = new BIGPOLY[5];
	init_bigpoly_vec(pibv,pIb,5);
	enc_bigpoly_vec(pIb,pIba,5);

	BIGPOLYARRAY r_qtb = enc_bigpoly(init_bigpoly(1*8)); //wuf*qfb
	BIGPOLYARRAY r_rib = enc_bigpoly(init_bigpoly(16000001*8)); //wuf=8
	BIGPOLYARRAY wuf = enc_bigpoly(init_bigpoly(8));

	BIGPOLYARRAY rib, qtb;

	perform_spp_friend(pIba, pRt, wuf, 5, rib, qtb);

	bool bres = false;
	bres = equal_c(r_rib, rib);
	CPPUNIT_ASSERT(bres);
	bres = equal_c(r_qtb, qtb);
	CPPUNIT_ASSERT(bres);

	delete[] pIba;
	delete[] pIb;
}


//void perform_spp_server(CSTMARK BIGPOLYARRAY *pFs, CSTMARK BIGPOLYARRAY *pTs, CSTMARK BIGPOLYARRAY *pQFs, CSTMARK BIGPOLYARRAY *pQTs,
//     BIGPOLY alpha, BIGPOLY beta, BIGPOLY ab, int f_size, int t_size, BIGPOLYARRAY x_u , BIGPOLYARRAY &y_u )

void CryptonbmTest::Test_perform_spp_server(void)
{
	int pfsv[5] = {100000, 200001, 0, 500000, -200000};
	int ptsv[5] = {0, 0, 0, 300000, -200000};
	int pqfsv[5] = {8,6,0,4,5}; //wuf*qfb
	int pqtsv[5] = {0,0,0,4,4}; //qtg*max(wufs)/2

	BIGPOLYARRAY *pFsa = new BIGPOLYARRAY[5];
	BIGPOLY *pFs = new BIGPOLY[5];
	BIGPOLYARRAY *pTsa = new BIGPOLYARRAY[5];
	BIGPOLY *pTs = new BIGPOLY[5];

	BIGPOLYARRAY *pQFsa = new BIGPOLYARRAY[5];
	BIGPOLY *pQFs = new BIGPOLY[5];
	BIGPOLYARRAY *pQTsa = new BIGPOLYARRAY[5];
	BIGPOLY *pQTs = new BIGPOLY[5];

	init_bigpoly_vec(pfsv,pFs,5);
	enc_bigpoly_vec(pFs,pFsa,5);
	init_bigpoly_vec(ptsv,pTs,5);
	enc_bigpoly_vec(pTs,pTsa,5);

	init_bigpoly_vec(pqfsv,pQFs,5);
	enc_bigpoly_vec(pQFs,pQFsa,5);
	init_bigpoly_vec(pqtsv,pQTs,5);
	enc_bigpoly_vec(pQTs,pQTsa,5);

	BIGPOLY alpha = init_bigpoly(8);
	BIGPOLY beta = init_bigpoly(2);
	BIGPOLY ab = init_bigpoly(10);

	//verificaiton value
	int dt = 8, df=23;
	int nt = 300000+(-200000); //100000
	int nf = 100000+200001+500000+(-200000); //600001
	int xu = 2*nt*df+8*nf*dt; //
	int yu = 10*dt*df; //1840

	BIGPOLYARRAY r_xu = enc_bigpoly(init_bigpoly(xu));
	BIGPOLYARRAY r_yu = enc_bigpoly(init_bigpoly(yu));

	BIGPOLYARRAY x_u, y_u;

	perform_spp_server(pFsa,pTsa,pQFsa,pQTsa,alpha,beta,ab,5,5,x_u,y_u);

	bool bres = false;
	bres = equal_c(r_xu, x_u);
	CPPUNIT_ASSERT(bres);
	bres = equal_c(r_yu, y_u);
	CPPUNIT_ASSERT(bres);

	delete[] pFsa;
	delete[] pFs;
	delete[] pTsa;
	delete[] pTs;

	delete[] pQFsa;
	delete[] pQFs;
	delete[] pQTsa;
	delete[] pQTs;
}

void CryptonbmTest::Test_perform_spp(void)
{

}


//void perform_topn_stranger(CSTMARK int *pRt, BIGPOLYARRAY *pIb, BIGPOLYARRAY *pBias, int item_size)
void CryptonbmTest::Test_perform_topn_stranger(void)
{
    int pRt[5] = {32000000,48000001,0,0,16000000};
    BIGPOLYARRAY *pIb = new BIGPOLYARRAY[5];
    BIGPOLYARRAY *pBias = new BIGPOLYARRAY[5];

    perform_topn_stranger(pRt,pIb,pBias,5);

    bool bres = true;
    bres &= equal_c(pIb[0],enc_bigpoly(init_bigpoly(1)));
    bres &= equal_c(pIb[1],enc_bigpoly(init_bigpoly(1)));
    bres &= equal_c(pIb[2],enc_bigpoly(init_bigpoly(0)));
    bres &= equal_c(pIb[3],enc_bigpoly(init_bigpoly(0)));
    bres &= equal_c(pIb[4],enc_bigpoly(init_bigpoly(1)));

    bres &= equal_c(pBias[0],enc_bigpoly(init_bigpoly(0)));
    bres &= equal_c(pBias[1],enc_bigpoly(init_bigpoly(16000001)));
    bres &= equal_c(pBias[2],enc_bigpoly(init_bigpoly(0)));
    bres &= equal_c(pBias[3],enc_bigpoly(init_bigpoly(0)));
    bres &= equal_c(pBias[4],enc_bigpoly(init_bigpoly(-16000000)));

    CPPUNIT_ASSERT(bres);

    delete[] pIb;
    delete[] pBias;
}

//void perform_topn_friend(CSTMARK int *pRf, CSTMARK BIGPOLYARRAY wuf, BIGPOLYARRAY *pIb, BIGPOLYARRAY *pBias, int item_size)
void CryptonbmTest::Test_perform_topn_friend(void)
{
	int pRf[5] = {32000000,48000001,0,0,16000000};
    BIGPOLYARRAY *pIb = new BIGPOLYARRAY[5];
    BIGPOLYARRAY *pBias = new BIGPOLYARRAY[5];

    BIGPOLYARRAY wuf = enc_bigpoly(init_bigpoly(5));

    perform_topn_friend(pRf, wuf, pIb, pBias, 5);

    bool bres = true;
    bres &= equal_c(pIb[0],enc_bigpoly(init_bigpoly(1)));
    bres &= equal_c(pIb[1],enc_bigpoly(init_bigpoly(1)));
    bres &= equal_c(pIb[2],enc_bigpoly(init_bigpoly(0)));
    bres &= equal_c(pIb[3],enc_bigpoly(init_bigpoly(0)));
    bres &= equal_c(pIb[4],enc_bigpoly(init_bigpoly(1)));

    bres &= equal_c(pBias[0],enc_bigpoly(init_bigpoly(0)));
    bres &= equal_c(pBias[1],enc_bigpoly(init_bigpoly(16000001*5)));
    bres &= equal_c(pBias[2],enc_bigpoly(init_bigpoly(0)));
    bres &= equal_c(pBias[3],enc_bigpoly(init_bigpoly(0)));
    bres &= equal_c(pBias[4],enc_bigpoly(init_bigpoly(-16000000*5)));

    CPPUNIT_ASSERT(bres);

    delete[] pIb;
    delete[] pBias;

}


//void perform_topn_server(CSTMARK BIGPOLYARRAY **pFs, CSTMARK BIGPOLYARRAY **pTs, CSTMARK BIGPOLYARRAY **pQFs, \
//	 CSTMARK BIGPOLYARRAY **pQTs, int alpha, int beta, int item_size, int f_num, int t_num)

void CryptonbmTest::Test_perform_topn_server(void)
{

}

void CryptonbmTest::Test_perform_topn(void)
{


}