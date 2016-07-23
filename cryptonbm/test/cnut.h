#ifndef __CNUT__H__
#define __CNUT__H__

#include <cppunit/TestFixture.h>
#include <cppunit/extensions/HelperMacros.h>


class CryptonbmTest : public CppUnit::TestFixture {
    CPPUNIT_TEST_SUITE( CryptonbmTest );
  
    CPPUNIT_TEST( Test_perform_spp_stranger );
    CPPUNIT_TEST( Test_perform_spp_friend );
    CPPUNIT_TEST( Test_perform_spp_server );
    CPPUNIT_TEST( Test_perform_spp );

    CPPUNIT_TEST( Test_perform_topn_stranger );
    CPPUNIT_TEST( Test_perform_topn_friend );
    CPPUNIT_TEST( Test_perform_topn_server );
    CPPUNIT_TEST( Test_perform_topn );

    CPPUNIT_TEST( Test_math_op );
    CPPUNIT_TEST( Test_get_data_2d );
    CPPUNIT_TEST( Test_get_user_sim );

    CPPUNIT_TEST_SUITE_END();

 public:
    void setUp(void) {}    // 
    void tearDown(void) {} //

    void Test_perform_spp_stranger(void); 
    void Test_perform_spp_friend(void); 
    void Test_perform_spp_server(void);
    void Test_perform_spp(void);

    void Test_perform_topn_stranger(void); 
    void Test_perform_topn_friend(void); 
    void Test_perform_topn_server(void);
    void Test_perform_topn(void);

    void Test_math_op(void);
    void Test_get_data_2d(void);
    void Test_get_user_sim(void);

};




#endif