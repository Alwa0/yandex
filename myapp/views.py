from django.http import HttpResponse, JsonResponse
from _datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import json
from myapp.models import Courier, Order


def couriers(request):
    if request.method == 'POST':
        data = request.POST.getlist("data")
        response = []
        error = []
        for d in data:
            d = d.replace("\'", "\"")
            d = json.loads(d)
            if (d['courier_id'] is None) | (d.get('courier_type') is None) \
                    | (d.get('regions') is None) | (d.get('working_hours') is None):
                error.append({"id": d['courier_id']})
                continue
            flag = False
            for key in d:
                if not ((key == 'courier_id') | (key == 'courier_type') | (key == 'regions') | (
                        key == 'working_hours')):
                    error.append({"id": d['courier_id']})
                    flag = True
                    break
            if flag:
                continue
            id = d['courier_id']
            type = d.get('courier_type')
            regions = d.get('regions')
            hours = d.get('working_hours')
            weight_remained = 10
            if type == "bike":
                weight_remained = 15
            if type == "car":
                weight_remained = 50
            c = Courier.objects.create(id=id, type=type, regions=regions, working_hours=hours, weight_remained=weight_remained)
            c.save()
            response.append({"id": id})
        if len(error) > 0:
            return JsonResponse(data={"validation_error": {"couriers": error}}, status=400, safe=False)
        return JsonResponse(data={"couriers": response}, status=201)
    else:
        return HttpResponse(status=404)


def edit(request, courier_id):
    if request.method == 'PATCH':
        courier = Courier.objects.get(id=courier_id)
        data = str(request.body).replace("b", "").replace("\"", "").replace("\'", "\"")
        data = json.loads(data)
        for key in data:
            if key == 'courier_id':
                courier.id = data["courier_id"]
            elif key == 'courier_type':
                new_type = data["courier_type"]
                if courier.type == "foot":
                    if new_type == "ike":
                        new_type = "bike"
                        courier.weight_remained += 5
                    elif new_type == "car:":
                        courier.weight_remained += 40
                elif courier.type == "bike":
                    if new_type == "foot":
                        courier.weight_remained -= 5
                    elif new_type == "car":
                        courier.weight_remained += 35
                else:
                    if new_type == "foot":
                        courier.weight_remained -= 40
                    elif new_type == "ike":
                        new_type = "bike"
                        courier.weight_remained -= 35
                courier.type = new_type
            elif key == 'regions':
                courier.regions = data["regions"]
            elif key == 'working_hours':
                courier.working_hours = data['working_hours']
            else:
                return HttpResponse(status=400)
        orders = courier.orders.filter(complete_time=None)
        for order in orders:
            flag = True
            for interval in order.delivery_hours:
                begin = datetime.strptime(interval[0:5], '%H:%M').time()
                end = datetime.strptime(interval[6:11], '%H:%M').time()
                for j in courier.working_hours:
                    j1 = datetime.strptime(j[0:5], '%H:%M').time()
                    j2 = datetime.strptime(j[6:11], '%H:%M').time()
                    if (begin >= j1) & (begin <= j2) | (end >= j1) & (end <= j2):
                        flag = False
                        break
            if (courier.weight_remained < 0) | (order.region not in courier.regions) | flag:
                courier.orders.remove(order)
                order.assign_time = None
                order.save()
                courier.weight_remained += order.weight
        courier.save()

        return JsonResponse(data={"courier_id": courier.id, "courier_type": courier.type,
                                  "regions": courier.regions, "working_hours": courier.working_hours}, status=200)

    elif request.method == "GET":
        return get_courier(request, courier_id)
    else:
        return HttpResponse(status=404)


