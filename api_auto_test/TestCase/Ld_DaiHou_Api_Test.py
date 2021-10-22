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
        '''【LanaDigital】/api/credit/payment/delay_payout_handler用户提现接口(延迟放款)-正案例'''
    def test_payment_detail(self):
        '''【LanaDigital】/api/credit/payment/detail提现详情接口-正案例'''
    def test_hook_payment(self):
        '''【LanaDigital】/api/hook/payment支付还款回调接口-正案例'''
    def test_hook_repayment(self):
        '''【LanaDigital】/api/hook/repayment用户还款回调接口-正案例'''
    def test_hook_repayment_cancel(self):
        '''【LanaDigital】/api/hook/repayment/cancel_repayment_orders取消还款订单接口-正案例'''
    def test_hook_repayment_cancel(self):
        '''【LanaDigital】/api/hook/repayment/cancel_repayment_orders取消还款订单接口-正案例'''
    def test_hook_repay_apply_collection(self):
        '''【LanaDigital】/api/hook/repay/apply/collection催收还款码获取接口-正案例'''

    @classmethod
    def tearDownClass(cls): # 在所有用例都执行完之后运行的
        print("我是tearDownClass，我位于所有用例运行的结束")

