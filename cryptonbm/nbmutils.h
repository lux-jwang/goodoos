//7-20-2016 jun.wang@uni.lu

#ifndef LUX_NBMUTILS_H
#define LUX_NBMUTILS_H

//#define SIM
#define CSTMARK 

#define ADD_C  add_c
#define ADD_P  add_p
#define MUL_C  mul_c
#define MUL_P  mul_p
#define SUB_C  sub_c
#define SUB_P  sub_p

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
#include <fstream>
#include <sstream>
#include <ctime>
#include <iomanip> 
#include <string>

#include "seal.h"


using namespace std;
using namespace seal;

/*
 * only used for xx_many
 * we will not use it.
typedef vector<BIGPOLYARRAY> BPAvec; 
typedef vector<BIGPOLY> BPvec;
**/

BIGPOLYARRAY add_c(BIGPOLYARRAY a, BIGPOLYARRAY b);
BIGPOLYARRAY add_p(BIGPOLYARRAY a, BIGPOLY b);
BIGPOLYARRAY mul_c(BIGPOLYARRAY a, BIGPOLYARRAY b);
BIGPOLYARRAY mul_p(BIGPOLYARRAY a, BIGPOLY b);
BIGPOLYARRAY sub_c(BIGPOLYARRAY a, BIGPOLYARRAY b);
BIGPOLYARRAY sub_p(BIGPOLYARRAY a, BIGPOLY b);
BIGPOLY init_bigpoly(int val);
BIGPOLYARRAY enc_bigpoly(BIGPOLY val);
bool equal_c(BIGPOLYARRAY a, BIGPOLYARRAY b);
int get_plain_int(BIGPOLYARRAY a);


void init_bigpoly_vec(int *pVec, BIGPOLY *pBpvec, int item_size);
void enc_bigpoly_vec(BIGPOLY *pBpvec, BIGPOLYARRAY *pBpavec, int item_size);
//BIGPOLYARRAY sum_vector(BIGPOLYARRAY *pBpavec, int item_size);
BIGPOLYARRAY sum_vector(BIGPOLYARRAY *pBpavec, int item_size, BIGPOLYARRAY sum_v);
bool tdsc_compare(BIGPOLY xu, BIGPOLY yu, BIGPOLY threshhold);
int get_mean(int *pVec, int item_size);
BIGPOLYARRAY dot_vector(BIGPOLYARRAY *pVec1, BIGPOLYARRAY *pVec2, int item_size);

int** get_data_2d(string filename, int user_num, int item_size);
int** get_friend_data(UID u_id, int f_num, int item_size);
int** get_stranger_data(UID u_id, int t_num, int item_size);
int* get_user_sim(UID u_id, int f_num);

//--------------------------------------------------------------
//meta

template <typename Type> 
void delete_p2p(Type** ptr, int r_num)
{
	for(int i = 0; i < r_num; i++){
	    delete[] ptr[i];
	}
};

template <typename Type>
Type** create_p2p(int row, int column)
{
    Type** x = new Type*[row];

    for (int i = 0; i < row; ++i) {
        x[i] = new Type[column];
    }

    return x;
}


#endif //LUX_NBMUTILS_H