def orders(request):
    if request.method == 'POST':
        data = request.POST.getlist("data")
        response = []
        error = []
        for d in data:
            d = d.replace("\'", "\"")
            d = json.loads(d)
            if (d['order_id'] is None) | (d.get('weight') is None) \
                    | (d.get('region') is None) | (d.get('delivery_hours') is None):
                error.append({"id": d['order_id']})
                continue
            flag = False
            for key in d:
                if not ((key == 'order_id') | (key == 'weight') | (key == 'region') | (key == 'delivery_hours')):
                    error.append({"id": d['order_id']})
                    flag = True
                    break
            if flag:
                continue
            id = d['order_id']
            weight = d.get('weight')
            region = d.get('region')
            hours = d.get('delivery_hours')
            o = Order.objects.create(id=id, weight=weight, region=region, delivery_hours=hours)
            o.save()
            response.append({"id": id})
        if len(error) > 0:
            return JsonResponse(data={"validation_error": {"orders": error}}, status=400, safe=False)
        return JsonResponse(data={"orders": response}, status=201)
    else:
        return HttpResponse(status=404)


def assign(request):
    courier_id = request.GET.get("courier_id")
    response = ""
    courier = Courier.objects.get(id=courier_id)
    orders = Order.objects.order_by("weight").filter(assign_time=None)
    assigned = []
    now = datetime.now()
    working_hours = []
    for interval in courier.working_hours:
        begin = datetime.strptime(interval[0:5], '%H:%M').time()
        end = datetime.strptime(interval[6:11], '%H:%M').time()
        working_hours.append((begin, end))
    for order in orders:
        flag = False
        if order.weight <= courier.weight_remained:
            if order.region in courier.regions:
                for interval in order.delivery_hours:
                    begin = datetime.strptime(interval[0:5], '%H:%M').time()
                    end = datetime.strptime(interval[6:11], '%H:%M').time()
                    for j in working_hours:
                        if (begin >= j[0]) & (begin <= j[1]) | (end >= j[0]) & (end <= j[1]):
                            order.assign_time = now
                            order.save()
                            courier.weight_remained -= order.weight
                            courier.orders.add(order)
                            courier.save()
                            assigned.append({"id": order.id})
                            flag = True
                            break
                    if flag:
                        break
    response += "orders " + str(assigned) + " are assigned to courier" + str(courier.id) + " at time " + str(now)
    if len(assigned) > 0:
        return JsonResponse(data={"orders": assigned, "assign_time": now}, status=200)
    else:
        return JsonResponse(data={"orders": []}, status=200)


def complete(request):
    courier_id = request.GET.get("courier_id")
    order_id = request.GET.get("order_id")
    complete_time = request.GET.get("complete_time")
    response = JsonResponse(data="Bad Request", status=400, safe=False)
    try:
        Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return response
    order = Order.objects.get(id=order_id)
    courier = Courier.objects.get(id=courier_id)
    for o in courier.orders.all():
        if o.id == order.id:
            order.complete = True
            order.complete_time = complete_time
            order.save()
            courier.weight_remained += order.weight
            c = 2
            if courier.type == "bike":
                c = 5
            elif courier.type == "car":
                c = 9
            courier.earnings += c * 500
            courier.save()
            response = JsonResponse(data={"order_id": order.id}, status=200)
            break
    return response


def get_courier(request, courier_id):
    courier = Courier.objects.get(id=courier_id)
    orders = courier.orders.filter(complete=True)
    td = []
    if len(orders) == 0:
        return JsonResponse(data={
            "courier_id": courier.id,
            "courier_type": courier.type,
            "regions": courier.regions,
            "working_hours": courier.working_hours,
            "earnings": courier.earnings
        })
    for region in courier.regions:
        sum = 0
        num = 0
        for order in orders:
            if order.region == region:
                sum += (order.complete_time - order.assign_time).seconds
                num += 1
        if num == 0:
            continue
        td.append(sum/num)

    t = min(td)
    courier.rating = (60*60 - min(t, 60*60))/(60*60) * 5
    courier.save()
    return JsonResponse(data={
        "courier_id": courier.id,
        "courier_type": courier.type,
        "regions": courier.regions,
        "working_hours": courier.working_hours,
        "rating": courier.rating,
        "earnings": courier.earnings
    })

