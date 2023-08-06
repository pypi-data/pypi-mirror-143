import datetime
import pandas as pd
import numpy as np
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality


util=functionality.Untils()
hbdb=db_engine.HBDB()
localdb=db_engine.PrvFunDB().engine

def read_hld_fromdb(jjdm_list,if_zc=False,start_date=None,end_date=None,ext_condtion=None):

    jjdm_con=util.list_sql_condition(jjdm_list)

    if((start_date is not None) and (end_date is not None) ):
        date_con="and jsrq>='{0}' and jsrq<='{1}'".format(start_date,end_date)
    elif((start_date is None) and (end_date is None)):
        date_con=''
    else:
        date_con="and jrsq='{}'".format(start_date)

    if(ext_condtion is None):
        ext_condtion=''

    sql = """select jjdm,jsrq,zqdm,zjbl from st_fund.t_st_gm_gpzh where jjdm in ({0}) {1} {2}
    """.format(jjdm_con, date_con,ext_condtion)
    hld =hbdb.db2df(sql, db='funduser')
    hld.reset_index(drop=True, inplace=True)
    hld['date'] = hld['jsrq'].astype(str)
    hld.drop('jsrq', inplace=True, axis=1)

    hld=hld_reportdate2trade_date(hld,date_col='date')

    #take zc only
    if(if_zc):
        hld['zjbl_rank'] = hld.groupby('date')['zjbl'].rank(ascending=False)
        hld=hld[hld['zjbl_rank']<=10]
        hld.drop('zjbl_rank',inplace=True,axis=1)
        hld.reset_index(drop=True, inplace=True)

    return hld

def hld_reportdate2trade_date(hld,date_col):
    for date in hld[date_col].unique():
        hld.loc[hld[date_col]==date,date_col]=util._shift_date(date)
    return  hld

def ticker_weight_history_perjj(hld):

    history_df=pd.DataFrame()

    zqdm_list=hld['zqdm'].unique().tolist()
    date_list=hld['date'].unique().tolist()
    date_list.sort()
    zqdm_list.sort()

    history_df['zqdm']=zqdm_list
    for date in date_list:
        tempdf=hld[hld['date']==date][['zjbl','zqdm']]
        history_df=pd.merge(history_df,tempdf,how='left',on='zqdm')
        history_df.rename(columns={'zjbl':date},inplace=True)

    return  history_df

def get_stock_price(date_list,ticker_list,add_pre_day=False,fre='Q'):

    date_list.sort()
    if(add_pre_day):
        if(fre=='Q'):
            add_days=91
        elif(fre=='M'):
            add_days=30
        elif(fre=='HA'):
            add_days=188
        else:
            print("input fre is not supported")
            raise Exception

        pre_date= (datetime.datetime.strptime(date_list[0], '%Y%m%d')-datetime.timedelta(days=add_days)).strftime('%Y%m%d')
        date_list=[pre_date]+date_list

    date_con=util.list_sql_condition(date_list)

    if(len(ticker_list)>900):
        sql = """
        select ZQDM,JYRQ,DRJJ from FUNDDB.ZGJY where JYRQ in ({0}) and SCDM !='STAS00'
         """.format(date_con)
        stock_price=pd.DataFrame(data=ticker_list,columns=['ZQDM'])
        stock_price =pd.merge(stock_price,hbdb.db2df(sql, db='readonly'),how='left',on='ZQDM')

    else:
        ticker_con=util.list_sql_condition(ticker_list)
        sql = """
        select ZQDM,JYRQ,DRJJ from FUNDDB.ZGJY where ZQDM in ({0}) and JYRQ in ({1})
         """.format(ticker_con, date_con)
        stock_price = hbdb.db2df(sql, db='readonly')


    return stock_price.drop('ROW_ID',axis=1)

def stock_price2ret(pricedf):

    pricedf['pctchange']=pricedf.groupby('ZQDM')['DRJJ'].pct_change()

    return pricedf

def hhi_index(arr):

    return np.sum([x**2 for x in arr])

class Industry_analysis:

    def __init__(self):

        self.theme_col = ['大金融', '消费', 'TMT', '周期', '制造']
        self.theme_map = dict(zip(self.theme_col,
                             [['bank', 'nonbankfinan', 'realestate'],
                              ['agriforest', 'conmat', 'commetrade', 'foodbever', 'health', 'leiservice', 'textile'],
                              ['computer', 'electronics', 'media', 'telecom'],
                              ['builddeco', 'chem', 'houseapp', 'ironsteel', 'mining', 'nonfermetal'],
                              ['auto', 'eleceqp', 'lightindus', 'machiequip', 'transportation', 'utilities']
                              ]
                             ))
        self.indus_col = ['aerodef', 'agriforest', 'auto', 'bank', 'builddeco', 'chem', 'conmat', 'commetrade',
                          'computer', 'conglomerates', 'eleceqp', 'electronics',
                          'foodbever', 'health', 'houseapp', 'ironsteel', 'leiservice', 'lightindus', 'machiequip',
                          'media', 'mining', 'nonbankfinan', 'nonfermetal',
                          'realestate', 'telecom', 'textile', 'transportation', 'utilities']
        chinese_name = ['国防军工', '农林牧渔', '汽车', '银行', '建筑装饰', '化工', '建筑材料', '商业贸易', '计算机', '综合', '电气设备',
                        '电子', '食品饮料', '医药生物', '家用电器', '钢铁', '休闲服务', '轻工制造', '机械设备', '传媒', '采掘', '非银金融',
                        '有色金属', '房地产', '通信', '纺织服装', '交通运输', '公用事业']
        self.industry_name_map = dict(zip(chinese_name, self.indus_col))

        self.industry_name_map_e2c = dict(zip(self.indus_col, chinese_name))

    def style_change_detect_engine(self,q_df,diff1,diff2,q_list,col_list,t1,t2):

        style_change=[]

        for col in col_list:

            potential_date=diff2[diff2[col]<=-1*t1].index.to_list()
            last_added_date=q_list[-1]
            for date in potential_date:
                if(diff1.loc[q_df.index[q_df.index<=date][-3]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-3]
                elif(diff1.loc[q_df.index[q_df.index<=date][-2]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-2]
                elif(diff1.loc[q_df.index[q_df.index<=date][-1]][col]<=-1*t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if((q_list.index(added_date)-q_list.index(last_added_date)<=2
                        and q_list.index(added_date)-q_list.index(last_added_date)>0) or added_date==q_list[-1]):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

            potential_date = diff2[diff2[col] >= t1].index.to_list()
            last_added_date = q_list[-1]
            for date in potential_date:
                if (diff1.loc[q_df.index[q_df.index <= date][-3]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-3]
                elif (diff1.loc[q_df.index[q_df.index <= date][-2]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-2]
                elif (diff1.loc[q_df.index[q_df.index <= date][-1]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if (q_list.index(added_date) - q_list.index(last_added_date) <= 2
                        and q_list.index(added_date) - q_list.index(last_added_date) > 0):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

        return style_change

    def style_change_detect_engine2(self, q_df, diff1, col_list, t1, t2):

        style_change=[]
        t3=t2/2

        for col in col_list:

            tempdf=pd.merge(q_df[col],diff1[col],how='left',on='date')
            tempdf['style']=''
            style_num=0
            tempdf['style'].iloc[0:2] = style_num

            for i in range(2,len(tempdf)-1):
                if(tempdf[col+'_y'].iloc[i]>t1 and tempdf[col+'_y'].iloc[i+1]>-1*t3 ):
                    style_num+=1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_x'].iloc[i]-tempdf[tempdf['style']==style_num][col+'_x'][0]>t1 and
                     tempdf[col+'_y'].iloc[i]>t2 and tempdf[col+'_y'].iloc[i+1]>-1*t3):
                    style_num += 1
                    added_date=tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_y'].iloc[i]<-1*t1 and tempdf[col+'_y'].iloc[i+1]<t3 ):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif (tempdf[col + '_x'].iloc[i] - tempdf[tempdf['style'] == style_num][col + '_x'][0] < -1*t1 and
                      tempdf[col + '_y'].iloc[i] < -1*t2 and tempdf[col + '_y'].iloc[i + 1] <  t3):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)

                tempdf['style'].iloc[i] = style_num

        return style_change

    def style_change_detect(self,df,q_list,col_list,t1,t2):

        q_list.sort()
        q_df = df.loc[q_list]
        diff1=q_df.diff(1)
        # diff2=q_df.rolling(3).mean().diff(2)
        # diff4 = q_df.rolling(3).mean().diff(4)

        # style_change_short=self.style_change_detect_engine(q_df,diff1,diff2,q_list,col_list,t1,t2)
        # style_change_long=self.style_change_detect_engine(q_df,diff1,diff4,q_list,col_list,t1,t2)
        # style_change=style_change_short+style_change_long

        style_change = self.style_change_detect_engine2(q_df, diff1, col_list, t1, t2)

        return list(set(style_change)),np.array(q_list)

    def shifting_expression(self,change_ret,name,jjdm,style='Total'):

        change_winning_pro_hld = sum(change_ret[3]) / len(change_ret)
        change_winning_pro_nextq=sum(change_ret[2]) / len(change_ret)
        left_ratio = sum(change_ret[0]) / len(change_ret)
        left_ratio_deep = sum(change_ret[1]) / len(change_ret)
        # right_ratio = 1-left_ratio
        # right_ratio_deep = 1 - left_ratio_deep
        one_q_ret = change_ret[4].mean()
        hid_q_ret = change_ret[5].mean()

        return  np.array([style.split('_')[0],len(change_ret),change_winning_pro_hld,change_winning_pro_nextq
                             ,one_q_ret,hid_q_ret,left_ratio,left_ratio_deep])

    def style_change_ret(self,df,q_list,col_list,t1,t2,factor_return):

        style_change,q_list = self.style_change_detect(df,q_list,col_list,t1,t2)
        change_count = len(style_change)
        style_changedf=pd.DataFrame()
        style_changedf['date']=[x.split('@')[0] for x in style_change]
        style_changedf['style']=[x.split('@')[1] for x in style_change]
        style_changedf.sort_values('date',inplace=True,ascending=False)
        style_chang_extret=dict(zip(style_change,style_change))


        def get_factor_return(q_list, first_change_date, style):

            fac_ret_df=factor_return[(factor_return['zqdm']==style.split('_')[0])
                                     &(factor_return.index>=q_list[q_list < first_change_date][-2])
                                     &(factor_return.index<=q_list[-1])]
            return fac_ret_df
        def q_ret(fac_ret_df,q0,q1,time_length=1):
            res=np.power(fac_ret_df.loc[q1]['price']/fac_ret_df.loc[q0]['price'],1/time_length)-1
            return  res


        if(change_count>0):
            for style in style_changedf['style']:

                changedf=style_changedf[style_changedf['style']==style]
                changedf=changedf.sort_values('date')
                first_change_date=changedf['date'].values[0]
                fac_ret_df=get_factor_return(q_list,first_change_date,style)
                fac_ret_df['ma20'] = fac_ret_df.rolling(20, 1)['price'].mean()

                for i in range(len(changedf)):
                    date=changedf.iloc[i]['date']

                    observer_term=np.append(q_list[q_list<date][-2:],q_list[(q_list>=date)][0:2])

                    new_exp=df[style].loc[observer_term[2]]
                    old_exp=df[style].loc[observer_term[1]]

                    q0=observer_term[0]
                    q1=observer_term[1]
                    old_ret=q_ret(fac_ret_df,q0,q1)
                    if_left_deep =( (fac_ret_df['price'].loc[q0:q1]<fac_ret_df['price'].loc[q0:q1].mean()).sum()\
                                   /len(fac_ret_df['price'].loc[q0:q1])>=0.5 )


                    q0=observer_term[1]
                    q1=observer_term[2]
                    current_ret=q_ret(fac_ret_df,q0,q1)
                    if_left = ( (fac_ret_df['price'].loc[q0:q1]<fac_ret_df['price'].loc[q0:q1].mean()).sum()\
                                   /len(fac_ret_df['price'].loc[q0:q1])>=0.5 )

                    q0=observer_term[2]
                    q1=observer_term[3]
                    if(q1>fac_ret_df.index[-1]):
                        q1=fac_ret_df.index[-1]
                    next_ret=q_ret(fac_ret_df,q0,q1)


                    if (i != len(changedf) - 1):
                        q1 = changedf.iloc[i + 1]['date']
                        q2 = q1
                    else:
                        q1 = q_list[-1]
                        q2=fac_ret_df.index[-1]

                    change_date=date
                    time_length = q_list.tolist().index(q1) - q_list.tolist().index(change_date)
                    holding_ret=q_ret(fac_ret_df,q0,q2,time_length=time_length)

                    if_win_next=(new_exp>old_exp)&(next_ret>current_ret)
                    if_win_hld=(new_exp>old_exp)&(holding_ret>current_ret)

                    shift_retur_next= (new_exp-old_exp)*(next_ret-current_ret)
                    shift_retur_hld = (new_exp - old_exp) * (holding_ret - current_ret)

                    style_chang_extret[date+"@"+style]=[if_left,if_left_deep,if_win_next,if_win_hld,shift_retur_next,shift_retur_hld]

        return style_chang_extret

    def style_shifting_analysis(self,df,q_list,col_list,t1,t2,name,jjdm,factor_return):

        # col_list=[x+"_exp_adj" for x in col]
        change_ret=self.style_change_ret(df,q_list,col_list,t1=t1,t2=t2,factor_return=factor_return)
        change_ret = pd.DataFrame.from_dict(change_ret).T
        change_ret['style'] = list([x.split('@')[1] for x in change_ret.index])
        change_ret['date'] = list([x.split('@')[0] for x in change_ret.index])

        data=[]

        if(len(change_ret)>0):
            data.append(self.shifting_expression(change_ret,name,jjdm))
            for style in change_ret['style'].unique():
                tempdf=change_ret[change_ret['style']==style]
                data.append(self.shifting_expression(tempdf,name,jjdm,style))

        shift_df = pd.DataFrame(data=data,columns=['风格类型','切换次数','胜率（直到下次切换）','胜率（下季度）',
                                                   '下季平均收益','持有平均收益','左侧比率','深度左侧比例'])
        # for col in ['胜率（直到下次切换）','胜率（下季度）','下季平均收益','持有平均收益','左侧比率','深度左侧比例']:
        #     shift_df[col] = shift_df[col].astype(float).map("{:.2%}".format)

        return  shift_df

    def save_industry_property2localdb(self,ba,asofdate=datetime.datetime.today().strftime('%Y%m%d'), time_length=3):

        theme_col = self.theme_col
        jjdm_list = util.get_mutual_stock_funds('20211231')
        collect_df = pd.DataFrame()

        start_date = str(int(asofdate[0:4]) - time_length) + asofdate[4:]

        mean_dict = dict(zip(ba.indus_col + theme_col, [[]] * 33))
        cen_list = []
        ratio_list = []
        new_jjdm_list = []
        average_ind_num_list = []
        cen_list2 = []
        ratio_list2 = []
        top5_ind = []

        theme_map = self.theme_map

        for jjdm in jjdm_list:

            try:
                df, q_list = ba.ret_div(jjdm, start_date, asofdate, True)
                # if(fre=='Q'):
                #     df=df.loc[(df.index.str[4:6]=='03')|(df.index.str[4:6]=='06')
                #               |(df.index.str[4:6]=='09')|(df.index.str[4:6]=='12')]

                # get the theme exp from industry exp
                for col in theme_map.keys():
                    df[col] = df[[x + '_exp' for x in theme_map[col]]].sum(axis=1)

                q_date = df.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in df.index]].index
                a_date = df.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in df.index]].index
                q_list = q_date.to_list() + a_date.to_list()

                themedf = df[theme_col]
                inddf = df[[x + '_exp' for x in ba.indus_col]]

                # calculate the industry and theme holding centralization_level
                average_ind_cen_level = ba.centralization_level(inddf.loc[q_list], 3, 5)
                cen_list.append(average_ind_cen_level)

                average_theme_cen_level = ba.centralization_level(themedf.loc[q_list], 1, 2)
                cen_list2.append(average_theme_cen_level)

                # calculate the industry and theme holding shift ratio
                shift_ratio = ba.ind_shift_rate(df[[x + '_exp' for x in ba.indus_col] + ['jjzzc']].loc[q_list])['mean']
                ratio_list.append(shift_ratio)

                shift_ratio_theme = ba.ind_shift_rate(df[theme_col + ['jjzzc']].loc[q_list])['mean']
                ratio_list2.append(shift_ratio_theme)

                average_ind_num_list.append((inddf.loc[q_list] > 0).sum(axis=1).mean())

                for col in ba.indus_col:
                    mean_dict[col] = mean_dict[col] + [inddf[col + '_exp'].mean()]

                # get the string list of top 5 industry
                top5 = [ba.industry_name_map_e2c[x.split('_')[0]] for x in
                        inddf.mean().sort_values()[-5:].index.tolist()]
                top5 = util.list_sql_condition(top5)
                top5_ind.append(top5)

                for col in theme_col:
                    mean_dict[col] = mean_dict[col] + [themedf[col].mean()]

                new_jjdm_list.append(jjdm)

            except Exception as e:
                print(jjdm)
                print(e)

        collect_df['cen_ind'] = cen_list
        collect_df['ratio_ind'] = ratio_list
        collect_df['jjdm'] = new_jjdm_list

        collect_df['cen_ind'] = collect_df['cen_ind'].rank(method='min') / len(collect_df)
        collect_df['ratio_ind'] = collect_df['ratio_ind'].rank(method='min') / len(collect_df)

        collect_df['cen_theme'] = cen_list2
        collect_df['ratio_theme'] = ratio_list2

        collect_df['cen_theme'] = collect_df['cen_theme'].rank(method='min') / len(collect_df)
        collect_df['ratio_theme'] = collect_df['ratio_theme'].rank(method='min') / len(collect_df)

        collect_df['industry_num'] = average_ind_num_list
        collect_df['top5'] = top5_ind

        for col in ba.indus_col + theme_col:
            collect_df[col] = mean_dict[col]

        collect_df['asofdate'] = asofdate
        collect_df.rename(columns=self.industry_name_map_e2c, inplace=True)

        collect_df.to_csv('collectdf.csv', encoding='gbk', index=False)

        # check if data already exist
        sql = "delete from hbs_industry_property where asofdate='{0}'".format(asofdate)
        localdb.execute(sql)

        collect_df.to_sql('hbs_industry_property', index=False, if_exists='append', con=localdb)

    def save_industry_shift_property2localdb(self,ba,asofdate=datetime.datetime.today().strftime('%Y%m%d'), time_length=3):

        jjdm_list = util.get_mutual_stock_funds('20211231')
        collect_df = pd.DataFrame()
        collect_df_theme=pd.DataFrame()
        start_date = str(int(asofdate[0:4]) - time_length) + asofdate[4:]

        theme_col = self.theme_col
        theme_map = self.theme_map

        def get_factor_return(start_date, asofdate,style_list):

            sql="select fldm,flmc,zsdm from st_market.t_st_zs_hyzsdmdyb where hyhfbz='2' and fljb='1' "
            industry_index_code=hbdb.db2df(sql,db='alluser')
            industry_index_code['name_eng']=[self.industry_name_map[x] for x in industry_index_code['flmc']]

            style=util.list_sql_condition(
                [industry_index_code[industry_index_code['name_eng']==x.split('_')[0]]['zsdm'].iloc[0] for x in style_list])

            sql="select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm in ({0}) and jyrq>='{1}' and  jyrq<='{2}'  "\
                .format(style,start_date,asofdate)
            fac_ret_df=hbdb.db2df(sql, db='alluser')
            fac_ret_df['jyrq']=fac_ret_df['jyrq'].astype(str)
            fac_ret_df.set_index('jyrq', drop=True, inplace=True)

            fac_ret_df['price'] = fac_ret_df['spjg']

            fac_ret_df['zqdm'] = [industry_index_code[industry_index_code['zsdm'] == x]['name_eng'].iloc[0] for x in
                                  fac_ret_df['zqdm']]

            return fac_ret_df

        def get_factor_return_theme(start_date,asofdate):

            factor_return_theme_raw = pd.read_sql(
                "select * from nav_theme_ret where TRADE_DATE>='{0}' and TRADE_DATE<='{1}' "
                .format(start_date, asofdate), con=localdb).rename(columns={'TRADE_DATE': "jyrq"})
            factor_return_theme_raw['jyrq']=factor_return_theme_raw['jyrq'].astype('str')
            factor_return_theme_raw.set_index('jyrq', inplace=True, drop=True)
            factor_return_theme_raw = factor_return_theme_raw + 1
            factor_return_theme_raw = factor_return_theme_raw.rolling(len(factor_return_theme_raw), 1).apply(np.prod)

            factor_return_theme = pd.DataFrame()
            for col in theme_col:
                temp_theme = factor_return_theme_raw['大金融'].to_frame('price')
                temp_theme['zqdm'] = col
                factor_return_theme = pd.concat([factor_return_theme, temp_theme], axis=0)

            return  factor_return_theme

        factor_return=get_factor_return(start_date,asofdate,self.indus_col)

        factor_return_theme=get_factor_return_theme(start_date,asofdate)

        for jjdm in jjdm_list:

            try:
                df, q_list = ba.ret_div(jjdm, start_date, asofdate, True)
                q_date = df.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in df.index]].index
                a_date = df.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in df.index]].index
                q_list = q_date.to_list() + a_date.to_list()
                q_list.sort()
                average_a_w = df.loc[a_date]['published_stock_weight'].mean()

                # get the theme exp from industry exp
                for col in theme_map.keys():
                    df[col] = df[[x + '_exp' for x in theme_map[col]]].sum(axis=1)

                # ind_shift_df=pd.merge(pd.Series(['Total']+self.indus_col).to_frame('风格类型'),
                #                       self.style_shifting_analysis(
                #     df[[x + "_exp" for x in ba.indus_col] + [x for x in ba.indus_col]].astype(float),
                #     q_list, [x + "_exp" for x in ba.indus_col],
                #     t1=0.1 * average_a_w, t2=0.075 * average_a_w, name='industry', jjdm=jjdm,factor_return=factor_return),how='left',
                #                       on=['风格类型'])

                theme_shift_df=pd.merge(pd.Series(['Total']+theme_col).to_frame('风格类型'),
                                      self.style_shifting_analysis(
                    df[theme_col].astype(float),
                    q_list, theme_col,
                    t1=0.2 * average_a_w, t2=0.75*0.2 * average_a_w, name='theme', jjdm=jjdm,factor_return=factor_return_theme),how='left',
                                      on=['风格类型'])

                # ind_shift_df=ind_shift_df.T
                # ind_shift_df.columns=ind_shift_df.loc['风格类型']
                # ind_shift_df.drop('风格类型',axis=0,inplace=True)
                # ind_shift_df['jjdm'] = jjdm
                # ind_shift_df.reset_index(drop=False,inplace=True)


                theme_shift_df=theme_shift_df.T
                theme_shift_df.columns=theme_shift_df.loc['风格类型']
                theme_shift_df.drop('风格类型',axis=0,inplace=True)
                theme_shift_df['jjdm'] = jjdm
                theme_shift_df.reset_index(drop=False,inplace=True)

                # collect_df=pd.concat([collect_df,ind_shift_df],axis=0)
                collect_df_theme=pd.concat([collect_df_theme,theme_shift_df],axis=0)

                print('{} done'.format(jjdm))

            except Exception as e:
                print(jjdm)
                print(e)


        # collect_df[['Total']+self.indus_col] = collect_df[['Total']+self.indus_col].astype(
        #     float)
        collect_df_theme[['Total']+theme_col] = collect_df_theme[['Total']+theme_col].astype(
            float)

        # collect_df.rename(columns=self.industry_name_map_e2c, inplace=True)

        # collect_df[[x+'_rank' for
        #             x in ['Total']+
        #             list(self.industry_name_map_e2c.values())
        #             ]]=collect_df.groupby('index').rank(method='min')[['Total']+
        #                                                                list(self.industry_name_map_e2c.values())]\
        #                /collect_df.groupby('index').count()[['Total']+
        #                                                                list(self.industry_name_map_e2c.values())].loc['切换次数']

        collect_df_theme[[x+'_rank' for
                    x in ['Total']+
                    theme_col
                    ]]=collect_df_theme.groupby('index').rank(method='min')[['Total']+
                                                                       theme_col]\
                       /collect_df_theme.groupby('index').count()[['Total']+
                                                                       theme_col].loc['切换次数']

        # collect_df.rename(columns={'index': '项目名'}, inplace=True)
        collect_df_theme.rename(columns={'index': '项目名'}, inplace=True)


        # collect_df['asofdate']=df.index.max()
        collect_df_theme['asofdate']=df.index.max()


        #check if already exist
        # sql="delete from hbs_industry_shift_property where asofdate='{0}'".format(df.index.max())
        # localdb.execute(sql)
        #
        # collect_df.to_sql('hbs_industry_shift_property',index=False,if_exists='append',con=localdb)

        #check if already exist
        # sql="delete from hbs_theme_shift_property where asofdate='{0}'".format(df.index.max())
        # localdb.execute(sql)
        collect_df_theme.to_excel('theme_shit.xlsx')
        collect_df_theme.to_sql('hbs_theme_shift_property',index=False,if_exists='append',con=localdb)

