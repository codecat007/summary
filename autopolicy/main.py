#!/usr/bin/python
# -*- coding: UTF-8 -*-
#python2 version

#import os
#import time
import sys
import openpyxl
import pandas as pd

OUTPUT_CSV="./output.csv"
HIT_CNT_THRESHOLD=2
SIP_CNT_THRESHOLD=2
#g_output_df = pd.DataFrame({'hit_cnt':[],'dip':[],'dport':[],'proto':[],'sip_cnt':[]})
g_output_df = pd.DataFrame(columns = ["hit_cnt","sip_cnt","dip", "dport", "proto","inif","outif","src_ip"])

def write_csv(dip, dport,proto,sip_dtf,inif_dtf,outif_dtf,hit_cnt):
    sip_cnt = sip_dtf.nunique()

    if sip_cnt <  SIP_CNT_THRESHOLD and hit_cnt < HIT_CNT_THRESHOLD:
        return

    inif_line = ""
    outif_line = ""
    sip_line = ""
    sip_dtf = sip_dtf.sort_values(ascending=False)

    for m in inif_dtf.index:
        inif_line = inif_line + str(inif_dtf[m]) + ";"

    for n in outif_dtf.index:
        outif_line = outif_line + str(outif_dtf[n]) + ";"

    for i in sip_dtf.index:
        sip_line = sip_line + str(sip_dtf[i]) + ";"

    inif_line = inif_line[:-1]
    outif_line = outif_line[:-1]
    sip_line = sip_line[:-1]
    #f = open(OUTPUT_CSV, 'a+')
    #line =  str(hit_cnt) + "," + str(dip) + "," + str(dport) + "," + str(proto) + ","  + str(dtf.nunique())
    #for i in dtf.index:
        #line = line + "," + str(dtf[i])
    #f.writelines(line  + "\n")
    #f.close()
    new = pd.DataFrame([[hit_cnt,sip_cnt,dip,dport,proto,inif_line,outif_line,sip_line]], columns = ["hit_cnt","sip_cnt","dip", "dport", "proto","inif","outif","src_ip"])
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

def get_proto_dtf(dtf,dip):
    proto_dtf = dtf[dtf['dip'] == dip].proto.drop_duplicates()
    return proto_dtf

def get_sip_dtf(dtf,dip,dport):
    sip_dtf = dtf[(dtf['dip'] == dip) & (dtf['dport'] == dport)].sip
    return sip_dtf

def get_sip_dtf_by_proto(dtf,dip,proto):
    sip_dtf = dtf[(dtf['dip'] == dip) & (dtf['proto'] == proto)].sip
    return sip_dtf

def get_inif_dtf(dtf,dip,dport):
    inif_dtf = dtf[(dtf['dip'] == dip) & (dtf['dport'] == dport)].inif.drop_duplicates()
    return inif_dtf

def get_outif_dtf(dtf,dip,dport):
    outif_dtf = dtf[(dtf['dip'] == dip) & (dtf['dport'] == dport)].outif.drop_duplicates()
    return outif_dtf

def study_loop(dtf,proto):
    dip_dtf = get_dip_dtf(dtf)
    for i in dip_dtf.index:
        dport_dtf = get_dport_dtf(dtf,dip_dtf[i])
        for j in dport_dtf.index:
            sip_dtf = get_sip_dtf(dtf, dip_dtf[i], dport_dtf[j])
            hit_cnt = sip_dtf.count()
            sip_dtf = sip_dtf.drop_duplicates()
            inif_dtf = dtf[(dtf['dip'] == dip_dtf[i]) & (dtf['dport'] ==  dport_dtf[j])].inif.drop_duplicates()
            outif_dtf = dtf[(dtf['dip'] ==  dip_dtf[i]) & (dtf['dport'] == dport_dtf[j])].outif.drop_duplicates()
            write_csv(dip_dtf[i], dport_dtf[j], proto, sip_dtf,inif_dtf,outif_dtf, hit_cnt)

def study_not_tcpudp_loop(dtf):
    dip_dtf = get_dip_dtf(dtf)
    for i in dip_dtf.index:
        proto_dtf = get_proto_dtf(dtf, dip_dtf[i])
        for j in proto_dtf.index:
            sip_dtf = get_sip_dtf_by_proto(dtf, dip_dtf[i], proto_dtf[j])
            hit_cnt = sip_dtf.count()
            sip_dtf = sip_dtf.drop_duplicates()
            inif_dtf = dtf[(dtf['dip'] == dip_dtf[i]) & (dtf['proto'] == proto_dtf[j])].inif.drop_duplicates()
            outif_dtf = dtf[(dtf['dip'] == dip_dtf[i]) & (dtf['proto'] == proto_dtf[j])].outif.drop_duplicates()
            write_csv(dip_dtf[i], 0, proto_dtf[j], sip_dtf,inif_dtf,outif_dtf,hit_cnt)

