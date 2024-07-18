# -*- coding: utf-8 -*-
"""
PUMAT is an interfacing code to run UMAT constitutive models from python using
IncrementalDriver (r).
This code was developed by Luis Zambrano-Cruzatty.
"""
import numpy as np
import matplotlib.pyplot as plt
from frake import FileFunctions as FF
from frake import GraphFunctions as GF
from frake import ModifierFunctioins as MF
import subprocess
import os
import shutil










#The following is a function that generates the input files for NorSand model
def SSMCVMAT_Run(sigma, G, nu, c_p, c_r, phi_p, phi_r, psi_p, psi_r, eta, loads,\
                 alpha_G=0, alpha_K=0, alpha_chi=0, alpha_beta=0.0, refrate=0.0,\
                smooth=0, degree=0,\
                foldername="mymodel", outputfile="output", Plot=True):

    #__________________________________________________________________________
    #Step 0: prepares folder destination
    #__________________________________________________________________________
    # Get executable path
    full_path=os.getcwd()
    folderpath=r"%s\%s" %(full_path, foldername)
    #Delete folder if it exist
    if not(os.path.exists(foldername)):
            os.mkdir(foldername)

    exe_path=full_path #executable must be in the same folder
    print(exe_path)
    exe=r"%s\%s" %(exe_path, "incrementalDriver.exe")
    dll1=r"%s\%s" %(full_path, r"dlls\libifcoremd.dll")#After I installed OneAPI I need to put this dlls next to my exe file
                                                       #Not needed outside jupyter
    dll2=r"%s\%s" %(full_path, r"dlls\libifcoremdd.dll")#After I installed OneAPI I need to put this dlls next to my exe file
                                                       #Not needed outside jupyter
    # Copy the executable into the benchmark path
    shutil.copy(exe, folderpath)
    shutil.copy(dll1, folderpath)
    shutil.copy(dll2, folderpath)
    #_____________________________________________________________________

    #______________________________________________________________________
    #Step 1: create parameters.inp file
    #______________________________________________________________________
    f=open('%s\parameters.inp' %(folderpath), 'w+') #Create an empty file
    f.write('SSMC_VMAT\n')
    f.write('16\n')
    f.write('%s\n' % G)       # Shear Modulus
    f.write('%s\n' % nu)      # Poisson's ratio
    f.write('%s\n' % c_p)     # Peak cohession
    f.write('%s\n' % c_r)     # Residual cohession.
    f.write('%s\n' % phi_p)   # Peak friction in degrees
    f.write('%s\n' % phi_r)   # Residual friciton in degrees
    f.write('%s\n' % psi_p)   # peak dilation angle in degrees
    f.write('%s\n' % psi_r)   # peak dilation angle in degrees
    f.write('%s\n' % eta)     # softening rate
    f.write('%s\n' % alpha_G)   # Shear viscosity
    f.write('%s\n' % alpha_K)   # Bulk viscosity
    f.write('%s\n' % alpha_chi) # friction and cohession viscosity
    f.write('%s\n' % alpha_beta) # dilation viscosity
    f.write('%s\n' % refrate)   #Reference strain rate
    f.write('%s\n' % smooth) #Apply smoothening algorithm (false=0)
    f.write('%s\n' % degree) #Degree of smoothing
    f.close() #close file
    #_________________________________________________________________

    #_________________________________________________________________
    #Step 2: write initialconditions.inp file
    #_________________________________________________________________
    f=open('%s\initialconditions.inp' %(folderpath), 'w+') #Create an empty file
    f.write('6\n')
    f.write('%s\n' % sigma[0]) #Cell pressure
    f.write('%s\n' % sigma[1]) #Cell pressure
    f.write('%s\n' % sigma[2]) #Cell pressure
    f.write('%s\n' % sigma[3]) #shear
    f.write('%s\n' % sigma[4]) #shear
    f.write('%s\n' % sigma[5]) #shear
    f.write('23\n') #State parameters being stored
    for i in range(0,23):
        f.write('0\n') # zeroed state paramters
    f.close() #close file
    #___________________________________________________________________

    #___________________________________________________________________
    #Step 3: create test.inp file
    #___________________________________________________________________
    nloads=loads.total_loads()

    name_f='%s.txt' % outputfile #name of output files
    f=open('%s\\test.inp' %(folderpath), 'w+') #Create an empty file
    f.write('%s\n' % name_f)

    for i in range(nloads):
        if (loads.loads[i].path=='TX'):#Triaxial
            if (loads.loads[i].control=='E'):
                if (loads.loads[i].drain):
                    f.write('*TriaxialE1\n') # strain controlled CD test (need to generalize)
                    f.write('%s %s %s: %s\n' % (loads.loads[i].NSTEPS,loads.loads[i].MAXITER,\
                                                loads.loads[i].DTIME, loads.loads[i].INC) )#numerical values
                    f.write('%s\n'% loads.loads[i].load) #axial strain
                else:
                    f.write('*TriaxialUEq\n') # strain controlled CD test (need to generalize)
                    f.write('%s %s %s: %s\n' % (loads.loads[i].NSTEPS,loads.loads[i].MAXITER,\
                                                loads.loads[i].DTIME, loads.loads[i].INC) )#numerical values
                    f.write('%s\n'% loads.loads[i].load) #axial strain
            elif (loads.loads[i].control=='S'):
                if (loads.loads[i].drain):
                    f.write('*TriaxialS1\n') # strain controlled CD test (need to generalize)
                    f.write('%s %s %s: %s\n' % (loads.loads[i].NSTEPS,loads.loads[i].MAXITER,\
                                                loads.loads[i].DTIME, loads.loads[i].INC) )#numerical values
                    f.write('%s\n'% loads.loads[i].load) #axial strain
                else:
                    f.write('*TriaxialUq\n') # strain controlled CD test (need to generalize)
                    f.write('%s %s %s: %s\n' % (loads.loads[i].NSTEPS,loads.loads[i].MAXITER,\
                                                loads.loads[i].DTIME, loads.loads[i].INC) )#numerical values
                    f.write('%s\n'% loads.loads[i].load) #axial strain