class General_holding:

    @staticmethod
    def read_hld_fromdb(start_date,end_date,jjdm):

        sql="""select jjdm,jsrq,zqdm,zjbl from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq>='{1}' and jsrq<='{2}'
        """.format(jjdm,start_date,end_date)
        hld=hbdb.db2df(sql,db='funduser')
        hld['jsrq']=hld['jsrq'].astype(str)
        return hld

    @staticmethod
    def hld_compenzation(hlddf,fund_allocation):

        q_date=hlddf.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in hlddf['jsrq']]]['jsrq'].unique().tolist()
        a_date=hlddf.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in hlddf['jsrq']]]['jsrq'].unique().tolist()
        q_list=hlddf['jsrq'].unique().tolist()
        q_list.sort()

        hld_H=pd.DataFrame()
        hld_L = pd.DataFrame()
        #get heavy hld for annual and half_annual report
        for date in a_date:
            hld_H=pd.concat([hld_H,hlddf[hlddf['jsrq']==date].sort_values('zjbl')[-10:].reset_index(drop=True)],axis=0)
            hld_L=pd.concat([hld_L,hlddf[hlddf['jsrq']==date].sort_values('zjbl')[0:-10].reset_index(drop=True)],axis=0)
        for date in q_date:
            hld_H=pd.concat([hld_H,hlddf[hlddf['jsrq']==date]],axis=0)


        for i in range(len(q_list)):
            t1=q_list[i]
            if((i>0) and (t1[4:6] == '03') or  (t1[4:6] == '09')):
                t0=q_list[i-1]
            else:
                continue
            #calculate the no hevay hld for quarter report data by the mean of two annaul data if next annaul report exists
            if(i!=len(q_list)-1):
                t2=q_list[i+1]
                temp=pd.merge(hlddf[hlddf['jsrq']==t0].sort_values('zjbl')[0:-10],
                              hlddf[hlddf['jsrq']==t2].sort_values('zjbl')[0:-10],
                              how='outer',on='zqdm').fillna(0)
                temp.set_index('zqdm',inplace=True)
                if(len(temp)==0):
                    continue
                drop_list=list(set(temp.index).intersection( set(hlddf[hlddf['jsrq']==t1]['zqdm'])))
                temp.drop(drop_list,axis=0,inplace=True)
                temp['zjbl']=(temp['zjbl_x']+temp['zjbl_y'])/2
                temp['zjbl']=temp['zjbl']*((fund_allocation[fund_allocation['jsrq'] == t1]['gptzzjb']*100-hld_H[hld_H['jsrq']==t1]['zjbl'].sum()).values[0]/temp['zjbl'].sum())
                temp['jsrq']=t1
                temp.reset_index(drop=False,inplace=True)
                hld_L=pd.concat([hld_L,temp[['zjbl','jsrq','zqdm']]],axis=0)

            else:
                temp=hlddf[hlddf['jsrq']==t0].sort_values('zjbl')[0:-10]
                temp['zjbl']=temp['zjbl']/temp['zjbl'].sum()
                temp['zjbl']=temp['zjbl']*(fund_allocation[fund_allocation['jsrq'] == t1]['gptzzjb']*100-hld_H[hld_H['jsrq']==t1]['zjbl'].sum()).values[0]
                temp['jsrq']=t1
                temp.reset_index(drop=False,inplace=True)
                hld_L=pd.concat([hld_L,temp[['zjbl','jsrq','zqdm']]],axis=0)
        return pd.concat([hld_H,hld_L],axis=0).sort_values('jsrq').reset_index(drop=True)

    @staticmethod
    def fund_asset_allocation(jjdm,date_list):

        sql="select jjdm,jsrq,jjzzc,gptzzjb from st_fund.t_st_gm_zcpz where jjdm='{2}' and jsrq>='{0}' and jsrq<='{1}'"\
            .format(date_list[0],date_list[-1],jjdm)
        fund_allocation=hbdb.db2df(sql,db='funduser')
        fund_allocation['gptzzjb']=fund_allocation['gptzzjb']/100
        fund_allocation['jsrq']=fund_allocation['jsrq'].astype(str)
        return fund_allocation

    @staticmethod
    def stock_centralization_lv(hld):

        top3w=(hld[(hld.groupby('jsrq').rank(ascending=False,method='min')<=3)['zjbl']]
               .groupby('jsrq')['zjbl'].sum()).mean()
        top5w=(hld[(hld.groupby('jsrq').rank(ascending=False,method='min')<=5)['zjbl']]
               .groupby('jsrq')['zjbl'].sum()).mean()
        top10w=(hld[(hld.groupby('jsrq').rank(ascending=False,method='min')<=10)['zjbl']]
               .groupby('jsrq')['zjbl'].sum()).mean()

        result=(top10w+top3w+top5w)/3


        return result,top3w,top5w,top10w

    @staticmethod
    def get_fund_financial_info(jjdm_list,start_date,end_date):

        jjdm_con=util.list_sql_condition(jjdm_list)

        sql="""
        select jjdm,jsrq,pe,pb,roe,dividend from st_fund.t_st_gm_jjggfg 
        where jsrq>='{0}' and jsrq<='{1}' and jjdm in ({2}) and zclb=2
        """\
            .format(start_date,end_date,jjdm_con)

        df=hbdb.db2df(sql,db='funduser')

        df['jsrq']=df['jsrq'].astype(str)

        for col in ['pe','pb','roe','dividend']:
            df.loc[df[col]==99999,col]=np.nan

        return  df

    @staticmethod
    def get_stock_price(zqdm_list=None,date_list=None):

        count=0
        if(zqdm_list is not None):
            zqdm_con="ZQDM in ({0})".format(util.list_sql_condition(zqdm_list))
            count+=1
        else:
            zqdm_con=""

        if(date_list is not None):
            date_con="JYRQ in ({0})".format(util.list_sql_condition(date_list))
            count += 1
        else:
            date_con=""

        if(count==2):
            joint="and"
        else:
            joint=""

        sql="""
        select ZQDM,JYRQ,SPJG from FUNDDB.ZGJY where {0} {2} {1} and SPJG!=99999 and SPJG!=0
         """.format(zqdm_con,date_con,joint)

        stock_price=hbdb.db2df(sql,db='readonly')
        stock_price.drop('ROW_ID',axis=1,inplace=True)

        return stock_price

    def fund_holding_date_manufacture(self,jjdm_list,start_date,end_date):

        hld=pd.DataFrame()
        fund_allocation = pd.DataFrame()
        new_jjdm_list=[]

        for jjdm in jjdm_list:

            try:

                #read holding info
                hld=pd.concat([hld,self.read_hld_fromdb(start_date,end_date,jjdm)]
                              ,axis=0)

                # get fund asset allocation info
                fund_allocation =pd.concat([fund_allocation,
                                            self.fund_asset_allocation(jjdm, hld['jsrq'].unique().tolist())],axis=0)
                # #remove HK stock
                # tickerlist=tempdf['zqdm'][~tempdf['zqdm'].dropna().str.contains('H')].unique()

                new_jjdm_list.append(jjdm)

            except Exception as e:
                print('{0}@{1}'.format(jjdm,e))


        #shift the report date to trading date
        org_date_list=hld['jsrq'].unique().tolist()
        date_list = [util._shift_date(x) for x in org_date_list]
        date_map=dict(zip(org_date_list,date_list))
        changed_date=set(org_date_list).difference(set(date_list))

        #read the fund pe,pb,roe,dividend information from db
        financial_df=self.get_fund_financial_info(new_jjdm_list,start_date,end_date)

        #transfor report date to trading date
        for date in changed_date:
            hld.loc[hld['jsrq']==date,'jsrq']=date_map[date]
            fund_allocation.loc[fund_allocation['jsrq'] == date, 'jsrq'] = date_map[date]
            financial_df.loc[financial_df['jsrq']==date,'jsrq']=date_map[date]

        hld=pd.merge(hld,fund_allocation,how='inner',on=['jsrq','jjdm'])
        hld = pd.merge(hld, financial_df, how='left', on=['jsrq', 'jjdm'])
        hld['zjbl']=hld['zjbl']/100/hld['gptzzjb']
        hld.set_index('jsrq',inplace=True,drop=True)

        return  hld,new_jjdm_list

    def save_holding_trading_2db(self,jjdm_list,start_date,end_date):

        #backward the start date one quarter more and make the holding of this quarter as history holding
        last_quarter=(datetime.datetime.strptime(start_date, '%Y%m%d')-datetime.timedelta(days=93))\
            .strftime('%Y%m%d')

        #get the cleaning holding data
        hld, new_jjdm_list = self.fund_holding_date_manufacture(jjdm_list, last_quarter, end_date)
        date_list = hld.index.unique().tolist()

        #get the week end date list and use this list to collect stock price data
        sql_script = "SELECT JYRQ FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {} and SFZM=1 and SFJJ=0".format(
            str(int(date_list[0][0:4])-1)+date_list[0][4:],date_list[-1])
        jyrl=hbdb.db2df(sql_script,db='readonly').drop('ROW_ID',axis=1)
        jyrl=jyrl.sort_values('JYRQ')

        date_list_new=list(set(date_list+jyrl['JYRQ'].tolist()))
        date_list_new.sort()

        #get the stock price which will be used in calculating the MA price later
        stock_price=pd.DataFrame()

        for i in range(int(len(date_list_new)/10)+1):
            tempdate_list=date_list_new[i*10:(i+1)*10]
            if(len(tempdate_list)>0):
                stock_price=pd.concat([stock_price,
                                       self.get_stock_price(date_list=tempdate_list)],
                                      axis=0)

        stock_price['JYRQ'] = stock_price['JYRQ'].astype(str)
        stock_price.sort_values(['ZQDM', 'JYRQ'], inplace=True)
        stock_price.reset_index(drop=True,inplace=True)

        #calculate the average price for last 26,52weeks
        avgprice=stock_price.groupby('ZQDM').rolling(26)['SPJG'].mean().reset_index(drop=True).to_frame('26weeks_mean')
        avgprice['52weeks_mean']=stock_price.groupby('ZQDM').rolling(52)['SPJG'].mean().reset_index(drop=True)
        stock_price=pd.concat([stock_price,avgprice],axis=1)

        stock_price=stock_price.set_index('JYRQ')
        stock_price=stock_price.loc[date_list]
        stock_price=stock_price.reset_index(drop=False)


        sql="""
        select a.zqdm,b.yjxymc,b.yjxydm,b.ejxydm,b.ejxymc,b.xxfbrq from 
        st_ashare.t_st_ag_zqzb a left join 
        st_ashare.t_st_ag_gshyhfb b on a.gsdm=b.gsdm 
        where b.xyhfbz={0} and b.xxfbrq='20210730' """\
            .format(38)
        ind_map=hbdb.db2df(sql,db='alluser')
        stock_price=pd.merge(stock_price,ind_map,how='left',left_on='ZQDM',right_on='zqdm')

        stock_price.to_excel('hdb_stock_price_rawdata.xlsx',encoding='gbk')

        # outputdf = pd.DataFrame()
        #
        # for jjdm in new_jjdm_list:
        #     print(jjdm)
        #     hld_jj=hld[hld['jjdm']==jjdm]
        #
        #     key_hld=hld_jj[(hld_jj.groupby('jsrq').rank(ascending=False,method='min')<=10)['zjbl']]
        #
        #     a_date = list(hld_jj.index.unique()[[(x[4:6] == '06') | (x[4:6] == '12') for x in hld_jj.index.unique()]])
        #
        #     date_list=list(key_hld.index.unique())
        #     history_key_hld=pd.DataFrame()
        #     history_key_hld['zqdm']=key_hld.loc[date_list[0]]['zqdm']
        #     history_key_hld['in_date']=date_list[0]
        #     history_key_hld['out_date']=np.NAN
        #     history_key_hld.reset_index(drop=True,inplace=True)
        #     last_key_hld=history_key_hld
        #
        #     #find the date that jj get in and get out of the key holding
        #     for date in date_list[1:]:
        #         tempdf=key_hld.loc[date]
        #
        #         if(date in a_date):
        #             for zqdm in list(set(history_key_hld[history_key_hld['out_date'].isnull()]['zqdm']).
        #                                      difference(set(hld_jj.loc[date]['zqdm']))):
        #
        #                 history_key_hld.loc[(history_key_hld['zqdm'] == zqdm)&(history_key_hld['out_date'].isnull()),
        #                                     'out_date'] = date
        #
        #         new_adding_zq=pd.DataFrame()
        #         #get the zqdm that is entering the key holding for the first time
        #         new_adding_zq['zqdm']=list(set(tempdf['zqdm'])
        #                                    .difference(
        #             set(history_key_hld[history_key_hld['out_date'].isnull()]['zqdm'])
        #         )
        #         )
        #
        #         new_adding_zq['in_date']=date
        #         new_adding_zq['out_date'] = np.NAN
        #         history_key_hld=pd.concat([history_key_hld,new_adding_zq],axis=0)
        #         #edit the out date for zq leave the key holding
        #         for zqdm in list(set(last_key_hld[last_key_hld['out_date'].isnull()]['zqdm']).
        #                                  difference(set(tempdf['zqdm']))):
        #
        #             last_key_hld.loc[(last_key_hld['zqdm']==zqdm)&(last_key_hld['out_date'].isnull()),'out_date']=date
        #         #get the zq that entering the key holding while is not in the key holding last report date
        #         new_adding_zq = pd.DataFrame()
        #         new_adding_zq['zqdm']=list(set(tempdf['zqdm'])
        #                                     .difference(
        #              set(last_key_hld[last_key_hld['out_date'].isnull()]['zqdm'])
        #          )
        #          )
        #         new_adding_zq['in_date']=date
        #         new_adding_zq['out_date'] = np.NAN
        #         last_key_hld = pd.concat([last_key_hld, new_adding_zq], axis=0)
        #
        #     #from the in and out date, get the in and out price
        #     history_key_hld=pd.merge(history_key_hld,stock_price,how='left',
        #                              left_on=['zqdm','in_date'],right_on=['ZQDM','JYRQ'])\
        #         .drop(['ZQDM','JYRQ'],axis=1).rename(columns={'SPJG':'in_price',
        #                                                       '26weeks_mean':'26weeks_mean_in',
        #                                                       '52weeks_mean':'52weeks_mean_in'})
        #
        #     history_key_hld=pd.merge(history_key_hld,stock_price,how='left',
        #                              left_on=['zqdm','out_date'],right_on=['ZQDM','JYRQ'])\
        #         .drop(['ZQDM','JYRQ'],axis=1).rename(columns={'SPJG':'out_price',
        #                                                       '26weeks_mean':'26weeks_mean_out',
        #                                                       '52weeks_mean':'52weeks_mean_out'})
        #
        #
        #
        #
        #     history_key_hld['jjdm']=jjdm
        #     history_key_hld['asofdate'] = date
        #     history_key_hld['type']='all'
        #     outputdf=pd.concat([outputdf,history_key_hld],axis=0)
        #
        #
        #
        #
        #     last_key_hld = pd.merge(last_key_hld, stock_price, how='left',
        #                                left_on=['zqdm', 'in_date'], right_on=['ZQDM', 'JYRQ']) \
        #         .drop(['ZQDM','JYRQ'],axis=1).rename(columns={'SPJG':'in_price',
        #                                                       '26weeks_mean':'26weeks_mean_in',
        #                                                       '52weeks_mean':'52weeks_mean_in'})
        #
        #     last_key_hld = pd.merge(last_key_hld, stock_price, how='left',
        #                                left_on=['zqdm', 'out_date'], right_on=['ZQDM', 'JYRQ']) \
        #         .drop(['ZQDM','JYRQ'],axis=1).rename(columns={'SPJG':'out_price',
        #                                                       '26weeks_mean':'26weeks_mean_out',
        #                                                       '52weeks_mean':'52weeks_mean_out'})
        #
        #
        #
        #     last_key_hld['jjdm']=jjdm
        #     last_key_hld['asofdate'] = date
        #     last_key_hld['type']='key'
        #     outputdf=pd.concat([outputdf,last_key_hld],axis=0)
        #
        # #check if data already exist
        # sql="delete from hbs_stock_trading_data where asofdate='{}'".format(date)
        # localdb.execute(sql)
        #
        # outputdf.to_sql('hbs_stock_trading_data', con=localdb, index=False, if_exists='append')

    @staticmethod
    def get_holding_trading_analysis(asofdate):

        #get the saved trading data in the local db
        sql="select * from hbs_stock_trading_data where asofdate='{}'".format(asofdate)
        rawdata=pd.read_sql(sql,con=localdb)


        rawdata['left_flag_26']=(rawdata['in_price']<=rawdata['26weeks_mean_in'])
        rawdata['left_flag_52'] = (rawdata['in_price'] <= rawdata['52weeks_mean_in'])

        rawdata.loc[rawdata['left_flag_26'],'left_level_26']=rawdata[rawdata['left_flag_26']]['26weeks_mean_in']\
                                                             /rawdata[rawdata['left_flag_26']]['in_price']
        rawdata.loc[rawdata['left_flag_52'], 'left_level_52'] = rawdata[rawdata['left_flag_52']]['52weeks_mean_in'] \
                                                                / rawdata[rawdata['left_flag_52']]['in_price']

        rawdata['new_stock_flag'] = (rawdata['in_price'].notnull())&(rawdata['26weeks_mean_in'].isnull())
        rawdata['less_new_stock_flag'] = (rawdata['in_price'].notnull()) & (rawdata['26weeks_mean_in'].notnull())\
                                         & (rawdata['52weeks_mean_in'].isnull())

        jjdm_list=rawdata['jjdm'].unique().tolist()

        avg_holding_length_all = []
        avg_holding_length_key = []
        abs_return_all = []
        abs_return_key = []
        left_26_ratio_all=[]
        left_52_ratio_all=[]
        left_26_lv_all=[]
        left_52_lv_all=[]
        left_26_ratio_key=[]
        left_52_ratio_key=[]
        left_26_lv_key=[]
        left_52_lv_key=[]
        new_ratio_all=[]
        new_ratio_key=[]
        less_new_ratio_all=[]
        less_new_ratio_key=[]



        for jjdm in jjdm_list:


            history_key_hld=rawdata[(rawdata['jjdm']==jjdm)&(rawdata['type']=='all')]
            last_key_hld = rawdata[(rawdata['jjdm'] == jjdm) & (rawdata['type'] == 'key')]

            left_26_ratio_all.append(history_key_hld['left_flag_26'].sum()/len(history_key_hld))
            left_52_ratio_all.append(history_key_hld['left_flag_52'].sum() / len(history_key_hld))

            left_26_ratio_key.append(last_key_hld['left_flag_26'].sum()/len(last_key_hld))
            left_52_ratio_key.append(last_key_hld['left_flag_52'].sum() / len(last_key_hld))

            left_26_lv_all.append(history_key_hld['left_level_26'].mean() )
            left_52_lv_all.append(history_key_hld['left_flag_52'].mean())

            left_26_lv_key.append(last_key_hld['left_level_26'].mean())
            left_52_lv_key.append(last_key_hld['left_flag_52'].mean())

            new_ratio_all.append(history_key_hld['new_stock_flag'].sum()/len(history_key_hld))
            new_ratio_key.append(last_key_hld['less_new_stock_flag'].sum()/len(last_key_hld))
            less_new_ratio_all.append(history_key_hld['new_stock_flag'].sum()/len(history_key_hld))
            less_new_ratio_key .append(last_key_hld['less_new_stock_flag'].sum()/len(last_key_hld))

            tempdf = history_key_hld[history_key_hld['out_date'].notnull()]
            tempdf['out_date'] = [datetime.datetime.strptime(x, '%Y%m%d') for x in tempdf['out_date']]
            tempdf['in_date'] = [datetime.datetime.strptime(x, '%Y%m%d') for x in tempdf['in_date']]
            avg_holding_length_all.append(int(
                np.mean((tempdf['out_date'] - tempdf['in_date']).values / (3600 * 24 * 1000000000))))

            abs_return_all.append((history_key_hld['out_price']/history_key_hld['in_price']-1).mean())

            tempdf = last_key_hld[last_key_hld['out_date'].notnull()]
            tempdf['out_date'] = [datetime.datetime.strptime(x, '%Y%m%d') for x in tempdf['out_date']]
            tempdf['in_date'] = [datetime.datetime.strptime(x, '%Y%m%d') for x in tempdf['in_date']]
            avg_holding_length_key.append(int(
                np.mean((tempdf['out_date'] - tempdf['in_date']).values / (3600 * 24 * 1000000000))))

            abs_return_key.append((last_key_hld['out_price']/last_key_hld['in_price']-1).mean())


        outputdf=pd.DataFrame()
        outputdf['jjdm']=jjdm_list
        outputdf['平均持有时间（出重仓前）']=avg_holding_length_key
        outputdf['平均持有时间（出持仓前）'] = avg_holding_length_all
        outputdf['出重仓前平均收益率'] =abs_return_key
        outputdf['出全仓前平均收益率'] =abs_return_all

        outputdf['左侧概率（出重仓前,半年线）']=left_26_ratio_key
        outputdf['左侧概率（出持仓前,半年线）'] = left_26_ratio_all
        outputdf['左侧概率（出重仓前,年线）']=left_52_ratio_key
        outputdf['左侧概率（出持仓前,年线）'] = left_52_ratio_all

        outputdf['左侧程度（出重仓前,半年线）']=left_26_lv_key
        outputdf['左侧程度（出持仓前,半年线）'] = left_26_lv_all
        outputdf['左侧程度（出重仓前,年线）']=left_52_lv_key
        outputdf['左侧程度（出持仓前,年线）'] = left_52_lv_all


        outputdf['新股概率（出重仓前）']=new_ratio_key
        outputdf['新股概率（出持仓前）'] = new_ratio_all
        outputdf['次新股概率（出重仓前）'] = less_new_ratio_key
        outputdf['次新股概率（出持仓前）'] = less_new_ratio_all



        for col in ['平均持有时间（出重仓前）','平均持有时间（出持仓前）','出重仓前平均收益率','出全仓前平均收益率',
                    '左侧概率（出重仓前,半年线）','左侧概率（出持仓前,半年线）','左侧概率（出重仓前,年线）','左侧概率（出持仓前,年线）',
                    '新股概率（出重仓前）','新股概率（出持仓前）','次新股概率（出重仓前）','次新股概率（出持仓前）']:
            outputdf[col+"_rank"]=outputdf[col].rank(method='min')/len(outputdf)

        for col in ['左侧程度（出重仓前,半年线）','左侧程度（出持仓前,半年线）',
                    '左侧程度（出重仓前,年线）','左侧程度（出持仓前,年线）']:
            outputdf[col]=outputdf[col].rank(method='min')/len(outputdf)

        outputdf['asofdate'] = asofdate

        outputdf.to_sql('hbs_stock_trading_property',con=localdb,index=False,if_exists='append')

    def get_hld_property(self,jjdm_list,start_date,end_date,add=False):

        hld,new_jjdm_list=self.fund_holding_date_manufacture(jjdm_list, start_date, end_date)

        # full_hld=hld.loc[a_date]

        outputdf=pd.DataFrame()
        cen_lv_list=[]
        hhi_list=[]
        top10_list=[]
        top5_list = []
        top3_list = []
        avg_stock_num_list=[]
        avg_stock_weight=[]
        stock_weigth_hsl=[]
        pe_list=[]
        pb_list=[]
        roe_list=[]
        dividend_list=[]
        pe_m_list=[]
        pb_m_list=[]
        roe_m_list=[]
        dividend_m_list=[]
        asofdate=np.max(hld.index)


        for jjdm in new_jjdm_list:

            hld_jj=hld[hld['jjdm']==jjdm]

            a_date = list(hld_jj.index.unique()[[(x[4:6] == '06') | (x[4:6] == '12') for x in hld_jj.index.unique()]])

            full_hld = hld_jj.loc[a_date]

            #key_hld=hld_jj[(hld_jj.groupby('jsrq').rank(ascending=False,method='min')<=10)['zjbl']]
            hhi_lv=full_hld.groupby('jsrq')['zjbl'].apply(hhi_index).mean()
            cen_lv,top3w,top5w,top10w=self.stock_centralization_lv(hld_jj)
            avg_stock_num=full_hld.groupby('jsrq')['jjdm'].count().mean()

            top10_list.append(top10w)
            top5_list.append(top5w)
            top3_list.append(top3w)

            hhi_list.append(hhi_lv)
            cen_lv_list.append(cen_lv)
            avg_stock_num_list.append(avg_stock_num)

            gpzb=full_hld.groupby('jsrq').mean()['gptzzjb'].to_frame('zzjb')
            gpzb['diff'] = gpzb['zzjb'].diff().abs()
            gpzb['sum2'] = gpzb.rolling(2)['zzjb'].sum()
            avg_stock_weight.append(gpzb['zzjb'].mean())
            stock_weigth_hsl.append((gpzb['diff']/gpzb['sum2']).mean())

            financial_property=full_hld.groupby('jsrq').mean()[['pe','pb','roe','dividend']].mean()
            pe_list.append(financial_property['pe'])
            pb_list.append(financial_property['pb'])
            roe_list.append(financial_property['roe'])
            dividend_list.append(financial_property['dividend'])
            financial_property = full_hld.groupby('jsrq').mean()[['pe', 'pb', 'roe', 'dividend']].median()
            pe_m_list.append(financial_property['pe'])
            pb_m_list.append(financial_property['pb'])
            roe_m_list.append(financial_property['roe'])
            dividend_m_list.append(financial_property['dividend'])





        outputdf['jjdm']=new_jjdm_list
        outputdf['个股集中度']=cen_lv_list
        outputdf['hhi']=hhi_list
        outputdf['持股数量']=avg_stock_num_list
        outputdf['前三大'] = top3_list
        outputdf['前五大'] = top5_list
        outputdf['前十大'] = top10_list
        outputdf['平均仓位']=avg_stock_weight
        outputdf['仓位换手率'] = stock_weigth_hsl
        outputdf['PE'] = pe_list
        outputdf['PB'] = pb_list
        outputdf['ROE'] = roe_list
        outputdf['股息率'] = dividend_list
        outputdf['PE_中位数'] = pe_m_list
        outputdf['PB_中位数'] = pb_m_list
        outputdf['ROE_中位数'] = roe_m_list
        outputdf['股息率_中位数'] = dividend_m_list
        outputdf['asofdate']=asofdate


        outputdf[['个股集中度','hhi','仓位换手率']]=\
            outputdf[['个股集中度','hhi','仓位换手率']].rank(method='min')/len(outputdf)


        outputdf[[x+"_rank" for x in ['PE','PB','ROE','股息率','PE_中位数','PB_中位数','ROE_中位数','股息率_中位数']]]=\
            outputdf[['PE','PB','ROE','股息率','PE_中位数','PB_中位数','ROE_中位数','股息率_中位数']]\
                .rank(method='min')/len(outputdf)

        #check the same data has already exist
        sql="delete from hbs_holding_property where asofdate='{0}'"\
            .format(asofdate)
        localdb.execute(sql)

        #outputdf.to_csv('hbs_holding_property.csv',index=False,encoding='gbk')
        outputdf.to_sql('hbs_holding_property',con=localdb,index=False,if_exists='append')

        print('Done')

