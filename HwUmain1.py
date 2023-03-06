from HwUclasses import *

#file_path = 'ttbar_work/ppttx_testEWmodel_QCD/Events/run_03/MADatNLO.HwU'
file_path = 'ttbar_work/ppttx_fastnlo/Events/run_03/MADatNLO.HwU'

data = MADHwU(file_path,scale_var=True,pdf_var=False)

for kvar in data.list_kin_var:
    #data.save_distr(kvar,norm=True,scalevar=True,path_save='/home/atonero/Desktop/ONGOING/ttGKT/Results/MG5/QCDsm/MSHT20NNLO/pT/CMSll36/')
    data.save_distr(kvar,norm=True,scalevar=True,path_save='/home/atonero/Desktop/ONGOING/ttGKT/Results/MG5/QCDsm/CT18NNLO/Yt/CMSll36/')
    #data.save_distr(kvar,norm=True,scalevar=True,path_save='/home/atonero/Desktop/ONGOING/ttGKT/Results/MG5/QCD/CT18NNLO/Yt/CMSll36/')