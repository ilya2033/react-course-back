from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Good, Image
from .serializers import GoodSerializer, ImageSerializer
from django.db.models import Count
import json
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAdminUser,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

@csrf_exempt
@api_view(['GET'])
def good_list(request,):

    skip = int(request.GET.get("skip",0))
    limit = int(request.GET.get("limit",50))
    popular = int(request.GET.get("pupular",0))
    text = request.GET.get("text","")
    orderBy = request.GET.get("orderBy","_id")

    try:
        if text:
            goods  = Good.objects.filter(Q(name__contains = text) | Q(description__contains = text)  ).order_by(orderBy)[skip:skip+limit]
        elif popular:
            goods  = Good.objects.annotate(order_count=Count('orderGoods')).order_by("order_count")[skip:skip+limit]
        else:
            goods  = Good.objects.all().order_by(orderBy)[skip:skip+limit]
    except Exception as e:
        return JsonResponse({"errors":[{"message":"Не вірні дані запиту"}]}, safe=False)

    serializer = GoodSerializer(goods, many=True)

    return JsonResponse({"data":serializer.data}, safe=False)


@csrf_exempt
@api_view(['GET'])
def good_detail(request,_id):
    try:
        good  = Good.objects.get(_id = _id)
    except Exception as e:
        return JsonResponse({"errors":[{"message":"Товар не знайдено"}]}, safe=False)

    if good:
        serializer = GoodSerializer(good)

        return JsonResponse({"data":serializer.data}, safe=False)
    else:
        return JsonResponse({"data":{}}, safe=False)

@csrf_exempt
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes((IsAdminUser, ))
def good_delete(request,_id):

    try:
        good  = Good.objects.get(_id = _id)
    except Exception as e:
        return JsonResponse({"errors":[{"message":"Товар не знайдено"}]}, safe=False)

    if good:
        good.delete()
        return JsonResponse({"data":{"_id":_id}}, safe=False)

    return JsonResponse({"data":{}}, safe=False)





@csrf_exempt
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes((IsAdminUser, ))
def good_upsert(request):
    try:
        _id = request.POST.get('_id',None)
        name = request.POST.get("name", "")
        price =  request.POST.get("price", "").replace(" ","")
        description = request.POST.get("description", "")
        amount = request.POST.get("amount","").replace(" ","")
        images = json.loads(request.POST.get("images", "[]"))
        categories = json.loads(request.POST.get("categories", "[]"))

        if not price.isdigit() or not amount.isdigit():
            return JsonResponse({"errors":[{"message":"Не вірні дані"}]}, safe=False)

    except:
        return JsonResponse({"errors":[{"message":"Не вірні дані"}]}, safe=False)

    if _id :
        try:
            good  = Good.objects.get(_id = _id)
        except Exception as e:
            return JsonResponse({"errors":[{"message":"Не вірні дані запиту"}]}, safe=False)
        good.description = description
        good.name = name
        good.price = price
        good.amount = amount

    else:
        good = Good.objects.create(name=name,price=price,amount=amount,description=description)

    good.images.clear()
    for image in images:
        good.images.add(image["_id"])

    good.categories.clear()
    for category in categories:
        good.categories.add(category["_id"])

    if good:
        good.save()
        serializer = GoodSerializer(good)
        return JsonResponse({"data":serializer.data}, safe=False)
    else:
        return JsonResponse({"data":{}}, safe=False)




@csrf_exempt
def image_upsert(request):
    file = request.FILES.get("photo" , None)
    if file:
        image = Image.objects.create(url =file )
        image.save()
        serializer = ImageSerializer(image)
        return JsonResponse({"data":serializer.data}, safe=False)
    else:
        return JsonResponse({"data":{}}, safe=False)