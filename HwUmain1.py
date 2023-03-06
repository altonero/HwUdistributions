from HwUclasses import *

file_path = '<MG5_output_dir>/Events/run_01/MADatNLO.HwU'

data = MADHwU(file_path,scale_var=True,pdf_var=False)

for kvar in data.list_kin_var:
    data.save_distr(kvar,norm=True,scalevar=True,path_save='<where_to_save>')
    
