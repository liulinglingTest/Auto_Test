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

    def test_credit_index(self):
        '''【LanaDigital】/api/credit/index用户首页状态接口-正案例'''
        test_data = cx_registNo_04()
        registNo = test_data[0]
        head = login_code(registNo)
        r = requests.get(host_api+'/api/credit/index',headers=head,verify=False)
        t = r.json()
        #print(t)
        self.assertEqual(t['errorCode'],0)
    def test_payment_detail_1(self):
        '''【LanaDigital】/api/credit/payment/detail提现详情接口(包含额外费用)-正案例'''
        text_data = payout_stp_data_1()
        head = login_code(text_data)
        r = requests.post(host_api+'/api/credit/payment/detail',headers=head,verify=False)
        t = r.json()
        #print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data']['allowWithdraw'],True)
        self.assertEqual(t['data']['totalFeeRate'], '3.50')
        feeDetailList = t['data']['feeDetailList']
        self.assertEqual(feeDetailList[0]['feeValue'],'30.00')
        self.assertEqual(feeDetailList[0]['fixedVal'], True)
        self.assertEqual(feeDetailList[1]['feeValue'],'50.00')
        self.assertEqual(feeDetailList[1]['fixedVal'], True)
    def test_payment_detail_2(self):
        '''【LanaDigital】/api/credit/payment/detail提现详情接口(不包含额外费用)-正案例'''
        text_data = payout_stp_data_2()
        head = login_code(text_data[0])
        r = requests.post(host_api+'/api/credit/payment/detail',headers=head,verify=False)
        t = r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data']['allowWithdraw'], True)
        #self.assertEqual(t['data']['feeDetailList'],None)
        self.assertEqual(t['data']['totalFeeRate'],"3.50")
    def test_credit_payment_1(self):
        '''【LanaDigital】/api/credit/payment用户提现接口-正案例(没有正在处理的贷款，允许再次提现)'''
        text_data = payout_stp_data_3()
        head = login_code(text_data[0])
        amt = '600'
        data = {"withdrawAmt":amt}
        r = requests.post(host_api+'/api/credit/payment',data=json.dumps(data),headers=head,verify=False)
        t = r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
    def test_credit_payment_2(self):
        '''【LanaDigital】/api/credit/payment用户提现接口-正案例(有正在处理的贷款，不允许再次提现)'''
        text_data = payout_stp_data_4()
        head = login_code(text_data[0])
        amt = '600'
        data = {"withdrawAmt":amt}
        r = requests.post(host_api+'/api/credit/payment',data=json.dumps(data),headers=head,verify=False)
        t = r.json()
        print(t)
        self.assertEqual(t['errorCode'],1019)
        self.assertEqual(t['message'],'Se está procesando el retiro del pedido')
    def test_credit_payment_delay(self):
        '''【LanaDigital】/api/credit/payment/anon/delay_payout_handler用户提现(延迟放款)接口-正案例'''
        phone = lay_registNo()
        head = login_code(phone)
        t = requests.post(host_api + '/api/credit/payment/anon/delay_payout_handler', headers=head,verify=False)
        # print(t)
        self.assertEqual(t.status_code,200)
    def test_payout_stp_1(self):
        '''【LanaDigital】/api/web_hook/payout/stp模拟stp放款回调成功接口-正案例'''
        text_data = payout_stp_data_success()
        folioOrigen = text_data[0]
        id = text_data[1]
        head = login_code(text_data[2])
        data = {"causaDevolucion": {"code": 16,"msg": "Tipo de operación errónea"},"empresa": "ASSERTIVE",
                "estado": {"code": "0000","msg": "canll"},"folioOrigen": folioOrigen,"id": id}
        r = requests.post(host_pay+'/api/web_hook/payout/stp', data=json.dumps(data), headers=head, verify=False)
        # print(r)
        t = r.json()
        self.assertEqual(t['errorCode'], 0)
        list_data = check_table_success(text_data[3])
        print(list_data)
        self.assertEqual(list_data[0],'10260005') # lo_loan_dtl表中贷前状态为已提现
        self.assertIsNotNone(list_data[1]) # 账单日不为空【cu_cust_bill_dtl】
        self.assertIsNotNone(list_data[2]) # 账单日不为空【cu_cust_fee_bill_dtl】
        # self.assertIsNotNone(list_data[3]) # 账单日不为空【cu_cust_fee_dtl】
        self.assertEqual(list_data[4],'10220002') # pay_交易明细表 【放款成功，状态变更为10220002-交易成功】
        self.assertIsNotNone(list_data[5]) # 账单日不为空【fin_account_info】
        #self.assertEqual(list_data[6],'10420002') # fin_payout_dtl 【放款成功,状态置为10420002成功】
    def test_payout_stp_2(self):
        '''【LanaDigital】/api/web_hook/payout/stp模拟stp放款回调失败接口-正案例("code": "0002")'''
        text_data = payout_stp_data_failure()
        folioOrigen = text_data[0]
        id = text_data[1]
        head = login_code(text_data[2])
        data = {"causaDevolucion": {"code": 16, "msg": "Tipo de operación errónea"}, "empresa": "ASSERTIVE",
                "estado": {"code": "0002", "msg": "error"}, "folioOrigen": folioOrigen,"id": id}
        r = requests.post(host_pay + '/api/web_hook/payout/stp', data=json.dumps(data), headers=head, verify=False)
        # print(r)
        t = r.json()
        self.assertEqual(t['errorCode'], 0)
        # list_data = check_table_failure(text_data[3])
        # print(list_data)
        # self.assertEqual(list_data[0], '10260009') # lo_loan_dtl 放款失败会回滚-贷前状态变更为10260009
        # self.assertEqual(list_data[1], None) # cu_账单信息表：账单日，状态正确【放款失败会回滚，删掉数据】
        # self.assertEqual(list_data[2], None) # cu_账单信息表,关联了放款本金和额外费用【放款失败会回滚，删掉数据】
        # self.assertEqual(list_data[3], '10420003') # lo_客户收费信息表，记录额外费用【放款失败会回滚，状态变更为10420003-交易失败】
        # self.assertEqual(list_data[4], None) # cu_客户费用项关系信息表:【放款失败会回滚】放款失败,bill_date为空
        # self.assertEqual(list_data[5], '10220003') # pay_交易明细表 【放款失败会回滚，状态变更为10220003-交易失败】
        # self.assertEqual(list_data[6], None) # fin_账户信息表，BILL_DATE回滚置空
        # self.assertEqual(list_data[7], None) # fin_账户流水表，order_no=tran_order_no值【放款失败会回滚-删掉放款数据】
        # self.assertEqual(list_data[8], None) # fin_应收明细表，汇总【放款失败会回滚，删掉数据】
        # self.assertEqual(list_data[9], None) # fin_应收明细记录表，每笔记录【放款失败会回滚，删掉数据】
        # self.assertEqual(list_data[10], '10420003') # fin_payout_dtl 【放款失败会回滚,状态置为10420003失败】
        # self.assertEqual(list_data[11], None) # fin_实付明细表【放款失败会回滚-删掉数据】
    def test_credit_repayment_bill(self):
        '''【LanaDigital】/api/credit/repayment/bill账单详情接口-正案例'''
        text_data = repay_data()
        headt_api = login_code(text_data[0][1])
        r = requests.get(host_api + '/api/credit/repayment/bill', headers=headt_api,verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        # self.assertEqual(t['data']['totalUsedAmt'],'5080.00')
        # billDetailList = t['data']['billDetailList']
        # for i in range(len(billDetailList)):
        #     # print(billDetailList[i])
        #     self.assertEqual(billDetailList[i]['settlementTime'],0)
        #     #self.assertEqual(billDetailList[i][''])
    def test_credit_repayment_history_bill(self):
        '''【LanaDigital】/api/credit/repayment/history/bill账单历史详情接口-正案例'''
        text_data = repay_data()
        head = login_code(text_data[0][1])
        r = requests.get(host_api+'/api/credit/repayment/history/bill',headers=head,verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'],0)
    def test_credit_repayMethods(self):
        '''【LanaDigital】/api/credit/repayment/repay/methods/CUST_NO还款方式接口-正案例'''
        text_data = repay_data()
        cust_no = text_data[0][0]
        headt_api = login_code(text_data[0][1])
        r = requests.post(host_api + '/api/credit/repayment/repay/methods/' + cust_no, headers=headt_api,verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(t,
                  {"data": {"stp": {"paymentMethod": "STP", "free": True, "recommended": True, "serviceCharge": "0.00","supportTime": "24/7"},
                  "oxxo": {"paymentMethod": "OXXO", "free": False, "recommended": False, "serviceCharge": "12.00","supportTime": "24/7"}}, "errorCode": 0, "message": "ok"})
    # def test_credit_repaySTP(self):
    #     '''【LanaDigital】/api/hook/repayment/cancel_repayment_orders取消还款订单接口-正案例'''
    def test_credit_repaymentRepay_STP(self):
        '''【LanaDigital】/api/credit/repayment/repay还款获取码(STP)-正案例'''
        text_data = repay_data()
        head = login_code(text_data[0][1])
        loan_no = text_data[0][2]
        amt = text_data[0][3]
        data = {"repaymentList":[{"loanNo":loan_no,"repayAmt":amt}],"repaymentMethod":"STP"}
        r = requests.post(host_pay + '/api/credit/repayment/repay',data=json.dumps(data),headers=head,verify=False)
        t = r.json()
        # print(t)
        # self.assertEqual(t['errorCode'],0)
    def test_credit_repaymentRepay_OXXO(self):
        '''【LanaDigital】/api/credit/repayment/repay还款获取码(OXXO)-正案例'''
        text_data = repay_data()
        head = login_code(text_data[0][1])
        loan_no = text_data[0][2]
        amt = text_data[0][3]
        data = {"repaymentList": [{"loanNo": loan_no, "repayAmt": amt}], "repaymentMethod": "OXXO"}
        r = requests.post(host_pay + '/api/credit/repayment/repay', data=json.dumps(data), headers=head, verify=False)
        t = r.json()
        # print(t)
        #self.assertEqual(t['errorCode'], 0)
    def test_webhook_repaySTP(self):
        '''【LanaDigital】/api/web_hook/repay/stp模拟stp还款回调接口-正案例'''
        ids = str(random.randint(111111111,999999999)) #9位随机数作为id
        text_data = repay_data()
        head = login_code(text_data[0][1])
        clabe_no = text_data[0][4]
        amt = 100
        data = {"abono": {"id": ids,"monto": amt,"cuentaBeneficiario": clabe_no,"fechaOperacion": "20210108","institucionOrdenante": "40012",
        "institucionBeneficiaria": "90646","claveRastreo": "MBAN01002101080089875109","nombreOrdenante": "HAZEL VIRIDIANA RUIZ RICO","tipoCuentaOrdenante": "40",
        "cuentaOrdenante": "012420028362208190","rfcCurpOrdenante": "RURH8407075F8","nombreBeneficiario": "STP","tipoCuentaBeneficiario": "40",
        "rfcCurpBeneficiario": "null","conceptoPago": "ESTELA SOLICITO TRANSFERENCIA","referenciaNumerica": "701210","empresa": "QUANTX_TECH"}}
        r = requests.post(host_pay+'/api/web_hook/repay/stp',data=json.dumps(data),headers=head,verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'],0)
    @classmethod
    def tearDownClass(cls): # 在所有用例都执行完之后运行的
        print("我是tearDownClass，我位于所有用例运行的结束")