class Brinson_ability:

    def __init__(self):
        self.localengine=db_engine.PrvFunDB().engine
        self.hbdb=db_engine.HBDB()
        self.today=str(datetime.datetime.today().date())

    def rank_perc(self,ret_df):

        ret_col=ret_df.columns
        ret_df[ret_col] = ret_df[ret_col].rank(ascending=False)
        for col in ret_col:
            ret_df[col] = ret_df[col] / ret_df[col].max()

        return ret_df

    def get_brinson_data(self,asofdate):

        sql="select distinct tjrq from st_fund.r_st_hold_excess_attr_df where tjrq>='{0}' and tjrq<='{1}' "\
            .format(str(int(asofdate[0:4])-7)+'0101',asofdate)
        tjrq_list=self.hbdb.db2df(sql,db='funduser').sort_values('tjrq',ascending=False)['tjrq'].tolist()
        tjrq_list.sort()

        fin_df=pd.DataFrame(data=util.get_mutual_stock_funds(tjrq_list[-1]),columns=['jjdm'])

        ret_col = ['asset_allo', 'sector_allo', 'equity_selection', 'trading']
        for tjrq in tjrq_list:
            sql="""select jjdm,asset_allo,sector_allo,equity_selection,trading 
            from st_fund.r_st_hold_excess_attr_df where tjrq='{0}'""".format(tjrq)
            ret_df=self.hbdb.db2df(sql,db='funduser')

            for col in ret_col:

                ret_df.rename(columns={col: col + "_" + tjrq}, inplace=True)

            fin_df=pd.merge(fin_df,ret_df,how='left',on='jjdm')

        return  fin_df

    def brinson_rank(self,fin_df,threshold):

        outputdf = pd.DataFrame()
        outputdf['jjdm'] = fin_df.columns.tolist()

        for i in range(4):
            step = int(len(fin_df) / 4)
            tempdf = fin_df.iloc[i * step:(i + 1) * step]
            inputdf = pd.DataFrame()
            inputdf['jjdm'] = tempdf.columns.tolist()

            for j in range(1, 13):
                inputdf['{}month_ave_rank'.format(6 * j)] = self.rank_perc(tempdf.rolling(j).sum().T).T.mean().values

            short_term = inputdf.columns[1:7]
            long_term = inputdf.columns[7:13]

            new_col = 'short_term_{}'.format(tempdf.index[0].split('_')[0])
            inputdf[new_col] = 0
            inputdf.loc[(inputdf[short_term] <= threshold).sum(axis=1) >= 1, new_col] = 1

            new_col2 = 'long_term_{}'.format(tempdf.index[0].split('_')[0])
            inputdf[new_col2] = 0
            inputdf.loc[(inputdf[long_term] <= threshold).sum(axis=1) >= 1, new_col2] = 1

            outputdf = pd.merge(outputdf, inputdf[['jjdm', new_col, new_col2]], how='left', on='jjdm')

            return outputdf

    def target_fun_brinson(self,outputdf,iteration):

        target = outputdf[['short_term_trading', 'long_term_trading', 'short_term_sector',
                         'long_term_sector', 'short_term_equity', 'long_term_equity',
                         'short_term_asset', 'long_term_asset']].sum(axis=1)

        print('iteration {}'.format(iteration))
        print("ratio of multi label is {0}, ratio of null label is {1}".format(len(target[target > 1]) / len(target),
                                                                               len(target[target == 0]) / len(target)))
        print('sum of two ratio is {}'.format(len(target[target > 1]) / len(target) + len(target[target == 0]) / len(target)))

    def classify_threshold(self,iteration_num=100):

        fin_df=self.get_brinson_data()

        fin_df=fin_df.T.sort_index(ascending=False)
        fin_df.columns=fin_df.loc['jjdm']
        fin_df.drop('jjdm',axis=0,inplace=True)


        # for iteration in range(0,iteration_num):
        #
        #     threshold=0.01*(iteration+1)
        #
        #     outputdf=self.brinson_rank(fin_df,threshold)
        #
        #     self.target_fun_brinson(outputdf, iteration)

        inputdf=self.brinson_rank(fin_df,0.1)

        print('Done')

    def classify_socring(self,asofdate):

        fin_df=self.get_brinson_data(asofdate)

        asofdate=fin_df.columns[-1].split('_')[-1]

        fin_df=fin_df.T.sort_index()
        fin_df.columns=fin_df.loc['jjdm']
        fin_df.drop('jjdm',axis=0,inplace=True)

        outputdf = pd.DataFrame()
        outputdf['jjdm'] = fin_df.columns.tolist()

        for i in range(4):
            step = int(len(fin_df) / 4)
            tempdf = fin_df.iloc[i * step:(i + 1) * step]
            inputdf = pd.DataFrame()
            inputdf['jjdm'] = tempdf.columns.tolist()


            for j in [6,12]:
                inputdf['{}month_ave_rank'.format(6 * j)] = self.rank_perc(tempdf.rolling(j).sum().T).T.mean().values
            short_term = inputdf.columns[1]
            long_term = inputdf.columns[2]

            # for j in range(1, 13):
            #     inputdf['{}month_ave_rank'.format(6 * j)] = self.rank_perc(tempdf.rolling(j).sum().T).T.mean().values
            #
            # short_term = inputdf.columns[1:7]
            # long_term = inputdf.columns[7:13]

            inputdf=inputdf[inputdf.mean(axis=1).notnull()]


            # new_col = 'short_term_{}'.format(tempdf.index[0].split('_')[0])
            # inputdf[new_col] = 10-(inputdf[short_term].mean(axis=1)*10).astype(int)
            #
            # new_col2 = 'long_term_{}'.format(tempdf.index[0].split('_')[0])
            # inputdf[new_col2] =10- (inputdf[long_term].mean(axis=1)*10).fillna(0).astype(int)


            new_col = 'short_term_{}'.format(tempdf.index[0].split('_')[0])
            inputdf[new_col] = 10-(inputdf[short_term]*10).astype(int)

            new_col2 = 'long_term_{}'.format(tempdf.index[0].split('_')[0])
            inputdf[new_col2] =10- (inputdf[long_term]*10).fillna(0).astype(int)

            outputdf = pd.merge(outputdf, inputdf[['jjdm', new_col, new_col2]], how='left', on='jjdm')

        outputdf['asofdate']=asofdate

        #check if data already exist
        sql='select distinct asofdate from brinson_score'
        date_list=pd.read_sql(sql,con=self.localengine)['asofdate'].tolist()
        if(asofdate in date_list):
            sql="delete from brinson_score where asofdate='{}'".format(asofdate)
            self.localengine.execute(sql)


        #check if data already exist
        sql="delete from brinson_score where asofdate='{0}'".format(asofdate)
        localdb.execute(sql)

        outputdf.to_sql('brinson_score',con=self.localengine,index=False,if_exists='append')

    def brinson_score_pic(self,jjdm,asofdate):

        sql="select * from brinson_score where jjdm='{0}' and asofdate='{1}'".format(jjdm,asofdate)
        scoredf=pd.read_sql(sql,con=self.localengine)
        plot=functionality.Plot(fig_width=1000,fig_height=600)

        new_name=['jjdm','交易能力_短期','交易能力_长期','行业配置能力_短期',
                  '行业配置能力_长期','选股能力_短期','选股能力_长期','大类资产配置能力_短期',
                  '大类资产配置能力_长期','asofdate']
        scoredf.columns=new_name
        col=['交易能力_短期','交易能力_长期','行业配置能力_短期',
                  '行业配置能力_长期','选股能力_短期','选股能力_长期','大类资产配置能力_短期',
                  '大类资产配置能力_长期']

        plot.ploty_polar(scoredf[col],'Brinson能力图')

    @staticmethod
    def factorlize_brinson(factor_name):

        sql="select jjdm,{0},asofdate from brinson_score".format(factor_name)
        raw_df=pd.read_sql(sql,con=localdb)
        raw_df.rename(columns={'asofdate':'date'},inplace=True)

        return  raw_df

