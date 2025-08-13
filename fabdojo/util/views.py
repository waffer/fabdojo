import csv, io
from django.shortcuts import render
from django.contrib import messages
from card.models import Card
from events.models import *

# Create your views here.
# one parameter named request
def card_upload(request):
    # declaring template
    template = "util/card_upload.html"
    data = Card.objects.all()
# prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be name, email, address,    phone, profile',
        'cards': data    
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=','):
        if not column[3]:
            column[3] = 0
        Card.objects.update_or_create(
            card_id=column[0],
            name=column[1],
            set=column[2],
            pitch=column[3],
            cost=column[4],
            power=column[5],
            defense=column[6],
            card_class=column[7],
            type=column[8],
            sub_type=column[9],
            rarity=column[10],
            text=column[11]
        )
    print("csv reader done")
    context = {}
    return render(request, template, context)

def deck_upload(request):
    # declaring template
    template = "util/deck_upload.html"
    data = Card.objects.all()
# prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be name, email, address,    phone, profile',
        'cards': data    
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    event_name = request.POST['event_name']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=','):
        event = Event.objects.filter(name=event_name).first()
        decklist = Decklist.objects.update_or_create(
                deck_id=column[0],
                player_id=column[1],

            )
    context = {}
    return render(request, template, context)