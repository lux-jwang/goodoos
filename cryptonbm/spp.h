
#include "utils.h"

using namespace std;



void perform_spp_stranger(const BIGPOLY *pIb, const int *pRt, int item_size, BIGPOLY &rib, BIGPOLY &qtb);
void perform_spp_friend(const BIGPOLY *pIb, const int *pRf, const BIGPOLY wuf, int item_size, BIGPOLY &rib, BIGPOLY &qfb);
void perform_spp_server(BIGPOLY *pFs, int f_size, BIGPOLY *pTs, int t_size, BIGPOLY *pQFs, int qf_size, BIGPOLY *pQTs, int qt_size, BIGPOLY x_u , BIGPOLY &y_u);
void perform_spp(UID u_id, int *pTgt, int tgt_size, int item_size);