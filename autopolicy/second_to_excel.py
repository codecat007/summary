#!/usr/bin/python
# -*- coding: UTF-8 -*-
#python2 version

import sys
import time
import struct
import socket
import pandas as pd

BYTE_ORDER=0
OUTPUT_FILE="./summary.xlsx"

def split_ip_list(ip_list):
    ret_str = ""
    tmp_list = ip_list.split(';')
    for i in tmp_list:
        tmp_ip = int(i)
        if (BYTE_ORDER == 0):
            tmp_ip = socket.htonl(tmp_ip)
        str_ip = socket.inet_ntoa(struct.pack('!I', tmp_ip))
        ret_str = ret_str + str_ip + ";"
    return ret_str

def first_to_excel(dtf):
    g_output_df = pd.DataFrame(columns=["命中次数", "源地址数", "目的地址", "目的端口", "协议号", "进口", "出口", "源地址列表"])
    dtf = pd.read_csv(input_csv, header=0)
    for i in dtf.index:
        # print dtf[i].dip
        dip = dtf.loc[i].dip
        if (BYTE_ORDER == 0):
            dip = socket.htonl(dip)
        str_ip = socket.inet_ntoa(struct.pack('!I', dip))
        ip = struct.unpack('!I', socket.inet_aton(str_ip))[0]
        src_ip_list = split_ip_list(dtf.loc[i].src_ip)
        # print host,str_ip,ip
        new_row = pd.DataFrame([[dtf.loc[i].hit_cnt, dtf.loc[i].sip_cnt, str_ip, dtf.loc[i].dport, dtf.loc[i].proto,
                                 dtf.loc[i].inif, dtf.loc[i].outif, src_ip_list]],
                               columns=["命中次数", "源地址数", "目的地址", "目的端口", "协议号", "进口", "出口", "源地址列表"])
        g_output_df = g_output_df.append(new_row, ignore_index=True)
    g_output_df.to_excel(OUTPUT_FILE, header=True, index=False)

def second_to_excel(dtf):
    g_output_df = pd.DataFrame(columns=["命中次数", "源地址数", "目的址数", "目的地址", "目的端口", "协议号", "进口", "出口", "源地址列表"])
    for i in dtf.index:
        # print dtf[i].dip
        # dip = dtf.loc[i].dip
        # if(BYTE_ORDER == 0):
        #    dip = socket.htonl(dip)
        # str_ip = socket.inet_ntoa(struct.pack('!I',dip))
        # ip = struct.unpack('!I',socket.inet_aton(str_ip))[0]
        src_ip_list = split_ip_list(dtf.loc[i].src_ip)
        dst_ip_list = split_ip_list(dtf.loc[i].dip)
        # print host,str_ip,ip
        new_row = pd.DataFrame([[dtf.loc[i].hit_cnt, dtf.loc[i].sip_cnt, dtf.loc[i].dip_cnt, dst_ip_list,
                                 dtf.loc[i].dport, dtf.loc[i].proto, dtf.loc[i].inif, dtf.loc[i].outif, src_ip_list]],
                               columns=["命中次数", "源地址数", "目的址数", "目的地址", "目的端口", "协议号", "进口", "出口", "源地址列表"])
        g_output_df = g_output_df.append(new_row, ignore_index=True)
    g_output_df.to_excel(OUTPUT_FILE, header=True, index=False)

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == "-h":
        usage = "Usage:" + sys.argv[0] + " file.csv(输入数据集) " + "{summary.xlsx(输出excel)} " + "{学习深度(1|2)} " + "{host|network} "
        print usage
        sys.exit()

    input_csv = sys.argv[1]
    deep_level = 1
    if(len(sys.argv) > 3):
        OUTPUT_FILE = sys.argv[2]
        deep_level = int(sys.argv[3])

    dtf = pd.read_csv(input_csv,header=0)

    if (deep_level == 1):
        first_to_excel(dtf)
    elif (deep_level == 2):
        second_to_excel(dtf)
    print "转换为Excel文件结束..."