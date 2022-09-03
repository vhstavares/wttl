import pandas as pd 
import json
import numpy as np
from django.http import JsonResponse
from django.http import HttpResponse


def struct_data(request):
     urlContex = "https://mc3nt37jj5.execute-api.sa-east-1.amazonaws.com/default/hourth_desafio"
     df = pd.read_json(urlContex)
     
    
     init_date = request.GET.get("init_date")
     finish_date = request.GET.get("finish_date")
     
     if not init_date:
          init_date = ""
     if not finish_date:
          finish_date = ""
        
     response = []
     df_filtrado = df.copy()

     if (init_date != "" and finish_date != ""):
          print(init_date, finish_date)
          df['consult_date'] = pd.to_datetime(df['consult_date'], format='%Y-%m-%d')
          filtro = (df['consult_date'] >= init_date) & (df['consult_date'] <= finish_date)
          if np.count_nonzero(filtro) > 0:
               df_filtrado = df[filtro]

     df_filtrado['consult_date'] = df_filtrado['consult_date'].astype(str)
     df_filtrado['product_url__created_at'] = df_filtrado['product_url__created_at'].astype(str)
     df_by = df_filtrado.groupby('product_url')

     for by, frame in df_by:
          result = None
          f = frame
          f['total_sales'] = f['vendas_no_dia'].sum()
          f_consult = f[['consult_date', 'vendas_no_dia']]
          f_consult_1 = f_consult.set_index('consult_date')
          product = f[['product_url__image', 'product_url', 'product_url__created_at', 'total_sales']].drop_duplicates()
          consult = f_consult_1.T.reset_index(drop=True)
          l1 = set(np.array(consult.columns))
          l2 = None
          if (init_date == "" and finish_date == ""):
               l2 = set(np.array(pd.date_range(start=df.consult_date.min(),end=df.consult_date.max()).astype(str)))
          else:
               l2 = set(np.array(pd.date_range(start=init_date,end=finish_date).astype(str)))
          datesNoSale = l2-l1
          for d in datesNoSale:
               consult.insert(0,d,0)
          product = product.reset_index(drop=True)
          frames = [product, consult]
          result = pd.concat(frames, axis=1, join='inner')
          result_json = result.to_json(orient="records")
          response.append(json.loads(result_json))
          
     return JsonResponse(response, safe=False)
