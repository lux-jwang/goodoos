#include "nbmutils.h"


class Worker
{
public:
    static Worker *pInstance()
    {
		if(!s_pInstance){
			s_pInstance = new Worker();
			return s_pInstance;
		}
		return s_pInstance;
    }

    ~Worker(){
    }
	
	// @member variables
	EncryptionParameters m_parms;
	BalancedEncoder m_encoder;
	//KeyGenerator m_generator;
	//BigPolyArray m_public_key;
	//BigPoly m_secret_key;
	Encryptor m_encryptor; //(parms, this->m_public_key);
	Evaluator m_evaluator; //(parms);
	Decryptor m_decryptor;
		
private:
    static  Worker *s_pInstance;
	Worker(){
		build_he_params();
		build_he_tools(this->m_parms);
	}
	void build_he_params();
	void auto_build_he_params();
	void build_he_tools(EncryptionParameters parms);
	
};


Worker *Worker::s_pInstance=0;

void Worker::build_he_params()
{
	//EncryptionParameters m_parms;
	m_parms.poly_modulus() = "1x^2048 + 1";
	m_parms.coeff_modulus() = ChooserEvaluator::default_parameter_options().at(2048);
	m_parms.plain_modulus() = 1 << 8;
	cout << "Encryption parameters specify " << m_parms.poly_modulus().significant_coeff_count() << " coefficients with "
        << m_parms.coeff_modulus().significant_bit_count() << " bits per coefficient" << endl;
}

void Worker::auto_build_he_params()
{
	return;
}

void Worker::build_he_tools(EncryptionParameters parms)
{

	this->m_encoder = BalancedEncoder(parms.plain_modulus());
	// Generate keys.
    cout << "Generating keys..." << endl;
	KeyGenerator generator(parms);
	generator.generate();
	cout << "... key generation complete" << endl;
	BigPolyArray m_public_key = generator.public_key();
	BigPoly m_secret_key = generator.secret_key();

	//cout << "my key1: " << m_secret_key.coeff_count()<<endl;
	//cout << "my key2: " << m_secret_key.coeff_count()<<endl;
	//
	this->m_encryptor = Encryptor(parms, m_public_key);
	this->m_evaluator = Evaluator(parms);
	this->m_decryptor = Decryptor(parms, m_secret_key);

	/*
	this->m_encoder = BalancedEncoder(parms.plain_modulus());
	// Generate keys.
    cout << "Generating keys..." << endl;
	 KeyGenerator m_generator(parms);
	m_generator.generate();
	cout << "... key generation complete" << endl;
	this->m_public_key = m_generator.public_key();
	this->m_secret_key = m_generator.secret_key();

	//
	this->m_encryptor = Encryptor(parms, this->m_public_key);
	this->m_evaluator = Evaluator(parms);
	this->m_decryptor = Decryptor(parms, this->m_secret_key);
	*/
}

//-----------------------------------------------------------



//------------------------------------------------------------
//first level

BIGPOLYARRAY add_c(BIGPOLYARRAY a, BIGPOLYARRAY b) 
{
#ifdef SIM
	return a + b;
#else
	Worker *pwk = Worker::pInstance();
    return pwk->m_evaluator.add(a,b);
#endif	
}

BIGPOLYARRAY add_p(BIGPOLYARRAY a, BIGPOLY b)
{
#ifdef SIM
	return a + b;
#else
	Worker *pwk = Worker::pInstance();
    return pwk->m_evaluator.add_plain(a,b);
#endif	
}

BIGPOLYARRAY mul_c(BIGPOLYARRAY a, BIGPOLYARRAY b)
{
#ifdef SIM
	return a*b;
#else
	Worker *pwk = Worker::pInstance();
    return pwk->m_evaluator.multiply(a,b);
#endif	
}

BIGPOLYARRAY mul_p(BIGPOLYARRAY a, BIGPOLY b)
{
#ifdef SIM
	return a*b;
#else
	Worker *pwk = Worker::pInstance();
    return pwk->m_evaluator.multiply_plain(a,b);
#endif
}

BIGPOLYARRAY sub_c(BIGPOLYARRAY a, BIGPOLYARRAY b)
{
#ifdef SIM
	return a-b;
#else
	Worker *pwk = Worker::pInstance();
    return pwk->m_evaluator.sub(a,b);
#endif	
}

