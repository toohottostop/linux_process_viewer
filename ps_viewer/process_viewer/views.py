from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import PsValues
from .serializers import PsValuesSerializer
from django.views.generic import ListView


@csrf_exempt
def values_list(request):
    if request.method == 'GET':
        values = PsValues.objects.all()
        serializer = PsValuesSerializer(values, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PsValuesSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=201)
        return JsonResponse(serializer.errors, safe=False, status=400)


@csrf_exempt
def values_detail(request, pk):
    try:
        snippet = PsValues.objects.get(pk=pk)
    except PsValues.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PsValuesSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PsValuesSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


class DataList(ListView):
    model = PsValues
    template_name = 'data_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = PsValues.objects.all()
        return context