#dtf.to_csv('D:\\a.csv', sep=',', header=True, index=True)
def get_second_study_des(dtf):
    dipstr = ""
    inifstr = ""
    outifstr = ""
    src_ips = ""
    hit_cnts = 0
    sip_cnt = 0
    dport = 0
    proto = 0
    dip_cnt = dtf.dip.drop_duplicates().count()

    inifs = dtf.inif.drop_duplicates()
    outifs = dtf.outif.drop_duplicates()

    for i in dtf.index:
        dipstr = dipstr + str(dtf.loc[i].dip) + ";"
        hit_cnts  += dtf.loc[i].hit_cnt
        src_ips = dtf.loc[i].src_ip
        sip_cnt = dtf.loc[i].sip_cnt
        dport = dtf.loc[i].dport
        proto = dtf.loc[i].proto

    for i in inifs.index:
        inifstr = inifstr + inifs[i]  + ";"

    for i in outifs.index:
        outifstr = outifstr + outifs[i]  + ";"

    dipstr = dipstr[:-1]
    return (hit_cnts,sip_cnt,dip_cnt,dipstr,dport,proto,inifstr,outifstr,src_ips)

def second_study(dtf):
    output_df = pd.DataFrame(columns=["hit_cnt","sip_cnt","dip_cnt", "dip", "dport", "proto", "inif", "outif", "src_ip"])
    tmp = dtf.src_ip.drop_duplicates()
    for i in tmp.index:
        src_dtf = dtf[dtf['src_ip'] == tmp[i]]
        dport_dtf = src_dtf.dport.drop_duplicates()
        for j in dport_dtf.index:
            src_dp_dtf = dtf[(dtf['src_ip'] == tmp[i]) & (dtf['dport'] == dport_dtf[j])]
            (a,b,c,d,e,f,g,h,k) = get_second_study_des(src_dp_dtf)
            #print d, src_dtf.loc[str(0)].sip_cnt, a
            new = pd.DataFrame([[a,b,c,d,e,f,g,h,k]], columns=["hit_cnt", "sip_cnt", "dip_cnt", "dip", "dport", "proto", "inif", "outif", "src_ip"])
            output_df = output_df.append(new,ignore_index=True)
    output_df = output_df.sort_values(by=['hit_cnt', 'sip_cnt'], ascending=False)
    output_df.to_csv(OUTPUT_CSV, encoding='utf-8', index=False)
    #output_df.to_excel('second_result.xlsx', header=True, index=False)
    return output_df

if __name__ == '__main__':

    if len(sys.argv) < 2 or sys.argv[1] == "-h":
        usage = "Usage:" + sys.argv[0] + " input.csv(输入数据集) " + "{output.csv(输出数据集)} " + "{学习深度(1|2)}"
        print usage
        sys.exit()
    input_csv = sys.argv[1]
    deep_level = 1
    if(len(sys.argv) > 3):
        OUTPUT_CSV = sys.argv[2]
        deep_level = int(sys.argv[3])

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
    print "TCP协议分析开始...",tcp_dtf.iloc[:,0].size
    study_loop(tcp_dtf,6)
    print "UDP协议分析开始...",udp_dtf.iloc[:,0].size
    study_loop(udp_dtf,17)
    print "其他协议分析开始...",other_dtf.iloc[:,0].size
    study_not_tcpudp_loop(other_dtf)
    print "分析结束..."
    print "学习出元策略个数：",g_output_df.dip.count()
    print "结果排序..."

    if (deep_level == 1):
        g_output_df = g_output_df.sort_values(by=['hit_cnt', 'sip_cnt'], ascending=False)
        g_output_df.to_csv(OUTPUT_CSV, encoding='utf-8', index=False)
        #g_output_df.to_excel('first_study.xlsx', header=True, index=False)
    elif(deep_level == 2):
        print "深度2分析开始..."
        second_study_dtf = second_study(g_output_df)
        print "深度2分析结束...",second_study_dtf.dip.count()
        #print second_study_dtf.src_ip.drop_duplicates().count()

    #print g_output_df
    #out_dtf = pd.read_csv(OUTPUT_CSV, header=0)
    #out_dtf.sort_index()
    #print "分析结果:",dip_dtf.nunique()
