from tkinter import *
from sector_creator import create_sector_kml
from sector_creator_3g import create_sector_3g
import pandas as pd
from tkinter import filedialog
import customtkinter as ctk

ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = ctk.CTk()
app.geometry("570x430")
app.title("TA KML Generator")

root = ctk.CTkFrame(master=app)
root.pack(pady=20, padx=20, fill="both", expand=True)

e=Entry(root, width=40)
l=ctk.CTkLabel(root, text=" ")
ll=ctk.CTkLabel(root, text=" ")
stats=ctk.CTkLabel(root, text="-")
stats_cln=ctk.CTkLabel(root, text="-")

kml_title=ctk.CTkLabel(root, text="TA KML Generator")
data_cln_title=ctk.CTkLabel(root, text="Clean TA File")

data_ecno_title=ctk.CTkLabel(root, text="3G Ec/No Analysis")
stats_ecno=ctk.CTkLabel(root, text="-")
#status = Label(root, text = "Coded by: Ahmad Dawara", bd=2, relief=SUNKEN, anchor = E)
# -----------------------------------------------------
choc = IntVar()

rb_2g = ctk.CTkRadioButton(root, text="2G", variable=choc, value=1)
rb_3g = ctk.CTkRadioButton(root, text="3G", variable=choc, value=2)
rb_4g = ctk.CTkRadioButton(root, text="4G", variable=choc, value=3)

choc_cln = IntVar()
rb_2g3g = ctk.CTkRadioButton(root, text="2G / 3G", variable=choc_cln, value=2)
rb_4gg = ctk.CTkRadioButton(root, text="4G", variable=choc_cln, value=4)

umts=0
gsm=0
# -----------------------------------------------------
def chk():
    return
# ----------------------------------------------------
var1 = IntVar()
vr1 = ctk.CTkCheckBox(root, text='Extract Cell Name.',variable=var1, onvalue=1, offvalue=0, command=chk)
var2 = IntVar()
vr2 = ctk.CTkCheckBox(root, text='Sum TA Columns.',variable=var2, onvalue=1, offvalue=0, command=chk)

def cln():
    df = pd.read_excel(fp)
    if (var1.get() == 1):
        col_name=df.columns[3]
        #print(col_name)
        if (choc_cln.get() == 4):
            df['a'] = df[str(col_name)].str.slice(start=21)
            print(df.head())
            df[['r','x', 'y','z']] = df['a'].str.split(',',3, expand=True)
            print(df.head())
            df[['b','Cell']] = df['y'].str.split('=',1, expand=True)
            print(df.head())
            col_x_name=df.columns[2]
            df.rename(columns={str(col_x_name): 'Site'}, inplace=True)
            df = df.drop(['r','b','a','x','y','z'], axis=1, errors='ignore')
            col_x_name=df.columns[2]
            print(df.head())
        else:
            if 'TRX' in df.columns:
                df.drop(df['TRX'], axis=1,inplace=True, errors='ignore')
            df.rename(columns={str(col_name): 'Cells'}, inplace=True)
            col_name=df.columns[3]
            df['a'] = df[str(col_name)].str.slice(start=6)
            df[['Cell','b','c']] = df['a'].str.split(',',2, expand=True)
            df[str(col_name)]=df['Cell']
            df[['Site','x']] = df[str(col_name)].str.split('_',1, expand=True)
            scol_name=df.columns[2]
            df[str(scol_name)]=df['Site']
            df = df.drop(['b','a','c','x','Site','Cell'], axis=1, errors='ignore')
            df.rename(columns={str(scol_name): 'Site'}, inplace=True)
            df.to_csv('1-cleaned-ta.csv',index=False)

    if (var2.get() == 1):
        col_name=df.columns[3]
        cells_list=df[str(col_name)].unique()
        #print(cells_list)
        appended_data=list()
        for c in cells_list:
            dft=df[df[str(col_name)]==c]
            s1 = pd.Series([c],index=['Cell Name'])
            df_sum=dft.iloc[:,4:].sum()
            s1=s1.append(df_sum)
            appended_data.append(s1)
            
        df = pd.concat(appended_data,axis=1)
        df = df.transpose()

    #df = df.drop(['level_0'], axis=1, errors='ignore')    
    df.to_csv('cleaned-ta.csv',index=False)
    stats_cln.configure(text='Done.')
# -------------------------------------------------------------------
def opn_cln():
    global fp
    fp=filedialog.askopenfilename()
# -------------------------------------------------------------------
def opn_ecno():
    global fp_ecno
    fp_ecno=filedialog.askopenfilename()
# -----------------------------------------------------------------
def opn_kml():
    global filepath
    filepath=filedialog.askopenfilename()
