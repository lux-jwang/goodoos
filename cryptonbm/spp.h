#ifndef LUX_SPP_H
#define LUX_SPP_H

#include "nbmutils.h"

void perform_spp_stranger(CSTMARK BIGPOLYARRAY *pIb, CSTMARK int *pRt, int item_size, BIGPOLYARRAY &rib, BIGPOLYARRAY &qtb);
void perform_spp_friend(CSTMARK BIGPOLYARRAY *pIb, CSTMARK int *pRf, CSTMARK BIGPOLYARRAY wuf, int item_size, BIGPOLYARRAY &rib, BIGPOLYARRAY &qfb);
void perform_spp_server(CSTMARK BIGPOLYARRAY *pFs, CSTMARK BIGPOLYARRAY *pTs, CSTMARK BIGPOLYARRAY *pQFs, CSTMARK BIGPOLYARRAY *pQTs, \
	 BIGPOLY alpha, BIGPOLY beta, BIGPOLY ab, int f_size, int t_size, BIGPOLYARRAY &x_u , BIGPOLYARRAY &y_u );
//void perform_spp(UID u_id, int *pTgt, int item_size);
void perform_spp(UID u_id, int *pTgt, int tgt_size, int f_num, int t_num, int item_size);

#endif