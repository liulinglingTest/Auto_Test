from Public.var_mex_credit import *
from Public.dataBase_ld import *
from Public.heads_ld import *
from Public.check_api import *
import random,string,datetime
def check_table_success(cust_no):
    list_data = []
    # 客户账户信息表,查询account_no
    sql = "select ACCOUNT_NO from cu_cust_account_dtl where CUST_NO='" + cust_no + "';"
    data = DataBase(which_db).get_one(sql)
    account_no = str(data[0])
    # lo_loan_dtl贷款基本信息表,查询loan_no等【放款成功-贷前状态变更为10260005】
    sql1 = "select loan_no,before_stat from lo_loan_dtl where CUST_NO = '" + cust_no + "' order by INST_TIME desc limit 1;"
    data1 = DataBase(which_db).get_one(sql1)
    # print(data1)
    loan_no = str(data1[0])
    before_stat = str(data1[1])
    list_data.append(before_stat)
    # cu_账单信息表：账单日，状态正确【放款成功】
    sql2 = "select BILL_DATE from cu_cust_bill_dtl  where cust_no = '" + cust_no + "' order by INST_TIME desc limit 1;"
    data2 = DataBase(which_db).get_one(sql2)
    # print(data2)
    bill_date = str(data2[0])
    list_data.append(bill_date)
    # cu_账单信息表,关联了放款本金和额外费用【放款成功】业务管
    sql3 = "select BILL_DATE from cu_cust_fee_bill_dtl where cust_no = '" + cust_no + "' order by INST_TIME desc limit 1;"
    data3 = DataBase(which_db).get_one(sql3)
    # print(data3)
    bill_date1 = str(data3[0])
    list_data.append(bill_date1)
    # cu_客户费用项关系信息表:放款成功 BILL_DATE正确
    sql5 = "select BILL_DATE from cu_cust_fee_dtl where cust_no = '" + cust_no + "' order by INST_TIME desc limit 1;"
    data5 = DataBase(which_db).get_one(sql5)
    # print(data5)
    bill_date2 = str(data5[0])
    list_data.append(bill_date2)
    # pay_交易明细表 【放款成功，状态变更为10220002-交易成功】
    sql6 = "select TRAN_STAT from pay_tran_dtl t where t.tran_no = (select ORDER_NO from lo_loan_payout_dtl where LOAN_NO='" + loan_no + "');"
    data6 = DataBase(which_db).get_one(sql6)
    # print(data6)
    tran_stat = str(data6[0])
    list_data.append(tran_stat)
    # fin_账户信息表，BILL_DATE正确
    sql7 = "select BILL_DATE from fin_account_info where ACCOUNT_NO = '" + account_no + "' order by INST_TIME desc limit 1;"
    data7 = DataBase(which_db).get_one(sql7)
    # print(data7)
    bill_date3 = str(data7[0])
    list_data.append(bill_date3)
    # lo_放款信息表 【放款成功,状态置为10420002成功】
    sql8 = "select ORDER_STATUS from fin_payout_dtl where ACCOUNT_NO = '" + account_no + "' order by INST_TIME desc limit 1;"
    data8 = DataBase(which_db).get_one(sql8)
    # print(data8)
    order_status2 = str(data8[0])
    list_data.append(order_status2)
    return list_data
