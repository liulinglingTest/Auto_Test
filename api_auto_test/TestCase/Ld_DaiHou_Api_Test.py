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
    def test_payment_detail(self):
        '''【LanaDigital】/api/credit/payment/detail提现详情接口-正案例'''
    def test_credit_payment_delay(self):
        '''【LanaDigital】/api/credit/payment/anon/delay_payout_handler用户提现(延迟放款)接口-正案例'''
        phone=lay_registNo()
        head=login_code(phone)
        t = requests.post(host_api + '/api/credit/payment/anon/delay_payout_handler', headers=head,verify=False)
        # print(t)
        self.assertEqual(t.status_code,200)
    def test_payout_stp_1(self):
        '''【LanaDigital】/api/web_hook/payout/stp模拟stp放款回调成功接口-正案例'''
        text_data=payout_stp_data()
        folioOrigen=text_data[0]
        id=text_data[1]
        head = login_code(text_data[2])
        data={"causaDevolucion": {"code": 16,"msg": "Tipo de operación errónea"},"empresa": "ASSERTIVE","estado": {"code": "0000","msg": "canll"},"folioOrigen": folioOrigen,"id": id}
        r=requests.post(host_pay+'/api/web_hook/payout/stp', data=json.dumps(data), headers=head, verify=False)
        # print(r)
        t = r.json()
        self.assertEqual(t['errorCode'], 0)
    def test_payout_stp_2(self):
        '''【LanaDigital】/api/web_hook/payout/stp模拟stp放款回调失败接口-正案例("code": "0002")'''
        text_data = payout_stp_data()
        folioOrigen = text_data[0]
        id = text_data[1]
        head = login_code(text_data[2])
        data = {"causaDevolucion": {"code": 16, "msg": "Tipo de operación errónea"}, "empresa": "ASSERTIVE",
                "estado": {"code": "0002", "msg": "error"}, "folioOrigen": folioOrigen,"id": id}
        r = requests.post(host_pay + '/api/web_hook/payout/stp', data=json.dumps(data), headers=head, verify=False)
        # print(r)
        t = r.json()
        self.assertEqual(t['errorCode'], 0)
    def test_hook_payment(self):
        '''【LanaDigital】/api/hook/payment支付还款回调接口-正案例'''
    def test_hook_repayment(self):
        '''【LanaDigital】/api/hook/repayment用户还款回调接口-正案例'''
    def test_hook_repayment_cancel(self):
        '''【LanaDigital】/api/hook/repayment/cancel_repayment_orders取消还款订单接口-正案例'''
    def test_credit_repayment_bill(self):
        '''【LanaDigital】/api/credit/repayment/bill账单详情接口-正案例'''
        text_data = repay_data()
        headt_api = login_code(text_data[1])
        r = requests.get(host_api + '/api/credit/repayment/bill', headers=headt_api,verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        #self.assertEqual(t['data']['totalUsedAmt'],'5080.00')
        billDetailList=t['data']['billDetailList']
        for i in range(len(billDetailList)):
            # print(billDetailList[i])
            self.assertEqual(billDetailList[i]['settlementTime'],0)
            #self.assertEqual(billDetailList[i][''])

    def test_credit_repayment_history_bill(self):
        '''【LanaDigital】/api/credit/repayment/history/bill账单历史详情接口-正案例'''
    def test_credit_repayMethods(self):
        '''【LanaDigital】/api/credit/repayment/repay/methods/CUST_NO还款方式接口-正案例'''
        text_data = repay_data()
        cust_no = text_data[0]
        headt_api = login_code(text_data[1])
        r = requests.post(host_api + '/api/credit/repayment/repay/methods/' + cust_no, headers=headt_api,verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(t,
                  {"data": {"stp": {"paymentMethod": "STP", "free": True, "recommended": True, "serviceCharge": "0.00","supportTime": "24/7"},
                  "oxxo": {"paymentMethod": "OXXO", "free": False, "recommended": False, "serviceCharge": "12.00","supportTime": "24/7"}}, "errorCode": 0, "message": "ok"})
    @classmethod
    def tearDownClass(cls): # 在所有用例都执行完之后运行的
        print("我是tearDownClass，我位于所有用例运行的结束")

