import pandas as pd
import matplotlib.pyplot as plt


class MADHwU:

    # Class varaibles

    list_columns = []
    list_kin_var = []

    # Initializing
    def __init__(self,file_path,scale_var=True,pdf_var=False):
        
        self.file_path = file_path
        self.scale_var=scale_var
        self.pdf_var=pdf_var
        
        # Reading .HwU file as pandas dataframe
        self.df1 = pd.read_csv(self.file_path, sep="&")
        self.df2 = self.df1.iloc[: , :1] 
        print('Importing .HwU file with pandas...')
        
        # Extracting list of column names
        col = list(self.df1.columns)
        del col[0]
        col = [s.strip() for s in col]
        self.list_columns = col 
        self.len_columns = len(col)
        # Adjust columns for case of no scale and no PDF variation
        if self.len_columns == 5:
            self.list_columns = self.list_columns[:-1]
            self.len_columns = len(col)-1
        
                   
        if (scale_var==False and pdf_var==False):
            if self.len_columns != 4:
                print('Something wrong with number of colums. Check scale_/pdf_variation flags or .HwU file!')
            else:
                print('No scale_variation and no PDF_variation.\nNumber of columns =', self.len_columns,'.')
                
        if (scale_var==True and pdf_var==False):
            if self.len_columns != 16:
                print('Something wrong with number of colums. Check scale_/pdf_variation flags or .HwU file!')
            else:
                print('Only scale_variation.\nNumber of columns =', self.len_columns,'.')
        
        if (scale_var==False and pdf_var==True):
            if self.len_columns <= 16:
                print('Something wrong with number of colums. Check scale_/pdf_variation flags or .HwU file!')
            else:
                self.pdf_eing_pairs = int((self.len_columns-8)/2)
                print('Only PDF_variation.\nNumber of columns =', self.len_columns ,'. PDF eigenvecotr pairs:',self.pdf_eing_pairs,'.')
                
        if (scale_var==True and pdf_var==True):
            if self.len_columns <= 16:
                print('Something wrong with number of colums. Check scale_/pdf_variation flags or .HwU file!')
            else:
                self.pdf_eing_pairs = int((self.len_columns-20)/2)
                print('Scale and PDF variation.\nNumber of columns =', self.len_columns ,'. PDF eigenvecotr pairs:',self.pdf_eing_pairs,'.')
                    
                    
        # Extracting kinematic variables
        lkin = []
        for i in range(len(self.df2)):
            row = self.df2['##'][i]
            if '<histogram>' in row:
                # Removing Initial word <histogram> from row
                res = row.split(' ', 1)[1]
                x = res.split("|")
                y = [s.strip() for s in x[0].split("\"")]
                lkin.append(y[1])
        self.list_kin_var = lkin
        if len(self.list_kin_var) < 1:
            print('No kinematic variable detected. Check the .HwU file!')
        else:
            print('Number of kinematic variables =',len(self.list_kin_var),'.')
    

    # Printing column names
    def print_columns(self):
        if not self.list_columns:
            print('Empty list!\n')
        else:
            print('Printing column names:')            
            print(self.list_columns,'\n')    
    

    # Printing kinematic variable names
    def print_kvariables(self):
        if not self.list_kin_var:
            print('Empty list!\n')
        else:
            print('Printing kinematic variable names:')            
            print(self.list_kin_var,'\n') 


    # Creating kinematic variable dataframe
    def dfkin(self,kin_var):
        if kin_var not in self.list_kin_var:
            kin_varb = self.list_kin_var[0]
            print('Kinematic variable', kin_var, 'not found...using',kin_varb)
        else:
            kin_varb = kin_var

        for i in range(len(self.df2)):
            row = self.df2['##'][i]
            if '<histogram>' in row:
                res = row.split(' ', 1)[1]
                x = res.split("|")
                y = [s.strip() for s in x[0].split("\"")]
                if kin_varb == y[1]:
                    dfkv = self.df2.iloc[i+1:i+int(y[0])+1,:].reset_index(drop=True)
                
        dfkv['##'] = dfkv['##'].str.strip() 
        dfkv[self.list_columns]=dfkv['##'].str.split('  ', expand=True)
        del dfkv['##']
        
        dfkv['bin_c']=(dfkv[self.list_columns[1]].astype(float) +dfkv[self.list_columns[0]].astype(float))/2
    
        return dfkv, kin_varb


    def save_distr(self,kin_var,norm=True,scalevar=False,path_save=''):
        
        dfkv, kin_varb = self.dfkin(kin_var)
        
        if norm==True:
            df_save = dfkv[['bin_c',self.list_columns[2]]].astype(float)
            df_save['bin_min']=dfkv[self.list_columns[0]].astype(float)
            df_save['bin_max']=dfkv[self.list_columns[1]].astype(float)
            df_save['cental value/GeV'] = (dfkv[self.list_columns[2]].astype(float)/(dfkv[self.list_columns[1]].astype(float)-dfkv[self.list_columns[0]].astype(float))).round(8)
            #df_save[['bin_c','cental value/GeV']].to_csv('dist_cen_'+kin_varb.replace(" ", "")+'_binc_norm.dat', sep='\t',index=False,header=False)
            df_save[['bin_min','bin_max','cental value/GeV']].to_csv(path_save+'dist_cen_'+kin_varb.replace(" ", "")+'_edges_norm.dat', sep='\t',index=False,header=False)
            
        if norm==False:
            df_save = dfkv[['bin_c',self.list_columns[2]]].astype(float)
            df_save['bin_min']=dfkv[self.list_columns[0]].astype(float)
            df_save['bin_max']=dfkv[self.list_columns[1]].astype(float)
            #df_save[['bin_c',self.list_columns[2]]].to_csv('dist_cen_'+kin_varb.replace(" ", "")+'_binc_abs.dat', sep='\t',index=False,header=False)
            df_save[['bin_min','bin_max',self.list_columns[2]]].to_csv(path_save+'dist_cen_'+kin_varb.replace(" ", "")+'_edges_abs.dat', sep='\t',index=False,header=False)
        
        if self.scale_var==True and scalevar==True:
            
            if norm==True:
                df_save = dfkv[['bin_c',self.list_columns[5],self.list_columns[6]]].astype(float)
                df_save['bin_min']=dfkv[self.list_columns[0]].astype(float)
                df_save['bin_max']=dfkv[self.list_columns[1]].astype(float)
                df_save['min value/GeV'] = (dfkv[self.list_columns[5]].astype(float)/(dfkv[self.list_columns[1]].astype(float)-dfkv[self.list_columns[0]].astype(float))).round(8)
                df_save['max value/GeV'] = (dfkv[self.list_columns[6]].astype(float)/(dfkv[self.list_columns[1]].astype(float)-dfkv[self.list_columns[0]].astype(float))).round(8)
                #df_save[['bin_c','min value/GeV','max value/GeV']].to_csv('dist_mm_'+kin_varb.replace(" ", "")+'_binc_norm.dat', sep='\t',index=False,header=False)
                df_save[['bin_min','bin_max','min value/GeV','max value/GeV']].to_csv(path_save+'dist_mm_'+kin_varb.replace(" ", "")+'_edges_norm.dat', sep='\t',index=False,header=False)
                
            if norm==False:
                df_save = dfkv[['bin_c',self.list_columns[5],self.list_columns[6]]].astype(float)
                df_save['bin_min']=dfkv[self.list_columns[0]].astype(float)
                df_save['bin_max']=dfkv[self.list_columns[1]].astype(float)
                #df_save[['bin_c',self.list_columns[5],self.list_columns[6]]].to_csv('dist_mm_'+kin_varb.replace(" ", "")+'_binc_abs.dat', sep='\t',index=False,header=False)
                df_save[['bin_min','bin_max',self.list_columns[5],self.list_columns[6]]].to_csv(path_save+'dist_mm_'+kin_varb.replace(" ", "")+'_edges_abs.dat', sep='\t',index=False,header=False)
