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
    def test_check_user_stat(self): #函数名要以test开头，否则不会被执行
        '''【LanaDigital】/api/cust/check/user/state检查用户状态接口(是否已设置密码)-正案例'''  #用例描述，在函数下，用三个单引号里面写用例描述
        registNo=str(random.randint(8000000000, 9999999999))  # 10位随机数作为手机号
        data1={"registNo": registNo}
        r=requests.post(host_api + "/api/cust/check/user/state", data=json.dumps(data1), headers=head_api, verify=False)
        t=r.json()
        #print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertFalse(t['data']['hasPwd'])
        phone='9224250993'  #已设置密码
        data2={"registNo": phone}
        r = requests.post(host_api + "/api/cust/check/user/state", data=json.dumps(data2), headers=head_api, verify=False)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertTrue(t['data']['hasPwd'])
    def test_login_code(self):
        '''【LanaDigital】/api/cust/login注册登录接口-正案例'''
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
        registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
        head=login_code(registNo)
        data={"phoneNo":registNo,"newPwd":"123456"}
        r=requests.post(host_api+"/api/cust/pwd/update",data=json.dumps(data),headers=head,verify=False)
        s=r.json()
        self.assertEqual(s['errorCode'],0)
    def test_auth_cert(self):
        '''【LanaDigital】/api/cust/auth/cert身份认证接口-正案例'''
        st=random_four_zm()
        registNo = str(random.randint(8000000000, 9999999999))  # 10位随机数作为手机号
        head = login_code(registNo)
        data={"birthdate":"1998-11-18","civilStatus":"10050002","civilStatusName":"Soltero","curp":st+"981118MM"+st+"V8","delegationOrMunicipality":"zxcvbbbccxxx","education":"10190002","educationName":"Primaria","fatherLastName":"WANG","gender":"10030000",
              "genderName":"Mujer","motherLastName":"LIU","name":"SHUANG","outdoorNumber":"qweetyyu","phoneNo":registNo,"postalCode":"55555","state":"11130001","street":"444444","suburb":"asdfhhj"}
        r=requests.post(host_api+'/api/cust/auth/cert',data=json.dumps(data),headers=head)
        s=r.json()
        custNo=s['data']['custNo']
        self.assertEqual(s['errorCode'],0)
        self.assertIsNotNone(custNo)
        sql="select CERT_AUTH from cu_cust_auth_dtl  where CUST_NO='"+custNo+"';"  #cu_客户认证信息明细表
        cert_auth=DataBase(which_db).get_one(sql)
        self.assertEqual(cert_auth[0],1)
    def test_auth_review(self):
        '''【LanaDigital】/api/cust/auth/review接口-正案例'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        head=test_data[2]
        data={"certType":"WORK","custNo":custNo}
        r1=requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data),headers=head)
        s1=r1.json()
        self.assertEqual(s1['errorCode'],0)
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
        data1={"custNo":custNo,"dataType":"11090003","grabData":{"deviceId":"28884415e8dc4bc3please open wifiSM-A5160","imei":"28884415e8dc4bc3",
        "ipAddress":"192.168.20.100","ipResolveCit":"","ipResolveCom":"","mac":"please open wifi","mobileBrand":"samsung","mobileModel":"SM-A5160",
        "otherInfo":"API:,30,deviceId:28884415e8dc4bc3,dield:unknown","phoneNo":phoneNo,"systemVersion":"11","userId":""},"loanNo":"",
           "pageGet":"Contact","phoneNo":phoneNo,"recordTime":"1634898295311"}
        #联系人
        data2={"custNo":custNo,"dataType":"11090002","grabData":{"data":[{"contactName":"5qV0PQ","contactNo":"8293338387","deviceId":"28884415e8dc4bc3please open wifiSM-A5160",
        "imei":"28884415e8dc4bc3","mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"联系人列表抓取","recordTime":1634898331133,"userId":""},
        {"contactName":"KlMwSp","contactNo":"8451760297","deviceId":"28884415e8dc4bc3please open wifiSM-A5160","imei":"28884415e8dc4bc3",
        "mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"联系人列表抓取","recordTime":1634898331283,"userId":""}]},"loanNo":"",
        "pageGet":"Contact","phoneNo":phoneNo,"recordTime":"1634898388674"}
        #短信内容
        data3={"custNo":custNo,"dataType":"11090005","grabData":{"data":[{"address":"+525590632527","body":"[AprestamoPlus] Felicitaciones https://bit.ly/3xBJoCT",
        "date":1634890751559,"kind":"11140002","receiver":"-1491790776","sender":"+525590632527"}]},"loanNo":"","pageGet":"Contact","phoneNo":phoneNo,
        "recordTime":"1634898295245"}
        #位置信息
        data4={"custNo":custNo,"dataType":"11090004","grabData":{"deviceId":"66af3c496c59bc733a:1e:f6:81:46:daV2031A","imei":"66af3c496c59bc73",
        "latitude":"104.062505","longitude":"30.550497","mac":"3a:1e:f6:81:46:da","phoneNo":phoneNo,"userId":""},"loanNo":"",
        "pageGet":"Contact","phoneNo":phoneNo,"recordTime":"1635147615526"}
        #已安装应用
        data5={"custNo":custNo,"dataType":"11090001","grabData":{"data":[{"appName":"GBA Service","appPackage":"com.mediatek.gba","appVersionNo":"29",
        "deviceId":"66af3c496c59bc733a:1e:f6:81:46:daV2031A","imei":"66af3c496c59bc73","installTime":"1230768000000","lastUpdateTime":"1230768000000",
        "mac":"3a:1e:f6:81:46:da","phoneNo":phoneNo,"recordBehavior":"Contact","recordTime":1635147615405,"userId":""}]},"loanNo":"",
        "pageGet":"Contact","phoneNo":phoneNo,"recordTime":"1635147616281"}
        data0=[data1,data2,data3,data4,data5]
        for data0 in data0:
            r0=requests.post(host_api+'/api/common/grab/app_grab_data',data=json.dumps(data0),headers=head)  #抓取用户手机短信，通讯录，已安装app等信息
            t0=r0.json()
            self.assertEqual(t0['errorCode'],0)
            time.sleep(1)
    def test_auth_contact(self):
        '''【LanaDigital】/api/cust/auth/other/contact接口(填写联系人联系方式)app第四个页面-正案例'''
        test_data=for_test_for_contact_other()
        custNo=test_data[0]
        head=test_data[1]
        # print('custNo---',custNo)
        # sql = "UPDATE cu_cust_auth_dtl set cert_auth='1', kyc_auth = '1', work_auth = '1' WHERE CUST_NO='"+custNo+"';"
        # DataBase(which_db).executeUpdateSql(sql)
        data={"custNo":custNo,"contacts":[{"custNo":custNo,"name":"Advance Talktime","phone":"52141","relationship":"10110004","relationshipName":"Hermanos"},{"custNo":custNo,"name":"Cricket","phone":"543212601","relationship":"10110001","relationshipName":"Padres"}]}
        r=requests.post(host_api+'/api/cust/auth/other/contact',data=json.dumps(data),headers=head)#最后一步，填写2个联系人的联系方式
        t=r.json()
        # print(t)
        self.assertEqual(t['errorCode'],0)
        # sql = "select OTHER_CONTACT_AUTH from cu_cust_auth_dtl  where CUST_NO='" + custNo + "';"  # cu_客户认证信息明细表
        # other_contact_auth = DataBase(which_db).get_one(sql)
        # self.assertEqual(other_contact_auth[0], 1)
    def test_bank_auth_01(self):
        '''【LanaDigital】/api/cust/auth/bank绑定银行卡接口-正案例'''
        bank_acct_no=str(random.randint(1000,9999))
        test_data = for_apply_loan()
        custNo = test_data[0]
        head = test_data[1]
        data={"bankCode":"10020008","bankCodeName":"BBVA BANCOMER","clabe":"012121212121212128","custNo":custNo}
        r=requests.post(host_api+'/api/cust/auth/bank',data=json.dumps(data),headers=head)
        self.assertEqual(r.status_code,200)
        t=r.json()
        self.assertEqual(t['errorCode'],0)                                    #改为4位随机数
        sql="update cu_cust_bank_card_dtl set BANK_ACCT_NO='"+bank_acct_no+"' where CUST_NO='"+custNo+"';"
        DataBase(which_db).executeUpdateSql(sql)  #防止被真实放款给该银行卡
    def test_bank_auth_02(self):
        '''【LanaDigital】/api/cust/auth/bank绑定银行卡接口(有在贷不能更换银行卡)-正案例'''
        list = cx_registNo_04()
        registNo = list[0]
        # print(registNo)
        custNo = list[1]
        headt_api = login_code(registNo)
        data = {"bankCode": "10020037", "clabe": "138455214411441118", "custNo": custNo}
        r = requests.post(host_api + '/api/cust/auth/bank', data=json.dumps(data), headers=headt_api)
        t = r.json()
        self.assertEqual(t['errorCode'], 30001)
        self.assertEqual(t['message'],'Su préstamo no ha sido liquidado y CLABE no se puede modificar temporalmente. Modifíquelo después de que se complete el pago.')
    def test_bank_auth_03(self):
        '''【lanaPlus】/api/cust/auth/bank绑定银行卡接口(客户未认证，不能绑卡)-正案例'''
        registNo = cx_registNo_07()
        headt_api = login_code(registNo)
        data = {"bankCode": "10020037", "clabe": "138455214411441118", "custNo": ''}
        r = requests.post(host_api + '/api/cust/auth/bank', data=json.dumps(data), headers=headt_api)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 30001)
        self.assertEqual(t['message'], 'custNoParámetro anormal ')
    def test_feedback_record(self):
        '''【LanaDigital】/api/hook/feedback提交feedback记录接口-正案例'''
        registNo='1166777777'
        headt_api_f=login_code_f(registNo)
        custNo='C2082111048144516475940700160'
        files={'custNo':(None,custNo),'phoneNo':(None,registNo),'feedbackDesc':(None,'test123456789'),'feedbackType':(None,'11110003'),'feedbackPage':(None,'CLABE'),
               'feedbackOption':(None,'No sé cuál es mi cuenta CLABE'),'imgs':('key.png',open(r'D:\pic\app.png', 'rb'),'text/plain')}
        r=requests.post(host_api+"/api/hook/feedback",files=files,headers=headt_api_f)
        t=r.json()
        # print(t)
        self.assertEqual(t['errorCode'],0)
    def test_risk_credit(self):
        '''【LanaDigital】/api/task/risk/credit风控授信接口-正案例'''
        test_data=for_test_auth_other()
        head=test_data[2]
        r=requests.post(host_api+'/api/task/risk/credit', headers=head)
        self.assertEqual(r.status_code,200)
    def test_bank_codes(self):
        '''【LanaDigital】/api/common/bank/codes获取银行卡码值及前缀接口-正案例'''
        registNo=cx_registNo_10()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/common/bank/codes",headers=headt_api)
        t=r.json()
        # print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t,{"data":{"bankList":[{"bankCode":"10020037","bankName":"ABC CAPITAL","preNums":"138"},{"bankCode":"10020020","bankName":"ACCENDO BANCO","preNums":"102"},{"bankCode":"10020034","bankName":"ACTINVER","preNums":"133"},{"bankCode":"10020018","bankName":"AFIRME","preNums":"062"},{"bankCode":"10020067","bankName":"AKALA","preNums":"638"},{"bankCode":"10020021","bankName":"AMERICAN EXPRES","preNums":"103"},{"bankCode":"10020030","bankName":"AUTOFIN","preNums":"128"},{"bankCode":"10020029","bankName":"AZTECA","preNums":"127"},{"bankCode":"10020011","bankName":"BAJIO","preNums":"030"},{"bankCode":"10020007","bankName":"BANAMEX","preNums":"002"},{"bankCode":"10020047","bankName":"BANCO FINTERRA","preNums":"154"},{"bankCode":"10020052","bankName":"BANCO S3","preNums":"160"},{"bankCode":"10020001","bankName":"BANCOMEXT","preNums":"006"},{"bankCode":"10020036","bankName":"BANCOPPEL","preNums":"137"},{"bankCode":"10020046","bankName":"BANCREA","preNums":"152"},{"bankCode":"10020003","bankName":"BANJERCITO","preNums":"019"},{"bankCode":"10020022","bankName":"BANK OF AMERICA","preNums":"106"},{"bankCode":"10020042","bankName":"BANKAOOL","preNums":"147"},{"bankCode":"10020002","bankName":"BANOBRAS","preNums":"009"},{"bankCode":"10020019","bankName":"BANORTE","preNums":"072"},{"bankCode":"10020015","bankName":"BANREGIO","preNums":"058"},{"bankCode":"10020005","bankName":"BANSEFI","preNums":"166"},{"bankCode":"10020017","bankName":"BANSI","preNums":"060"},{"bankCode":"10020031","bankName":"BARCLAYS","preNums":"129"},{"bankCode":"10020041","bankName":"BBASE","preNums":"145"},{"bankCode":"10020008","bankName":"BBVA BANCOMER","preNums":"012"},{"bankCode":"10020025","bankName":"BMONEX","preNums":"112"},{"bankCode":"10020075","bankName":"CAJA POP MEXICA","preNums":"677"},{"bankCode":"10020077","bankName":"CAJA TELEFONIST","preNums":"683"},{"bankCode":"10020063","bankName":"CB INTERCAM","preNums":"630"},{"bankCode":"10020064","bankName":"CI BOLSA","preNums":"631"},{"bankCode":"10020040","bankName":"CIBANCO","preNums":"143"},{"bankCode":"10020032","bankName":"COMPARTAMOS","preNums":"130"},{"bankCode":"10020038","bankName":"CONSUBANCO","preNums":"140"},{"bankCode":"10020071","bankName":"CREDICAPITAL","preNums":"652"},{"bankCode":"10020028","bankName":"CREDIT SUISSE","preNums":"126"},{"bankCode":"10020076","bankName":"CRISTOBAL COLON","preNums":"680"},{"bankCode":"10020083","bankName":"CoDi Valida","preNums":"903"},{"bankCode":"10020027","bankName":"DEUTSCHE","preNums":"124"},{"bankCode":"10020045","bankName":"DONDE","preNums":"151"},{"bankCode":"10020057","bankName":"ESTRUCTURADORES","preNums":"606"},{"bankCode":"10020070","bankName":"EVERCORE","preNums":"648"},{"bankCode":"10020060","bankName":"FINAMEX","preNums":"616"},{"bankCode":"10020065","bankName":"FINCOMUN","preNums":"634"},{"bankCode":"10020081","bankName":"FOMPED","preNums":"689"},{"bankCode":"10020079","bankName":"FONDO (FIRA)","preNums":"685"},{"bankCode":"10020054","bankName":"GBM","preNums":"601"},{"bankCode":"10020066","bankName":"HDI SEGUROS","preNums":"636"},{"bankCode":"10020006","bankName":"HIPOTECARIA FED","preNums":"168"},{"bankCode":"10020010","bankName":"HSBC","preNums":"021"},{"bankCode":"10020048","bankName":"ICBC","preNums":"155"},{"bankCode":"10020012","bankName":"INBURSA","preNums":"036"},{"bankCode":"10020082","bankName":"INDEVAL","preNums":"902"},{"bankCode":"10020044","bankName":"INMOBILIARIO","preNums":"150"},{"bankCode":"10020035","bankName":"INTERCAM BANCO","preNums":"136"},{"bankCode":"10020080","bankName":"INVERCAP","preNums":"686"},{"bankCode":"10020016","bankName":"INVEX","preNums":"059"},{"bankCode":"10020024","bankName":"JP MORGAN","preNums":"110"},{"bankCode":"10020074","bankName":"LIBERTAD","preNums":"670"},{"bankCode":"10020055","bankName":"MASARI","preNums":"602"},{"bankCode":"10020013","bankName":"MIFEL","preNums":"042"},{"bankCode":"10020051","bankName":"MIZUHO BANK","preNums":"158"},{"bankCode":"10020053","bankName":"MONEXCB","preNums":"600"},{"bankCode":"10020023","bankName":"MUFG","preNums":"108"},{"bankCode":"10020033","bankName":"MULTIVA BANCO","preNums":"132"},{"bankCode":"10020059","bankName":"MULTIVA CBOLSA","preNums":"613"},{"bankCode":"10020004","bankName":"NAFIN","preNums":"135"},{"bankCode":"10020043","bankName":"PAGATODO","preNums":"148"},{"bankCode":"10020062","bankName":"PROFUTURO","preNums":"620"},{"bankCode":"10020049","bankName":"SABADELL","preNums":"156"},{"bankCode":"10020009","bankName":"SANTANDER","preNums":"014"},{"bankCode":"10020084","bankName":"SANTANDER2","preNums":"814"},{"bankCode":"10020014","bankName":"SCOTIABANK","preNums":"044"},{"bankCode":"10020050","bankName":"SHINHAN","preNums":"157"},{"bankCode":"10020069","bankName":"STP","preNums":"646"},{"bankCode":"10020078","bankName":"TRANSFER","preNums":"684"},{"bankCode":"10020072","bankName":"UNAGRA","preNums":"656"},{"bankCode":"10020061","bankName":"VALMEX","preNums":"617"},{"bankCode":"10020056","bankName":"VALUE","preNums":"605"},{"bankCode":"10020026","bankName":"VE POR MAS","preNums":"113"},{"bankCode":"10020058","bankName":"VECTOR","preNums":"608"},{"bankCode":"10020039","bankName":"VOLKSWAGEN","preNums":"141"}],"hotBankList":[{"bankCode":"10020008","bankName":"BBVA BANCOMER","preNums":"012"},{"bankCode":"10020029","bankName":"AZTECA","preNums":"127"},{"bankCode":"10020007","bankName":"BANAMEX","preNums":"002"},{"bankCode":"10020009","bankName":"SANTANDER","preNums":"014"},{"bankCode":"10020019","bankName":"BANORTE","preNums":"072"},{"bankCode":"10020010","bankName":"HSBC","preNums":"021"},{"bankCode":"10020014","bankName":"SCOTIABANK","preNums":"044"},{"bankCode":"10020069","bankName":"STP","preNums":"646"}]},"errorCode":0,"message":"ok"})
    def test_feedback_codes(self):
        '''【LanaDigital】/api/common/feedback/codes获取feedback码值接口-正案例'''
        registNo = cx_registNo_10()
        headt_api = login_code(registNo)
        r = requests.get(host_api + "/api/common/feedback/codes", headers=headt_api)
        t = r.json()
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(str(t['data']),"[{'valName': 'Acosado', 'valCode': '11110001', 'options': ['Me acosaron por mensajes de WhatsApp.', 'Me acosaron por mensajes de texto.', 'Me acosaron por una llamada telefónica.']}, {'valName': 'Aprobación es demasiado largo', 'valCode': '11110002', 'options': ['El tiempo de aprobación es demasiado largo.']}, {'valName': 'CLABE', 'valCode': '11110003', 'options': ['No sé cuál es mi cuenta CLABE.', 'Quiero cambiar mi cuenta CLABE.']}, {'valName': 'CURP', 'valCode': '11110004', 'options': ['La CURP marca error.', 'Necesito ayuda para completar la CURP.']}, {'valName': 'Depósito', 'valCode': '11110005', 'options': ['Apareció un error de limitación en la parte superior de la página.', 'He pagado pero el estatus no se ha actualizado.', 'La cuenta que ha pagado marca error.', 'No recibí el depósito.', 'Pagos múltiples.']}, {'valName': 'El tiempo de carga es demasiado largo', 'valCode': '11110007', 'options': ['Carga lenta en la página de inicio.', 'Carga prolongada de la página de pago']}, {'valName': 'Error de red', 'valCode': '11110006', 'options': ['Apareció un error de [01] en la parte superior de la página.', 'Apareció un error de [02] en la parte superior de la página.', 'Apareció un error de [03] en la parte superior de la página.', 'Apareció un error de [04] en la parte superior de la página.']}, {'valName': 'Foto', 'valCode': '11110008', 'options': ['Informar un error después de cargar la foto.', 'La cámara funciona mal y deseo cargar fotos.', 'No se pudo cargar la foto.']}, {'valName': 'INE', 'valCode': '11110009', 'options': ['Informe del error después de cargar el INE.', 'No se pudo cargar el INE.', 'Reemplace la credencial INE.', 'Sin credencial de INE / perdida', 'Sin credencial física INE, quiero subir fotos.']}, {'valName': 'Monto del préstamo', 'valCode': '11110011', 'options': ['Quiero elegir el monto del préstamo que más me convenga por mí mismo.', 'Quiero un monto de préstamo mayor.', 'Quiero una cantidad de préstamo menor.']}, {'valName': 'Otros', 'valCode': '11110012', 'options': ['Otros.']}, {'valName': 'Sorteo', 'valCode': '11110013', 'options': ['Gané el sorteo, pero no obtuve el premio.']}, {'valName': 'Teléfono', 'valCode': '11110014', 'options': ['Cambiar el número de teléfono móvil.', 'Error al registrar el número de teléfono móvil.', 'Número de teléfono incompatible.']}]")
    def test_get_state_codes(self):
        '''【LanaDigital】/api/common/code/STATE获取州列表接口-正案例'''
        registNo = cx_registNo_07()
        headt_api = login_code(registNo)
        r = requests.get(host_api + '/api/common/code/STATE', headers=headt_api)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(str(t['data']),
            "[{'codeName': 'Aguascalientes', 'codeValue': '11130001', 'note': None}, {'codeName': 'Baja California', 'codeValue': '11130002', 'note': None}, {'codeName': 'Baja California Sur', 'codeValue': '11130003', 'note': None}, {'codeName': 'Campeche', 'codeValue': '11130004', 'note': None}, {'codeName': 'Chiapas', 'codeValue': '11130005', 'note': None}, {'codeName': 'Chihuahua', 'codeValue': '11130007', 'note': None}, {'codeName': 'Ciudad de México', 'codeValue': '11130006', 'note': None}, {'codeName': 'Coahuila', 'codeValue': '11130008', 'note': None}, {'codeName': 'Colima', 'codeValue': '11130009', 'note': None}, {'codeName': 'Durango', 'codeValue': '11130010', 'note': None}, {'codeName': 'Guanajuato', 'codeValue': '11130011', 'note': None}, {'codeName': 'Guerrero', 'codeValue': '11130012', 'note': None}, {'codeName': 'Hidalgo', 'codeValue': '11130013', 'note': None}, {'codeName': 'Jalisco', 'codeValue': '11130014', 'note': None}, {'codeName': 'Michoacán', 'codeValue': '11130016', 'note': None}, {'codeName': 'Morelos', 'codeValue': '11130017', 'note': None}, {'codeName': 'México', 'codeValue': '11130015', 'note': None}, {'codeName': 'Nayarit', 'codeValue': '11130018', 'note': None}, {'codeName': 'Nuevo León', 'codeValue': '11130019', 'note': None}, {'codeName': 'Oaxaca', 'codeValue': '11130020', 'note': None}, {'codeName': 'Puebla', 'codeValue': '11130021', 'note': None}, {'codeName': 'Querétaro', 'codeValue': '11130022', 'note': None}, {'codeName': 'Quintana Roo', 'codeValue': '11130023', 'note': None}, {'codeName': 'San Luis Potosí', 'codeValue': '11130024', 'note': None}, {'codeName': 'Sinaloa', 'codeValue': '11130025', 'note': None}, {'codeName': 'Sonora', 'codeValue': '11130026', 'note': None}, {'codeName': 'Tabasco', 'codeValue': '11130027', 'note': None}, {'codeName': 'Tamaulipas', 'codeValue': '11130028', 'note': None}, {'codeName': 'Tlaxcala', 'codeValue': '11130029', 'note': None}, {'codeName': 'Veracruz', 'codeValue': '11130030', 'note': None}, {'codeName': 'Yucatán', 'codeValue': '11130031', 'note': None}, {'codeName': 'Zacatecas', 'codeValue': '11130032', 'note': None}]")
    def test_get_marriage_codes(self):
        '''【LanaDigital】/api/common/code/MARRIAGE获取婚姻码值接口-正案例'''
        registNo = cx_registNo_07()
        headt_api = login_code(registNo)
        r = requests.get(host_api + '/api/common/code/MARRIAGE', headers=headt_api)
        t = r.json()
        #print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(str(t['data']),"[{'codeName': 'Casado', 'codeValue': '10050001', 'note': None}, {'codeName': 'Divorced', 'codeValue': '10050004', 'note': None}, {'codeName': 'Soltero', 'codeValue': '10050002', 'note': None}, {'codeName': 'Unión libre', 'codeValue': '10050005', 'note': None}, {'codeName': 'Viudo', 'codeValue': '10050003', 'note': None}]")
    def test_get_contactType_codes(self):
        '''【LanaDigital】/api/common/code/CONTACT_TYPE获取联系人类型码值接口-正案例'''
        registNo = cx_registNo_07()
        headt_api = login_code(registNo)
        r = requests.get(host_api + '/api/common/code/CONTACT_TYPE', headers=headt_api)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(str(t['data']),"[{'codeName': 'Hermanos', 'codeValue': '10110004', 'note': None}, {'codeName': 'Hijos', 'codeValue': '10110003', 'note': None}, {'codeName': 'Padres', 'codeValue': '10110001', 'note': None}, {'codeName': 'Pareja', 'codeValue': '10110002', 'note': None}, {'codeName': 'uno mismo', 'codeValue': '10110005', 'note': None}]")
    def test_get_education_codes(self):
        '''【LanaDigital】/api/common/code/EDUCATION获取教育类型码值接口-正案例'''
        registNo = cx_registNo_07()
        headt_api = login_code(registNo)
        r = requests.get(host_api + '/api/common/code/EDUCATION', headers=headt_api)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(str(t['data']),"[{'codeName': 'Licenciatura', 'codeValue': '10190005', 'note': None}, {'codeName': 'No Escolaridad', 'codeValue': '10190001', 'note': None}, {'codeName': 'Posgrado / Maestria', 'codeValue': '10190006', 'note': None}, {'codeName': 'Preparatoria/ Bachillerato', 'codeValue': '10190004', 'note': None}, {'codeName': 'Primaria', 'codeValue': '10190002', 'note': None}, {'codeName': 'Secundaria', 'codeValue': '10190003', 'note': None}]")
    def test_get_jobType_codes(self):
        '''【LanaDigital】/api/common/code/JOB_TYPE获取工作类型码值接口-正案例'''
        registNo = cx_registNo_07()
        headt_api = login_code(registNo)
        r = requests.get(host_api + '/api/common/code/JOB_TYPE', headers=headt_api)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(str(t['data']),"[{'codeName': 'Desempleado', 'codeValue': '10130006', 'note': None}, {'codeName': 'Empleado', 'codeValue': '10130001', 'note': None}, {'codeName': 'Empresario', 'codeValue': '10130002', 'note': None}, {'codeName': 'Estudiante', 'codeValue': '10130004', 'note': None}, {'codeName': 'Independiente', 'codeValue': '10130003', 'note': None}, {'codeName': 'Jubilado', 'codeValue': '10130005', 'note': None}]")
    def test_get_income_codes(self):
        '''【LanaDigital】/api/common/code/INCOME获取收入码值接口-正案例'''
        registNo = cx_registNo_07()
        headt_api = login_code(registNo)
        r = requests.get(host_api + '/api/common/code/INCOME', headers=headt_api)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(str(t['data']),"[{'codeName': '$12000 - $24000', 'codeValue': '10870004', 'note': None}, {'codeName': '$3000 - $6000', 'codeValue': '10870002', 'note': None}, {'codeName': '$6000 - $12000', 'codeValue': '10870003', 'note': None}, {'codeName': 'Menos de $3000', 'codeValue': '10870001', 'note': None}, {'codeName': 'Más de $24000', 'codeValue': '10870005', 'note': None}]")
    def test_get_industry_codes(self):
        '''【LanaDigital】/api/common/code/INDUSTRY获取行业码值接口-正案例'''
        registNo = cx_registNo_07()
        headt_api = login_code(registNo)
        r = requests.get(host_api + '/api/common/code/INDUSTRY', headers=headt_api)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(str(t['data']),"[{'codeName': 'Administrativo', 'codeValue': '10860001', 'note': None}, {'codeName': 'Ayudante en General', 'codeValue': '10860004', 'note': None}, {'codeName': 'Call center', 'codeValue': '10860005', 'note': None}, {'codeName': 'Comerciante', 'codeValue': '10860015', 'note': None}, {'codeName': 'Construcción', 'codeValue': '10860008', 'note': None}, {'codeName': 'Dependencias del Gobierno', 'codeValue': '10860007', 'note': None}, {'codeName': 'Director - Gerente - Encargado', 'codeValue': '10860006', 'note': None}, {'codeName': 'Finanzas - Contador - Agobado', 'codeValue': '10860009', 'note': None}, {'codeName': 'Ingeniero - Arquitecto', 'codeValue': '10860002', 'note': None}, {'codeName': 'Negocio propio', 'codeValue': '10860014', 'note': None}, {'codeName': 'Operario de Transporte', 'codeValue': '10860003', 'note': None}, {'codeName': 'Otros', 'codeValue': '10860016', 'note': None}, {'codeName': 'Recepcionista', 'codeValue': '10860010', 'note': None}, {'codeName': 'Repartidor de plataforma', 'codeValue': '10860012', 'note': None}, {'codeName': 'Servidor Público', 'codeValue': '10860011', 'note': None}, {'codeName': 'Transporte privado', 'codeValue': '10860013', 'note': None}]")
    def test_get_fileType_codes(self):
        '''【LanaDigital】/api/common/code/FILE_TYPE获取文件类型码值接口-正案例'''
        registNo = cx_registNo_07()
        headt_api = login_code(registNo)
        r = requests.get(host_api + '/api/common/code/FILE_TYPE', headers=headt_api)
        t = r.json()
        # print(t)
        self.assertEqual(t['errorCode'], 0)
        self.assertEqual(str(t['data']),"[{'codeName': 'Anverso de la tarjeta Aadhaar', 'codeValue': '10070015', 'note': None}, {'codeName': 'Anverso de la tarjeta de identificación', 'codeValue': '10070001', 'note': None}, {'codeName': 'Datos brutos de API konjac', 'codeValue': '10070008', 'note': None}, {'codeName': 'Datos de informes de API konjac', 'codeValue': '10070009', 'note': None}, {'codeName': 'Foto de mosaico A_card', 'codeValue': '10070014', 'note': None}, {'codeName': 'Foto personal', 'codeValue': '10070004', 'note': None}, {'codeName': 'Foto viva', 'codeValue': '10070032', 'note': None}, {'codeName': 'Frente de PAN', 'codeValue': '10070017', 'note': None}, {'codeName': 'Historial de llamadas telefónicas API', 'codeValue': '10070010', 'note': None}, {'codeName': 'Información de contactos telefónicos', 'codeValue': '10070023', 'note': None}, {'codeName': 'Información de la aplicación móvil', 'codeValue': '10070012', 'note': None}, {'codeName': 'Información del dispositivo telefónico', 'codeValue': '10070021', 'note': None}, {'codeName': 'Información del teléfono', 'codeValue': '10070007', 'note': None}, {'codeName': 'Informe de crédito CRIF', 'codeValue': '10070030', 'note': None}, {'codeName': 'Informe de crédito de NBFC', 'codeValue': '10070027', 'note': None}, {'codeName': 'Libreta de direcciones local', 'codeValue': '10070006', 'note': None}, {'codeName': 'Lista de llamadas locales', 'codeValue': '10070005', 'note': None}, {'codeName': 'Lista de llamadas telefónicas API', 'codeValue': '10070011', 'note': None}, {'codeName': 'Prueba de empleo', 'codeValue': '10070018', 'note': None}, {'codeName': 'Prueba de ingresos', 'codeValue': '10070019', 'note': None}, {'codeName': 'Resultado de búsqueda de caras', 'codeValue': '10070013', 'note': None}, {'codeName': 'Resultado de comprobación simple de A_card', 'codeValue': '10070025', 'note': None}, {'codeName': 'Resultado de la verificación de la tarjeta A', 'codeValue': '10070026', 'note': None}, {'codeName': 'Resultado de la verificación de la tarjeta PAN', 'codeValue': '10070024', 'note': None}, {'codeName': 'Resultado de la verificación de la tarjeta bancaria', 'codeValue': '10070028', 'note': None}, {'codeName': 'Reverso de la tarjeta Aadhaar', 'codeValue': '10070016', 'note': None}, {'codeName': 'Reverso de la tarjeta de identificación', 'codeValue': '10070002', 'note': None}, {'codeName': 'SMS', 'codeValue': '10070031', 'note': None}, {'codeName': 'Solicitud de préstamos', 'codeValue': '10070029', 'note': None}, {'codeName': 'Un frente de tarjeta de pasaporte tripartito', 'codeValue': '10070020', 'note': None}, {'codeName': 'nformación de ubicación GPS', 'codeValue': '10070022', 'note': None}, {'codeName': 'prueba de reembolso', 'codeValue': '10070035', 'note': None}, {'codeName': 'tarjeta bancaria', 'codeValue': '10070003', 'note': None}]")
    @classmethod
    def tearDownClass(cls): #在所有用例都执行完之后运行的
        DataBase(which_db).closeDB()
        print('我是tearDownClass，我位于所有用例运行的结束')