# --------------------------------------------------------------------
def ecno_fun():
    
    # 17 columns 28  --- ecno
    # 29 to 40       --- rscp
    appended_data = list()
    out_file_name='3G-TA'
    ta_dist=[234,468,702,936,1170,1404,2340,3744,6084,8424,13104,17784]
    ta_dist.sort(reverse=True)
    g=3
    std = 25
    st_list=list()

    #filename = 'ta.csv'
    df = pd.read_csv(fp_ecno)
    df.iloc[:,4:] = df.iloc[:,4:].replace('NIL', 0)
    dfx=df.iloc[:,4:]
    all_zero_mask=(dfx != 0).any(axis=1) # Is there anything in this row non-zero?
    df=df.loc[all_zero_mask,:]
    #print(df.head())

    last_col=df.shape[1]
    print(df.head())
    df.iloc[:,4:] = df.iloc[:,4:].astype(int)
    #df_cut=df.iloc[:,4:16]                         # only TA
    #df_cut=df.iloc[:,16:28]                        # only EcNo
    #df_cut=df.iloc[:,28:]                          # only RSCP
    # ------------------------------------------------------------
    df_samples = df.iloc[0:,4:16].transpose()
    df_samples.reset_index(inplace=True)
    df_samples = df_samples.drop(['index'], axis=1, errors='ignore')
    df_samples=df_samples.iloc[::-1]
    df_samples.to_csv('df_samples.csv',index=False)

    df['TA Total']= df.iloc[:, 4:16].sum(axis=1)
    
    cells_list=df['name'].unique()
    
    #print(df_samples)
    df.iloc[:,4:16] = df.iloc[:,4:16].div(df['TA Total'], axis=0)
    df.iloc[:,4:16] = df.iloc[:,4:16].mul(100, axis=0)
    df.iloc[:,4:16] = df.iloc[:,4:16].round(1)
    # -------------------------------------------------------------


    df.iloc[:,16:28] = df.iloc[:,16:28].sub(49, axis=0)
    df.iloc[:,16:28] = df.iloc[:,16:28].div(2.2, axis=0)
    df.iloc[:,16:28] = df.iloc[:,16:28].round(1)

    df_ecno = df.iloc[0:,16:28].transpose()
    df_ecno.reset_index(inplace=True)
    df_ecno = df_ecno.drop(['index'], axis=1, errors='ignore')
    df_ecno=df_ecno.iloc[::-1]
    df_ecno.to_csv('df_ecno.csv',index=False)
    # -------------------------------------------------------------
    df.iloc[:,28:last_col] = df.iloc[:,28:last_col].sub(115, axis=0)
    df.iloc[:,28:last_col] = df.iloc[:,28:last_col].round(1)

    df_rscp = df.iloc[0:,28:last_col].transpose()
    df_rscp.reset_index(inplace=True)
    df_rscp = df_rscp.drop(['index'], axis=1, errors='ignore')
    df_rscp=df_rscp.iloc[::-1]
    df_rscp.to_csv('df_rscp.csv',index=False)
