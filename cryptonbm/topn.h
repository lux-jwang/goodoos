#ifndef LUX_TOPN_H
#define LUX_TOPN_H


#include "nbmutils.h"

void perform_topn_stranger(CSTMARK int *pRt, BIGPOLYARRAY *pIb, BIGPOLYARRAY *pBias, int item_size);
void perform_topn_friend(CSTMARK int *pRf, CSTMARK BIGPOLYARRAY wuf, BIGPOLYARRAY *pIb, BIGPOLYARRAY *pBias, int item_size);
void perform_topn_server(CSTMARK BIGPOLYARRAY **pFs, CSTMARK BIGPOLYARRAY **pTs, CSTMARK BIGPOLYARRAY **pQFs, \
	 CSTMARK BIGPOLYARRAY **pQTs, int alpha, int beta, int item_size, int f_num, int t_num, BIGPOLYARRAY *pXu, BIGPOLYARRAY *pYu);
//void perform_topn(UID u_id, int *pTgt, int tgt_size);
void perform_topn(UID u_id, int f_num, int t_num, int item_size);

#endif