from Public.base_ld import *
from Public.dataBase_ld import *
from Public.var_mex_credit import *
import random
import unittest,requests,json
class DaiQian_Api_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  #在所有用例执行之前运行的
        print('我是setUpclass，我位于所有用例的开始')
    def setUp(self):  #每个用例运行之前运行的
        print('setup_test')
    def tearDown(self): #每个用例运行之后运行的
        print('teardown_test')
    def test_login_code(self):    #函数名要以test开头，否则不会被执行
        '''【LanaDigital】/api/cust/login注册登录接口-正案例'''      #用例描述，在函数下，用三个单引号里面写用例描述
        registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
        '''/api/cust/check/user/state获取用户状态'''
        s=huoqu_user_state(registNo)
        code=compute_code(registNo)
        data={"code":code,"hasPwd":s['data']['hasPwd'],"phoneNo":registNo,"gaid":"Exception:null"}
        r=requests.post(host_api+"/api/cust/login",data=json.dumps(data),headers=head_api,verify=False)
        self.assertEqual(r.status_code,200)
        t=r.json()
        token=t['data']['token']
        self.assertIsNotNone(token)
        self.assertEqual(t['errorCode'],0)
    def test_login_pwd(self):
        '''【LanaDigital】/api/cust/pwd/login使用密码登录接口-正案例'''
        phoneNo=cx_old_phoneNo()
        s=huoqu_user_state(phoneNo)
        #print('s--',s)
        data={"phoneNo":phoneNo,"password":"123456","hasPwd":s['data']['hasPwd'],"gaid":"Exception:null"}
        r=requests.post(host_api+"/api/cust/pwd/login",data=json.dumps(data),headers=head_api,verify=False)
        t=r.json()
        #print('t--',t)
        self.assertEqual(t['errorCode'],0)
        token=t['data']['token']
        self.assertIsNotNone(token)
    def test_update_pwd(self):
        '''【LanaDigital】/api/cust/pwd/update更新用户密码接口-正案例'''
        test_data=login_code()
        phoneNo=test_data[0]
        head=test_data[1]
        data={"phoneNo":phoneNo,"newPwd":"123456"}
        r=requests.post(host_api+"/api/cust/pwd/update",data=json.dumps(data),headers=head,verify=False)
        s=r.json()
        self.assertEqual(s['errorCode'],0)
    def test_auth_cert(self):
        '''【LanaDigital】/api/cust/auth/cert身份认证接口-正案例'''
        st=random_four_zm()
        test_data=login_code()
        registNo=test_data[0]
        head=test_data[1]
        data={"birthdate":"1999-5-18","civilStatus":"10050002","civilStatusName":"Soltero","curp":st+"990518MM"+st+"V8","delegationOrMunicipality":"zxcvbbbccxxx","education":"10190002","educationName":"Primaria","fatherLastName":"WANG","gender":"10030000",
              "genderName":"Mujer","motherLastName":"LIU","name":"SHUANG","outdoorNumber":"qweetyyu","phoneNo":registNo,"postalCode":"55555","state":"11130001","street":"444444","suburb":"asdfhhj"}
        r=requests.post(host_api+'/api/cust/auth/cert',data=json.dumps(data),headers=head)
        s=r.json()
        custNo=s['data']['custNo']
        self.assertEqual(s['errorCode'],0)
        self.assertIsNotNone(custNo)
        sql="select CERT_AUTH from cu_cust_auth_dtl  where CUST_NO='"+custNo+"';"  #cu_客户认证信息明细表
        cert_auth=DataBase(which_db).get_one(sql)
        self.assertEqual(cert_auth[0],1)
    def test_auth_kycStat(self):
        '''【LanaDigital】/api/cust/auth/kyc/stat KYC认证信息查询，判断是否kyc认证项都完成-正案例'''
        test_data=for_test_auth_other()
        phone=test_data[0]
        custNo=test_data[1]
        head=test_data[2]
        update_kyc_auth(phone,custNo)
        data={"custNo":custNo}
        r=requests.post(host_api+'/api/cust/auth/kyc/stat',data=json.dumps(data),headers=head)
        s=r.json()
        self.assertEqual(s['errorCode'],0)
    def test_auth_review(self):
        '''【LanaDigital】/api/cust/auth/review接口-正案例'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        # registNo=test_data[0]
        head=test_data[2]
        data={"certType":"WORK","custNo":custNo}
        r1=requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data),headers=head)
        s1=r1.json()
        self.assertEqual(s1['errorCode'],0)
    def test_auth_work(self):
        '''【LanaDigital】/api/cust/auth/work接口（客户工作情况）-正案例'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        head=test_data[2]
        data={"companyAddress":"","companyName":"","companyPhone":"","custNo":custNo,"income":"10870004","industry":"","jobType":"10130006"}#工作收入来源
        r=requests.post(host_api+'/api/cust/auth/work',data=json.dumps(data),headers=head)
        s=r.json()
        self.assertEqual(s['errorCode'],0)
        self.assertEqual(s['data']['authSuccess'],True)
        sql = "select WORK_AUTH from cu_cust_auth_dtl  where CUST_NO='" + custNo + "';"  # cu_客户认证信息明细表
        work_auth = DataBase(which_db).get_one(sql)
        self.assertEqual(work_auth[0], 1)
    def test_app_grab_data(self):
        '''【LanaDigital】/api/common/grab/app_grab_data接口-正案例-app第三个页面接口（抓取用户手机短信，通讯录，设备信息，已安装app等信息）'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        phoneNo=test_data[0]
        head=test_data[2]
        #设备信息
        data1={"appNo":"208","phoneNo":phoneNo,"dataType":"11090003","pageGet":"10000001","recordTime":"1621332187810","grabData":{"ipAddress":"2409:8162:a46:5405:1:0:107f:acec%20","ipResolveCit":"2409:8162:a46:5405:1:0:107f:acec%20",
        "ipResolveCom":"2409:8162:a46:5405:1:0:107f:acec%20","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"抓取设备数据","recordTime":"1621332187810","userId":custNo,"mobileBrand":"HUAWEI","mobileModel":"LIO-AL00","systemVersion":"10","otherInfo":"274b98eb5c8aed06"},"custNo":custNo}
        #联系人
        data2={"appNo":"208","phoneNo":phoneNo,"dataType":"11090002","pageGet":"10000001","recordTime":"1621332187811","grabData":{"data":
        [{"contactName":"test","contactNo":"888 845 5666","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc",
          "mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"联系人列表抓取","recordTime":"1621332187811","userId":custNo},{"contactName":"test2","contactNo":"888 335 5777",
        "deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"联系人列表抓取",
        "recordTime":"1621332187811","userId":custNo}]},"custNo":custNo}
        #短信内容
        data3={"appNo":"208","phoneNo":phoneNo,"dataType":"11090005","pageGet":"10000001","recordTime":"1621332187836","grabData":{"data":[{"body":"【中国农业银行】您尾号8579账户05月18日17:02完成支付宝交易人民币-5000.00，余额9999999999.19。","address":"95599","date":"2021-05-18 17:02:48.863","dateSent":"2021-05-18 17:02:46.000","sender":"95599","kind":"SmsMessageKind.Received"}]},"custNo":custNo}
        #设备信息
        data4={"appNo":"208","phoneNo":phoneNo,"dataType":"11090004","pageGet":"10000001","recordTime":"1621332187838","grabData":{"latitude":"30.550366","longitude":"104.062236","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"11000003","recordTime":"1621332187838","userId":custNo},"custNo":custNo}
        #已安装应用
        data5={"appNo":"208","phoneNo":phoneNo,"dataType":"11090001","pageGet":"10000001","recordTime":"1621332187731","grabData":{"data":[{"appName":"安全教育平台","appPackage":"com.jzzs.ParentsHelper","appVersionNo":"1.7.0","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","installTime":1599480832637,"lastUpdateTime":1618934047038,"mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"App列表抓取","recordTime":"1621332187731","userId":custNo}]},"custNo":custNo}
        data0=[data1,data2,data3,data4,data5]
        for data0 in data0:
            r0=requests.post(host_api+'/api/common/grab/app_grab_data',data=json.dumps(data0),headers=head)  #抓取用户手机短信，通讯录，已安装app等信息
            t0=r0.json()
            self.assertEqual(t0['errorCode'],0)
            time.sleep(1)
    def test_auth_contact(self):
        '''【LanaDigital】/api/cust/auth/other/contact接口(填写联系人联系方式)app第四个页面-正案例'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        head=test_data[2]
        # print('custNo---',custNo)
        sql = "UPDATE cu_cust_auth_dtl set cert_auth='1', kyc_auth = '1', work_auth = '1',OTHER_CONTACT_AUTH='1' WHERE CUST_NO='"+custNo+"';"
        DataBase(which_db).executeUpdateSql(sql)
        data={"custNo":custNo,"contacts":[{"custNo":custNo,"name":"test1","phone":"123333","relationship":"10110004","relationshipName":"Hermanos"},{"custNo":custNo,"name":"test2","phone":"543212601","relationship":"10110001","relationshipName":"Padres"}]}
        r=requests.post(host_api+'/api/cust/auth/other/contact',data=json.dumps(data),headers=head)#最后一步，填写2个联系人的联系方式
        t=r.json()
        self.assertEqual(t['errorCode'],0)
        sql = "select OTHER_CONTACT_AUTH from cu_cust_auth_dtl  where CUST_NO='" + custNo + "';"  # cu_客户认证信息明细表
        other_contact_auth = DataBase(which_db).get_one(sql)
        self.assertEqual(other_contact_auth[0], 1)
    def test_bank_auth(self):
        '''【LanaDigital】/api/cust/auth/bank绑定银行卡接口-正案例'''
        bank_acct_no=str(random.randint(1000,9999))
        test_data = for_test_auth_other()
        custNo = test_data[1]
        head = test_data[2]
        data={"bankCode":"10020008","BBVA BANCOMER":"","clabe":"012121212121212128","custNo":custNo}
        r=requests.post(host_api+'/api/cust/auth/bank',data=json.dumps(data),headers=head)
        self.assertEqual(r.status_code,200)
        t=r.json()
        self.assertEqual(t['errorCode'],0)                                    #改为4位随机数
        sql="update cu_cust_bank_card_dtl set BANK_ACCT_NO='"+bank_acct_no+"' where CUST_NO='"+custNo+"';"
        DataBase(which_db).executeUpdateSql(sql)  #防止被真实放款给该银行卡
    def test_risk_credit(self):
        '''【LanaDigital】/api/task/risk/credit风控授信接口-正案例'''
        test_data=for_test_auth_other()
        head=test_data[2]
        r=requests.post(host_api+'/api/task/risk/credit', headers=head)
        self.assertEqual(r.status_code,200)
    # def test_credit_payment(self):
    #     '''【LanaDigital】/api/credit/payment用户提现接口-正案例'''
    #     test_data=for_apply_loan()
    #     custNo=test_data[0]
    #     head=test_data[1]
    #     data10={"withdrawAmt":withdrawAmt}
    #     r=requests.post(host_api+'/api/credit/payment',data=json.dumps(data10),headers=head)
    #     self.assertEqual(r.status_code,200)
    #     t=r.json()
    #     self.assertIsNotNone(t['data']['withdrawAcctNo'])
    # def test_payment_detail(self):
    #     '''【LanaDigital】/api/credit/payment/detail提现详情接口-正案例'''
    #     registNo=
    @classmethod
    def tearDownClass(cls): #在所有用例都执行完之后运行的
        DataBase(which_db).closeDB()
        print('我是tearDownClass，我位于所有用例运行的结束')
