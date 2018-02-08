 #df.cloumns = ['sip','dip','sport','dport','proto']
    print df.head(5)
    #print (df.loc['1690872001','80'])
    print df[(df['dip'] == 1690872001) & (df['dport'] == 80)].sip.drop_duplicates()
    print "test pandas"
    #print df.tail(5)
    #print df.describe()
    dip_df = df.dip
    dipf =  dip_df.drop_duplicates()
    print dipf
    print dipf[0],dipf[1],dipf[2]



    dip_df_cnt = df.dip.nunique()
    print dip_df_cnt

    df = df.set_index('dip')
    dport_df = df.ix[dipf[0],"dport"]
    dport_df = dport_df.drop_duplicates()
    print dport_df

    df = df.reset_index('dip')
    df = df.set_index(['dip','dport'])
