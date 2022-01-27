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

    def test_credit_index_1(self):
        '''【LanaDigital】/api/credit/index用户首页状态接口(新客)-正案例'''
        test_data = cx_registNo_01()
        registNo = test_data[0]
        head = login_code(registNo)
        r = requests.get(host_api + '/api/credit/index', headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(t['data']['stat'], 'NEW')
    def test_credit_index_2(self):
        '''【LanaDigital】/api/credit/index用户首页状态接口(逾期)-正案例'''
        test_data = cx_registNo_02()
        registNo = test_data[0]
        head = login_code(registNo)
        r = requests.get(host_api + '/api/credit/index', headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(t['data']['stat'], 'OVERDUE')
    def test_credit_index_3(self):
        '''【LanaDigital】/api/credit/index用户首页状态接口(授信中)-正案例'''
        test_data = cx_registNo_03()
        registNo = test_data[0]
        head = login_code(registNo)
        r = requests.get(host_api + '/api/credit/index', headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(t['data']['stat'], 'CREDITING')
    def test_credit_index_3(self):
        '''【LanaDigital】/api/credit/index用户首页状态接口(冻结)-正案例'''
        test_data = cx_registNo_04()
        registNo = test_data[0]
        head = login_code(registNo)
        r = requests.get(host_api + '/api/credit/index', headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
    def test_credit_index_5(self):
        '''【LanaDigital】/api/credit/index用户首页状态接口(待提现)-正案例'''
        test_data = cx_registNo_05()
        registNo = test_data[0]
        head = login_code(registNo)
        r = requests.get(host_api + '/api/credit/index', headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(t['data']['stat'], 'UNDER_WITHDRAW')
    def test_credit_index_6(self):
        '''【LanaDigital】/api/credit/index用户首页状态接口(锁定)-正案例'''
        test_data = cx_registNo_06()
        registNo = test_data[0]
        head = login_code(registNo)
        r = requests.get(host_api + '/api/credit/index', headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        #self.assertEqual(t['data']['stat'], 'UNDER_WITHDRAW')
    def test_credit_index_7(self):
        '''【LanaDigital】/api/credit/index用户首页状态接口(撤销)-正案例'''
        test_data = cx_registNo_07()
        registNo = test_data[0]
        head = login_code(registNo)
        r = requests.get(host_api + '/api/credit/index', headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(t['data']['stat'], 'NEW')
    def test_payment_detail_1(self):
        '''【LanaDigital】/api/credit/payment/detail提现详情接口(包含额外费用)-正案例'''
        text_data = payout_stp_data_1()
        # print(text_data)
        head = login_code(text_data)
        r = requests.post(host_api + '/api/credit/payment/detail', headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(t['data']['allowWithdraw'], True)
        self.assertEqual(t['data']['totalFeeRate'], '3.50')
        feeDetailList = t['data']['feeDetailList']
        self.assertEqual(feeDetailList[0]['feeValue'], '30.00')
        self.assertEqual(feeDetailList[0]['fixedVal'], True)
        self.assertEqual(feeDetailList[1]['feeValue'], '50.00')
        self.assertEqual(feeDetailList[1]['fixedVal'], True)
    def test_payment_detail_2(self):
        '''【LanaDigital】/api/credit/payment/detail提现详情接口(不包含额外费用)-正案例'''
        text_data = payout_stp_data_2()
        head = login_code(text_data[0])
        r = requests.post(host_api + '/api/credit/payment/detail', headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(t['data']['allowWithdraw'], True)
        #self.assertEqual(t['data']['feeDetailList'], None)
        self.assertEqual(t['data']['totalFeeRate'], "3.50")
    def test_credit_payment_1(self):
        '''【LanaDigital】/api/credit/payment用户提现接口-正案例(没有正在处理的贷款，允许再次提现)'''
        text_data = payout_stp_data_3()
        # print(text_data)
        head = login_code(text_data[0])
        amt = '500'
        data = {"withdrawAmt": amt}
        r = requests.post(host_api + '/api/credit/payment', data=json.dumps(data), headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
    def test_credit_payment_2(self):
        '''【LanaDigital】/api/credit/payment用户提现接口-正案例(有正在处理的贷款，不允许再次提现)'''
        text_data = payout_stp_data_4()
        head = login_code(text_data[0])
        amt = '500'
        data = {"withdrawAmt": amt}
        r = requests.post(host_api + '/api/credit/payment', data=json.dumps(data), headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 1019)
        self.assertEqual(t['message'], 'Se está procesando el retiro del pedido')
    def test_credit_payment_delay(self):
        '''【LanaDigital】/api/credit/payment/anon/delay_payout_handler用户提现(延迟放款)接口-正案例'''
        phone = lay_registNo()
        head = login_code(phone)
        t = requests.post(host_api + '/api/credit/payment/anon/delay_payout_handler', headers=head, verify=False)
        # print(t)
        self.assertEqual(t.status_code, 200)
    def test_payout_stp_1(self):
        '''【LanaDigital】/api/web_hook/payout/stp模拟stp放款回调成功接口-正案例'''
        text_data = payout_stp_data_success()
        # print(text_data)
        folioOrigen = text_data[0]
        id = text_data[1]
        head = login_code(text_data[2])
        data = {"causaDevolucion": {"code": 16,
                                    "msg": "Tipo de operación errónea"},
                "empresa": "ASSERTIVE",
                "estado": {"code": "0000",
                           "msg": "canll"},
                "folioOrigen": folioOrigen,
                "id": id}
        r = requests.post(host_pay + '/api/web_hook/payout/stp', data=json.dumps(data), headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
    def test_payout_stp_2(self):
        '''【LanaDigital】/api/web_hook/payout/stp模拟stp放款回调失败接口-正案例("code": "0002")'''
        text_data = payout_stp_data_failure()
        folioOrigen = text_data[0]
        id = text_data[1]
        head = login_code(text_data[2])
        data = {"causaDevolucion": {"code": 16,
                                    "msg": "Tipo de operación errónea"},
                "empresa": "ASSERTIVE",
                "estado": {"code": "0002",
                           "msg": "error"},
                "folioOrigen": folioOrigen,
                "id": id}
        r = requests.post(host_pay + '/api/web_hook/payout/stp', data=json.dumps(data), headers=head, verify=False)
        # print(r)
        t = r.json()
        self.assertEqual(t['errorCode'], 0)
    def test_index_evaluation(self):
        '''【LanaDigital】/api/credit/index/evaluation评价接口-正案例'''
        text_data = evaluation_registNo()
        head = login_code(text_data[0])
        cust_no = text_data[1]
        loan_no = text_data[2]
        data = {"custNo": cust_no,
                "loanNo": loan_no,
                "score": 2}
        r = requests.post(host_api + '/api/credit/index/evaluation', data=data, headers=head, verify=False)
        t = r.json()
        # print(t)
        # self.assertEqual(t['errorCode'], 0)
    def test_credit_repayment_bill(self):
        '''【LanaDigital】/api/credit/repayment/bill账单详情接口-正案例'''
        text_data = repay_data_1()
        headt_api = login_code(text_data[0][1])
        r = requests.get(host_api + '/api/credit/repayment/bill', headers=headt_api, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        # self.assertEqual(t['data']['totalUsedAmt'], '5080.00')
        # billDetailList = t['data']['billDetailList']
        # for i in range(len(billDetailList)):
        #     # print(billDetailList[i])
        #     self.assertEqual(billDetailList[i]['settlementTime'], 0)
        #     #self.assertEqual(billDetailList[i][''])
    def test_credit_repayment_history_bill(self):
        '''【LanaDigital】/api/credit/repayment/history/bill账单历史详情接口-正案例'''
        text_data = repay_data_1()
        head = login_code(text_data[0][1])
        r = requests.get(host_api + '/api/credit/repayment/history/bill', headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
    def test_credit_repayMethods(self):
        '''【LanaDigital】/api/credit/repayment/repay/methods/CUST_NO还款方式接口-正案例'''
        text_data = repay_data_1()
        cust_no = text_data[0][0]
        headt_api = login_code(text_data[0][1])
        r = requests.post(host_api + '/api/credit/repayment/repay/methods/' + cust_no, headers=headt_api, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(t,
                  {"data": {"stp": {"paymentMethod": "STP",
                                    "free": True,
                                    "recommended": True,
                                    "serviceCharge": "0.00",
                                    "supportTime": "24/7"},
                            "oxxo": {"paymentMethod": "OXXO",
                                     "free": False,
                                     "recommended": False,
                                     "serviceCharge": "12.00",
                                     "supportTime": "24/7"}},
                   "errorCode": 0,
                   "message": "ok"})
    def test_credit_repaymentRepay_STP_1(self):
        '''【LanaDigital】/api/credit/repayment/repay还款获取码(STP)有在贷（正常）-正案例'''
        text_data = repay_data_1()
        head = login_code(text_data[0][1])
        loan_no = text_data[0][2]
        amt = text_data[0][3]
        data = {"repaymentList": [{"loanNo": loan_no,
                                   "repayAmt": amt}],
                "repaymentMethod": "STP"}
        r = requests.post(host_pay + '/api/credit/repayment/repay', data=json.dumps(data), headers=head, verify=False)
        t = r.json()
        # print(t)
        # self.assertEqual(t['errorCode'],0)
    def test_credit_repaymentRepay_STP_2(self):
        '''【LanaDigital】/api/credit/repayment/repay还款获取码(STP)有在贷（逾期）-正案例'''
        text_data = repay_data_2()
        head = login_code(text_data[0][1])
        loan_no = text_data[0][2]
        amt = text_data[0][3]
        data = {"repaymentList": [{"loanNo": loan_no,
                                   "repayAmt": amt}],
                "repaymentMethod": "STP"}
        r = requests.post(host_pay + '/api/credit/repayment/repay', data=json.dumps(data), headers=head, verify=False)
        t = r.json()
        # print(t)
        # self.assertEqual(t['errorCode'],0)
    def test_credit_repaymentRepay_OXXO_1(self):
        '''【LanaDigital】/api/credit/repayment/repay还款获取码(OXXO)有在贷（正常）-正案例'''
        text_data = repay_data_1()
        head = login_code(text_data[0][1])
        loan_no = text_data[0][2]
        amt = text_data[0][3]
        data = {"repaymentList": [{"loanNo": loan_no,
                                   "repayAmt": amt}],
                "repaymentMethod": "OXXO"}
        r = requests.post(host_pay + '/api/credit/repayment/repay', data=json.dumps(data), headers=head, verify=False)
        t = r.json()
        # print(t)
        #self.assertEqual(t['errorCode'], 0)
    def test_credit_repaymentRepay_OXXO_2(self):
        '''【LanaDigital】/api/credit/repayment/repay还款获取码(OXXO)有在贷（逾期）-正案例'''
        text_data = repay_data_2()
        # print(text_data)
        head = login_code(text_data[0][1])
        loan_no = text_data[0][2]
        amt = text_data[0][3]
        data = {"repaymentList": [{"loanNo": loan_no,
                                   "repayAmt": amt}],
                "repaymentMethod": "OXXO"}
        r = requests.post(host_pay + '/api/credit/repayment/repay', data=json.dumps(data), headers=head,
                          verify=False)
        t = r.json()
        # print(t)
        # self.assertEqual(t['errorCode'], 0)
    def test_webhook_repaySTP_1(self):
        '''【LanaDigital】/api/web_hook/repay/stp还款接口-STP模拟银行回调-有在贷（正常）验证结清-正案例'''
        ids = str(random.randint(111111111, 999999999)) #9位随机数作为id
        text_data = repay_data_3()
        # print(text_data)
        head = login_code(text_data[0][0])
        amt = text_data[0][1]
        clabe_no = text_data[0][2]
        account_no = text_data[0][3]
        cust_no = text_data[0][4]
        data = {"abono": {"id": ids,
                          "monto": amt,
                          "cuentaBeneficiario": clabe_no,
                          "fechaOperacion": "20210108",
                          "institucionOrdenante": "40012",
                          "institucionBeneficiaria": "90646",
                          "claveRastreo": "MBAN01002101080089875109",
                          "nombreOrdenante": "HAZEL VIRIDIANA RUIZ RICO",
                          "tipoCuentaOrdenante": "40",
                          "cuentaOrdenante": "012420028362208190",
                          "rfcCurpOrdenante": "RURH8407075F8",
                          "nombreBeneficiario": "STP",
                          "tipoCuentaBeneficiario": "40",
                          "rfcCurpBeneficiario": "null",
                          "conceptoPago": "ESTELA SOLICITO TRANSFERENCIA",
                          "referenciaNumerica": "701210",
                          "empresa": "QUANTX_TECH"}}
        r = requests.post(host_pay + '/api/web_hook/repay/stp', data=json.dumps(data), headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        t1 = cx_fin_ad_dtl_1(account_no)
        self.assertIsNone(t1)
        t2 = cx_cu_cust_status_info(cust_no)
        # print(t2)
        self.assertEqual(t2, '20040007')
    def test_webhook_repaySTP_2(self):
        '''【LanaDigital】/api/web_hook/repay/stp还款接口-STP模拟银行回调-有在贷（逾期）验证结清-正案例'''
        ids = str(random.randint(111111111, 999999999)) #9位随机数作为id
        text_data = repay_data_4()
        # print(text_data)
        head = login_code(text_data[0][0])
        amt = text_data[0][1]
        clabe_no = text_data[0][2]
        account_no = text_data[0][3]
        cust_no = text_data[0][4]
        data = {"abono": {"id": ids,
                          "monto": amt,
                          "cuentaBeneficiario": clabe_no,
                          "fechaOperacion": "20210108",
                          "institucionOrdenante": "40012",
                          "institucionBeneficiaria": "90646",
                          "claveRastreo": "MBAN01002101080089875109",
                          "nombreOrdenante": "HAZEL VIRIDIANA RUIZ RICO",
                          "tipoCuentaOrdenante": "40",
                          "cuentaOrdenante": "012420028362208190",
                          "rfcCurpOrdenante": "RURH8407075F8",
                          "nombreBeneficiario": "STP",
                          "tipoCuentaBeneficiario": "40",
                          "rfcCurpBeneficiario": "null",
                          "conceptoPago": "ESTELA SOLICITO TRANSFERENCIA",
                          "referenciaNumerica": "701210",
                          "empresa": "QUANTX_TECH"}}
        r = requests.post(host_pay + '/api/web_hook/repay/stp', data=json.dumps(data), headers=head, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        t1 = cx_fin_ad_dtl_1(account_no)
        self.assertIsNone(t1)
        t2 = cx_cu_cust_status_info(cust_no)
        self.assertEqual(t2, '20040007')
    @classmethod
    def tearDownClass(cls): # 在所有用例都执行完之后运行的
        print("我是tearDownClass，我位于所有用例运行的结束")

 