class Barra_analysis:

    def __init__(self):
        self.localengine=db_engine.PrvFunDB().engine
        self.hbdb=db_engine.HBDB()
        self.barra_col=['size','beta','momentum','resvol','btop','sizenl','liquidity','earnyield','growth','leverage']
        self.indus_col=['aerodef','agriforest','auto','bank','builddeco','chem','conmat','commetrade','computer','conglomerates','eleceqp','electronics',
        'foodbever','health','houseapp','ironsteel','leiservice','lightindus','machiequip','media','mining','nonbankfinan','nonfermetal',
        'realestate','telecom','textile','transportation','utilities']
        chinese_name=['国防军工','农林牧渔','汽车','银行','建筑装饰','化工','建筑材料','商业贸易','计算机','综合','电气设备',
                      '电子','食品饮料','医药生物','家用电器','钢铁','休闲服务','轻工制造','机械设备','传媒','采掘','非银金融',
                      '有色金属','房地产','通信','纺织服装','交通运输','公用事业']
        self.industry_name_map=dict(zip(chinese_name,self.indus_col))

        self.industry_name_map_e2c = dict(zip(self.indus_col,chinese_name))

        self.style_trans_map=dict(zip(self.barra_col,['市值','市场','动量','波动率','价值','非线性市值','流动性','盈利','成长','杠杆',]))

        self.ability_trans=dict(zip(['stock_alpha_ret_adj', 'trading_ret', 'industry_ret_adj',
       'unexplained_ret', 'barra_ret_adj'],['股票配置','交易','行业配置','不可解释','风格配置']))

    def read_barra_fromdb(self,date_sql_con,tickerlist):

        # date_list=[''.join(x.split('-')) for x in date_list.astype(str)]
        # date_con="'"+"','".join(date_list)+"'"
        ticker_con="'"+"','".join(tickerlist)+"'"

        sql="""
        select ticker,trade_date,size,beta,momentum,resvol,btop,sizenl,liquidity,earnyield,growth,leverage,
        aerodef,agriforest,auto,bank,builddeco,chem,conmat,commetrade,computer,conglomerates,eleceqp,electronics,
        foodbever,health,houseapp,ironsteel,leiservice,lightindus,machiequip,media,mining,nonbankfinan,nonfermetal,
        realestate,telecom,textile,transportation,utilities 
        from st_ashare.r_st_barra_style_factor where trade_date in ({0}) and ticker in ({1})
        """.format(date_sql_con,ticker_con)
        expdf=self.hbdb.db2df(sql,db='alluser')

        fac_ret_df=pd.DataFrame()
        date_list=date_sql_con.split(',')
        date_list.sort()
        new_date=date_list[-1].replace("'","")
        new_date = datetime.datetime.strptime(new_date, '%Y%m%d')
        new_date = (new_date +datetime.timedelta(days=30)).strftime('%Y%m%d')
        date_list.append(new_date)
        for i in range(len(date_list)-1):
            t0=date_list[i]
            t1=date_list[i+1]
            sql="select factor_name,factor_ret,trade_date from st_ashare.r_st_barra_factor_return where trade_date>={0} and trade_date<{1} "\
                .format(t0,t1)
            temp=self.hbdb.db2df(sql,db='alluser')
            temp['factor_ret']=temp['factor_ret']+1
            temp=temp.groupby('factor_name').prod()
            temp['factor_ret'] = temp['factor_ret'] -1
            temp.reset_index(drop=False,inplace=True)
            temp['trade_date']=t0.replace("'","")
            fac_ret_df=pd.concat([fac_ret_df,temp],axis=0)


        return expdf,fac_ret_df

    def read_anon_fromdb(self,date_list,tickerlist):

        # date_list=[''.join(x.split('-')) for x in date_list.astype(str)]
        ticker_con="'"+"','".join(tickerlist)+"'"
        date_list.sort()
        outputdf=pd.DataFrame()
        for i in range(len(date_list)-1):
            t0=date_list[i]
            t1=date_list[i+1]
            sql=""" select ticker,trade_date,s_ret from st_ashare.r_st_barra_specific_return where ticker in ({0})
            and trade_date >='{1}' and trade_date<'{2}'
            """.format(ticker_con,t0,t1)

            anon_ret=self.hbdb.db2df(sql,db='alluser')
            anon_ret['s_ret']=1+anon_ret['s_ret']
            temp=anon_ret.groupby('ticker').prod()
            temp['s_ret']=temp['s_ret']-1
            temp['trade_date']=t0
            temp.reset_index(drop=False,inplace=True)
            outputdf=pd.concat([outputdf,temp],axis=0)

        return outputdf

    def read_hld_fromdb(self,start_date,end_date,jjdm):

        sql="""select jsrq,zqdm,zjbl from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq>='{1}' and jsrq<='{2}'
        """.format(jjdm,start_date,end_date)
        hld=self.hbdb.db2df(sql,db='funduser')
        hld['jsrq']=hld['jsrq'].astype(str)
        return hld

    def smooth_hld(self,hld,date_list_orgi,weight_col,date_col,code_col):

        date_list=date_list_orgi.copy()
        smoothed_hld=pd.DataFrame()
        ext_zqdm=[]
        ext_date=[]
        ext_zjbl=[]

        for i in range(len(date_list)-1):
            q0=date_list[i]
            q1=date_list[i+1]

            sql = """
            select distinct(trade_date)
            from st_ashare.r_st_barra_style_factor where trade_date>'{0}' and trade_date<'{1}'
            """.format(q0, q1)


            ext_date_list = self.hbdb.db2df(sql, db='alluser')
            ext_date_list['yeatmonth'] = [x[0:6] for x in ext_date_list['trade_date']]


            ext_date_list.drop(ext_date_list[ext_date_list['yeatmonth']==q1[0:6]].index,axis=0,inplace=True)

            ext_date_list=ext_date_list.drop_duplicates('yeatmonth', keep='last')['trade_date'].to_list()

            tempdf=pd.merge(hld[hld[date_col]==q0].drop_duplicates([code_col],keep='first')
                            ,hld[hld[date_col]==q1].drop_duplicates([code_col],keep='first'),
                            how='outer',on=code_col).fillna(0)
            tempdf['shift_rate']=(tempdf[weight_col+'_y']-tempdf[weight_col+'_x'])/(len(ext_date_list)+1)
            zqdm=tempdf[code_col].unique().tolist()
            zq_amt=len(zqdm)
            ini_zjbl=tempdf[weight_col+'_x'].tolist()

            for j  in range(len(ext_date_list)):
                ext_date+=[ext_date_list[j]]*zq_amt
                ext_zjbl+=(np.array(ini_zjbl)+np.array((tempdf['shift_rate']*(j+1)).tolist())).tolist()
                ext_zqdm+=zqdm

        smoothed_hld[weight_col]=ext_zjbl
        smoothed_hld[date_col] = ext_date
        smoothed_hld[code_col] = ext_zqdm

        hld=pd.concat([hld,smoothed_hld],axis=0)
        return hld

    def read_hld_ind_fromdb(self,start_date,end_date,jjdm):

        sql = """select jsrq,fldm,zzjbl from st_fund.t_st_gm_gpzhhytj where jjdm='{0}' and jsrq>='{1}' and jsrq<='{2}' and hyhfbz='2'
        """.format(jjdm, start_date, end_date)
        hld = self.hbdb.db2df(sql, db='funduser')
        hld['jsrq'] = hld['jsrq'].astype(str)

        sql="select fldm,flmc from st_market.t_st_zs_hyzsdmdyb where hyhfbz='2'"
        industry_map=self.hbdb.db2df(sql,db='alluser')

        hld=pd.merge(hld,industry_map,how='left',on='fldm')
        hld.drop(hld[hld['flmc'].isnull()].index,axis=0,inplace=True)
        hld['flmc']=[ self.industry_name_map[x] for x in hld['flmc']]

        hld.loc[hld['zzjbl']==99999,'zzjbl']=0
        hld['zzjbl']=hld['zzjbl']/100

        return hld

    def read_hld_ind_fromstock(self,hld,tickerlist,hfbz=24):

        ticker_con="'"+"','".join(tickerlist)+"'"

        sql="select a.zqdm,b.yjxymc,b.xxfbrq from st_ashare.t_st_ag_zqzb a left join st_ashare.t_st_ag_gshyhfb b on a.gsdm=b.gsdm where a.zqdm in ({0}) and b.xyhfbz={1} "\
            .format(ticker_con,hfbz)
        ind_map=self.hbdb.db2df(sql,db='alluser')
        ind_map.sort_values(['zqdm','xxfbrq'],inplace=True)
        temp=ind_map['zqdm']
        temp.drop_duplicates(keep='last', inplace=True)
        ind_map=ind_map.loc[temp.index][['zqdm','yjxymc']]

        ind_hld=pd.merge(hld,ind_map,how='left',on='zqdm')

        ind_hld=ind_hld.groupby(['jsrq', 'yjxymc'], as_index=False).sum()
        ind_hld.rename(columns={'yjxymc': 'flmc', 'zjbl': 'zzjbl'}, inplace=True)
        ind_hld['fldm']=''
        ind_hld['flmc']=[self.industry_name_map[x] for x in ind_hld['flmc']]
        ind_hld['zzjbl']=ind_hld['zzjbl']/100

        return ind_hld[['fldm','zzjbl', 'jsrq','flmc']]

    def weight_times_exp(self,fund_exp,col_list):

        for col in col_list:
            fund_exp[col]=fund_exp[col]*fund_exp['zjbl']

        return  fund_exp

    def _shift_date(self,date):
        trade_dt = datetime.datetime.strptime(date, '%Y%m%d')
        pre_date = (trade_dt -datetime.timedelta(days=30)).strftime('%Y%m%d')

        sql_script = "SELECT JYRQ, SFJJ, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            pre_date,date)
        df=self.hbdb.db2df(sql_script,db='readonly')
        df=df.rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                      "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        trading_day_list = df[df['isOpen'] == 1]['calendarDate'].tolist()

        return trading_day_list[-1]

    def stock_price(self,date_sql_con,tickerlist):

        # date_list=[''.join(x.split('-')) for x in date_list.astype(str)]
        ticker_con="'"+"','".join(tickerlist)+"'"

        sql="""
        select ZQDM,JYRQ,DRJJ from FUNDDB.ZGJY where ZQDM in ({0}) and JYRQ in ({1})
         """.format(ticker_con,date_sql_con)

        stock_price=self.hbdb.db2df(sql,db='readonly')

        jyrq_list=stock_price['JYRQ'].unique().tolist()
        jyrq_list.sort()
        right_df=pd.DataFrame()
        for i in range(0,len(jyrq_list)-1):
            tempdf=pd.merge(stock_price[stock_price['JYRQ']==jyrq_list[i]][['ZQDM','JYRQ','DRJJ']]
                            ,stock_price[stock_price['JYRQ']==jyrq_list[i+1]][['ZQDM','DRJJ']]
                            ,how='inner',on='ZQDM')
            tempdf['hld_ret']=tempdf['DRJJ_y']/tempdf['DRJJ_x']-1
            right_df=pd.concat([right_df,tempdf[['ZQDM','JYRQ','hld_ret']]])

        #stock_price['hld_ret']=stock_price['SPJG']/stock_price['QSPJ']-1
        stock_price=pd.merge(stock_price,right_df,how='left',on=['ZQDM','JYRQ'])

        return stock_price

    @staticmethod
    def hld_compenzation(hlddf,fund_allocation):

        q_date=hlddf.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in hlddf['jsrq']]]['jsrq'].unique().tolist()
        a_date=hlddf.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in hlddf['jsrq']]]['jsrq'].unique().tolist()
        q_list=hlddf['jsrq'].unique().tolist()
        q_list.sort()

        hld_H=pd.DataFrame()
        hld_L = pd.DataFrame()
        #get heavy hld for annual and half_annual report
        for date in a_date:
            hld_H=pd.concat([hld_H,hlddf[hlddf['jsrq']==date].sort_values('zjbl')[-10:].reset_index(drop=True)],axis=0)
            hld_L=pd.concat([hld_L,hlddf[hlddf['jsrq']==date].sort_values('zjbl')[0:-10].reset_index(drop=True)],axis=0)
        for date in q_date:
            hld_H=pd.concat([hld_H,hlddf[hlddf['jsrq']==date]],axis=0)


        for i in range(len(q_list)):
            t1=q_list[i]
            if((i>0) and (t1[4:6] == '03') or  (t1[4:6] == '09')):
                t0=q_list[i-1]
            else:
                continue
            #calculate the no hevay hld for quarter report data by the mean of two annaul data if next annaul report exists
            if(i!=len(q_list)-1):
                t2=q_list[i+1]
                temp=pd.merge(hlddf[hlddf['jsrq']==t0].sort_values('zjbl')[0:-10],
                              hlddf[hlddf['jsrq']==t2].sort_values('zjbl')[0:-10],
                              how='outer',on='zqdm').fillna(0)
                temp.set_index('zqdm',inplace=True)
                if(len(temp)==0):
                    continue
                drop_list=list(set(temp.index).intersection( set(hlddf[hlddf['jsrq']==t1]['zqdm'])))
                temp.drop(drop_list,axis=0,inplace=True)
                temp['zjbl']=(temp['zjbl_x']+temp['zjbl_y'])/2
                temp['zjbl']=temp['zjbl']*((fund_allocation[fund_allocation['jsrq'] == t1]['gptzzjb']*100-hld_H[hld_H['jsrq']==t1]['zjbl'].sum()).values[0]/temp['zjbl'].sum())
                temp['jsrq']=t1
                temp.reset_index(drop=False,inplace=True)
                hld_L=pd.concat([hld_L,temp[['zjbl','jsrq','zqdm']]],axis=0)

            else:
                temp=hlddf[hlddf['jsrq']==t0].sort_values('zjbl')[0:-10]
                temp['zjbl']=temp['zjbl']/temp['zjbl'].sum()
                temp['zjbl']=temp['zjbl']*(fund_allocation[fund_allocation['jsrq'] == t1]['gptzzjb']*100-hld_H[hld_H['jsrq']==t1]['zjbl'].sum()).values[0]
                temp['jsrq']=t1
                temp.reset_index(drop=False,inplace=True)
                hld_L=pd.concat([hld_L,temp[['zjbl','jsrq','zqdm']]],axis=0)
        return pd.concat([hld_H,hld_L],axis=0).sort_values('jsrq').reset_index(drop=True)

    def save_barra_ret2db(self,jjdm,start_date,end_date,add=False,hld_compenzation=False):

        #read holding info
        hld=self.read_hld_fromdb(start_date,end_date,jjdm)
        #remove HK stock
        tickerlist=hld['zqdm'][~hld['zqdm'].dropna().str.contains('H')].unique()
        #shift the report date to trading date
        org_date_list=hld['jsrq'].unique().tolist()
        date_list = [self._shift_date(x) for x in org_date_list]
        date_map=dict(zip(org_date_list,date_list))
        changed_date=set(org_date_list).difference(set(date_list))

        #get fund asset allocation info
        fund_allocation = self.fund_asset_allocation(jjdm, org_date_list)

        #hld compenzation if necessary
        if(hld_compenzation):
            hld = self.hld_compenzation(hld,fund_allocation)
            table_sur='barra_style_hldcom_'
            hld_industry = self.read_hld_ind_fromstock(hld,tickerlist)
        else:
            table_sur='barra_style_'
            hld_industry = self.read_hld_ind_fromdb(start_date, end_date, jjdm)

        #transfor report date to trading date
        for date in changed_date:
            hld.loc[hld['jsrq']==date,'jsrq']=date_map[date]
            hld_industry.loc[hld_industry['jsrq'] == date, 'jsrq'] = date_map[date]
            fund_allocation.loc[fund_allocation['jsrq'] == date, 'jsrq'] = date_map[date]

        #hld smoothing
        hld=self.smooth_hld(hld,date_list,weight_col='zjbl',date_col='jsrq',code_col='zqdm')
        hld_industry=self.smooth_hld(hld_industry[['zzjbl','jsrq','flmc']],date_list,weight_col='zzjbl',date_col='jsrq',code_col='flmc')
        fund_allocation = self.smooth_hld(fund_allocation, date_list, weight_col='gptzzjb', date_col='jsrq',
                                          code_col='jjdm')
        date_sql_con="'"+"','".join(hld['jsrq'].unique().tolist())+"'"

        #read barra exposure and return info
        expdf, fac_ret_df=self.read_barra_fromdb(date_sql_con,tickerlist)
        #read the stock price for each
        stock_df = self.stock_price(date_sql_con, tickerlist)
        #read the special return for each stock
        anno_df=self.read_anon_fromdb(hld['jsrq'].unique().tolist(),tickerlist)

        fund_exp=pd.merge(hld,expdf[['ticker','trade_date']+self.barra_col],
                          how='inner',left_on=['zqdm','jsrq'],
                          right_on=['ticker','trade_date']).drop(['ticker', 'trade_date'],axis=1)

        fund_exp=pd.merge(fund_exp, stock_df[['ZQDM', 'JYRQ', 'hld_ret']], how='inner', left_on=['zqdm', 'jsrq'],
                 right_on=['ZQDM', 'JYRQ']).drop(['ZQDM','JYRQ'],axis=1)

        fund_exp=pd.merge(fund_exp, anno_df, how='left', left_on=['zqdm', 'jsrq'],
                 right_on=['ticker', 'trade_date']).drop(['ticker', 'trade_date'],axis=1)

        fund_exp=self.weight_times_exp(fund_exp,self.barra_col+['hld_ret','s_ret'])

        fund_exp.drop(['zqdm'],axis=1,inplace=True)

        fund_exp=fund_exp.groupby(by='jsrq').sum()/100

        hld_ret=fund_exp[['zjbl','hld_ret']]
        s_ret=fund_exp[['zjbl','s_ret']]

        fund_exp.drop(['hld_ret','s_ret'],axis=1,inplace=True)
        fund_exp=fund_exp.T

        indus_exp = pd.DataFrame()
        indus_exp['industry'] = self.indus_col

        for date in hld_industry['jsrq'].unique():
            indus_exp=pd.merge(indus_exp,hld_industry[hld_industry['jsrq']==date][['zzjbl','flmc','jsrq']]
                               ,how='left',left_on='industry',right_on='flmc').drop(['flmc','jsrq'],axis=1).fillna(0)
            indus_exp.rename(columns={'zzjbl':date},inplace=True)

        for date in fac_ret_df['trade_date'].unique():

            tempdf=fac_ret_df[fac_ret_df['trade_date']==date][['factor_ret','factor_name']].T
            tempdf.columns = [x.lower() for x in  tempdf.loc['factor_name']]

            # indus_exp=pd.merge(indus_exp,hld_industry[hld_industry['jsrq']==date][['zzjbl','flmc','jsrq']]
            #                    ,how='left',left_on='industry',right_on='flmc').drop(['flmc','jsrq'],axis=1).fillna(0)
            # indus_exp.rename(columns={'zzjbl':date},inplace=True)
            fund_exp[date+'_ret']=fund_exp[date].values*np.append([1],tempdf[self.barra_col].loc['factor_ret'].values)
            indus_exp[date+'_ret']=indus_exp[date].values*tempdf[self.indus_col].loc['factor_ret'].values

        fund_exp=fund_exp.T
        indus_exp.set_index(['industry'], inplace=True)
        indus_exp=indus_exp.T

        fund_exp['total_bar']=fund_exp[self.barra_col].sum(axis=1)
        indus_exp['total_ind'] = indus_exp[self.indus_col].sum(axis=1)

        fund_exp['index']=fund_exp.index
        indus_exp['index'] = indus_exp.index
        fund_exp['jjrq']=[x.split('_')[0] for x in fund_exp['index']]
        indus_exp['jjrq'] = [x.split('_')[0] for x in indus_exp['index']]
        hld_ret['jjrq'] = hld_ret.index
        s_ret['jjrq'] = s_ret.index
        for df in [fund_exp,indus_exp,hld_ret,s_ret]:
            df['jjdm']=jjdm

        fund_allocation=pd.merge(s_ret['jjrq'],fund_allocation,how='left',left_on='jjrq',
                                 right_on='jsrq').drop('jjrq',axis=1)

        if(not add):
            sql="select distinct jjrq from {1}hld_ret where jjdm='{0}'".format(jjdm,table_sur)
            date_list=pd.read_sql(sql,con=self.localengine)['jjrq']
            common_date=list(set(date_list).intersection(set(fund_allocation['jsrq'] )))
            date_con="'"+"','".join(common_date)+"'"

            sql="delete from {2}fund_exp where jjdm='{0}' and jjrq in ({1})".format(jjdm,date_con,table_sur)
            self.localengine.execute(sql)
            sql="delete from {2}indus_exp where jjdm='{0}' and jjrq in ({1})".format(jjdm,date_con,table_sur)
            self.localengine.execute(sql)
            sql="delete from {2}hld_ret where jjdm='{0}' and jjrq in ({1})".format(jjdm,date_con,table_sur)
            self.localengine.execute(sql)
            sql="delete from {2}s_ret where jjdm='{0}' and jjrq in ({1})".format(jjdm,date_con,table_sur)
            self.localengine.execute(sql)
            sql = "delete from {2}fund_allocation where jjdm='{0}' and jsrq in ({1})".format(jjdm, date_con,table_sur)
            self.localengine.execute(sql)

        fund_exp.to_sql(table_sur+'fund_exp',con=self.localengine,index=False,if_exists='append')
        indus_exp.to_sql(table_sur+'indus_exp', con=self.localengine,index=False,if_exists='append')
        hld_ret.to_sql(table_sur+'hld_ret', con=self.localengine,index=False,if_exists='append')
        s_ret.to_sql(table_sur+'s_ret', con=self.localengine,index=False,if_exists='append')
        fund_allocation.to_sql(table_sur+'fund_allocation', con=self.localengine,index=False,if_exists='append')

        #print('{0} data for {1} to {2} has been saved in local db'.format(jjdm,start_date,end_date))

    def read_barra_retfromdb(self,jjdm,start_date,end_date,hld_com):

        if(hld_com):
            surname='barra_style_hldcom_'
        else:
            surname='barra_style_'

        sql="select * from {3}fund_exp where jjdm='{0}' and jjrq>='{1}' and jjrq<='{2}'"\
            .format(jjdm,start_date,end_date,surname)
        fund_exp=pd.read_sql(sql,con=self.localengine).drop(['jjdm','jjrq'],axis=1)
        fund_exp.set_index('index',drop=True,inplace=True)

        sql="select * from {3}indus_exp where jjdm='{0}' and jjrq>='{1}' and jjrq<='{2}'"\
            .format(jjdm,start_date,end_date,surname)
        indus_exp=pd.read_sql(sql,con=self.localengine).drop(['jjdm','jjrq'],axis=1)
        indus_exp.set_index('index', drop=True,inplace=True)

        sql="select * from {3}hld_ret where jjdm='{0}' and jjrq>='{1}' and jjrq<='{2}'"\
            .format(jjdm,start_date,end_date,surname)
        hld_ret=pd.read_sql(sql,con=self.localengine).drop(['jjdm'],axis=1)
        hld_ret.set_index('jjrq', drop=True,inplace=True)

        sql="select * from {3}s_ret where jjdm='{0}' and jjrq>='{1}' and jjrq<='{2}'"\
            .format(jjdm,start_date,end_date,surname)
        s_ret=pd.read_sql(sql,con=self.localengine).drop(['jjdm'],axis=1)
        s_ret.set_index('jjrq', drop=True,inplace=True)

        sql="select * from {3}fund_allocation where jjdm='{0}' and jsrq>='{1}' and jsrq<='{2}'"\
            .format(jjdm,start_date,end_date,surname)
        fund_allocation=pd.read_sql(sql,con=self.localengine).drop(['jjdm'],axis=1)

        sql="""select jsrq from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq>='{1}' and jsrq<='{2}'
        """.format(jjdm,start_date,end_date)
        hld=self.hbdb.db2df(sql,db='funduser')
        hld['jsrq']=hld['jsrq'].astype(str)

        date_list=hld['jsrq'].unique().tolist()

        return fund_exp, indus_exp, hld_ret, s_ret, date_list,fund_allocation

    def fund_nv(self,jjdm,date_list):

        date_con="'"+"','".join(date_list)+"'"

        sql="""
        select jzrq,zbnp from st_fund.t_st_gm_rqjhb where jjdm='{0}' and zblb='2101'
        and jzrq in ({1})
        """.format(jjdm,date_con)

        fundnv=self.hbdb.db2df(sql,db='funduser')
        fundnv.rename(columns={'zbnp':'hbdr'},inplace=True)
        fundnv['jzrq']=fundnv['jzrq'].astype(str)
        fundnv['hbdr']=fundnv['hbdr']/100

        return fundnv

    def fund_asset_allocation(self,jjdm,date_list):

        sql="select jjdm,jsrq,jjzzc,gptzzjb from st_fund.t_st_gm_zcpz where jjdm='{2}' and jsrq>='{0}' and jsrq<='{1}'"\
            .format(date_list[0],date_list[-1],jjdm)
        fund_allocation=self.hbdb.db2df(sql,db='funduser')
        fund_allocation['gptzzjb']=fund_allocation['gptzzjb']/100
        fund_allocation['jsrq']=fund_allocation['jsrq'].astype(str)
        return fund_allocation

    def ret_div(self,jjdm,start_date,end_date,hld_com):

        fund_exp,indus_exp,hld_ret,s_ret,date_list,fund_allocation=self.read_barra_retfromdb(jjdm,start_date,end_date,hld_com)

        fundnv=self.fund_nv(jjdm,hld_ret.index.tolist())
        hld_ret['jzrq']=hld_ret.index
        hld_ret=pd.merge(hld_ret,fundnv,how='left',on='jzrq')

        barra_ret=fund_exp.loc[[x+'_ret' for x in hld_ret['jzrq'][0:-1]]][self.barra_col+['total_bar']].reset_index(drop=True)
        barra_exp=fund_exp.loc[hld_ret['jzrq']][self.barra_col+['total_bar']].reset_index(drop=True)
        barra_exp.columns=[x+'_exp' for x in barra_exp.columns]

        ind_ret = indus_exp.loc[[x + '_ret' for x in hld_ret['jzrq'][0:-1]]].reset_index(
            drop=True)
        ind_exp = indus_exp.loc[hld_ret['jzrq']].reset_index(drop=True)
        ind_exp.columns = [x + '_exp' for x in ind_exp.columns]

        s_ret=s_ret['s_ret'].reset_index(drop=True)
        ouputdf=pd.concat([hld_ret,barra_ret,barra_exp,ind_ret,ind_exp,s_ret],axis=1)

        columns=['zjbl', 'hld_ret', 'jzrq', 'hbdr', 'total_bar', 'total_bar_exp', 's_ret','total_ind']

        new_names=['published_stock_weight','hld_based_ret','date','nv_ret','barra_ret','barra_exp','stock_alpha_ret','industry_ret']

        ouputdf.rename(columns=dict(zip(columns,new_names)),inplace=True)

        ouputdf=pd.merge(ouputdf,fund_allocation,how='left',left_on='date',right_on='jsrq').drop('jsrq',axis=1)

        for col in self.barra_col+self.indus_col:
            ouputdf[col+"_adj"]=ouputdf[col]/ouputdf['published_stock_weight']*ouputdf['gptzzjb']
            ouputdf[col + "_exp_adj"] = ouputdf[col+"_exp"] / ouputdf['published_stock_weight'] * ouputdf['gptzzjb']

        ouputdf.set_index('date',drop=True,inplace=True)

        return  ouputdf,date_list

    def date_trans(self,date_list,inputlist):

        missing_date=set(inputlist).difference(set(date_list))
        available_list=list(set(inputlist).difference(set(missing_date)))
        new_list = []
        if(len(missing_date)>0):
            for date in missing_date:
                diff=abs(date_list.astype(int)-int(date)).min()
                new_list.append(date_list[abs(date_list.astype(int)-int(date))==diff][0])
        available_list+=new_list
        available_list.sort()
        return  available_list

    def cul_ret(self,weight,ret):

        cul_ret=1
        for i in range(len(weight)):
            cul_ret*=weight[i]*(ret[i]+1)

        return cul_ret

    def style_change_detect_engine(self,q_df,diff1,diff2,q_list,col_list,t1,t2):

        style_change=[]

        for col in col_list:

            potential_date=diff2[diff2[col]<=-1*t1].index.to_list()
            last_added_date=q_list[-1]
            for date in potential_date:
                if(diff1.loc[q_df.index[q_df.index<=date][-3]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-3]
                elif(diff1.loc[q_df.index[q_df.index<=date][-2]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-2]
                elif(diff1.loc[q_df.index[q_df.index<=date][-1]][col]<=-1*t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if((q_list.index(added_date)-q_list.index(last_added_date)<=2
                        and q_list.index(added_date)-q_list.index(last_added_date)>0) or added_date==q_list[-1]):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

            potential_date = diff2[diff2[col] >= t1].index.to_list()
            last_added_date = q_list[-1]
            for date in potential_date:
                if (diff1.loc[q_df.index[q_df.index <= date][-3]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-3]
                elif (diff1.loc[q_df.index[q_df.index <= date][-2]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-2]
                elif (diff1.loc[q_df.index[q_df.index <= date][-1]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if (q_list.index(added_date) - q_list.index(last_added_date) <= 2
                        and q_list.index(added_date) - q_list.index(last_added_date) > 0):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

        return style_change

    def style_change_detect_engine2(self, q_df, diff1, col_list, t1, t2):

        style_change=[]
        t3=t2/2

        for col in col_list:

            tempdf=pd.merge(q_df[col],diff1[col],how='left',on='date')
            tempdf['style']=''
            style_num=0
            tempdf['style'].iloc[0:2] = style_num

            for i in range(2,len(tempdf)-1):
                if(tempdf[col+'_y'].iloc[i]>t1 and tempdf[col+'_y'].iloc[i+1]>-1*t3 ):
                    style_num+=1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_x'].iloc[i]-tempdf[tempdf['style']==style_num][col+'_x'][0]>t1 and
                     tempdf[col+'_y'].iloc[i]>t2 and tempdf[col+'_y'].iloc[i+1]>-1*t3):
                    style_num += 1
                    added_date=tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_y'].iloc[i]<-1*t1 and tempdf[col+'_y'].iloc[i+1]<t3 ):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif (tempdf[col + '_x'].iloc[i] - tempdf[tempdf['style'] == style_num][col + '_x'][0] < -1*t1 and
                      tempdf[col + '_y'].iloc[i] < -1*t2 and tempdf[col + '_y'].iloc[i + 1] <  t3):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)

                tempdf['style'].iloc[i] = style_num

        return style_change

    def style_change_detect(self,df,q_list,col_list,t1,t2):

        q_list.sort()
        q_df = df.loc[q_list]
        diff1=q_df.diff(1)
        # diff2=q_df.rolling(3).mean().diff(2)
        # diff4 = q_df.rolling(3).mean().diff(4)

        # style_change_short=self.style_change_detect_engine(q_df,diff1,diff2,q_list,col_list,t1,t2)
        # style_change_long=self.style_change_detect_engine(q_df,diff1,diff4,q_list,col_list,t1,t2)
        # style_change=style_change_short+style_change_long

        style_change = self.style_change_detect_engine2(q_df, diff1, col_list, t1, t2)

        return list(set(style_change)),np.array(q_list)

    def shifting_expression(self,change_ret,name,jjdm,style='Total'):

        change_winning_pro = sum(change_ret[2]) / len(change_ret)
        left_ratio = sum(change_ret[0]) / len(change_ret)
        right_ratio = 1-left_ratio
        one_q_ret = change_ret[3].mean()
        hid_q_ret = change_ret[4].mean()

        return  np.array([style.split('_')[0],len(change_ret),change_winning_pro,one_q_ret,hid_q_ret,left_ratio,right_ratio])

    def style_change_ret(self,df,q_list,col_list,t1,t2):

        style_change,q_list = self.style_change_detect(df,q_list,col_list,t1,t2)
        change_count = len(style_change)
        style_changedf=pd.DataFrame()
        style_changedf['date']=[x.split('@')[0] for x in style_change]
        style_changedf['style']=[x.split('@')[1] for x in style_change]
        style_changedf.sort_values('date',inplace=True,ascending=False)
        style_chang_extret=dict(zip(style_change,style_change))

        if(len(df.columns)>20):
            def get_factor_return(q_list, first_change_date, style):

                sql="select fldm,flmc,zsdm from st_market.t_st_zs_hyzsdmdyb where hyhfbz='2' and fljb='1' "
                industry_index_code=hbdb.db2df(sql,db='alluser')
                industry_index_code['name_eng']=[self.industry_name_map[x] for x in industry_index_code['flmc']]

                sql="select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm='{0}' and jyrq>='{1}' and  jyrq<='{2}'  "\
                    .format(industry_index_code[industry_index_code['name_eng']==style.split('_')[0]]['zsdm'].iloc[0],
                            q_list[q_list < first_change_date][-2],q_list[-1])
                fac_ret_df=hbdb.db2df(sql, db='alluser')
                fac_ret_df['jyrq']=fac_ret_df['jyrq'].astype(str)
                fac_ret_df.set_index('jyrq', drop=True, inplace=True)

                fac_ret_df['price'] = fac_ret_df['spjg']

                return fac_ret_df
            def q_ret(fac_ret_df,q0,q1,time_length=1):
                res=np.power(fac_ret_df.loc[q1]['price']/fac_ret_df.loc[q0]['price'],1/time_length)-1
                return  res
        else:
            def get_factor_return(q_list,first_change_date,style):
                sql = "select factor_ret,trade_date from st_ashare.r_st_barra_factor_return where trade_date>='{0}' and UPPER(factor_name)='{1}' and trade_date<='{2}'" \
                    .format(q_list[q_list<first_change_date][-2], style.split('_')[0].upper(),q_list[-1])
                fac_ret_df = self.hbdb.db2df(sql, db='alluser')
                fac_ret_df.set_index('trade_date', drop=True, inplace=True)
                fac_ret_df['factor_ret_adj'] = fac_ret_df['factor_ret'] + 1
                fac_ret_df['price']=fac_ret_df.rolling(len(fac_ret_df), 1)['factor_ret_adj'].apply(np.prod, raw=True)

                return  fac_ret_df
            def q_ret(fac_ret_df,q0,q1,time_length=1):
                ret=np.power(fac_ret_df['factor_ret_adj'].loc[q0:q1].prod(),
                                         1/time_length)-1
                return  ret

        if(change_count>0):
            for style in style_changedf['style']:

                changedf=style_changedf[style_changedf['style']==style]
                changedf=changedf.sort_values('date')
                first_change_date=changedf['date'].values[0]
                fac_ret_df=get_factor_return(q_list,first_change_date,style)


                for i in range(len(changedf)):
                    date=changedf.iloc[i]['date']

                    observer_term=np.append(q_list[q_list<date][-2:],q_list[(q_list>=date)][0:2])

                    new_exp=df[style].loc[observer_term[2]]
                    old_exp=df[style].loc[observer_term[1]]

                    q0=observer_term[0]
                    q1=observer_term[1]
                    old_ret=q_ret(fac_ret_df,q0,q1)


                    q0=observer_term[1]
                    q1=observer_term[2]
                    current_ret=q_ret(fac_ret_df,q0,q1)
                    if_left=fac_ret_df['price'].loc[q0:q1].mean()>fac_ret_df['price'].loc[q1]

                    q0=observer_term[2]
                    q1=observer_term[3]
                    next_ret=q_ret(fac_ret_df,q0,q1)


                    if (i != len(changedf) - 1):
                        q1 = changedf.iloc[i + 1]['date']
                        q2 = q1
                    else:
                        q1 = q_list[-1]
                        q2=fac_ret_df.index[-1]

                    change_date=date
                    time_length = q_list.tolist().index(q1) - q_list.tolist().index(change_date)
                    holding_ret=q_ret(fac_ret_df,q0,q2,time_length=time_length)

                    if_win_next=(new_exp>old_exp)&(next_ret>current_ret)
                    if_win_hld=(new_exp>old_exp)&(holding_ret>current_ret)

                    shift_retur_next= (new_exp-old_exp)*(next_ret-current_ret)
                    shift_retur_hld = (new_exp - old_exp) * (holding_ret - current_ret)

                    style_chang_extret[date+"@"+style]=[if_left,if_win_next,if_win_hld,shift_retur_next,shift_retur_hld]

        return style_chang_extret

    def style_shifting_analysis(self,df,q_list,col_list,t1,t2,name,jjdm):

        # col_list=[x+"_exp_adj" for x in col]
        change_ret=self.style_change_ret(df,q_list,col_list,t1=t1,t2=t2)
        change_ret = pd.DataFrame.from_dict(change_ret).T
        change_ret['style'] = list([x.split('@')[1] for x in change_ret.index])
        change_ret['date'] = list([x.split('@')[0] for x in change_ret.index])

        data=[]

        if(len(change_ret)>0):
            data.append(self.shifting_expression(change_ret,name,jjdm))
            for style in change_ret['style'].unique():
                tempdf=change_ret[change_ret['style']==style]
                data.append(self.shifting_expression(tempdf,name,jjdm,style))

        shift_df = pd.DataFrame(data=data,columns=['风格类型','切换次数','胜率','下季平均收益','持有平均收益','左侧比率','右侧比例'])

        for col in ['胜率','下季平均收益','持有平均收益','左侧比率','右侧比例']:
            shift_df[col] = shift_df[col].astype(float).map("{:.2%}".format)

        return  shift_df

    def style_label_engine(self,desc,style_stable_list,exp1,exp2,exp3,map_dict):

        style_lable=[]

        for style in style_stable_list:
            if(abs(desc[style]['mean'])>=exp2 and abs(desc[style]['mean'])<exp1):
                label="稳定偏好{}".format("较@"+map_dict[style.split('_')[0]])
            elif(abs(desc[style]['mean'])>=exp1):
                label="稳定偏好{}".format("@"+map_dict[style.split('_')[0]])
            elif(abs(desc[style]['mean'])<=exp3):
                label = "规避{}暴露".format(map_dict[style.split('_')[0]])
            else:
                continue
            if(desc[style]['mean'])<0:
                label=label.replace('@','低')
            else:
                label=label.replace('@','高')
            style_lable.append(label)

        return style_lable

    def style_label_generator(self,df,style_shift_df,ind_shift_df,average_a_w,hld_com):

        style_noshift_col=list(set(self.barra_col).difference(set(style_shift_df.iloc[1:]['风格类型'])))
        ind_noshift_col=list(set(self.indus_col).difference(set(ind_shift_df.iloc[1:]['风格类型'])))

        if(len(style_noshift_col)>0):
            if (hld_com):
                desc=df[[x+"_exp" for x in style_noshift_col]].describe()
            else:
                desc=df[[x+"_exp_adj" for x in style_noshift_col]].describe()

            style_stable_list=desc.columns[((desc.loc['max'] - desc.loc['min']) < 0.5*average_a_w).values].tolist()
            style_lable = self.style_label_engine(desc, style_stable_list,0.75*average_a_w,0.5*average_a_w,0.25*average_a_w,self.style_trans_map)
        else:
            style_lable=[]


        if(len(ind_noshift_col)>0):
            if (hld_com):
                desc=df[[x+"_exp" for x in ind_noshift_col]].describe()
            else:
                desc=df[[x+"_exp_adj" for x in ind_noshift_col]].describe()

            ind_stable_list=desc.columns[((desc.loc['max'] - desc.loc['min']) < 0.1*average_a_w).values].tolist()
            ind_lable = self.style_label_engine(desc, ind_stable_list,0.2*average_a_w,0.1*average_a_w,0.05*average_a_w,self.industry_name_map_e2c)
        else:
            ind_lable=[]

        return style_lable+ind_lable

    def ret_analysis(self,df,a_list,hld_com):

        ret_col_list = ['hld_based_ret', 'barra_ret', 'stock_alpha_ret', 'industry_ret']

        if(hld_com):
            for col in ret_col_list:
                df[col + '_adj'] = np.append([np.nan], df[col][0:-1])
        else:
            for col in ret_col_list:
                df[col+'_adj']=df[col]/df['published_stock_weight']*df['gptzzjb']
                df[col+'_adj'] = np.append([np.nan], df[col+'_adj'][0:-1])

        df = df[[x + '_adj' for x in ret_col_list] + ['nv_ret']]

        df['unexplained_ret'] = df['hld_based_ret_adj'] - (
                    df['barra_ret_adj'] + df['industry_ret_adj'] + df['stock_alpha_ret_adj'])
        df['trading_ret'] =df['nv_ret']- df['hld_based_ret_adj']

        ability_label = []
        for col in ['barra_ret_adj','industry_ret_adj','stock_alpha_ret_adj','unexplained_ret']:
            temp=(df[col]/df['hld_based_ret_adj']).describe()
            # print(col)
            # print(temp['50%'])
            # print(temp['std'])
            if(abs(temp['50%'])>0.35):
                if(temp.std()/temp.mean()<=1):
                    ext = '稳定'
                else:
                    ext = ''
                if(temp['50%']>0):
                    ext2='良好的'
                else:
                    ext2 = '糟糕的'
                ability_label.append(ext+ext2 + self.ability_trans[col] + "能力")

        temp=(df['trading_ret']/df['nv_ret']).describe()

        if(abs(temp['50%'])>0.5):
            if(temp.std()/temp.mean()<=1):
                ext = '稳定'
            else:
                ext = ''
            if(temp['50%']>0):
                ext2='良好的'
            else:
                ext2 = '糟糕的'
            ability_label.append(ext+ext2 + self.ability_trans[col] + "能力")

        return ability_label

    def exp_analysis(self,df,q_list,jjdm,average_a_w,hld_com):

        if(hld_com):
            style_shift_df = self.style_shifting_analysis(
                df[[x + "_exp" for x in self.barra_col] + [x for x in self.barra_col]].astype(float),
                q_list,[x + "_exp" for x in self.barra_col],
                t1=0.5 * average_a_w, t2=0.2 * average_a_w, name='barra style', jjdm=jjdm)

            ind_shift_df = self.style_shifting_analysis(
                df[[x + "_exp" for x in self.indus_col] + [x  for x in self.indus_col]].astype(float),
                q_list,[x + "_exp" for x in self.indus_col],
                t1=0.1 * average_a_w, t2=0.075 * average_a_w, name='industry', jjdm=jjdm)

        else:

            style_shift_df=self.style_shifting_analysis(
                df[[x+"_exp_adj" for x in self.barra_col]+[x+"_adj" for x in self.barra_col]].astype(float)
                ,q_list,[x+"_exp_adj" for x in self.barra_col],t1=0.3*average_a_w,
                t2=0.15*average_a_w,name='barra style',jjdm=jjdm)

            ind_shift_df=self.style_shifting_analysis(
                df[[x + "_exp_adj" for x in self.indus_col]+[x+"_adj" for x in self.indus_col]].astype(float),
                q_list,[x+"_exp_adj" for x in self.indus_col], t1=0.1*average_a_w,
                t2=0.075*average_a_w, name='industry',jjdm=jjdm)

        style_lable = self.style_label_generator(df,style_shift_df,ind_shift_df,average_a_w,hld_com)

        return  style_shift_df,ind_shift_df,style_lable

    def centralization_level(self,df,num1=3,num2=5):

        outputdf=pd.DataFrame(index=df.index,columns=['c_level'])

        for i in range(len(df)):
            outputdf.iloc[i]['c_level']=(df.iloc[i].sort_values()[-1*num1:].sum()+df.iloc[i].sort_values()[-1*num2:].sum())/2/df.iloc[i].sum()

        return outputdf.mean()[0]

    @staticmethod
    def ind_shift_rate(indf):
        indf.sort_index(inplace=True)
        indus_col=indf.columns.tolist()
        indus_col.remove('jjzzc')
        for col in indus_col:
            indf[col+'_mkt']=indf[col]*indf['jjzzc']
        diff=indf[[x+'_mkt' for x in indus_col]].diff(1)
        diff['jjzzc']=indf[[x+'_mkt' for x in indus_col]].sum(axis=1)
        diff['jjzzc']=diff['jjzzc'].rolling(2).mean()
        shift_ratio=diff[[x+'_mkt' for x in indus_col]].abs().sum(axis=1)/2/diff['jjzzc']
        return shift_ratio.describe()

    def ind_analysis(self,df,hld_com):

        q_date=df.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in df.index]].index
        a_date=df.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in df.index]].index
        q_list=q_date.to_list()+a_date.to_list()

        if(not hld_com):
            #calculate the ratio between quarter report stock weigth and annual report stock weight
            average_q_w=(df.loc[q_date]['published_stock_weight']).mean()
            average_a_w=(df.loc[a_date]['published_stock_weight']).mean()
            shift_confidence=average_q_w/average_a_w

            # calculate the average industry exp num
            inddf = df[[x + '_exp_adj' for x in self.indus_col]].loc[q_list]
            average_ind_num = (inddf.loc[a_date] > 0).sum(axis=1).mean()
            adj_average_ind_num = ((inddf > 0).sum(axis=1) * df.loc[q_list][
                'published_stock_weight']).mean() / average_a_w

            # calculate the industry holding centralization_level
            average_ind_cen_level = self.centralization_level(inddf.loc[a_date])

            # calculate the industry holding shift ratio
            shift_ratio = self.ind_shift_rate(df[[x + '_exp' for x in self.indus_col] + ['jjzzc']].loc[a_date])

            # the 50,75,25 for c is 0.0.617,0.712,0.0.55
            # the 50,75,25 for r is 0.288,0.343,0.235
            if (average_ind_cen_level > 0.617 and shift_ratio['mean'] > 0.288):
                ind_label = '行业博弈型'
            elif (average_ind_cen_level > 0.617 and shift_ratio['mean'] < 0.288):
                ind_label = '行业专注型'
            elif (average_ind_cen_level < 0.617 and shift_ratio['mean'] > 0.288):
                ind_label = '行业轮动型'
            elif (average_ind_cen_level < 0.617 and shift_ratio['mean'] < 0.288):
                ind_label = '行业配置型'
            else:
                ind_label = ''

            a_date=a_date.tolist()

        else:
            shift_confidence=1
            inddf = df[[x + '_exp' for x in self.indus_col]]

            average_q_w = (df.loc[q_date]['published_stock_weight']).mean()
            average_a_w = (df.loc[a_date]['published_stock_weight']).mean()

            # calculate the average industry exp num
            average_ind_num = (inddf.loc[q_list] > 0).sum(axis=1).mean()

            # calculate the industry holding centralization_level
            average_ind_cen_level = self.centralization_level(inddf)

            # calculate the industry holding shift ratio
            shift_ratio = self.ind_shift_rate(df[[x + '_exp' for x in self.indus_col] + ['jjzzc']].loc[q_list])
            #the 50,75,25 for c is 0.0.63,0.72,0.56
            #the 50,75,25 for r is 0.43,0.51,0.34
            if(average_ind_cen_level>0.63 and shift_ratio['mean']>0.43):
                ind_label='行业博弈型'
            elif (average_ind_cen_level > 0.63 and shift_ratio['mean'] < 0.43):
                ind_label = '行业专注型'
            elif (average_ind_cen_level < 0.63 and shift_ratio['mean'] > 0.43):
                ind_label = '行业轮动型'
            elif (average_ind_cen_level <0.63 and shift_ratio['mean'] < 0.43):
                ind_label = '行业配置型'
            else:
                ind_label=''

            a_date=q_list

        # print(ind_label)

        return ind_label,q_list,average_a_w,average_ind_cen_level,shift_ratio['mean'],shift_confidence,a_date

    def classify(self,jjdm,start_date,end_date,hld_com=False):

        df,q_list=self.ret_div(jjdm,start_date,end_date,hld_com)

        ind_label,q_list,average_a_w,average_ind_cen_level,\
        shift_ratio,shift_confidence,a_list=self.ind_analysis(df,hld_com)

        # q_date=df.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in df.index]].index
        # a_date=df.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in df.index]].index
        # q_list=q_date.to_list()+a_date.to_list()
        # average_a_w=df.loc[a_date]['published_stock_weight'].mean()
        style_shift_df,ind_shift_df,style_lable=self.exp_analysis(df,q_list,jjdm,average_a_w,hld_com)

        ability_label=self.ret_analysis(df,q_list,hld_com)

        if(hld_com):
            df=df[[x + "_exp" for x in self.barra_col]+[x + "_exp" for x in self.indus_col]]
        else:
            df = df[[x + "_exp_adj" for x in self.barra_col] + [x + "_exp_adj" for x in self.indus_col]]

        return df,style_shift_df,ind_shift_df,style_lable,average_ind_cen_level,shift_ratio,shift_confidence,average_a_w,ind_label,ability_label

    def data_preparation(self,hld_compenzation=False):

        jjdm_list=util.get_mutual_stock_funds('20211231')
        #'001291'
        # jjdm_list=jjdm_list.iloc[508:]
        for jjdm in jjdm_list:

            sql = """select min(jsrq) from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq>=20150101
            """.format(jjdm)
            jsrq = str(self.hbdb.db2df(sql, db='funduser')['min(jsrq)'][0])
            #['2016','2017','2018','2019','2020','2021']
            for year in ['2018','2019','2020','2021']:
                if(year<jsrq[0:4]):
                    continue
                elif(year==jsrq[0:4]):
                    start_date=jsrq
                else:
                    start_date = str(int(year)-1) + "1231"

                end_date=year+"1231"
                try:
                    self.save_barra_ret2db(jjdm=jjdm,start_date=start_date,end_date=end_date,
                                           add=False,hld_compenzation=hld_compenzation)
                except Exception as e :
                    print(e)
                    print("{} failed at start date {} and end date{}".format(jjdm,start_date,end_date))

    def new_joinner_old(self,jjdm,start_date,end_date):

        ##get holding info for give jjdm
        sql="""select jsrq,zqdm,zjbl,zqmc from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq<='{1}'  
        """.format(jjdm,end_date)
        hld=self.hbdb.db2df(sql,db='funduser')
        hld['jsrq']=hld['jsrq'].astype(str)

        #get the history ticker list based on start date
        history_ticker=hld[hld['jsrq']<start_date]['zqdm'].unique().tolist()
        #take only the holding after the start date
        hld=hld[(hld['jsrq']>=start_date)&(hld['zjbl']>0)].reset_index(drop=True)
        date_list=hld['jsrq'].unique().tolist()

        #get the date map between report date and the trade date
        new_date_list=[self._shift_date(x) for x in hld['jsrq'].unique()]
        date_map=dict(zip(hld['jsrq'].unique().tolist(),new_date_list))

        #take holding without the latest date since we need atleast one more quarter to calcualte the new joinner ret
        hld=hld[hld['jsrq']<end_date]


        hld['HK']=[len(x) for x in hld['zqdm']]
        hld=hld[hld['HK']==6]

        new_joinner_list=[]
        ret_list=[]
        q_list=[]
        adding_date=[]

        #for each item in the holding,check if it is a new joinner
        for i in range(len(hld)):
            if(len(new_joinner_list)>0):
                if(len(new_joinner_list)!=len(ret_list)):
                    print(i-1)
                    raise Exception
            zqdm=hld.iloc[i]['zqdm']
            zqmc=hld.iloc[i]['zqmc']
            if(zqdm not in history_ticker):
                #if new joinner, add it to new joinner list and history list
                history_ticker.append(zqdm)
                new_joinner_list.append(zqdm)

                # get the next report date
                t0 = hld.iloc[i]['jsrq']
                date_ind=date_list.index(t0)
                t0=date_map[hld.iloc[i]['jsrq']]
                adding_date.append(t0)
                t1=date_map[date_list[date_ind+1]]
                q_list.append('t1')
                date_sql_con="and JYRQ in ({})".format("'"+t0+"','"+t1+"'"+"@")

                # get the report date after the next report date if possible
                if(date_ind<len(date_list)-3):
                    t2=date_map[date_list[date_ind+2]]
                    t3=date_map[date_list[date_ind+3]]
                    date_sql_con=date_sql_con.replace("@",",'{0}','{1}'".format(t2,t3))
                    new_joinner_list.append(zqdm)
                    new_joinner_list.append(zqdm)
                    q_list.append('t2')
                    q_list.append('t3')
                    adding_date.append(t0)
                    adding_date.append(t0)

                elif(date_ind<len(date_list)-2):
                    t2=date_map[date_list[date_ind+2]]
                    date_sql_con=date_sql_con.replace("@",",'"+t2+"'")
                    new_joinner_list.append(zqdm)
                    q_list.append('t2')
                    adding_date.append(t0)
                else:
                    date_sql_con = date_sql_con.replace("@", "")

                #get ticker price for given date
                sql = """
                select ZQDM,JYRQ,DRJJ,SCDM from FUNDDB.ZGJY where ZQDM ='{0}' {1}
                 """.format(zqdm, date_sql_con)
                quarter_price = self.hbdb.db2df(sql, db='readonly')

                # get benchmark price for given date
                sql="select zqdm,spjg,jyrq from st_market.t_st_zs_hq where  zqdm='000002' {0} "\
                    .format(date_sql_con)
                benchmakr_ret=self.hbdb.db2df(sql,db='alluser')

                # continue_flag=False
                if(len(quarter_price)!=len(benchmakr_ret)):
                    sql = "select min(JYRQ) as jyrq from  FUNDDB.ZGJY where ZQDM ='{0}' and ZQMC='{1}'".format(zqdm,zqmc)
                    min_jyrq =self.hbdb.db2df(sql, db='readonly')['JYRQ'][0]
                    if(min_jyrq>t0):
                        sql = """
                        select ZQDM,JYRQ,DRJJ,SCDM from FUNDDB.ZGJY where ZQDM ='{0}' {1}
                         """.format(zqdm, date_sql_con)
                        sql=sql.replace(t0,min_jyrq)
                        quarter_price = self.hbdb.db2df(sql, db='readonly')
                #     else:
                #         continue_flag=True
                #
                # if(continue_flag):
                #     continue

                for i in range(1,len(quarter_price)):
                    ret_list.append( (quarter_price.iloc[i]['DRJJ'] /quarter_price.iloc[0]['DRJJ']-1)-
                                     (benchmakr_ret.iloc[i]['spjg'] /benchmakr_ret.iloc[0]['spjg']-1))

        retdf=pd.DataFrame()
        retdf['zqdm']=new_joinner_list
        retdf['qt']=q_list
        retdf['ret']=ret_list
        retdf['added_date']=adding_date

        # outputdf=pd.DataFrame(columns=['收益时序','胜率','平均超额收益'])
        # outputdf['收益时序']=['1个季度后','2个季度后','3个季度后']
        # outputdf['胜率']=(retdf[retdf['ret']>0]).groupby('qt').count()['zqdm'].values/retdf.groupby('qt').count()['zqdm'].values
        # outputdf['平均超额收益']=retdf.groupby('qt').mean()['ret'].values
        # outputdf['超额收益中位数']=retdf.groupby('qt').median()['ret'].values
        # outputdf['最大超额收益'] = retdf.groupby('qt').max()['ret'].values
        # outputdf['最小超额收益'] = retdf.groupby('qt').min()['ret'].values
        # for col in ['胜率','平均超额收益','超额收益中位数','最大超额收益','最小超额收益']:
        #     outputdf[col] = outputdf[col].astype(float).map("{:.2%}".format)
        #
        # return  outputdf

        return retdf

    def new_joinner(self,jjdm):

        ##get holding info for give jjdm no older than 20151231
        sql="""select jsrq,zqdm,zjbl,zqmc from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq>='20151231'  
        """.format(jjdm)
        hld=self.hbdb.db2df(sql,db='funduser')
        hld['jsrq']=hld['jsrq'].astype(str)
        end_date=hld['jsrq'].unique()[-1]
        start_date=hld['jsrq'].unique()[1]


        #get the history ticker list based on start date
        history_ticker=hld[hld['jsrq']<start_date]['zqdm'].unique().tolist()
        #take only the holding after the start date
        hld=hld[(hld['jsrq']>=start_date)&(hld['zjbl']>0)].reset_index(drop=True)
        date_list=hld['jsrq'].unique().tolist()

        #get the date map between report date and the trade date
        new_date_list=[self._shift_date(x) for x in hld['jsrq'].unique()]
        date_map=dict(zip(hld['jsrq'].unique().tolist(),new_date_list))

        #take holding without the latest date since we need atleast one more quarter to calcualte the new joinner ret
        hld=hld[hld['jsrq']<end_date]


        hld['HK']=[len(x) for x in hld['zqdm']]
        hld=hld[hld['HK']==6]

        new_joinner_list=[]
        ret_list=[]
        q_list=[]
        adding_date=[]

        #for each item in the holding,check if it is a new joinner
        for i in range(len(hld)):
            # if(len(new_joinner_list)>0):
            #     if(len(new_joinner_list)!=len(ret_list)):
            #         print(i-1)
            #         raise Exception
            zqdm=hld.iloc[i]['zqdm']
            zqmc=hld.iloc[i]['zqmc']
            if(zqdm not in history_ticker):
                #if new joinner, add it to new joinner list and history list
                history_ticker.append(zqdm)
                # new_joinner_list.append(zqdm)

                # get the next report date
                t0 = hld.iloc[i]['jsrq']
                date_ind=date_list.index(t0)
                t0=date_map[hld.iloc[i]['jsrq']]
                # adding_date.append(t0)
                t1=date_map[date_list[date_ind+1]]
                # q_list.append('t1')
                date_sql_con="and JYRQ in ({})".format("'"+t0+"','"+t1+"'"+"@")

                # get the report date after the next report date if possible
                if(date_ind<len(date_list)-3):
                    t2=date_map[date_list[date_ind+2]]
                    t3=date_map[date_list[date_ind+3]]
                    date_sql_con=date_sql_con.replace("@",",'{0}','{1}'".format(t2,t3))


                elif(date_ind<len(date_list)-2):
                    t2=date_map[date_list[date_ind+2]]
                    date_sql_con=date_sql_con.replace("@",",'"+t2+"'")

                else:
                    date_sql_con = date_sql_con.replace("@", "")

                #get ticker price for given date
                sql = """
                select ZQDM,JYRQ,DRJJ,SCDM from FUNDDB.ZGJY where ZQDM ='{0}' and DRJJ is not null  {1}
                 """.format(zqdm, date_sql_con)
                quarter_price = self.hbdb.db2df(sql, db='readonly')

                # get benchmark price for given date
                sql="select zqdm,spjg,jyrq from st_market.t_st_zs_hq where  zqdm='000002' {0} "\
                    .format(date_sql_con)
                benchmakr_ret=self.hbdb.db2df(sql,db='alluser')
                benchmakr_ret['jyrq']=benchmakr_ret['jyrq'].astype(str)
                benchmakr_ret['ind']=benchmakr_ret.index
                if(len(quarter_price)>0):
                    if(quarter_price['JYRQ'].min()>t0):
                        sql = "select min(JYRQ) as jyrq from  FUNDDB.ZGJY where ZQDM ='{0}' and ZQMC='{1}' and JYRQ>'{2}' and DRJJ is not null ".format(zqdm,zqmc,t0)
                        min_jyrq =self.hbdb.db2df(sql, db='readonly')['JYRQ'][0]
                        if(min_jyrq>t0 and min_jyrq<t1):
                            sql = """
                            select ZQDM,JYRQ,DRJJ,SCDM from FUNDDB.ZGJY where ZQDM ='{0}' and DRJJ is not null {1}
                             """.format(zqdm, date_sql_con)
                            sql=sql.replace(t0,min_jyrq)
                            quarter_price = self.hbdb.db2df(sql, db='readonly')

                    if(quarter_price['JYRQ'].min()==t0):

                        tempdf=pd.merge(quarter_price,benchmakr_ret,how='left',left_on='JYRQ',right_on='jyrq')
                        for i in range(1,len(tempdf)):
                            new_joinner_list.append(zqdm)
                            adding_date.append(t0)
                            q_list.append("t"+str(tempdf['ind'][i]))
                            ret_list.append( (quarter_price.iloc[i]['DRJJ'] /quarter_price.iloc[0]['DRJJ']-1)-
                                             (benchmakr_ret.iloc[i]['spjg'] /benchmakr_ret.iloc[0]['spjg']-1))

        retdf=pd.DataFrame()
        retdf['zqdm']=new_joinner_list
        retdf['qt']=q_list
        retdf['ret']=ret_list
        retdf['added_date']=adding_date

        return retdf

    def save_new_joinner_date2localdb(self):


        jjdm_list=util.get_mutual_stock_funds('20211231')

        erro_df=pd.DataFrame()
        error_list=[]
        for i in range(0,len(jjdm_list)):
            try:
                # check if data alreay in db
                sql="select count(jjdm) as c from new_joinner_ret where jjdm='{0}'".format(jjdm_list[i])
                if(pd.read_sql(sql,con=localdb).values[0][0]==0):
                    retdf=self.new_joinner(jjdm_list[i])
                    retdf['jjdm']=jjdm_list[i]
                    retdf.to_sql('new_joinner_ret',index=False,if_exists='append',con=self.localengine)
                    print("{0} done ".format(jjdm_list[i]))
            except Exception as e :
                error_list.append(jjdm_list[i]+"@"+str(e))
                continue
        erro_df['error']=error_list
        erro_df.to_csv(r"E:\新股错误数据.csv")
        print('Done')

    def change_analysis(self,jjdm,start_date,end_date,hld_com=True):

        df,q_list=self.ret_div(jjdm,start_date,end_date,hld_com)
        q_list=df.loc[[(x[4:6] == '03') | (x[4:6] == '09')|(x[4:6] == '06')
                              | (x[4:6] == '12') for x in df.index]].index.tolist()
        q_list.sort()
        df=df.loc[q_list][[x+"_exp" for x in self.indus_col]]

        diff = df.diff(1, axis=0)
        diff['total_w'] = df.sum(axis=1)
        change_ret = diff.copy()
        change_ret_nextq = diff.copy()
        sql = "select flmc,zsdm from st_market.t_st_zs_hyzsdmdyb where hyhfbz='2'"
        zqdm_list = self.hbdb.db2df(sql, db='alluser')

        for col in self.indus_col:
            # print(col)
            zqdm = zqdm_list[zqdm_list['flmc'] == self.industry_name_map_e2c[col]]['zsdm'].tolist()[0]
            for i in range(1, len(diff) - 1):
                #print(i)
                t0 = diff.index[i - 1]
                t1 = diff.index[i]
                t2 = diff.index[i + 1]
                date_con = "'{0}','{1}','{2}'".format(t0, t1,t2)
                sql = """select zqdm,spjg,jyrq from  st_market.t_st_zs_hqql where jyrq in ({0}) and (zqdm='{1}' or zqdm='000002')
                """.format(date_con, zqdm)
                index_price = self.hbdb.db2df(sql, db='alluser')
                index_price['ret'] = index_price['spjg'].pct_change()
                index_price['jyrq']=index_price['jyrq'].astype(str)
                index_price.set_index('jyrq', drop=True, inplace=True)

                change_ret.loc[t1, col+"_exp"] = \
                    (index_price[index_price['zqdm']==zqdm].loc[t1]['ret']
                                                  - index_price[index_price['zqdm']=='000002'].loc[t1]['ret']) \
                    * diff.loc[t1, col+"_exp"] / diff.loc[t1, "total_w"]
                if(t2 in index_price[index_price['zqdm']==zqdm].index):
                    change_ret_nextq.loc[t1, col+"_exp"] = \
                        (index_price[index_price['zqdm']==zqdm].loc[t2]['ret']
                                                      - index_price[index_price['zqdm']=='000002'].loc[t2]['ret']) \
                        * diff.loc[t1, col+"_exp"] / diff.loc[t1, "total_w"]
                else:
                    change_ret_nextq.loc[t1, col + "_exp"]=np.nan

        change_ret=change_ret.loc[change_ret.index[1:-1]].drop('total_w',axis=1)
        change_ret_nextq = change_ret_nextq.loc[change_ret_nextq.index[1:-1]].drop('total_w',axis=1)

        industry_based_ret=pd.concat([change_ret.sum(axis=0),change_ret_nextq.sum(axis=0)],axis=1)
        term_based_ret=pd.concat([change_ret.sum(axis=1),change_ret_nextq.sum(axis=1)],axis=1)
        industry_based_ret.columns=['当季','下季']
        term_based_ret.columns = ['当季', '下季']

        for col in industry_based_ret.columns:
            industry_based_ret[col] = industry_based_ret[col].astype(float).map("{:.2%}".format)
        for col in term_based_ret.columns:
            term_based_ret[col] = term_based_ret[col].astype(float).map("{:.2%}".format)

        industry_based_ret.sort_values('当季',ascending=False,inplace=True)

        return change_ret,change_ret_nextq,industry_based_ret,term_based_ret

    def change_analysis_givendf(self,df):

        q_list=df.loc[[(x[4:6] == '03') | (x[4:6] == '09')|(x[4:6] == '06')
                              | (x[4:6] == '12') for x in df.index]].index.tolist()
        q_list.sort()
        df=df.loc[q_list][[x+"_exp" for x in self.indus_col]]

        diff = df.diff(1, axis=0)
        diff['total_w'] = df.sum(axis=1)
        change_ret = diff.copy()
        change_ret_nextq = diff.copy()
        sql = "select flmc,zsdm from st_market.t_st_zs_hyzsdmdyb where hyhfbz='2'"
        zqdm_list = self.hbdb.db2df(sql, db='alluser')

        for col in self.indus_col:
            # print(col)
            zqdm = zqdm_list[zqdm_list['flmc'] == self.industry_name_map_e2c[col]]['zsdm'].tolist()[0]
            for i in range(1, len(diff) - 1):
                #print(i)
                t0 = diff.index[i - 1]
                t1 = diff.index[i]
                t2 = diff.index[i + 1]
                date_con = "'{0}','{1}','{2}'".format(t0, t1,t2)
                sql = """select zqdm,spjg,jyrq from  st_market.t_st_zs_hqql where jyrq in ({0}) and (zqdm='{1}' or zqdm='000002')
                """.format(date_con, zqdm)
                index_price = self.hbdb.db2df(sql, db='alluser')
                index_price['ret'] = index_price['spjg'].pct_change()
                index_price['jyrq']=index_price['jyrq'].astype(str)
                index_price.set_index('jyrq', drop=True, inplace=True)

                change_ret.loc[t1, col+"_exp"] = \
                    (index_price[index_price['zqdm']==zqdm].loc[t1]['ret']
                                                  - index_price[index_price['zqdm']=='000002'].loc[t1]['ret']) \
                    * diff.loc[t1, col+"_exp"] / diff.loc[t1, "total_w"]
                if(t2 in index_price[index_price['zqdm']==zqdm].index):
                    change_ret_nextq.loc[t1, col+"_exp"] = \
                        (index_price[index_price['zqdm']==zqdm].loc[t2]['ret']
                                                      - index_price[index_price['zqdm']=='000002'].loc[t2]['ret']) \
                        * diff.loc[t1, col+"_exp"] / diff.loc[t1, "total_w"]
                else:
                    change_ret_nextq.loc[t1, col + "_exp"]=np.nan

        change_ret=change_ret.loc[change_ret.index[1:-1]].drop('total_w',axis=1)
        change_ret_nextq = change_ret_nextq.loc[change_ret_nextq.index[1:-1]].drop('total_w',axis=1)

        industry_based_ret=pd.concat([change_ret.sum(axis=0),change_ret_nextq.sum(axis=0)],axis=1)
        term_based_ret=pd.concat([change_ret.sum(axis=1),change_ret_nextq.sum(axis=1)],axis=1)
        industry_based_ret.columns=['当季','下季']
        term_based_ret.columns = ['当季', '下季']

        for col in industry_based_ret.columns:
            industry_based_ret[col] = industry_based_ret[col].astype(float).map("{:.2%}".format)
        for col in term_based_ret.columns:
            term_based_ret[col] = term_based_ret[col].astype(float).map("{:.2%}".format)

        industry_based_ret.sort_values('当季',ascending=False,inplace=True)

        return change_ret,change_ret_nextq,industry_based_ret,term_based_ret

    @staticmethod
    def factorlize_new_joinner(factor_name):

        sql="select jjdm,added_date,avg(ret) as {0} from new_joinner_ret  where qt='t1' GROUP BY jjdm,added_date "\
            .format(factor_name)

        raw_df=pd.read_sql(sql,con=localdb)
        date_list=raw_df['added_date'].unique()
        date_list.sort()
        first_date=date_list[0]
        raw_df.rename(columns={'added_date':'date'},inplace=True)
        raw_df[factor_name]=[np.nan] + raw_df[factor_name][0:-1].tolist()

        raw_df=raw_df[raw_df['date']!=first_date]
        #take the last 3years mean t_ret as factor
        raw_df['new_join_'+factor_name] = raw_df.groupby(by='jjdm',as_index=False)[factor_name].rolling(12, 1).mean().values

        return raw_df

