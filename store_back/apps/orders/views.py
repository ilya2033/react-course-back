from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Order, OrderGood
from goods.models import Good
from .serializers import OrderSerializer
from .permissions import OrderUpsertPermission
import json
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAdminUser,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q


@csrf_exempt
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes((IsAdminUser, ))
def order_list(request):
    try:
        skip = int(request.GET.get("skip",0))
        limit = int(request.GET.get("limit",50))
        orderBy = request.GET.get("orderBy","date")
        status = int(request.GET.get("status",0))
    except:
        return JsonResponse({"errors":[{"message":"Невірні параметри запиту"}]}, safe=False)

    text = request.GET.get("text","")
    try:
        if text:
            orders  = Order.objects.filter(Q(name__contains = text) | Q(email__contains = text) | Q(phoneNumber__contains = text) | Q(surname__contains = text) | Q(_id__contains = text) ).order_by(orderBy)
        else:
            orders  = Order.objects.all().order_by(orderBy)

        if status != 0:
            orders = orders.filter(status = status)
        serializer = OrderSerializer(orders[skip:skip+limit], many=True)
    except Exception as e:
        return JsonResponse({"errors":[{"message":"Замовлення не знайдено"}]}, safe=False)

    return JsonResponse({"data":serializer.data}, safe=False)


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAdminUser])
@authentication_classes([JWTAuthentication])
def order_detail(request,_id):
    try:
        order = Order.objects.get(_id = _id)
    except Exception as e:
        return JsonResponse({"errors":[{"message":"Замовлення не знайдено"}]}, safe=False)

    order  = Order.objects.get(_id = _id)
    if order:
        serializer = OrderSerializer(order)
        return JsonResponse({"data":serializer.data}, safe=False)
    else:
        return JsonResponse({"data":{}}, safe=False)



@csrf_exempt
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes((IsAdminUser, ))
def order_delete(request,_id):

    try:
        order  = Order.objects.get(_id = _id)
    except Exception as e:
        return JsonResponse({"errors":[{"message":"Замовлення не знайдено"}]}, safe=False)

    if order:
        order.delete()
        return JsonResponse({"data":{"_id":_id}}, safe=False)

    return JsonResponse({"data":{}}, safe=False)



@csrf_exempt
@api_view(["POST"])
@permission_classes([OrderUpsertPermission, ])
@authentication_classes([JWTAuthentication])
def order_upsert(request):
    orderPrice = 0
    try:
        _id = request.POST.get('_id',None)
        name = request.POST.get("name", "-")
        orderGoods=  json.loads(request.POST.get("orderGoods", "[]"))
        email = request.POST.get("email", "")
        phoneNumber = request.POST.get("phoneNumber", "-")
        if _id:
            status = request.POST.get("status", "1")
        else:
            status = "1"
        delivery = request.POST.get("delivery", "-")
        address = request.POST.get("address", "-")
        surname = request.POST.get("surname", "-")
    except:
        return JsonResponse({"errors":[{"message":"Не вірні дані"}]}, safe=False)


    if len(orderGoods) == 0:
        return JsonResponse({"errors":[{"message":"Товари відсутні"}]}, safe=False)

    if _id :
        order = Order.objects.get(_id = _id)
        order.email = email
        order.name = name
        order.surname = surname
        order.address = address
        order.delivery = delivery
        order.phoneNumber = phoneNumber


    else:
        order = Order.objects.create(email=email,phoneNumber=phoneNumber,status=status,address=address,delivery=delivery,name = name,surname =surname)


    for orderGood in order.orderGoods.all():
        if order.status != 4:
            orderGood.good.amount += orderGood.count
            orderGood.good.save()

    order.orderGoods.clear()
    for orderGood in orderGoods:
        try:
            good = Good.objects.get(_id = orderGood.get("good")["_id"])
        except:
            return JsonResponse({"errors":[{"message":"Товар не знайдено"}]}, safe=False)

        count = orderGood.get("count")
        if int(good.amount) - int(count) >= 0:
            price = int(count) * int(good.price)
            orderGoodToSave = OrderGood.objects.create(price = price, count = count, good = good)
            orderGoodToSave.save()
            order.orderGoods.add(orderGoodToSave)
            orderPrice+=int(price)

            if int(status) != 4:
                good.amount = int(good.amount) - int(count)
                good.save()

        else:
            return JsonResponse({"errors":[{"message":f"{good.name}:Недостатньо товару!"}]}, safe=False)

    order.price = orderPrice
    order.status = status


    if order:
        order.save()
        serializer = OrderSerializer(order)
        return JsonResponse({"data":serializer.data}, safe=False)
    else:
        return JsonResponse({"data":{}}, safe=False)