BIGPOLYARRAY sub_p(BIGPOLYARRAY a, BIGPOLY b)
{
#ifdef SIM
	return a-b;
#else
	Worker *pwk = Worker::pInstance();
    return pwk->m_evaluator.sub_plain(a,b);
#endif
}



BIGPOLY init_bigpoly(int val)
{
#ifdef SIM
	return val;
#else
	Worker *pwk = Worker::pInstance();
    return pwk->m_encoder.encode(val);
#endif
}

BIGPOLYARRAY enc_bigpoly(BIGPOLY val)
{
#ifdef SIM
	return val;
#else
	Worker *pwk = Worker::pInstance();
    return pwk->m_encryptor.encrypt(val);
#endif
}

//for int type
bool equal_c(BIGPOLYARRAY a, BIGPOLYARRAY b)
{
#ifdef SIM
	return (a==b);
#else
	Worker *pwk = Worker::pInstance();
    BigPoly da = pwk->m_decryptor.decrypt(a);
    BigPoly db = pwk->m_decryptor.decrypt(b);

    int decoded1 = pwk->m_encoder.decode_int32(da);
    int decoded2 = pwk->m_encoder.decode_int32(db);
    cout <<"a="<<decoded1<<";  b="<<decoded2<<endl;
    return (decoded1 == decoded2);
#endif
}

//--------------------------------------------------------------------
//second level

void init_bigpoly_vec(int *pVec, BIGPOLY *pBpvec, int item_size)
{
	if(NULL == pBpvec || NULL == pVec){return;
    }
   
    for(int indx=0; indx<item_size; indx++)
    {
		pBpvec[indx] = init_bigpoly(pVec[indx]);
	}
}

void enc_bigpoly_vec(BIGPOLY *pBpvec, BIGPOLYARRAY *pBpavec, int item_size)
{
	if(NULL == pBpvec || NULL == pBpavec){return;
    }
   
    for(int indx=0; indx<item_size; indx++)
    {
		pBpavec[indx] = enc_bigpoly(pBpvec[indx]);
	}
}


BIGPOLYARRAY sum_vector(BIGPOLYARRAY *pBpavec, int item_size)
{
    BIGPOLYARRAY sum_v = enc_bigpoly(init_bigpoly(0));
    if(NULL == pBpavec){
    	return sum_v;
    }

    for(int indx=0; indx<item_size; indx++)
    {
         sum_v = ADD_C(sum_v,pBpavec[indx]);
    }

    return sum_v;
}

bool tdsc_compare(BIGPOLY xu, BIGPOLY yu, BIGPOLY threshhold)
{

	return true;
}

//only count non-zero elements
int get_mean(int *pVec, int item_size)
{
    if(NULL == pVec || item_size  < 1){
    	return 0;
    }

    int imean = 0; 
    int count = 0;

    for(int indx=0; indx<item_size; indx++)
    {
    	if(pVec[indx]==0){
    		continue;
    	}
    	imean += pVec[indx];
    	count++;
    }

    if(count==0){
    	return 0;
    }
    return imean/count; //int
}

BIGPOLYARRAY dot_vector(BIGPOLYARRAY *pVec1, BIGPOLYARRAY *pVec2, int item_size)
{
	BIGPOLYARRAY isum = enc_bigpoly(init_bigpoly(0)); // direct assert?

	if(NULL == pVec1 || NULL == pVec2 || item_size <  1){
    	return isum;
    }
    
    for(int indx=0; indx<item_size; indx++)
    {

    	BIGPOLYARRAY tmp = MUL_C(pVec1[indx], pVec2[indx]);
    	isum = ADD_C(tmp,isum);
    }
    return isum;

}


//-----------------------------------------------------------

int** get_friend_data(UID u_id, int &f_num, int &item_size)
{
	f_num = 4;
	item_size = 5;
	return NULL;

}

int** get_stranger_data(UID u_id, int &t_num, int &item_size)
{
	t_num = 4;
	item_size = 5;
	return NULL;

}

int* get_user_sim(UID u_id)
{
	return NULL;
}