class Stock_trade_timing:

    @staticmethod
    def data_factory(ticker):

        jjdm_list=util.get_mutual_stock_funds('20211231')
        jjdm_con=util.list_sql_condition(jjdm_list)

        sql="select distinct(jsrq) from st_fund.t_st_gm_jjcgbd "
        hld_reprot_date_list=hbdb.db2df(sql,db='funduser').sort_values('jsrq')['jsrq'].astype(str).tolist()

        #get the stock that become zc
        sql="""select jjdm,jsrq from st_fund.t_st_gm_jjcgbd where zqdm='{0}' 
        and zclb='1' and jjdm in ({1}) and jsrq>='20120101'
        """.format(ticker,jjdm_con)
        hld_df=hbdb.db2df(sql,db='funduser')
        hld_df['jsrq']=hld_df['jsrq'].astype(str)


        #get the stock zgbl
        jjdm_con_new=util.list_sql_condition(hld_df['jjdm'].unique().tolist())
        sql="select jjdm,jsrq,zgbl from st_fund.t_st_gm_gpzh where zqdm='{2}' and jjdm in ({0}) and jsrq in ({1})"\
            .format(jjdm_con_new,
                    util.list_sql_condition(hld_df['jsrq'].unique().tolist()),
                    ticker)
        zgbl=hbdb.db2df(sql,db='funduser')
        zgbl['jsrq'] = zgbl['jsrq'].astype(str)
        hld_df=pd.merge(hld_df,zgbl,how='left',on=['jjdm','jsrq'])

        hld_df['lastdate'] = [hld_reprot_date_list[hld_reprot_date_list.index(x) - 1] for x in hld_df['jsrq']]
        hld_df.loc[hld_df['jsrq']<hld_reprot_date_list[-1],'nextdate'] = [hld_reprot_date_list[hld_reprot_date_list.index(x) + 1]
                              for x in hld_df[hld_df['jsrq']<hld_reprot_date_list[-1]]['jsrq']]

        hld_df = pd.merge(hld_df, hld_df[['jjdm', 'jsrq']], how='left',
                          left_on=['jjdm','lastdate'],right_on=['jjdm','jsrq'])

        hld_df = pd.merge(hld_df, hld_df[['jjdm', 'jsrq_x']], how='left',
                          left_on=['jjdm','nextdate'],right_on=['jjdm','jsrq_x'])


        #map the jjdm to jjjl
        sql="select jjdm,ryxm,rzrq,lrrq from st_fund.t_st_gm_jjjl where jjdm in ({0})"\
            .format(jjdm_con_new)
        jjjl=hbdb.db2df(sql,db='funduser')
        jjjl['rzrq']=jjjl['rzrq'].astype(str)
        jjjl['lrrq'] = jjjl['lrrq'].astype(str)

        hld_df=pd.merge(hld_df,jjjl,how='left',on='jjdm')

        #map the jjdm with jjjc
        sql="select jjdm,jjjc from st_fund.t_st_gm_jjxx  "
        jjjc=hbdb.db2df(sql,db='funduser')
        hld_df=pd.merge(hld_df,jjjc,how='left',on='jjdm')
        hld_df['ryxm']=hld_df['ryxm']+'_'+hld_df['jjjc']

        #map the jjdm to jjgs
        sql="select a.jjdm,b.jgjc from st_main.t_st_gg_jjxx a left join st_main.t_st_gg_jgxx b on a.glrm=b.jgdm where a.jjdm in ({0})"\
            .format(jjdm_con_new)
        jjgs=hbdb.db2df(sql,db='alluser')
        hld_df=pd.merge(hld_df,jjgs,how='left',on='jjdm')
        hld_df['ryxm']=hld_df['ryxm']+'_'+hld_df['jgjc']

        hld_df1=hld_df[hld_df['jsrq_y'].isnull()][['ryxm','jsrq_x_x','zgbl']].rename(columns={'jsrq_x_x':'jsrq'})
        hld_df2=hld_df[(hld_df['nextdate'].notnull())
                       &(hld_df['jsrq_x_y'].isnull())][['ryxm','nextdate','zgbl']].rename(columns={'nextdate':'jsrq'})
        del hld_df

        hld_df1=hld_df1.sort_values(['jsrq','zgbl']).groupby(['jsrq', 'ryxm'], as_index=False).mean()
        hld_df2 = hld_df2.sort_values(['jsrq','zgbl']).groupby(['jsrq', 'ryxm'], as_index=False).mean()

        hld_df1 = hld_reportdate2trade_date(hld_df1,date_col='jsrq')
        hld_df2 = hld_reportdate2trade_date(hld_df2, date_col='jsrq')

        hld_df1['jjdm_new'] =hld_df1['ryxm']+ [": "+str(x)[0:4] + "<br />" for x in hld_df1['zgbl']]
        hld_df2['jjdm_new'] =hld_df2['ryxm']+ [": "+str(x)[0:4]  + "<br />" for x in hld_df2['zgbl']]

        #rank by zgbl
        hld_df1=pd.concat([hld_df1,
                           hld_df1.groupby('jsrq', as_index=False).rank(ascending=False,method='min').rename(columns={'zgbl': 'rank'})],
                          axis=1)

        hld_df2=pd.concat([hld_df2,
                           hld_df2.groupby('jsrq', as_index=False).rank(method='min').rename(columns={'zgbl': 'rank'})],
                          axis=1)

        #take only the top 20 for buy and last 20 for sell
        hld_df1=hld_df1[hld_df1['rank']<=20]
        hld_df2 = hld_df2[hld_df2['rank'] <= 20]

        hld_df_pic_1=hld_df1.groupby('jsrq')['jjdm_new'].sum().to_frame('jjdm')
        hld_df_pic_2 = hld_df2.groupby('jsrq')['jjdm_new'].sum().to_frame('jjdm')


        #get the stock price data
        sql = """
        select JYRQ,SPJG from FUNDDB.ZGJY where ZQDM='{0}' and DRJJ is not null and JYRQ>='20120101'
         """.format(ticker)
        price_df=hbdb.db2df(sql,db='readonly')
        price_df.sort_values('JYRQ',inplace=True)

        hld_df_pic_1=pd.merge(price_df,hld_df_pic_1,how='left',left_on='JYRQ',right_index=True).drop(['ROW_ID'],axis=1)
        hld_df_pic_1.set_index('JYRQ',drop=True,inplace=True)

        hld_df_pic_2=pd.merge(price_df,hld_df_pic_2,how='left',left_on='JYRQ',right_index=True).drop(['ROW_ID'],axis=1)
        hld_df_pic_2.set_index('JYRQ',drop=True,inplace=True)

        return hld_df1.drop(['jjdm_new','rank'],axis=1),hld_df2.drop(['jjdm_new','rank'],axis=1),hld_df_pic_1,hld_df_pic_2

