from Public.var_mex_credit import *
from Public.base_ld import *
from Public.dataBase_ld import *
from Public.heads_ld import *
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
    def test_credit_payment(self):
        '''【LanaDigital】/api/credit/payment用户提现接口-正案例'''
    def test_credit_payment_delay(self):
        '''【LanaDigital】/api/credit/payment/delay_payout_handler用户提现(延迟放款)接口-正案例'''
        test_data = for_test_auth_other()
        head = test_data[2]
        r = requests.post(host_api + '/api/credit/payment/delay_payout_handler', headers=head)
        self.assertEqual(r.status_code, 200)
    def test_payment_detail(self):
        '''【LanaDigital】/api/credit/payment/detail提现详情接口-正案例'''
    def test_hook_payment(self):
        '''【LanaDigital】/api/hook/payment支付还款回调接口-正案例'''
    def test_hook_repayment(self):
        '''【LanaDigital】/api/hook/repayment用户还款回调接口-正案例'''
    def test_hook_repayment_cancel(self):
        '''【LanaDigital】/api/hook/repayment/cancel_repayment_orders取消还款订单接口-正案例'''
    def test_credit_repayment_bill(self):
        '''【LanaDigital】/api/credit/repayment/bill账单详情接口-正案例'''
    def test_credit_repayment_history_bill(self):
        '''【LanaDigital】/api/credit/repayment/history/bill账单历史详情接口-正案例'''
    def test_credit_repayMethods(self):
        '''【LanaDigital】/api/credit/repayment/repay/methods/CUST_NO还款方式接口-正案例'''
        registNo = cx_registNo_10()
        headt_api = login_code(registNo)
        r = requests.get(host_api + "/api/credit/repayment/repay/methods" + cust_no, headers=headt_api)
        t = r.json()
        print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(t,
        {"data": {"stp": {"paymentMethod": "STP", "free": true, "recommended": true, "serviceCharge": "0.00",
                          "supportTime": "24/7"},
                  "oxxo": {"paymentMethod": "OXXO", "free": false, "recommended": false, "serviceCharge": "12.00",
                           "supportTime": "24/7"}}, "errorCode": 0, "message": "ok"})
    @classmethod
    def tearDownClass(cls): # 在所有用例都执行完之后运行的
        print("我是tearDownClass，我位于所有用例运行的结束")

