import json,requests
from Public.var_mex_credit import *
from Public.dataBase_ld import *
from Public.heads_ld import *
from Public.check_api import *
import random,string,datetime
#短信验证码，默认手机号后4位单个+5后取个位数，在逆序排列。
def compute_code(m):
    m = m[-4:]
    x1 = str(int(m[0])+5)
    x2 = str(int(m[1])+5)
    x3 = str(int(m[2])+5)
    x4 = str(int(m[3])+5)
    x = x4[-1:]+x3[-1:]+x2[-1:]+x1[-1:]
    return x
def huoqu_user_state(registNo):
    '''/api/cust/check/user/state获取用户状态'''
    data1 = {"registNo": registNo}
    q = requests.post(host_api + "/api/cust/check/user/state", data=json.dumps(data1), headers=head_api, verify=False)
    return q.json()
def cx_old_phoneNo():
    sql = '''#查询客户号不为空的用户手机号
    select PHONE_NO from cu_cust_reg_dtl where CUST_NO is not null and GAID='Exception:null' ORDER BY INST_TIME desc;'''
    phoneNo = DataBase(which_db).get_one(sql)
    #print('phoneNo----',phoneNo)
    phoneNo = str(phoneNo[0])
    return phoneNo
def cx_registNo_04():
    sql = '''#查询手机号c.phone_no,c.cust_no,a.loan_no有在贷未结清
        select c.phone_no,c.cust_no,a.loan_no from lo_loan_dtl a left join cu_cust_fee_bill_dtl b
        on a.loan_no = b.loan_no left join cu_cust_reg_dtl c on a.cust_no = c.cust_no
        where a.before_stat='10260005' and a.after_stat='10270002' or a.after_stat='10270003'
        order by a.inst_time desc limit 1;
    '''
    data = DataBase(which_db).get_one(sql)
    # print(tt)
    lists = list(data)
    return lists
def cx_registNo_07():
    sql = '''#查询无客户号的手机号
    select a.phone_no from cu_cust_reg_dtl a where a.CUST_NO is null order by a.INST_TIME desc limit 1;'''
    phone = DataBase(which_db).get_one(sql)
    phone = str(phone[0])
    return phone
def cx_registNo_10():
    sql = '''#查询有客户号的手机号
    select a.phone_no from cu_cust_reg_dtl a where a.CUST_NO is not null order by a.INST_TIME desc limit 1;'''
    phone = DataBase(which_db).get_one(sql)
    phone = str(phone[0])
    return phone
def lay_registNo():
    sql = '''#查询进入延迟放款的用户
        select phone_No from cu_cust_reg_dtl c left join lo_loan_payout_dtl l on c.CUST_NO=l.CUST_NO 
        where l.ORDER_STATUS='10420005' order by c.INST_TIME desc limit 1;'''
    phone = DataBase(which_db).get_one(sql)
    phone = str(phone[0])
    #print(phone)
    return phone
def payout_stp_data():
    sql = '''#查询能够放款成功的用户
        select p.TRAN_NO,p.TRAN_ORDER_NO,c.PHONE_NO,c.CUST_NO from cu_cust_reg_dtl c left join cu_cust_bank_card_dtl b on c.CUST_NO=b.CUST_NO
        left join pay_tran_dtl p on p.IN_ACCT_NO=b.BANK_ACCT_NO
        where p.TRAN_STAT='10220002' ORDER BY p.INST_TIME desc limit 1;'''
    data = DataBase(which_db).get_one(sql)
    lists = list(data)
    return lists
def payout_stp_data_1():
    sql = '''#查询能够放款的用户(包含额外费用)
        select c.PHONE_NO from cu_cust_reg_dtl c left join cu_cust_status_info s on c.CUST_NO=s.CUST_NO
        left join cu_cust_account_dtl a on a.CUST_NO=s.CUST_NO
        where s.`STATUS`='20040003'and a.REMAINING_AMT>'600' ORDER BY s.INST_TIME desc limit 1;'''
    data = DataBase(which_db).get_one(sql)
    phone = str(data[0])
    return phone
