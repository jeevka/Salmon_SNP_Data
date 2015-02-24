from __future__ import division
import sys
import re

#####################################################################################
############################### SUB PROGRAMS ########################################
#####################################################################################
def find_strand(temp):
    l = int(temp[0].split("_")[2])
    
    if int(temp[6]) > int(temp[7]):
        R1 = int(temp[7])
        R2 = int(temp[6])
        strand = "-"
    else:
        R1 = int(temp[6])
        R2 = int(temp[7])        
        strand = "+"
    
    return strand,R1+l,R1+l+1

def Calculate_QC(QRange,QL):
    dis = 0
    OL = 0
    HITS = []
    
    for i in xrange(len(QRange)):
	temp1 = QRange[i].split("-")

	###########################################
	# Length of the hit must be >=100 basepairs
	###########################################
        if int(temp1[1]) > int(temp1[0]):
	    HITS = HITS + range(int(temp1[0]),int(temp1[1])+1)
	else:
	    HITS = HITS + range(int(temp1[1]),int(temp1[0])+1)

    HITS1 = list(set(HITS))
    HITS1.sort()
    l2 = len(HITS1)
    
    return l2/QL
    
#####################################################################################
############################### MAIN PROGRAM ########################################
#####################################################################################
F1 = open("BLAST_Results.out","r")

COV = {}; IDN = {}
N = 0
IDS = []
QL = {}; QRange = {}

#####################################################################################
# PART I: Cross checking with SNP data file for same Chromosome number.
#####################################################################################
SNP_Chr = {}
F2 = open("SNP_5K_2.csv","r")
for i in F2:
    temp = i.split()
    if len(temp) == 9:
        SNP_Chr[temp[7]] = temp[0]
        
    elif len(temp) == 6:
        SNP_Chr[temp[4]] = temp[0]

F1.seek(0)
####################################################################################
# Part II: Print all the "highly mapped" hits
####################################################################################
for i in F1:
    temp = i.split()
    QCOV = (1 + int(temp[5]) - int(temp[4]))/int(temp[3])
    ID = temp[0].split("_")[1]
    
    if float(temp[2]) >= 80 and QCOV >= 0.75 and SNP_Chr[ID] == temp[1]:
        strand,R1,R2 = find_strand(temp)
        txt = temp[1] + "\t" + "Salmon" + "\t" + "SNP" + "\t" + str(R1) + "\t" + str(R2) + "\t.\t" + strand + "\t.\t" + "ID=" + ID + ";Name="+ ID
        print txt
        N += 1
        IDS.append(ID)
    else:
        if SNP_Chr[ID] == temp[1]:
            if QRange.has_key(temp[0]):
                QRange[temp[0]].append(temp[4] + "-" + temp[5])
            else:
                QRange[temp[0]] = [temp[4] + "-" + temp[5]]
        
    QL[temp[0]] = int(temp[3])

F1.seek(0)


#####################################################################################
# Part III: Hits which are broken into two
#####################################################################################
Temp_IDS = []
for i in F1:
    temp = i.split()
    ID = temp[0].split("_")[1]
    if not ID in IDS and SNP_Chr[ID] == temp[1]:
        if len(QRange[temp[0]]) == 2:
            QC = Calculate_QC(QRange[temp[0]],QL[temp[0]])
            if QC >= 0.75 and ID not in Temp_IDS:
                strand,R1,R2 = find_strand(temp)
                txt = temp[1] + "\t" + "Salmon" + "\t" + "SNP" + "\t" + str(R1) + "\t" + str(R2) + "\t.\t" + strand + "\t.\t" + "ID=" + ID + ";Name="+ ID 
                Temp_IDS.append(ID)
                print txt
        else:
            pass
            #print i.strip()
sys.exit()
#####################################################################################
# Part III: Take care of the other results
#####################################################################################
QC = Calculate_QC(QRange,IDS)

sys.exit()

#####################################################################################
# Part IV: 
#####################################################################################
for i in F1: 
    temp = i.split()
    if not temp[0] in IDS:
        
        print i.strip()

print N
F1.close()