#         elif (loads.loads[i].path=='SS'):#Simpleshear
#         elif (loads.loads[i].path=='REL'):#relaxation
#         elif (loads.loads[i].path=='CRE'):#creep
#         elif (loads.loads[i].path=='EDO'):#eodometric
#         elif (loads.loads[i].path=='CYC'):#cyclic
#         elif (loads.loads[i].path=='TRAN'):#transient

    f.close() #close file
    #___________________________________________________________________

    #___________________________________________________________________
    # Step 4: Run the code
    #___________________________________________________________________
    cmd=r"%s\incrementalDriver.exe" % (folderpath) #executable as comand
    print(cmd)
#     os.system('cmd %s "incrementalDriver"' %foldernamepath)
    process = subprocess.Popen(cmd, cwd = folderpath) #Runs comand in cmd
    process.wait() #Wait until it is finished
    #___________________________________________________________________

    #___________________________________________________________________
    # Step 5: Read data
    #___________________________________________________________________
    model_resutls, _, _=FF.OpenFromFolder(Path=folderpath, filetype='txt')#opens data
    #___________________________________________________________________

    #___________________________________________________________________
    #Step 6: Postprocess the results
    #___________________________________________________________________
    MF.DataOperation(model_resutls, '*', 'stran(1)', -100, 'Epsa') #axial strain in % and positive
    for frame in model_resutls:#Now compute invariants and write them
        Sig=[frame['stress(1)'], frame['stress(2)'], frame['stress(3)'], \
             frame['stress(4)'], frame['stress(5)'], frame['stress(6)']]
        q, p=Get_stress_invariants(Sig)
        frame['q']=q
        frame['p']=p

        Eps=[frame['stran(1)'], frame['stran(2)'], frame['stran(3)'], \
             frame['stran(4)'], frame['stran(5)'], frame['stran(6)']]
        Eps_q, Eps_v=Get_strain_invariants(Eps)
        frame['Epsq']=Eps_q*100 #In %
        frame['Epsv']=Eps_v*100 #in %
    #_____________________________________________________________________

    #_____________________________________________________________________
    # Step 7: Plot q vs epsa and epsv vs eps a
    #_____________________________________________________________________
    if (Plot):
        fig, axs=plt.subplots(2)
        xsize=3.4
        aspect_ratio=1.5
        ysize=2*xsize/aspect_ratio
        GF.PlotAll(model_resutls, ['1'], 'Epsa', 'q', xlabel=r'Axial strain ($\varepsilon_a$) [$\%$]'\
                 , ylabel=r'Deviatoric stress ($q$) [kPa]', hold=1, PlotName=axs[0], legendMode=False)
        GF.PlotAll(model_resutls, ['1'], 'Epsa', 'Epsv', xlabel=r'Axial strain ($\varepsilon_a$) [$\%$]'\
                 , ylabel=r'Vol. strain ($\varepsilon_v$) [$\%$]', hold=1, PlotName=axs[1], \
                   legendMode=False, xsize=xsize, ysize=ysize)
        plt.tight_layout()
    #_____________________________________________________________________

    return model_resutls
