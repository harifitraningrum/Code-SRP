#matriks rating
import csv,math

numOfUserRating = []

#read data from csv file
with open('matriksMovieLens.csv') as value:
    reader= csv.reader(value)
    header=next(reader)
    data = []
    matriks = []
    ind = 0
    for row in reader:
      jmlRatingOfUser = 0
      data.append(row)
      for i in range(1, len(data[ind])): #format string value to int
          data[ind][i] = int(data[ind][i])
          if (data[ind][i] != 0):
            jmlRatingOfUser +=1
      numOfUserRating.append(jmlRatingOfUser)
      matriks.append(data[ind])
      ind +=1
user = len(matriks)
item = len(matriks[0])

print("User\t"+"".join(["item"+str(itemn+1)+"\t" for itemn in range(item-1)]))
dataToyDict={}
for i in matriks:
  dataToyDict[i[0]] = i[1:]
  print(str(i[0])+"\t" + "".join( [str(d)+"\t" for d in dataToyDict[i[0]] ]))


#vector mean rating
meanRating = []
dictMeanRating = {}
print ('user\tphi')
for i in range(user):
  mean = sum(matriks[i][1:]) / numOfUserRating[i]
  meanRating.append(mean)
  dictMeanRating[str(matriks[i][0])] = meanRating[i] 
  mean = 0
  print (str(matriks[i][0])+'\t',str(meanRating[i])[:6])

#mean centered
meanCentered = []
indRatedItem = []
for i in range(user):
  centered = 0
  tempValCent = []
  tempIndRatedItem = []
  for j in range(1,item):
    if (matriks[i][j] != 0):
      centered = matriks[i][j] - meanRating[i]
      tempIndRatedItem.append(j)
    else:
      centered = 0
    tempValCent.append(centered)
  meanCentered.append(tempValCent)
  indRatedItem.append(tempIndRatedItem)

dictMeanCentered = {}

index = 0
for i in dataToyDict.keys():
  dictMeanCentered[i] =meanCentered[index]
  index+=1 

print("user\t"+"".join(["item"+str(i+1)+"\t\t" for i in range(item-1)]))
for i in dictMeanCentered.keys():
  print (str(i)+"\t"+ "".join([str(meanC)[:6]+"\t\t" for meanC in dictMeanCentered[i] ]) )
#print(dictMeanCentered)



#sim item
simItem = []
sameInd = []
indSim = 0
for i in range(item-1):
  temSim = []
  for j in range(item-1):
    if (i<j):
      #print ('=> ',i, ' , ', j )
      irisan = []
      ind = 0
      for k in range(user):
        if (matriks[k][i+1] !=0 and matriks[k][j+1] !=0):
          irisan.append(ind)
        ind +=1
      #print (irisan)

      numerator = 0
      sumDenom1 = 0
      sumDenom2 = 0
      for y in range(len(irisan)):
        indIrisan = irisan[y]
        #print ('indIrisan ', indIrisan)
        tmpNumerator = meanCentered[indIrisan][i] * meanCentered[indIrisan][j]
        #print (meanCentered[indIrisan][i] ,' * ', meanCentered[indIrisan][j])
        numerator += tmpNumerator
        denom1 = meanCentered[indIrisan][i]**2
        #print ('denom1 = ', meanCentered[indIrisan][i],' **2')
        denom2 = meanCentered[indIrisan][j]**2
        #print ('denom2 = ', meanCentered[indIrisan][j],' **2')
        sumDenom1 += denom1
        sumDenom2 += denom2
      denom = math.sqrt(sumDenom1) * math.sqrt(sumDenom2)
      #print ('<==> ', numerator ,' / ', denom, ' = ',numerator/denom)
      if (denom == 0):
        hasil = 0
      else:
        hasil = numerator / denom
      indSim +=1
      temSim.append(hasil)

    elif (i == j):
      temSim.append(1)
    else :
      temSim.append(0)
  simItem.append(temSim)

for i in range(item-1):
    for j in range(i, item-1):
        simItem[j][i] = simItem[i][j]
  
print ("\n")
print ("item\t"+"".join(["item"+str(i+1)+"\t" for i in range(item-1)]))
dictSimItem = {}
for i in range (item-1):
    
    print (str(i+1)+"\t" + "".join([str(sim)[:6]+"\t" for sim in simItem[i]]))

