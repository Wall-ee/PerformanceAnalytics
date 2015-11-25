import pandas as pd
from pandas import DataFrame as df
def ERi(closeprice,ERlength):
  absdailydiff=abs(closeprice.diff(1))
  #absdailydiff=abs(diff(closeprice,lag=1))
  Directioni=closeprice.diff(ERlength-1)
  # Volatilityi=absdailydiff#initalise
  # for (i in (1+ERlength):length(closeprice)){
  #   Volatilityi[i]=sum(absdailydiff[(i-ERlength):i])
  # }

  Volatilityi=pd.rolling_sum(absdailydiff,ERlength)
  #eri=Directioni
  #eri=abs(Directioni[(1+ERlength):length(closeprice)]/Volatilityi[(1+ERlength):length(closeprice)])
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
  amai=(Pricevector['close'][ERlength])
  for i in range(ERlength,len(closeprice)+1):
    amai=amai.tail(1)+Ci[i]*(closeprice[i]-amai.tail(1))
  return amai


import getRecord as gr
indexPrice = gr.getRecord(201023,'23020')

aa =AMAi(indexPrice,1,20,250,2)


