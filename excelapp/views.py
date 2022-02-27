from django.http import HttpResponseServerError, JsonResponse
import pandas as pd
import json

def home(request):
    try:
        limit = request.GET.get('limit', 10)
        excel = pd.read_excel('Meter0001.xlsx', engine="openpyxl", index_col=0)
        if limit == 'all':
            output = excel.to_json(orient="records")
        else:
            limit = int(limit)
            offset = int(request.GET.get('offset', 0))
            output = excel[offset:limit].to_json(orient="records")

        return JsonResponse(json.loads(output), safe=False)
    except Exception:
        return HttpResponseServerError
  