for i in range (item-1):
  dictSimItem[i+1] = {}
  for j in range (item-1):
    dictSimItem[i+1][j+1] = simItem[i][j]


    
#smooting
#find top-2 sim item
top2 = []
for i in range(len(simItem)):
    MAX = [[0, 0], [0, 0]]
    for j in range(len(simItem[0])):
        if i != j:
            if simItem[i][j] > MAX[0][0]:
                MAX[0][0] = simItem[i][j]
                MAX[0][1] = j
            MAX.sort()
    INDEX = [MAX[0][1], MAX[1][1]]
    INDEX.sort()
    top2.append(INDEX)
dictSmoothing = {}
matriksSmooth = matriks.copy()
for i in range(user):
    smooth = 0
    for j in range(item-1):
      if (matriksSmooth[i][j+1] == 0):
        pembilang = (float(matriksSmooth[i][top2[j][0]+1]))*(simItem[j][top2[j][0]]) + (float(matriksSmooth[i][top2[j][1]+1])*simItem[j][top2[j][1]])
        penyebut = abs(simItem[j][top2[j][0]]) + abs(simItem[j][top2[j][1]])
        smooth = pembilang / penyebut
        matriksSmooth[i][j+1] = smooth

    dictSmoothing[matriksSmooth[i][0]] = matriksSmooth[i][1:]
#print (dictSmoothing)
print ("user\t"+"".join(["item"+str(i+1)+"\t" for i in range(10)]))
for i in dictSmoothing.keys():
  print(str(i) +"\t" + "".join([str(s)[:7]+"\t" for s in dictSmoothing[i]]) )



#kmean cluster
import math  

class kmeanC():
    def __init__(self, data, m, n, delimiterData, numCluster):
        self.__numCluster = numCluster
        self.__delimiterData = delimiterData
        self.__nUser = m
        self.__nItem = n
        self.dataDict = data
        self.dataCluster = {}
        self.centeroid = []
        self.similarityWithCenteroid = {}
        self.main()

    # method Helper -- Avarage
    def __avg(self, arr):
        dump = 0
        for i in range(len(arr)):
            dump += arr[i]
        if len (arr) != 0 :
            return dump / len(arr)
        else : 
            return 0
        
    #method helper -- ed
    def ed(self, data, centeroid):
        ed = 0
        for i in range(len(data)):
            ed += pow(data[i] - centeroid[i], 2)
        return pow(ed, 0.5) 

    def calCenteroid(self, first):
        if first == True:
            n = 0
            for c in self.dataDict.keys():
                n +=1
                if n <= self.__numCluster:
                    self.centeroid.append(self.dataDict[c])
                    self.dataCluster["c"+str(n)] = []
                else :
                    break
        else :
            indexCen = 0
            self.centeroid = [];
            for cluster in self.dataCluster.keys():
                tempClus = []
                for i in range (self.__nItem):
                    tempX = []
                    for data in self.dataCluster["c"+str(indexCen+1)]:
                        tempX.append(self.dataDict[data][i])
                    tempClus.append(self.__avg(tempX))
                self.centeroid.append(tempClus.copy())
                indexCen += 1
        res = self.centeroid.copy()
        return res
    
    def clustering(self):
            #clearing data in dict cluster
            for clear in self.dataCluster.keys() :
                self.dataCluster[clear].clear()

            #calculate sim and place data in cluster
            for data in self.dataDict.keys():
                compare = []
                for centeroid in self.centeroid:
                    compare.append(self.ed(self.dataDict[data], centeroid))
                self.similarityWithCenteroid[data] = compare
                maxSim = compare.index(min(compare))
                self.dataCluster["c"+str(maxSim+1)].append(data)


    
    def printstep(self, n):
        print("iterasi-"+str(n)+"\n")
        # writing all data
        print("Data After Smoothing \n")
        print("User \t|\t", end="")
        print("".join(["item"+str(n+1)+"\t|\t" for n in range(self.__nItem)]) + "\n")
        for user in self.dataDict.keys():
            print( str(user) +" \t|\t", end="")
            for item in self.dataDict[user]:
                print( str(item)[:6] +" \t|\t", end="")
            print("\n")
        print("\n")

        # writing centeroid
        print("Centeroid : \n")
        c = 1
        centeroidS = ""
        cluster = ""
        for centeroid in self.centeroid:
            cluster = "c"+str(c)
            centeroidS += cluster+" : "+str(centeroid) +"\n"
            c+=1
        print(centeroidS)
        print("\n")

        #writing similarity
        print("Ecluidian Distance Data with Centeroid \n")
        print("User \t|\t", end="")
        print("".join(["c"+str(n+1)+"\t|\t" for n in range(self.__numCluster)]) + "\n")
        for user in self.similarityWithCenteroid.keys():
            print( str(user) +" \t|\t", end="")
            for item in self.similarityWithCenteroid[user]:
                print( str(item)[:6] +" \t|\t", end="")
            print("\n")
        print("\n")

        #writing cluster
        print("Clustering Data \n")
        for data in self.dataCluster.keys():
            print(str(data)+"\t|\t", end="")
            print("".join([str(user)+"\t|\t" for user in self.dataCluster[data]]), end="")
            print("\n")

    def oldCenteroid(self):
        data = []
        for i in self.centeroid:
            data.append(i)
        return data

    def main(self):
        iter = 1
        oldCenteroid = []
        newCenteroid = self.calCenteroid(True)
        self.clustering()
        self.printstep(iter)
        iter+=1
        index = 0;
        while (oldCenteroid != newCenteroid):
            oldCenteroid = self.oldCenteroid()
            newCenteroid = self.calCenteroid(False)
            self.clustering()
            self.printstep(iter)
            iter+=1
            index += 1
    