def payout_stp_data_2():
    sql = '''#查询能够放款的用户(不包含额外费用)
        select c.PHONE_NO,a.REMAINING_AMT,l.CUST_NO from lo_loan_dtl l 
        left join cu_cust_reg_dtl c on c.cust_no=l.cust_no
        left join cu_cust_status_info s on c.cust_no=s.cust_no
        left join cu_cust_account_dtl a on c.cust_no= a.cust_no
        where s.STATUS='20040004' and a.REMAINING_AMT>'600' and l.CUST_NO not in (
        select CUST_NO from lo_loan_dtl where BEFORE_STAT='10260008')
        order by l.INST_TIME desc limit 1;'''
    data = DataBase(which_db).get_one(sql)
    lists = list(data)
    return lists
def payout_stp_data_3():
    sql = '''#查询能够放款的用户(没有正在处理的贷款，允许再次提现)
        select c.PHONE_NO,a.REMAINING_AMT,l.CUST_NO from lo_loan_dtl l 
        left join cu_cust_reg_dtl c on c.cust_no=l.cust_no
        left join cu_cust_status_info s on c.cust_no=s.cust_no
        left join cu_cust_account_dtl a on c.cust_no= a.cust_no
        where s.STATUS='20040004' and a.REMAINING_AMT>'600' and l.CUST_NO not in (
        select CUST_NO from lo_loan_dtl where BEFORE_STAT='10260008')
        order by l.INST_TIME desc limit 1;'''
    data = DataBase(which_db).get_one(sql)
    #print(data)
    lists = list(data)
    return lists
def payout_stp_data_4():
    sql = '''#查询能够放款的用户(有正在处理的贷款，不允许再次提现)
        select c.PHONE_NO,a.REMAINING_AMT from cu_cust_reg_dtl c
        left join cu_cust_status_info s on c.cust_no=s.cust_no
        left join cu_cust_account_dtl a on c.cust_no= a.cust_no
        left join lo_loan_dtl l on c.cust_no=l.cust_no
        where s.STATUS='20040004' and a.REMAINING_AMT>'600' and l.before_stat='10260008'
        order by c.INST_TIME desc limit 1;'''
    data = DataBase(which_db).get_one(sql)
    #print(data)
    lists = list(data)
    return lists
def repay_data():
    sql1 = '''#查询能够还款的用户
        select a.CUST_NO,c.PHONE_NO,l.LOAN_NO,p.ORDER_NO,a.ACCOUNT_NO from cu_cust_reg_dtl c left join cu_cust_account_dtl a on c.CUST_NO=a.CUST_NO 
        left join fin_ad_dtl f on f.ACCOUNT_NO = a.ACCOUNT_NO
        left join lo_loan_dtl l on l.CUST_NO=a.CUST_NO
        left join lo_loan_payout_dtl p on l.LOAN_NO=p.LOAN_NO
        GROUP BY f.RECEIVE_AMT HAVING sum(f.RECEIVE_AMT>0) 
        ORDER BY a.INST_TIME desc limit 1;'''
    data = DataBase(which_db).get_one(sql1)
    #print(data)
    lists = list(data)
    # 查询还款用户的应还金额
    sql2 = "select sum(RECEIVE_AMT) from fin_ad_dtl where ORDER_NO='" + lists[3] + "';"
    data1 = DataBase(which_db).get_one(sql2)
    #print(data1)
    amt = str(data1[0])
    # 查询还款用户的CLABE_NO
    sql3 = "select CLABE_NO from fin_clabe_usable_dtl where ACCOUNT_NO='" + lists[4] + "';"
    data2 = DataBase(which_db).get_one(sql3)
    # print(data1)
    clabe_no = str(data2[0])
    lists.append(amt)
    lists.append(clabe_no)
    return lists
#更新密码，包含了用验证码方式注册登录的步骤
def update_pwd(phoneNo):
    token = login_code(phoneNo)
    headt = head_token(token)
    data = {"phoneNo": phoneNo, "newPwd": "123456"}
    r = requests.post(host_api + "/api/cust/pwd/update", data=json.dumps(data), headers=headt, verify=False)
    check_api(r)
def random_four_zm():
    st = ''
    for j in range(4):  #生成4个随机英文大写字母
        st += random.choice(string.ascii_uppercase)
    return st
#通过密码登录，返回token
def login_pwd(phoneNo):
    s = huoqu_user_state(phoneNo)
    data = {"phoneNo": phoneNo, "password": "123456", "hasPwd": s['data']['hasPwd'], "gaid": "Exception:null"}
    r = requests.post(host_api + "/api/cust/pwd/login", data=json.dumps(data), headers=head_api, verify=False)
    t = r.json()
    token = t['data']['token']
    return token