def check_table_failure(cust_no):
    list_data = []
    # 客户账户信息表,查询account_no
    sql = "select ACCOUNT_NO from cu_cust_account_dtl where CUST_NO='"+cust_no+"';"
    data = DataBase(which_db).get_one(sql)
    account_no = str(data[0])
    # print(account_no)
    # lo_loan_dtl贷款基本信息表,查询loan_no等【放款失败会回滚-贷前状态变更为10260009】业务管
    sql1 = "select loan_no,before_stat from lo_loan_dtl  where CUST_NO = '"+cust_no+"' order by INST_TIME desc;"
    data1 = DataBase(which_db).get_one(sql1)
    loan_no = str(data1[0])
    before_stat = str(data1[1])
    list_data.append(before_stat)
    # cu_账单信息表：账单日，状态正确【放款失败会回滚，删掉数据】业务管
    sql2 = "select * from cu_cust_bill_dtl  where cust_no = '"+cust_no+"';"
    data2 = DataBase(which_db).get_one(sql2)
    # print(data2)
    list_data.append(data2)
    # cu_账单信息表,关联了放款本金和额外费用【放款失败会回滚，删掉数据】业务管
    sql3 = "select * from cu_cust_fee_bill_dtl where cust_no = '"+cust_no+"';"
    data3 = DataBase(which_db).get_one(sql3)
    # print(data3)
    list_data.append(data3)
    # lo_客户收费信息表，记录额外费用【放款失败会回滚，状态变更为10420003-交易失败】业务管
    sql4 = "select order_status from cu_cust_fee_order_dtl where cust_no = '"+cust_no+"';"
    data4 = DataBase(which_db).get_one(sql4)
    # print(data4)
    order_status = str(data4[0])
    # print(order_status)
    list_data.append(order_status)
    # cu_客户费用项关系信息表:【放款失败会回滚】放款失败：IS_CHARGE=10000000,未出账，01则已出账，BILL_DATE回滚置空，支付只维护第一次放款失败。
    sql5 = "select BILL_DATE from cu_cust_fee_dtl where cust_no = '"+cust_no+"';"
    data5 = DataBase(which_db).get_one(sql5)
    # print(data5)
    bill_date = str(data5[0])
    list_data.append(bill_date)
    # pay_交易明细表 【放款失败会回滚，状态变更为10220003-交易失败】
    sql6 = "select TRAN_STAT from pay_tran_dtl t where t.tran_no = (select ORDER_NO from lo_loan_payout_dtl where LOAN_NO='"+loan_no+"');"
    data6 = DataBase(which_db).get_one(sql6)
    # print(data6)
    tran_stat = str(data6[0])
    list_data.append(tran_stat)
    # fin_账户信息表，BILL_DATE回滚置空，支付只维护第一次放款失败，【放款失败会回滚】
    sql7 = "select BILL_DATE from fin_account_info where ACCOUNT_NO = '"+account_no+"';"
    data7 = DataBase(which_db).get_one(sql7)
    # print(data7)
    bill_date1 = str(data7[0])
    list_data.append(bill_date1)
    # fin_账户流水表，order_no=tran_order_no值【放款失败会回滚-删掉放款数据】
    sql8 = "select * from fin_account_turnover_dtl where ACCOUNT_NO = '"+account_no+"' and TRANSACTION_TYPE='20030001' order by INST_TIME desc;"
    data8 = DataBase(which_db).get_one(sql8)
    # print(data8)
    list_data.append(data8)
    # fin_应收明细表，汇总【放款失败会回滚，删掉数据】
    sql9 = "select * from fin_ad_dtl where ACCOUNT_NO = '"+account_no+"' order by INST_TIME desc;"
    data9 = DataBase(which_db).get_one(sql9)
    # print(data9)
    list_data.append(data9)
    # fin_应收明细记录表，每笔记录【放款失败会回滚，删掉数据】
    sql10 = "select * from fin_ad_record where ACCOUNT_NO = '"+account_no+"' order by ADD_AMT_TIME asc;"
    data10 = DataBase(which_db).get_one(sql10)
    # print(data10)
    list_data.append(data10)
    # fin_payout_dtl 【放款失败会回滚,状态置为10420003失败】
    sql11 = "select ORDER_STATUS from fin_payout_dtl where ACCOUNT_NO = '"+account_no+"' order by INST_TIME desc;"
    data11 = DataBase(which_db).get_one(sql11)
    # print(data11)
    order_stat = str(data11[0])
    list_data.append(data11)
    # fin_实付明细表【放款失败会回滚-删掉数据】
    sql12 = "select * from fin_rc_dtl where ACCOUNT_NO = '"+account_no+"';"
    data12 = DataBase(which_db).get_one(sql12)
    print(list_data)
    list_data.append(data12)
if __name__ == '__main__':
    # check_table_success('C2082111108146986254630846464')
    check_table_failure('C2082111108146986254630846464')