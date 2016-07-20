//7-20-2016 jun.wang@uni.lu

#define SIM 1

#ifdef SIM

#define ADD_C  s_add_c
#define ADD_P  s_add_p
#define MUL_C  s_mul_c
#define MUL_P  s_mul_p
#define SUB_c  s_SUB_c
#define SUB_p  s_SUB_P
#define BIGPOLY int
#define CHOOSERPLOY int
#define BALANCEDENCODER int
#define  ENCRYPTOR int
#define  EVALUATOR int
#define DECRYPTOR int
#define UID int

#else

#define ADD_C  add_c
#define ADD_P  add_p
#define MUL_C  mul_c
#define MUL_P  mul_p
#define SUB_c  SUB_c
#define SUB_p  SUB_P
#define BIGPOLY int
#define CHOOSERPLOY int
#define BALANCEDENCODER int
#define  ENCRYPTOR int
#define  EVALUATOR int
#define DECRYPTOR int
#define UID int

#endif


BIGPOLY s_add_c(BIGPOLY a, BIGPOLY b) 
{
	return a + b
}

BIGPOLY s_add_p(BIGPOLY a, int b)
{

	return a + b
}

BIGPOLY s_mul_c(BIGPOLY a, BIGPOLY b)
{

	return a*b
}

BIGPOLY s_mul_p(BIGPOLY a, int b)
{

	return a*b
}

BIGPOLY init_bigpoly(int val)
{

	return val;
}

void get_bigpoly_vec(const int *pVec,  BIGPOLY *pBvec, int item_size)
{
   if(NULL == pBvec || NULL == pVec){return;
   }

   for(int indx=0; indx<item_size; indx++)
   {
   	    pBvec[indx] = init_bigpoly(pVec[indx]);

   }
   return;

}

BIGPOLY sum_vector(BIGPOLY *pVec, int item_size)
{
    if(NULL == pVec){
    	return NULL;
    }

    BIGPOLY sum_v = init_bigpoly(0);

    for(int indx=0; indx<item_size; indx++)
    {
         sum_v = ADD_C(sum_v,pVec[indx]);
    }

    return sum_v;
}

bool tdsc_compare(BIGPOLY xu, BIGPOLY yu, BIGPOLY threshhold)
{

	return NULL;
}

int get_mean(int *pVec, int item_size)
{
    if(NULL == pVec || item_size <  1){
    	return NULL;
    }

    int imean = 0; 

    for(int indx=0; indx<item_size; indx++)
    {
    	imean += pVec[indx];
         
    }
    return imean/item_size;
}

BIGPOLY dot_vector(BIGPOLY *pVec1, BIGPOLY *pVec2, int item_size)
{
	if(NULL == pVec1 || NULL == pVec2 || item_size <  1){
    	return NULL;
    }

    BIGPOLY isum = init_bigpoly(0);     
    for(int indx=0; indx<item_size; indx++)
    {

    	BIGPOLY tmp = MUL_C(pVec1[indx], pVec2[indx]);
    	isum = ADD_C(tmp,isum);
    }
    return isum


}