kmean = kmeanC(dictSmoothing, 943, 1682 , ";", 3)




#sim user w/ centroid
def simmilarity (a , b):
  pembilang = 0
  penyebuta = 0
  penyebutb = 0
  for i in range(len(a)):
    pembilang += a[i] * b[i]
    penyebuta += a[i] * a[i] 
    penyebutb += b[i] * b[i]
  result = pembilang / (pow(penyebuta,0.5) * pow(penyebutb,0.5))
  return result
centeroid = kmean.centeroid
cluster = kmean.dataCluster
simUserAandC = {}
for clus in cluster.keys():
  for user in cluster[clus]:
    simOnUser = []
    simUserAandC[user] = []
    for center in centeroid :
      simOnUser.append(simmilarity(kmean.dataDict[user],center))
    simUserAandC[user] = simOnUser

print ("user\t\t" + "".join(["Centeroid-"+str(i+1)+"\t\t\t" for i in range (len(centeroid))]))
for i in simUserAandC.keys():
  print(str(i)+"\t\t"+ "".join( [str(sim)+"\t\t" for sim in simUserAandC[i]] ))

#max sim
maxSimAC = {}
print ("user\tmost sim cluster")
for data in simUserAandC.keys():
  maxSimAC[data] = "c"+str(simUserAandC[data].index(max(simUserAandC[data]))+1)
  print(str(data)+"\t"+str(maxSimAC[data])+"\n")






#sum au dg 0,8
def Wuk (rate, lamda):
  if rate == 0 :
    return 1 - lamda
  else :
    return lamda

def simmilarityWithWeright (a, u, lamda):
  pembilang = 0
  penyebuta = 0
  penyebutb = 0
  for i in range(len(dictMeanCentered[a])):
    pembilang += dictMeanCentered[a][i] * Wuk(dataToyDict[u][i], lamda) * dictMeanCentered[u][i]
    penyebuta +=  pow(dictMeanCentered[a][i],2)
    penyebutb +=  pow(dictMeanCentered[u][i],2) * Wuk(dataToyDict[u][i], lamda)
  result = pembilang / (pow(penyebuta,0.5) * pow(penyebutb,0.5))
  return result
  
dictSim_au = {}
for a in maxSimAC.keys():
  dictSim_au[a] = {}
  for u in (kmean.dataCluster[maxSimAC[a]]):
    dictSim_au[a][u] = simmilarityWithWeright(a,u, 0.8) 

for user in dictSim_au.keys():
  print ("userA\t"+"".join(["user"+str(i)+"\t" for i in dictSim_au[user].keys() ]))
  print (user+"\t"+"".join([str(i)[:7]+"\t" for i in dictSim_au[user].values() ]))
  print("\n")







#clique
def delSelfUserData(key ,data):
  temp = []
  temp2 = []
  temp3 = []
  for i in data.keys():
    if key != i :
      temp.append(data[i])
    temp2.append(data[i])
    temp3.append(i)
  return temp,temp2, temp3

