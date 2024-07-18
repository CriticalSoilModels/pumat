import numpy as np

# post processing functions
def Get_stress_invariants(Sig):
    p=(Sig[0]+Sig[1]+Sig[2])/3.0 # Mean stress 1/3 tr(Sig)

    dev=Sig
    dev[0]=dev[0]-p
    dev[1]=dev[1]-p
    dev[2]=dev[2]-p #deviatoric stress tensor S

    norm=0
    for i in range(len(dev)):# S:S
        if (i<3):
            norm=norm+dev[i]**2
        else:
            norm=norm+2*dev[i]**2

    q=np.sqrt(3*norm/2) #sqrt(3/2 S:S)
    p=-p #Positive for compression
    return q, p

def Get_strain_invariants(Eps):
    eps_v=Eps[0]+Eps[1]+Eps[2]# vol strain tr(Eps)

    dev=Eps
    dev[0]=dev[0]-eps_v/3
    dev[1]=dev[1]-eps_v/3
    dev[2]=dev[2]-eps_v/3 #deviatoric strain tensor e

    print(dev)
    norm=0
    for i in range(len(dev)):# e:e
        if (i<3):
            norm=norm+dev[i]**2
        else:
            norm=norm+0.5*dev[i]**2 #UMAT convention is to use shear strain

    print(norm)
    eps_q=np.sqrt(2*norm/3) #sqrt(2/3 e:e)
    eps_v=-eps_v #Positive for compression
    return eps_q, eps_v

if __name__ == "__main__":
    strain = np.array([1,2, 3, 4, 5, 6])
    print(Get_strain_invariants(strain))
