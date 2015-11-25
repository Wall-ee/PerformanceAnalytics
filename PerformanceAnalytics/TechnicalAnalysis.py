import pandas as pd
from pandas import DataFrame as df
def ERi(closeprice,ERlength):
  absdailydiff=abs(closeprice.diff(1))

  Directioni=closeprice.diff(ERlength-1)
  Volatilityi=pd.rolling_sum(absdailydiff,ERlength)
  eri=abs(Directioni/Volatilityi)
  return eri



def AMAi(Pricevector,FastMaLength,SlowMALength,ERlength,depth):
      Fast=2/(FastMaLength+1)
      Slow=2/(SlowMALength+1)
      Pricevector=Pricevector.set_index('settledate')
      closeprice=Pricevector['close']['2005-04-08':]
      ERI=ERi(closeprice,ERlength)
      Ci=(ERI*(Fast-Slow)+Slow)**depth
      #amai=df(columns=closeprice.columns)
      #amai=df()
      #amai=df(columns=['close'],index=Pricevector['close'][ERlength])
      #amai=closeprice[:'2006-4-19']
      amai=closeprice
      #for i in closeprice['2006-4-20':].index:
      for i in range(ERlength,len(closeprice)):
          amai[i]=amai[i-1]+Ci[i]*(closeprice[i]-amai[i-1])

          # newAMAi=pd.Series(amai.tail(1)+Ci[i]*(closeprice[i]-amai.tail(1)))
          # newAMAi.index=[i]
          # amai=amai.append(newAMAi)
      return amai


import getRecord as gr
indexPrice = gr.getRecord(201023,'23020')

aa =AMAi(indexPrice,1,20,250,2)
print(aa)


