from .serializers import MyTokenObtainPairSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from .forms import RegisterForm
from .models import CustomUser


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            newUser = form.save()

            return JsonResponse({"data":{"_id":newUser._id}}, safe=False)
        else:
            print(form.errors)
            return JsonResponse({"errors":[{"message":"Невірні дані"}]}, safe=False)

    return JsonResponse({"errors":[{"message":"Invalid method, method must be POST"}]}, safe=False)