if __name__ == '__main__':


    #gh=General_holding()
    # jjdm_list=util.get_mutual_stock_funds('20211231')
    #
    # last_quarter = (datetime.datetime.strptime('20190304', '%Y%m%d') - datetime.timedelta(days=93)) \
    #     .strftime('%Y%m%d')
    # # get the cleaning holding data
    # hld, new_jjdm_list = gh.fund_holding_date_manufacture(jjdm_list, last_quarter, '20220304')
    # hld.reset_index(drop=False,inplace=True)
    # hld.drop_duplicates(inplace=True)
    # hld.to_excel('hbs_raw_data.xlsx',encoding='gbk')
    #
    # hld.to_sql('hbs_raw_data',index=False,if_exists='append',con=localdb)

    #gh.save_holding_trading_2db(jjdm_list, '20181231', '20220304')
    # #gh.get_holding_trading_analysis('20211231')
    #
    # jjdm_list=['005827']
    # gh.get_hld_property(jjdm_list,'20190304','20220304')
    #
    #

    df=pd.read_excel(r"E:\GitFolder\hbshare\fe\mutual_analysis\theme_shit.xlsx")
    df['jjdm'] = [x.replace("'", "") for x in df['jjdm']]
    df.to_sql('hbs_theme_shift_property',index=False,if_exists='append',con=localdb)


    ba = Barra_analysis()

    # df, style_shift_df, ind_shift_df, style_lable, average_ind_cen_level, \
    # shift_ratio, shift_confidence, average_a_w, ind_label \
    #     , ability_label = ba.classify('000729', '20180930', '20211231', hld_com=True)
    #
    # save_industry_property2localdb(ba,time_length=3)
    ia=Industry_analysis()
    # ia.save_industry_property2localdb(ba,time_length=3)
    ia.save_industry_shift_property2localdb(ba, time_length=3)

    # change_ret, change_ret_nextq, \
    # industry_based_ret, term_based_ret = fc.change_analysis('000167', '20151231', '20211231')
    #ba.data_preparation(hld_compenzation=True)
    #ba.save_new_joinner_date2localdb()


    #
    # br = Brinson_ability()
    # sql = "select distinct tjrq from st_fund.r_st_hold_excess_attr_df where tjrq>'20171229' "
    # tjrq_list=hbdb.db2df(sql,'funduser')['tjrq'].tolist()
    # tjrq_list=['20211231']
    # for tjrq in tjrq_list:
    #     br.classify_socring(tjrq)



    #plot the pic of fund trading point per stock
    # stt=Stock_trade_timing()
    # ticker = '600188'
    # buydf, selldf, buypicdf, sellpicdf = stt.data_factory(ticker)
    #
    # plot = functionality.Plot(1200, 600)
    # plot.plotly_line_with_annotation(buypicdf, data_col=['SPJG'], anno_col=['jjdm'], title_text='基金买入时序图')
    # plot.plotly_line_with_annotation(sellpicdf, data_col=['SPJG'], anno_col=['jjdm'], title_text='基金卖出时序图')
    #
    # plot = functionality.Plot(500, 200)
    # plot.plotly_table(buydf.rename(columns={'jsrq': '进入时点'}), 500, 'buy')
    # plot.plotly_table(selldf.rename(columns={'jsrq': '离开时点'}), 500, 'sell')