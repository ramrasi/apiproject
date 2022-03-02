from django.http import HttpResponseServerError, JsonResponse
import pandas as pd

def home(request):
    CONST_ACC = 16/32767
    CONST_GYRO = 250/32767
    CONST_MAG = 0.15
    
    try:
        limit = request.GET.get('limit', 10)
        excel = pd.read_csv('SampleLog1.csv')
        
        if limit == 'all':
            output = excel.to_dict(orient="records")
        else:
            limit = int(limit)
            offset = int(request.GET.get('offset', 0))
            output = excel[offset:limit].to_dict(orient="records")
        
        data = []

        # acc = lambda x: int(x, 16)*(16/32767)
        # cyro = lambda x: int(x, 16)*(250/32767)
        # mag = lambda x: int(x, 16)*(0.15)

        acc = lambda x: int(x, 16)*(CONST_ACC) if 'E+' not in x else int(str(int(float(x), 16)), 16)*(CONST_ACC)
        gyro = lambda x: int(x, 16)*(CONST_GYRO) if 'E+' not in x else int(str(int(float(x))), 16)*(CONST_GYRO)
        mag = lambda x: int(x, 16)*(CONST_MAG) if 'E+' not in x else int(str(int(float(x))), 16)*(CONST_MAG)

        for dd in output:
            temp = {}
            for key, value in dd.items():
                key = key.strip()
                if 'ACC' in key:
                    temp[key] = acc(value)
                elif 'GYRO' in key:
                    temp[key] = gyro(value)
                elif 'MAG' in key:
                    temp[key] = mag(value)
                
                if key == 'MAG Z':
                    data.append(temp)
                    temp = {}
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return HttpResponseServerError("Server Error")
  