# -------------------------------------------------------------
    df.to_csv('ec.csv')

    l=len(ta_dist)
    for i in range(l):
        st_list.append(std)
    #print('length : ',len(st_list))
    l=l-1
    j=0
    p=0
    lst_samp=list()
    lst_ecno=list()
    lst_rscp=list()
    
    for c in cells_list:
        ta_acc_per=list()
        dft=df[df['name']==c]
        lst_per = list(dft.iloc[0,4:16])
        #print(lst_per)
        #lst_per.pop()
        #print(lst_per)
        dft.drop(dft.iloc[:,4:16], inplace = True, axis = 1)
        #dfss=df_samples.iloc[:,j]
        p=p+1
        lst_dfss = list(df_samples.iloc[:,j])
        lst_samp = [*lst_samp,*lst_dfss]

        lst_dfecno = list(df_ecno.iloc[:,j])
        lst_ecno = [*lst_ecno,*lst_dfecno]

        lst_dfrscp = list(df_rscp.iloc[:,j])
        lst_rscp = [*lst_rscp,*lst_dfrscp]

        dfta = pd.DataFrame({'TA Percent %':lst_per})
        ta_per_list = dfta['TA Percent %'].tolist()
        len_lst=len(ta_per_list)
        #print(ta_per_list)
        #print(len_lst)
        x=0
        for x in range(len_lst):
            #print(x)
            if x==0:
                q=ta_per_list[0]
            else:
                q=q+ta_per_list[x]
            ta_acc_per.append(q)

        #print(ta_acc_per)
        dfta_acc = pd.DataFrame({'TA Acc. Percent %':ta_acc_per})
        dfta_acc['TA Acc. Percent %'] = dfta_acc['TA Acc. Percent %'].values[::-1]
        dfta['TA Percent %'] = dfta['TA Percent %'].values[::-1]
        dft=dft.append([dft]*l,ignore_index=True)
        #print(dft.head())
        dff = pd.DataFrame({'col':ta_dist})
        dfl = pd.DataFrame({'s':st_list})
        df_temp=pd.concat([dft,dfta,dfta_acc,dff,dfl],axis=1)
        #print(df_temp.head())
        appended_data.append(df_temp)
        j=j+1

    app_df = pd.concat(appended_data,axis=0)
    app_df=app_df.reset_index()
    dfx_samples = pd.DataFrame({'Samples':lst_samp})
    dfx_ecno = pd.DataFrame({'ECNO':lst_ecno})
    dfx_rscp = pd.DataFrame({'RSCP':lst_rscp})
    #dfx_samples['Samples'] = dfx_samples['Samples'].values[::-1]
    #print(dfx_samples)
    app_df=pd.concat([app_df,dfx_samples,dfx_ecno,dfx_rscp],axis=1)
    #app_df['TA Percent %'] = app_df['TA Percent %'].astype(str)+ ' %'
    #app_df['TA Acc. Percent %'] = app_df['TA Acc. Percent %'].astype(str)+ ' %'
    app_df.rename(columns={'col': 'dis'}, inplace=True)
    app_df.rename(columns={'s': 'sd'}, inplace=True)
    app_df=app_df.reset_index()

    app_df = app_df.drop(['index','level_0'], axis=1, errors='ignore')
    app_df=app_df.fillna(0)
    app_df.to_csv('app_df.csv',index=False)
    #print(app_df)
    create_sector_3g(app_df,'x','y','angle','dis','sd',g,name='name',output=out_file_name)
    stats_ecno.configure(text='Done.')
    
# --------------------------------------------------------------------

def kml_fun():
    e=0
    umts=0
    gsm=0
    out_file_name='x'
    appended_data = list()
    if(choc.get()==1):
        gsm=1
        out_file_name='2G-TA'
        ta_dist=[550,1100,1650,2200,2750,3300,3850,4400,4950,5500,6050,6600,7150,7700,8250,8800,9350,9900,10450,11000,11550,12100,12650,13200,13750,14300,14850,15400,15950,16500,17600,18700,19800,20900,22000,24750,27500,30250,33000,35000]
        g=2
    elif(choc.get()==2):
        umts=1
        out_file_name='3G-TA'
        g=3
        ta_dist=[234,468,702,936,1170,1404,2340,3744,6084,8424,13104,17784]

    elif(choc.get()==3):
        ta_dist=[156,234,546,1014,1950,3510,6630,14430]
        gsm=0
        umts=0
        out_file_name='4G-TA'
        g=4