def headtt(registNo):
    token = login_pwd(registNo)
    headt = head_token(token)
    return headt
def for_test_auth_other():
    st = random_four_zm()
    registNo = str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
    code = compute_code(registNo)
    s = huoqu_user_state(registNo)
    data = {"code": code, "hasPwd": s['data']['hasPwd'], "phoneNo": registNo}
    r = requests.post(host_api + "/api/cust/login", data=json.dumps(data), headers=head_api, verify=False)
    t = r.json()
    token = t['data']['token']
    head = head_token(token)
    data0 = {"birthdate":"1999-5-18","civilStatus":"10050001","curp":st+"990518MM"+st+"V8","delegationOrMunicipality":"zxcvbbbccxxx","education":"10190005","fatherLastName":"LIU","gender":"10030001",
          "motherLastName":"LLL","name":"TEST","outdoorNumber":"qweetyyu","phoneNo":registNo,"postalCode":"55555","state":"11130001","street":"444444","suburb":"asdfhhj","email":""}
    r = requests.post(host_api+'/api/cust/auth/cert',data=json.dumps(data0),headers=head)
    t = r.json()
    custNo = t['data']['custNo']
    headp = head_token_payment(token)
    list = []
    list.append(registNo)
    list.append(custNo)
    list.append(head)
    list.append(headp)
    return list
def for_test_for_contact_other():
    test_data = for_test_auth_other()
    custNo = test_data[1]
    registNo = test_data[0]
    head = test_data[2]
    data1 = {"certType": "WORK", "custNo": custNo}
    r1 = requests.post(host_api + '/api/cust/auth/review', data=json.dumps(data1), headers=head)
    data2 = {"companyAddress": "", "companyName": "", "companyPhone": "", "custNo": custNo, "income": "10870004",
             "industry": "", "jobType": "10130006"}  # 工作收入来源
    r2 = requests.post(host_api + '/api/cust/auth/work', data=json.dumps(data2), headers=head)
    data3 = {"certType": "CONTACT", "custNo": custNo}
    r3 = requests.post(host_api + '/api/cust/auth/review', data=json.dumps(data3), headers=head)
    update_kyc_auth(registNo, custNo)
    # work
    auth_work(registNo, head)
    # 抓取数据
    auth_app_grab_data(registNo, custNo, head)
    update_batch_log()
    list = []
    list.append(custNo)
    list.append(head)
    return list
def login_code(registNo):
    code = compute_code(registNo)
    s = huoqu_user_state(registNo)
    data = {"code": code, "hasPwd": s['data']['hasPwd'], "phoneNo": registNo}
    r = requests.post(host_api + "/api/cust/login", data=json.dumps(data), headers=head_api, verify=False)
    t = r.json()
    token = t['data']['token']
    head = head_token(token)
    return head
def login_code_f(registNo):
    code = compute_code(registNo)
    s = huoqu_user_state(registNo)
    data = {"code": code, "hasPwd": s['data']['hasPwd'], "phoneNo": registNo}
    r = requests.post(host_api + "/api/cust/login", data=json.dumps(data), headers=head_api, verify=False)
    t = r.json()
    token = t['data']['token']
    head = head_token_f(token)
    return head
def for_apply_loan():
    test_data = for_test_auth_other()
    custNo = test_data[1]
    registNo = test_data[0]
    head = test_data[2]
    data1 = {"certType":"WORK","custNo":custNo}
    r1 = requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data1),headers=head)
    data2 = {"companyAddress":"","companyName":"","companyPhone":"","custNo":custNo,"income":"10870004","industry":"","jobType":"10130006"}#工作收入来源
    r2 = requests.post(host_api+'/api/cust/auth/work',data=json.dumps(data2),headers=head)
    data3 = {"certType":"CONTACT","custNo":custNo}
    r3 = requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data3),headers=head)
    # kyc
    update_kyc_auth(registNo, custNo)
    # work
    auth_work(registNo, head)
    # 抓取数据
    auth_app_grab_data(registNo, custNo, head)
    update_batch_log()
    list = []
    list.append(custNo)
    list.append(head)
    return list

