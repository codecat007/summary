#!/usr/bin/python
# -*- coding: UTF-8 -*-
#python2 version

#import os
#import time
import sys
import pandas as pd

OUTPUT_CSV="./output.csv"
HIT_CNT_THRESHOLD=1
SIP_CNT_THRESHOLD=1
#g_output_df = pd.DataFrame({'hit_cnt':[],'dip':[],'dport':[],'proto':[],'sip_cnt':[]})
g_output_df = pd.DataFrame(columns = ["hit_cnt","sip_cnt","dip", "dport", "proto","src_ip"])

def write_csv(dip, dport,proto,dtf,hit_cnt):
    sip_cnt = dtf.nunique()
    if sip_cnt <  SIP_CNT_THRESHOLD and hit_cnt < HIT_CNT_THRESHOLD:
        return
    line = ""
    dtf = dtf.sort_values(ascending=False)
    for i in dtf.index:
        line = line + str(dtf[i]) + "-"
    #f = open(OUTPUT_CSV, 'a+')
    #line =  str(hit_cnt) + "," + str(dip) + "," + str(dport) + "," + str(proto) + ","  + str(dtf.nunique())
    #for i in dtf.index:
        #line = line + "," + str(dtf[i])
    #f.writelines(line  + "\n")
    #f.close()
    new = pd.DataFrame([[hit_cnt,sip_cnt,dip,dport,proto,line]], columns = ["hit_cnt","sip_cnt","dip", "dport", "proto","src_ip"])
    global g_output_df
    g_output_df = g_output_df.append(new,ignore_index=True)
    #new = pd.DataFrame(columns = ["hit_cnt", "dip", "dport", "proto","sip_cnt"])
    #print new[0],new[1]
    #g_output_df = g_output_df.append(tmp,ignore_index=True)
    #print g_output_df

def get_dip_dtf(dtf):
    dip_dtf = dtf.dip.drop_duplicates()
    return dip_dtf

def get_dport_dtf(dtf,dip):
    dp_dtf = dtf[dtf['dip'] == dip].dport.drop_duplicates()
    return dp_dtf

def get_proto_dtf(dtf,proto):
    proto_dtf = dtf[dtf['proto'] == proto].dport.drop_duplicates()
    return proto_dtf

def get_sip_dtf(dtf,dip,dport):
    sip_dtf = dtf[(dtf['dip'] == dip) & (dtf['dport'] == dport)].sip
    return sip_dtf

def get_sip_dtf_by_proto(dtf,dip,proto):
    sip_dtf = dtf[(dtf['dip'] == dip) & (dtf['proto'] == proto)].sip
    return sip_dtf

def study_loop(dtf,proto):
    dip_dtf = get_dip_dtf(dtf)
    for i in dip_dtf.index:
        dport_dtf = get_dport_dtf(dtf,dip_dtf[i])
        for j in dport_dtf.index:
            sip_dtf = get_sip_dtf(dtf, dip_dtf[i], dport_dtf[j])
            hit_cnt = sip_dtf.count()
            sip_dtf = sip_dtf.drop_duplicates()
            write_csv(dip_dtf[i], dport_dtf[j], proto, sip_dtf, hit_cnt)

def study_not_tcpudp_loop(dtf, proto):
    dip_dtf = get_dip_dtf(dtf)
    for i in dip_dtf.index:
        proto_dtf = get_proto_dtf(dtf, dip_dtf[i])
        for j in proto_dtf.index:
            sip_dtf = get_sip_dtf_by_proto(dtf, dip_dtf[i], proto_dtf[j])
            hit_cnt = sip_dtf.count()
            sip_dtf = sip_dtf.drop_duplicates()
            write_csv(dip_dtf[i], 0, proto, sip_dtf, hit_cnt)

#dtf.to_csv('D:\\a.csv', sep=',', header=True, index=True)

if __name__ == '__main__':

    if len(sys.argv) < 2 or sys.argv[1] == "-h":
        usage = "Usage:" + sys.argv[0] + " input.csv(输入数据集) " + "{output.csv(输出数据集)} "
        print usage
        sys.exit()
    input_csv = sys.argv[1]
    if(len(sys.argv) > 2):
        OUTPUT_CSV = sys.argv[2]

    dtf = pd.read_csv(sys.argv[1],header=0)
    print "分析开始..."
    dtf_count = dtf.iloc[:,0].size
    print "数据集总数为：", dtf_count
    print "数据集总共包含不同的目的地址数为：", dtf.dip.drop_duplicates().count()
    print "数据集总共包含不同的目的端口数为：", dtf.dport.drop_duplicates().count()
    print "数据集总共包含不同的源地址数为：", dtf.sip.drop_duplicates().count()
    print "数据集总共包含不同的协议数为：", dtf.proto.drop_duplicates().count()
    #dip_dtf = get_dip_dtf(dtf)
    tcp_dtf = dtf[dtf['proto'] == 6]
    udp_dtf = dtf[dtf['proto'] == 17]
    other_dtf = dtf[(dtf['proto'] != 6) & (dtf['proto'] != 17)]
    print "TCP协议分析开始..."
    study_loop(tcp_dtf,6)
    print "UDP协议分析开始..."
    study_loop(udp_dtf,17)
    print "其他协议分析开始..."
    #study_loop(other_dtf,0)
    print "分析结束..."
    print "学习出元策略个数：",g_output_df.dip.count()
    print "结果排序..."

    g_output_df = g_output_df.sort_values(by='hit_cnt',ascending=False)
    g_output_df.to_csv(OUTPUT_CSV, encoding='utf-8', index=False)
    #print g_output_df
    #out_dtf = pd.read_csv(OUTPUT_CSV, header=0)
    #out_dtf.sort_index()
    #print "分析结果:",dip_dtf.nunique()