# --------------------------------------------------------------------------------
    ta_dist.sort(reverse=True)
    std = 25
    st_list=list()

    #filename = 'ta.csv'
    df = pd.read_csv(filepath)
    df.iloc[:,4:] = df.iloc[:,4:].replace('NIL', 0)
    dfx=df.iloc[:,4:]
    all_zero_mask=(dfx != 0).any(axis=1) # Is there anything in this row non-zero?
    df=df.loc[all_zero_mask,:]
    #print(df.head())

    last_col=df.shape[1]
    df.iloc[:,4:] = df.iloc[:,4:].astype(int)
    df_samples = df.iloc[0:,4:].transpose()
    df_samples.reset_index(inplace=True)
    df_samples = df_samples.drop(['index'], axis=1, errors='ignore')
    df_samples=df_samples.iloc[::-1]
    df_samples.to_csv('df_samples.csv',index=False)

    df['TA Total']= df.iloc[:, 4:last_col].sum(axis=1)

    cells_list=df['name'].unique()
    
    #print(df_samples)
    df.iloc[:,4:] = df.iloc[:,4:].div(df['TA Total'], axis=0)
    df.iloc[:,4:] = df.iloc[:,4:].mul(100, axis=0)
    df.iloc[:,4:] = df.iloc[:,4:].round(1)
    
    l=len(ta_dist)
    for i in range(l):
        st_list.append(std)
    #print('length : ',len(st_list))
    l=l-1
    j=0
    p=0
    lst_dfsss=list()
    
    for c in cells_list:
        ta_acc_per=list()
        dft=df[df['name']==c]
        lst_per = list(dft.iloc[0,4:last_col])
        #lst_per.pop()
        dft.drop(dft.iloc[:,4:last_col], inplace = True, axis = 1)
        #dfss=df_samples.iloc[:,j]
        p=p+1
        lst_dfss = list(df_samples.iloc[:,j])
        lst_dfsss = [*lst_dfsss,*lst_dfss]
        dfta = pd.DataFrame({'TA Percent %':lst_per})
        ta_per_list = dfta['TA Percent %'].tolist()
        len_lst=len(ta_per_list)
        x=0
        for x in range(len_lst):
            #print(x)
            if x==0:
                q=ta_per_list[0]
            else:
                q=q+ta_per_list[x]
            ta_acc_per.append(q)

        #print(ta_acc_per)
        dfta_acc = pd.DataFrame({'TA Acc. Percent %':ta_acc_per})
        dfta_acc['TA Acc. Percent %'] = dfta_acc['TA Acc. Percent %'].values[::-1]
        dfta['TA Percent %'] = dfta['TA Percent %'].values[::-1]
        dft=dft.append([dft]*l,ignore_index=True)
        #print(dft.head())
        dff = pd.DataFrame({'col':ta_dist})
        dfl = pd.DataFrame({'s':st_list})
        df_temp=pd.concat([dft,dfta,dfta_acc,dff,dfl],axis=1)
        #print(df_temp.head())
        appended_data.append(df_temp)
        j=j+1

    app_df = pd.concat(appended_data,axis=0)
    app_df=app_df.reset_index()
    dfx_samples = pd.DataFrame({'Samples':lst_dfsss})
    #dfx_samples['Samples'] = dfx_samples['Samples'].values[::-1]
    #print(dfx_samples)
    app_df=pd.concat([app_df,dfx_samples],axis=1)
    #app_df['TA Percent %'] = app_df['TA Percent %'].astype(str)+ ' %'
    #app_df['TA Acc. Percent %'] = app_df['TA Acc. Percent %'].astype(str)+ ' %'
    app_df.rename(columns={'col': 'dis'}, inplace=True)
    app_df.rename(columns={'s': 'sd'}, inplace=True)
    app_df=app_df.reset_index()

    app_df = app_df.drop(['index','level_0'], axis=1, errors='ignore')
    app_df=app_df.fillna(0)
    app_df.to_csv('app_df.csv',index=False)
    #print(app_df)
    create_sector_kml(app_df,'x','y','angle','dis','sd',g,name='name',output=out_file_name)
    stats.configure(text='Done.')
# -------------------------------------------------------------
b_kml=ctk.CTkButton(root, text="Generate KML" ,command=kml_fun)
b_browse_kml=ctk.CTkButton(root, text="Browse" ,command=opn_kml)
b_opn_cln=ctk.CTkButton(root, text="Browse" ,command=opn_cln)
b_browse_cln=ctk.CTkButton(root, text="Clean File" ,command=cln)

b_opn_ecno=ctk.CTkButton(root, text="Browse",command=opn_ecno )
b_ecno=ctk.CTkButton(root, text="Ec/No Analysis",command=ecno_fun)
# ----------------------------------------------------------
data_cln_title.grid(row = 1, column = 2,pady=10,padx=10)
b_opn_cln.grid(row = 2, column = 2, pady=10)
vr1.grid(row = 5, column = 2, pady=10)
vr2.grid(row = 6, column = 2, pady=10)
stats_cln.grid(row = 7, column = 2, pady=10, padx=10)
b_browse_cln.grid(row = 10, column = 2, pady=10)
rb_2g3g.grid(row = 3, column = 2, pady=10, padx=10)
rb_4gg.grid(row = 4, column = 2, pady=10, padx=10)
# ---------------------------------------------------------
l.grid(row = 1, column = 1, pady=10, padx=10)
ll.grid(row = 1, column = 0, pady=10, padx=10)

kml_title.grid(row = 1, column = 3,pady=10,padx=10)
stats.grid(row = 7, column = 3, pady=10, padx=10)

b_kml.grid(row =10, column = 3, pady=10)    
b_browse_kml.grid(row = 2, column = 3, pady=10)

rb_2g.grid(row = 3, column = 3, pady=10, padx=10)
rb_3g.grid(row = 4, column = 3, pady=10, padx=10)
rb_4g.grid(row = 5, column = 3, pady=10, padx=10)

#status.grid(row=6, column=0, columnspan=2, sticky=W+E)
# ---------------------------------------------------------
data_ecno_title.grid(row = 1, column = 4,pady=10,padx=10)
stats_ecno.grid(row = 7, column = 4, pady=10, padx=10)

b_opn_ecno.grid(row = 2, column = 4, pady=10)
b_ecno.grid(row = 10, column = 4, pady=10)
# ----------------------------------------------------------
app.mainloop()


