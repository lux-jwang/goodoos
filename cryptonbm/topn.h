#include "utils.h"


void perform_topn_stranger(const BIGPOLY *pIb, const int *pRt, int item_size, BIGPOLY &rib, BIGPOLY &qtb);
void perform_topn_friend(const BIGPOLY *pIb, const int *pRf, const BIGPOLY wuf, int item_size, BIGPOLY &rib, BIGPOLY &qfb);
void perform_topn_server(BIGPOLY *pFs, int f_size, BIGPOLY *pTs, int t_size, BIGPOLY *pQFs, int qf_size, BIGPOLY *pQTs, int qt_size, BIGPOLY x_u , BIGPOLY &y_u);
void perform_topn(UID u_id, int *pTgt, int tgt_size, int item_size);