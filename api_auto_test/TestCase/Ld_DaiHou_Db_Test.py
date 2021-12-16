from Public.var_mex_credit import *
from Public.base_ld import *
from Public.dataBase_ld import *
from Public.heads_ld import *
from Public.check_table import *
import requests,json,datetime
import unittest
class DaiHou_Api_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # 在所有用例执行之前运行的
        print('我是setUpclass，我位于所有用例的开始')
    def setUp(self):  # 每个用例运行之前运行的
        print('setup_test')
    def tearDown(self):  # 每个用例运行之后运行的
        print('teardown_test')
    def test_check_success(self):
        '''【LanaDigital】放款成功后，无还款和减免，相关4个表关键字段值核对-正案例'''
        sql = 'select CURRENT_DATE;'
        date_time = DataBase(which_db).get_one(sql)
        billdate = str(date_time[0] + datetime.timedelta(days=30))
        # print(billdate)
        data = payout_stp_data_success_1()
        cust_no = data[0]
        loan_no = data[1]
        account_no = data[2]
        t1 = cx_lo_loan_dtl(loan_no)
        # print(t1)
        self.assertEqual(t1, [('500.00', '500.00', '10260005', '10270002')])

        t2 = cx_pay_tran_dtl(loan_no)
        # print(t2)
        self.assertEqual(t2, [('10220002', '500.00')])

        t3 = cx_fin_account_info(account_no)
        # print(t3)
        self.assertIsNotNone(t3)

        t4 = cx_fin_payout_dtl(loan_no)
        # print(t4)
        self.assertEqual(t4, [('10420002', '500.00')])
    def test_check_failure(self):
        '''【LanaDigital】放款成功后又失败，无还款和减免，相关10个表关键字段值核对-正案例'''
        data = payout_stp_data_failure_1()
        cust_no = data[0]
        loan_no = data[1]
        account_no = data[2]
        t1 = cx_lo_loan_dtl(loan_no)
        # print(t1)
        self.assertEqual(t1, [('500.00', '500.00', '10260009', 'None')])

        t2 = cx_cu_cust_bill_dtl(cust_no)
        # print(t2)
        self.assertIsNone(t2)

        t3 = cx_cu_cust_fee_bill_dtl(cust_no)
        # print(t3)
        self.assertIsNone(t3)

        t4 = cx_pay_tran_dtl(loan_no)
        # print(t4)
        self.assertEqual(t4, [('10220003', '0.00')])

        t5 = cx_fin_account_info(account_no)
        # print(t5)
        self.assertEqual(t5, (None,))

        t6 = cx_fin_payout_dtl(loan_no)
        # print(t6)
        self.assertEqual(t6, [( '10420003', '500.00')])

        t7 = cx_fin_account_turnover_dtl(account_no)
        # print(t7)
        self.assertIsNone(t7)

        t8 = cx_fin_ad_dtl(account_no)
        # print(t8)
        self.assertIsNone(t8)

        t9 = cx_fin_ad_record(account_no)
        # print(t9)
        self.assertIsNone(t9)

        t10 = cx_fin_rc_dtl(account_no)
        # print(t10)
        self.assertIsNone(t10)
    @classmethod
    def tearDownClass(cls): # 在所有用例都执行完之后运行的
        print("我是tearDownClass，我位于所有用例运行的结束")