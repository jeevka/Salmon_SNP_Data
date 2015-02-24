import sys
import re

#####################################################################
##################### SUB PROGRAMS ##################################
#####################################################################
def find_SNP_position(seq):
    try:
        p = re.compile(r"(\w+)(\[)(\w)(\/)(\w)\](\w+)")    
        g = re.search(p,seq)
        SNP = g.group(3)
    except:
        try:
            p = re.compile(r"(\[)(\w)(\/)(\w)\](\w+)")    
            g = re.search(p,seq)
            SNP = g.group(2)
        except:
            p = re.compile(r"(\[)(\w)(\/)(\w)\]")    
            g = re.search(p,seq)
            SNP = g.group(3)
            
    S1 = seq.split("[")[0]
    S2 = seq.split("]")[1]
    new_seq = S1 + SNP + S2
    pos = 1 + seq.index("[")
    
    return new_seq,pos

###################################################################
####################### MAIN PROGRAM ##############################
###################################################################
F1 = open("SNP_5K_2.csv","r")
F2 = F1.readlines()
N = 0; M = 0
for i in xrange(1,len(F2)):
    N += 1
    temp = F2[i].split()
    #print temp
    if len(temp) == 9:
        Seq,pos = find_SNP_position(temp[8])
        seq_name = ">" + temp[0] + "_" + temp[7] + "_" + str(pos)
        print seq_name
        print Seq
    elif len(temp) == 6:
        Seq,pos = find_SNP_position(temp[5])
        seq_name = ">" + temp[0] + "_" + temp[4] + "_" + str(pos)
        print seq_name
        print Seq
    else:
        print temp
        print len(temp)