clique_a = {}
for a in dictSim_au.keys():
  tempData = delSelfUserData(a, dictSim_au[a])
  clique_a[a] =[max(tempData[0]), tempData[2][tempData[1].index(max(tempData[0]))]]
print (clique_a)

clique_i = {}
for item in dictSimItem.keys():
  tempData = delSelfUserData(item, dictSimItem[item])
  clique_i[str(item)] =[max(tempData[0]), tempData[2][tempData[1].index(max(tempData[0]))]] 

print (clique_i)

#find user target
user_active = {}
for i in dataToyDict.keys():
  user_active[i] = []
  for rate in range (len(dataToyDict[i])):
    if dataToyDict[i][rate] == 0:
      user_active[i].append(str(rate+1))
  if user_active[i] == []:
    del user_active[i]
print (user_active)





#collaborative Prediction
def w(cliqueA, cliqueI):
  return cliqueA/(cliqueA+cliqueI)

def R_A_I (user_a, item_i):
  weight = w(clique_a[user_a][0], clique_i[item_i][0])
  #kanan
  VecRA = dictMeanRating[user_a]
  wuk = Wuk(dataToyDict[ clique_a[user_a][1] ][int(item_i)-1], 0.8)
  Sau = clique_a[user_a][0]
  meanCenteredRating = dictMeanCentered[clique_a[user_a][1]][int(item_i)-1]
  #kiri
  waj = Wuk(dataToyDict[user_a][clique_i[item_i][1] -1 ], 0.8)
  Sij = clique_i[item_i][0]
  Raj = dataToyDict[user_a][clique_i[item_i][1]-1]
  #hasil
  hasil = (weight*( VecRA + (wuk*Sau*meanCenteredRating/abs(wuk*Sau))))+ ((1 - weight) * (waj*Sij*Raj/abs(waj*Sij)))
  return hasil 

for a in user_active.keys():
  for item in user_active[a]:
    Prediction = R_A_I(a, item)
    print ("R("+str(a)+","+str(item)+") : "+ str(Prediction))







#evaluasi
for fold in range(1,6):
  globals()['matTest%s' % fold] = []
  globals()['matTrain%s' % fold] = []

  #raed data testing 20%
  with open('fold' + str(fold) + 'Test.txt') as value:
      reader= csv.reader(value)
      data = []
      matriks = []
      ind = 0
      for row in reader:
          isi = row[0].split('\t')
          data.append(isi)
          for i in range(len(data[ind])):
            data[ind][i] = int(data[ind][i])
          matriks.append(data[ind])
          ind +=1

  #read data training 80%
  with open('fold' + str(fold) + 'Train.txt') as value:
      reader= csv.reader(value)
      data = []
      matriksTrain = []
      ind = 0
      for row in reader:
          isi = row[0].split('\t')
          data.append(isi)
          for i in range(len(data[ind])):
            data[ind][i] = int(data[ind][i])
          matriksTrain.append(data[ind])
          ind +=1

  for i in range(user):
    tmp = []
    for j in range(item-1):
      tmp.append(0)
    globals()['matTest%s' % fold].append(tmp)

  for x in range(user):
    tmp = []
    for y in range(item-1):
      tmp.append(0)
    globals()['matTrain%s' % fold].append(tmp)

  #add value test
  for i in range(len(matriks)):
    globals()['matTest%s' % fold][matriks[i][0]-1][matriks[i][1]-1] = matriks[i][2]

  #add value train
  for i in range(len(matriksTrain)):
    globals()['matTrain%s' % fold][matriksTrain[i][0]-1][matriksTrain[i][1]-1] = matriksTrain[i][2]

for i in range(1,6):
  print ('matriks train fold '+str(i))
  print("".join(["item"+str(itemn+1)+"\t" for itemn in range(item)]))
  for j in range(item-1):
    print (str(globals()['matTrain%s' % i][0][j])+'\t', end='')
  print ('\n')

print()
print()

for i in range(1,6):
  print ('matriks test fold '+str(i))
  print("".join(["item"+str(itemn+1)+"\t" for itemn in range(item)]))
  for j in range(item-1):
    print (str(globals()['matTest%s' % i][0][j])+'\t', end='')
  print ('\n')
