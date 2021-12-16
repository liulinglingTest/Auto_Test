from Public.var_mex_credit import *
from Public.dataBase_ld import *
from Public.heads_ld import *
from Public.check_api import *
import random,string,datetime

def zhuan_huan(result):
    m = []
    m.append(result)
    t = [tuple(str(n) for n in m) for m in m]  #python列表数字里混入一个Decimal，转换方式
    return t
def cx_lo_loan_dtl(loan_no):
    # lo_loan_dtl贷款基本信息表,查询loan_no等【放款成功-贷前状态变更为10260005】
    # lo_loan_dtl贷款基本信息表,查询loan_no等【放款失败-贷前状态变更为10260009】
    sql = "select apply_loan_amt,loan_amt,before_stat,after_stat from lo_loan_dtl where LOAN_NO = '" + loan_no + "';"
    data = DataBase(which_db).get_one(sql)
    # print(data)
    lists = zhuan_huan(data)
    # print(lists)
    return lists
def cx_cu_cust_bill_dtl(cust_no):
    # cu_账单信息表：【放款失败】，删除数据
    sql = "select BILL_DATE,BILL_STATUS from cu_cust_bill_dtl  where cust_no = '" + cust_no + "' order by INST_TIME desc limit 1;"
    data = DataBase(which_db).get_one(sql)
    # print('sss',data)
    return data
def cx_cu_cust_fee_bill_dtl(cust_no):
    # cu_账单信息表【放款失败】，删除数据
    sql = "select BILL_DATE,BILL_STATUS,SETTLEMENT_TIME from cu_cust_fee_bill_dtl where cust_no = '" + cust_no + "' order by INST_TIME desc limit 1;"
    data = DataBase(which_db).get_one(sql)
    # print(data)
    return data
def cx_cu_cust_fee_dtl(cust_no):
    # cu_客户费用项关系信息表:放款成功 BILL_DATE正确
    # cu_客户费用项关系信息表:放款失败 BILL_DATE为空
    sql = "select BILL_DATE from cu_cust_fee_dtl where cust_no = '" + cust_no + "' order by INST_TIME desc limit 1;"
    data = DataBase(which_db).get_one(sql)
    # print(data)
    lists = zhuan_huan(data)
    return lists
def cx_pay_tran_dtl(loan_no):
    # pay_交易明细表 【放款成功，状态变更为10220002-交易成功】
    # pay_交易明细表 【放款失败会回滚，状态变更为10220003-交易失败】
    sql = "select TRAN_STAT,ACT_TRAN_AMT from pay_tran_dtl t where t.tran_no = (select ORDER_NO from lo_loan_payout_dtl where LOAN_NO='" + loan_no + "');"
    data = DataBase(which_db).get_one(sql)
    # print(data)
    lists = zhuan_huan(data)
    return lists
def cx_fin_account_info(account_no):
    # fin_账户信息表，BILL_DATE正确
    # fin_账户信息表，BILL_DATE回滚置空，支付只维护第一次放款失败，【放款失败会回滚】
    sql = "select BILL_DATE from fin_account_info where ACCOUNT_NO = '" + account_no + "' order by INST_TIME desc limit 1;"
    data = DataBase(which_db).get_one(sql)
    # print(data)
    return data
def cx_fin_payout_dtl(loan_no):
    # fin_payout_dtl 【放款成功,状态置为10420002成功】
    # fin_payout_dtl 【放款失败会回滚,状态置为10420003失败】
    sql = "select ORDER_STATUS,ACT_TRAN_AMT from fin_payout_dtl where ORDER_NO = (select ORDER_NO from lo_loan_payout_dtl where LOAN_NO='" + loan_no + "');"
    data = DataBase(which_db).get_one(sql)
    # print(data)
    lists = zhuan_huan(data)
    return lists
def cx_fin_account_turnover_dtl(account_no):
    # fin_账户流水表，order_no=tran_order_no值【放款失败会回滚-删掉放款数据】
    sql = "select TRANSACTION_AMOUNT,TRANSACTION_USE,TRANSACTION_TYPE from fin_account_turnover_dtl where ACCOUNT_NO = '" + account_no + "' and TRANSACTION_TYPE='20030001' order by INST_TIME desc;"
    data = DataBase(which_db).get_one(sql)
    # print(data)
    return data
def cx_fin_ad_dtl(account_no):
    # fin_应收明细表，汇总【放款失败会回滚，删掉数据】
    sql = "select BILL_DATE from fin_ad_dtl where ACCOUNT_NO = '" + account_no + "' order by INST_TIME desc;"
    data = DataBase(which_db).get_one(sql)
    # print(data)
    return data
def cx_fin_ad_record(account_no):
    # fin_应收明细记录表，每笔记录【放款失败会回滚，删掉数据】
    sql = "select * from fin_ad_record where ACCOUNT_NO = '" + account_no + "' order by ADD_AMT_TIME asc;"
    data = DataBase(which_db).get_one(sql)
    # print(data)
    return data
def cx_fin_rc_dtl(account_no):
    # fin_实付明细表【放款失败会回滚-删掉数据】
    sql = "select REAL_PAY_AMT,RC_STAT from fin_rc_dtl where ACCOUNT_NO = '" + account_no + "';"
    data = DataBase(which_db).get_one(sql)
    return data
# if __name__ == '__main__':
#     # check_table_success('C2082111108146986254630846464')
#     check_table_failure('C2082111058144858471813283840')