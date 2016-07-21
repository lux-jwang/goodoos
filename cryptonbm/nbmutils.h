//7-20-2016 jun.wang@uni.lu

#ifndef LUX_NBMUTILS_H
#define LUX_NBMUTILS_H

#define SIM
#define CSTMARK 

#define ADD_C  add_c
#define ADD_P  add_p
#define MUL_C  mul_c
#define MUL_P  mul_p
#define SUB_c  SUB_c
#define SUB_p  SUB_P

#define UID int

#ifdef SIM
#define BIGPOLY int
#define BIGPOLYARRAY int
#define CHOOSERPLOY int
#define BALANCEDENCODER int
#define ENCRYPTOR int
#define EVALUATOR int
#define DECRYPTOR int

#else
	
#define BIGPOLY BigPoly
#define BIGPOLYARRAY BigPolyArray
#define CHOOSERPLOY ChooserPoly
#define BALANCEDENCODER BalancedEncoder
#define ENCRYPTOR Encryptor
#define EVALUATOR Evaluator
#define DECRYPTOR Decryptor

#endif

//#include <vector>
//#include <utility>
#include <iostream>
#include <sstream>

#include "seal.h"


using namespace std;
using namespace seal;

/*
 * only used for xx_many
 * we will not use it.
typedef vector<BIGPOLYARRAY> BPAvec; 
typedef vector<BIGPOLY> BPvec;
**/

BIGPOLY add_c(BIGPOLYARRAY a, BIGPOLYARRAY b);
BIGPOLY add_p(BIGPOLYARRAY a, BIGPOLY b);
BIGPOLY mul_c(BIGPOLYARRAY a, BIGPOLYARRAY b);
BIGPOLY mul_p(BIGPOLYARRAY a, BIGPOLY b);
BIGPOLY init_bigpoly(int val);
BIGPOLYARRAY enc_bigpoly(BIGPOLY val);
void init_bigpoly_vec(int *pVec, BIGPOLY *pBpvec, int item_size);
void enc_bigpoly_vec(BIGPOLY *pBpvec, BIGPOLYARRAY *pBpavec, int item_size);
BIGPOLYARRAY sum_vector(BIGPOLYARRAY *pBpavec, int item_size);
bool tdsc_compare(BIGPOLY xu, BIGPOLY yu, BIGPOLY threshhold);
int get_mean(int *pVec, int item_size);
BIGPOLYARRAY dot_vector(BIGPOLYARRAY *pVec1, BIGPOLYARRAY *pVec2, int item_size);
int** get_friend_data(UID u_id, int &f_num, int &item_size);
int** get_stranger_data(UID u_id, int &t_num, int &item_size);
int* get_user_sim(UID u_id);

//--------------------------------------------------------------
//meta

template <typename Type> // this is the template parameter declaration
Type** create_p2p( int r_num, int c_num)
{
    Type **ptr;
    ptr = new Type*[r_num];
    //Assign second dimension
    for(int i = 0; i < r_num; i++)
	    ptr[i] = new Type[c_num];
	return ptr;
};


template <typename Type> 
void delete_p2p(Type** ptr, int r_num)
{
	for(int i = 0; i < r_num; i++)
	    delete[] ptr[i];
};



#endif //LUX_NBMUTILS_H