def for_test_payment():
    #到待提现，检查账单详情
    #cust,registNo,head,headp
    test_data = for_test_auth_other()
    registNo = test_data[0]
    custNo = test_data[1]
    head = test_data[2]
    headp = test_data[3]
    #kyc
    update_kyc_auth(registNo,custNo)
    #work
    auth_work(registNo,head)
    #抓取数据
    auth_app_grab_data(registNo,custNo,head)
    #联系人
    t4 = auth_contact(custNo,head)
    #风控
    risk_credit(head)
    #查询用户的状态
    sql1 = "select status from cu_cust_status_info WHERE CUST_NO='"+custNo+"';"
    result1 = DataBase(which_db).get_one(sql1)
    if result1 is ('20040004'or "20040003"):
        print("数据正确，不用改数！")
    else:
        print("要改数！")
#抓取数据
def auth_app_grab_data(phoneNo,custNo,headt):
    #设备信息
    data4 = {"custNo":custNo,"dataType":"11090003","grabData":{"deviceId":"28884415e8dc4bc3please open wifiSM-A5160","imei":"28884415e8dc4bc3",
    "ipAddress":"192.168.20.100","ipResolveCit":"","ipResolveCom":"","mac":"please open wifi","mobileBrand":"samsung","mobileModel":"SM-A5160",
    "otherInfo":"API:,30,deviceId:28884415e8dc4bc3,dield:unknown","phoneNo":phoneNo,"systemVersion":"11","userId":""},"loanNo":"",
           "pageGet":"Contact","phoneNo":phoneNo,"recordTime":"1634898295311"}
    #联系人
    data5 = {"custNo":custNo,"dataType":"11090002","grabData":{"data":[{"contactName":"5qV0PQ","contactNo":"8293338387","deviceId":"28884415e8dc4bc3please open wifiSM-A5160",
    "imei":"28884415e8dc4bc3","mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"联系人列表抓取","recordTime":1634898331133,"userId":""},
    {"contactName":"KlMwSp","contactNo":"8451760297","deviceId":"28884415e8dc4bc3please open wifiSM-A5160","imei":"28884415e8dc4bc3",
    "mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"联系人列表抓取","recordTime":1634898331283,"userId":""}]},"loanNo":"",
    "pageGet":"Contact","phoneNo":phoneNo,"recordTime":"1634898388674"}
    #短信内容
    data6 = {"custNo":custNo,"dataType":"11090005","grabData":{"data":[{"address":"+525590632527","body":"[AprestamoPlus] Felicitaciones https://bit.ly/3xBJoCT",
    "date":1634890751559,"kind":"11140002","receiver":"-1491790776","sender":"+525590632527"}]},"loanNo":"","pageGet":"Contact","phoneNo":phoneNo,
    "recordTime":"1634898295245"}
    #位置信息
    data7 = {"custNo":custNo,"dataType":"11090004","grabData":{"deviceId":"66af3c496c59bc733a:1e:f6:81:46:daV2031A","imei":"66af3c496c59bc73",
    "latitude":"104.062505","longitude":"30.550497","mac":"3a:1e:f6:81:46:da","phoneNo":phoneNo,"userId":""},"loanNo":"",
    "pageGet":"Contact","phoneNo":phoneNo,"recordTime":"1635147615526"}
    #已安装应用
    data8 = {"custNo":custNo,"dataType":"11090001","grabData":{"data":[{"appName":"GBA Service","appPackage":"com.mediatek.gba","appVersionNo":"29",
    "deviceId":"66af3c496c59bc733a:1e:f6:81:46:daV2031A","imei":"66af3c496c59bc73","installTime":"1230768000000","lastUpdateTime":"1230768000000",
    "mac":"3a:1e:f6:81:46:da","phoneNo":phoneNo,"recordBehavior":"Contact","recordTime":1635147615405,"userId":""}]},"loanNo":"",
    "pageGet":"Contact","phoneNo":phoneNo,"recordTime":"1635147616281"}
    data0 = [data4,data5,data6,data7,data8]
    for data0 in data0:
        r0 = requests.post(host_api+'/api/common/grab/app_grab_data',data=json.dumps(data0),headers=headt)  #抓取用户手机设备信息，短信，通讯录，已安装app，位置信息
        time.sleep(1)
def auth_work(custNo,headt):
    data1 = {"certType":"WORK","custNo":custNo}
    r1 = requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data1),headers=headt)
    data2 = {"companyAddress":"","companyName":"","companyPhone":"","custNo":custNo,"income":"10870004","industry":"","jobType":"10130006"}#工作收入来源
    r2 = requests.post(host_api+'/api/cust/auth/work',data=json.dumps(data2),headers=headt)

#更新kyc认证状态及其值
def update_kyc_auth(registNo,custNo):
    t = str(time.time() * 1000000)[:15]
    tnum1 = str(random.randrange(10000, 99999))
    tnum2 = str(random.randrange(10000, 99999))
    tnum3 = str(random.randrange(10000, 99999))
    inst_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sql = "update cu_cust_auth_dtl set KYC_AUTH='1' WHERE CUST_NO='" + custNo + "';"  # 客户认证信息明细表kyc认证状态
    DataBase(which_db).executeUpdateSql(sql)
    appNo = '208'
    sql2 = "INSERT INTO `mex_credit`.`cu_cust_file_dtl`(`ID`, `PHONE_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('" + t + 'b88f206222e0' + tnum1 + "', '" + registNo + "', '" + custNo + "','" + appNo + "', '10070001', '100700011634108027823.jpg', '100700011634108027823.jpg', NULL, '.jpg', '307350', '" + appNo + "/20211013/8712976528/', NULL, NULL, '" + inst_time + "', 'sys', NULL, NULL);"
    sql3 = "INSERT INTO `mex_credit`.`cu_cust_file_dtl`(`ID`, `PHONE_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('" + t + 'b88f206222e0' + tnum2 + "', '" + registNo + "', '" + custNo + "','" + appNo + "', '10070002', '100700021634108040427.jpg', '100700021634108040427.jpg', NULL, '.jpg', '317778',  '" + appNo + "/20211013/8712976528/', NULL, NULL, '" + inst_time + "', 'sys', NULL, NULL);"
    sql4 = "INSERT INTO `mex_credit`.`cu_cust_file_dtl`(`ID`, `PHONE_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('" + t + 'b88f206222e0' + tnum3 + "', '" + registNo + "', '" + custNo + "','" + appNo + "', '10070004', '100700041634108052112.jpg', '100700041634108052112.jpg', NULL, '.jpg', '190855',  '" + appNo + "/20211013/8712976528/', NULL, NULL, '" + inst_time + "', 'sys', NULL, NULL);"
    DataBase(which_db).executeUpdateSql(sql2)
    DataBase(which_db).executeUpdateSql(sql3)
    DataBase(which_db).executeUpdateSql(sql4)
# 第四个页面，其他联系人信息页面
def auth_contact(custNo,headt):
    #data9={"contacts":[{"name":"test","phone":"8888455666","relationship":"10110004"},{"name":"test2","phone":"8883355777","relationship":"10110003"}],"custNo":custNo}
    data9 = {"custNo":custNo,"contacts":[{"custNo":custNo,"name":"test1","phone":"123333","relationship":"10110004","relationshipName":"Hermanos"},{"custNo":custNo,"name":"test2","phone":"543212601","relationship":"10110001","relationshipName":"Padres"}]}
    r9 = requests.post(host_api+'/api/cust/auth/other/contact',data=json.dumps(data9),headers=headt)#最后一步，填写2个联系人的联系方式
    return r9.json()
#风控授信调度接口
def risk_credit(headt):
    print("调用风控授信接口")
    r = requests.post(host_api+'/api/task/risk/credit',headers=headt)
#当前时间的前一天=跑批业务日期，才能正常申请借款
def update_batch_log():
    sql = 'select now();'
    date_time = DataBase(which_db).get_one(sql)
    d = str(date_time[0]+datetime.timedelta(days=-1))
    yudate = d[:4]+d[5:7]+d[8:10]
    sql2 = 'select BUSI_DATE from sys_batch_log order by BUSI_DATE desc limit 1;'
    BUSI_DATE = DataBase(which_db).get_one(sql2)
    if yudate == BUSI_DATE[0]:
        print("当前服务器日期为:",date_time[0])
        print("当期系统跑批业务日期为:",BUSI_DATE[0],"无需修改批量日期")
    else:
        sql3 = "update sys_batch_log set BUSI_DATE='"+yudate+"' where BUSI_DATE='"+BUSI_DATE[0]+"';"
        DataBase(which_db).executeUpdateSql(sql3)
    DataBase(which_db).closeDB()

if __name__ == '__main__':
    #cx_registNo_04()
    repay_data()