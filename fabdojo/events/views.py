from django.views import generic
from django.utils import timezone
from django.db.models import *
from datetime import date, timedelta
from dateutil.relativedelta import *

from .models import *
from card.models import *

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'events/index.html'
    context_object_name = 'latest_event_list'
    paginate_by=20

    def get_queryset(self):
        """Return the last five published questions."""
        return Event.objects.order_by('-event_date', 'name')[:10]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['heroes'] = Hero.objects.order_by('name').all()
        context['pop_cards'] = get_card_percentage(class_type="Generic")
        return context

class EventListView(generic.ListView):
    template_name = 'events/index.html'
    context_object_name = 'latest_event_list'
    paginate_by=20
    
    def get_queryset(self):
        format_id = self.kwargs.get('format')
        if format_id == 'All':
            return Event.objects.order_by('-event_date', 'name')
        else:
            return Event.objects.order_by('-event_date', 'name').filter(format__code=format_id)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        format_id = self.kwargs.get('format')
        context = super().get_context_data(**kwargs)
        context['heroes'] = Hero.objects.order_by('name').all()
        context['format'] = Format.objects.filter(code=format_id).first()
        #this line is here so that it doesnt screw up with the filtering since there is no 'All' format
        if format_id == 'All':
            format_id=None
        context['pop_cards'] = get_card_percentage(format=format_id, class_type="Generic")
        return context

class EventView(generic.DetailView):
    template_name = 'events/event.html'
    context_object_name = 'events'
    model = Event

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
            
        event_id = self.kwargs.get('pk')
        if event_id is None:
            return context
        event = Event.objects.filter(id=event_id).first()
        context['decks'] = event.deck.order_by('position').all()
        context['heroes'] = Hero.objects.order_by('name').all()
        context['pop_cards'] = get_card_percentage()
        return context

class DecklistView(generic.DetailView):
    template_name = 'events/decklist.html'
    context_object_name = 'decklist'
    model = Decklist

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
            
        deck_id = self.kwargs.get('pk')
        if deck_id is None:
            return context
        decklist = Decklist.objects.filter(deck_id=deck_id).first()
        context['hero_card'] = Card.objects.filter(name=decklist.hero).first().card_id
        context['equipment'] = decklist.cardInfo.filter(Q(card__type='Equipment') | Q(card__type='Weapon')).order_by('card__name')
        context['equipment_count'] = decklist.cards.through.objects.filter(Q(card__type='Equipment') | Q(card__type='Weapon')).order_by('card__name').filter(deck=decklist).aggregate(Sum('card_count'))['card_count__sum']
        context['red'] = decklist.cardInfo.filter(card__pitch=1).order_by('card__name')
        context['red_count'] = fetch_pitch_count(decklist, 1)
        context['yellow'] = decklist.cardInfo.filter(card__pitch=2).order_by('card__name')
        context['yellow_count'] = fetch_pitch_count(decklist, 2)
        context['blue'] = decklist.cardInfo.filter(card__pitch=3).order_by('card__name')
        context['blue_count'] = fetch_pitch_count(decklist, 3)
        context['no_pitch'] = decklist.cardInfo.filter(Q(card__pitch=0) & ~Q(card__type='Equipment') & ~Q(card__type='Hero') & ~Q(card__type='Weapon')).order_by('card__name')
        context['no_pitch_count'] = decklist.cards.through.objects.filter(Q(card__pitch=0) & ~Q(card__type='Equipment') & ~Q(card__type='Hero') & ~Q(card__type='Weapon')).filter(deck=decklist).aggregate(Sum('card_count'))['card_count__sum']
        return context

class PlayerView(generic.ListView):
    template_name = 'events/player.html'
    model = Decklist
    paginate_by = 20
    context_object_name = 'decks'

    def get_queryset(self):
        player_id = self.kwargs.get('pk')
        return Decklist.objects.filter(player_id__gem_id=player_id).order_by('-event__event_date', 'event__name')

class HeroView(generic.ListView):
    template_name = 'events/hero.html'
    model = Decklist
    paginate_by=20
    context_object_name='decks'

    def get_queryset(self):
        hero_name = self.kwargs.get('hero')
        date_range = self.request.GET.get('date')
        start_date = date.today()
        end_date = None
        if date_range == "2week":
            end_date = start_date - relativedelta(weeks=2, weekday=SU)
        elif date_range == "1month":
            end_date = start_date - relativedelta(months=1, weekday=SU)
        elif date_range == "3month":
            end_date = start_date - relativedelta(months=3, weekday=SU)
        if end_date is None:
            return Decklist.objects.filter(hero__name__icontains=hero_name).order_by('-event__event_date', 'event__name')
        else:
            return Decklist.objects.filter(hero__name__icontains=hero_name).filter(event__event_date__gte=end_date).order_by('-event__event_date', 'event__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hero_name = self.kwargs.get('hero')   
        date_range = self.request.GET.get('date')
        context['hero_name'] = Hero.objects.filter(name__icontains=hero_name).first()
        context['CC_active'] = False
        context['Blitz_active'] = False
        if date_range is not None:
            context['date']  = date_range
        for deck in context['decks']:
            if deck.event.format.code == "CC":
                context['CC_active'] = True
            elif deck.event.format.code == "Blitz":
                context['Blitz_active'] = True
            if context['CC_active'] and context['Blitz_active']:
                break;
        
        context['pop_cards'] = get_card_percentage(hero = hero_name)
        return context
    
class DeckCompareView(generic.ListView):
    template_name = 'events/compare.html'
    model = Decklist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
            
        hero_name = self.kwargs.get('hero')
        format_id = self.kwargs.get('format')
        date_range = self.request.GET.get('date')

        if hero_name is None or format_id is None:
            return context

        start_date = date.today()
        end_date = None
        if date_range == "2week":
            end_date = start_date - relativedelta(weeks=2, weekday=SU)
        elif date_range == "1month":
            end_date = start_date - relativedelta(months=1, weekday=SU)
        elif date_range == "3month":
            end_date = start_date - relativedelta(months=3, weekday=SU)
        deck_ids = self.request.GET.get('less_deck')
        less_card_ids = self.request.GET.get('less_card')
        card_ids = self.request.GET.get('just_card')
        if end_date is not None:
            decks = Decklist.objects.filter(hero__name__startswith=hero_name).filter(event__format__code=format_id).filter(event__event_date__gte=end_date).order_by('-event__event_date', 'event__name').distinct()
        else:
            decks = Decklist.objects.filter(hero__name__startswith=hero_name).filter(event__format__code=format_id).order_by('-event__event_date', 'event__name').distinct()
        less_deck_counter = 0
        if deck_ids is not None:
            deck_ids = deck_ids.split(',')
            if len(deck_ids[-1]) == 0:
                deck_ids.pop()
            less_deck_counter = len(deck_ids)
            decks = decks.filter(~Q(deck_id__in=deck_ids)).distinct()
            context['prev_deck_ids'] = deck_ids
        if less_card_ids is not None:
            less_card_ids = less_card_ids.split(',')
            decks = decks.filter(~Q(cards__card_id__in=less_card_ids)).distinct()
            context['prev_less_card_ids'] = less_card_ids
        if card_ids is not None:
            card_ids = card_ids.split(',')
            decks = decks.filter(Q(cards__card_id__in=card_ids)).distinct()
            context['prev_just_card_ids'] = card_ids

        decks = decks[:20-less_deck_counter]
        unique_names = []
        context['decks'] = ["-", "-", "-"]
        context['pitch_count'] = []
        for deck in decks:
            context['decks'].append(deck)
            temp_pitch_list = []
            temp_pitch_list.append(deck.cards.through.objects.filter(Q(card__pitch=0) & Q(deck=deck)).filter(Q(card__type='Equipment') | Q(card__type='Weapon')).aggregate(Sum('card_count'))['card_count__sum'])
            temp_pitch_list.append(deck.cards.through.objects.filter(deck=deck).filter(Q(card__pitch=0) & ~Q(card__type='Equipment') & ~Q(card__type='Hero') & ~Q(card__type='Weapon')).aggregate(Sum('card_count'))['card_count__sum'])
            temp_pitch_list.append(fetch_pitch_count(deck, 1))
            temp_pitch_list.append(fetch_pitch_count(deck, 2))
            temp_pitch_list.append(fetch_pitch_count(deck, 3))
            context['pitch_count'].append(temp_pitch_list)
            #for loop to start gathering the unique names among all the decks
            for card in deck.cards.all():
                if card not in unique_names:
                    unique_names.append(card)
        
        unique_names = sorted(unique_names, key=lambda x:(pitch_name(x), x.name))
        #loop for creating the actual comparison table
        card_count_list = []
        for item in unique_names:
            temp_list = ['-'] * len(decks)
            temp_total = 0
            for index, deck in enumerate(decks):
                card_list = deck.cards.through.objects.filter(card=item).filter(deck=deck).all()
                for card in card_list:
                    temp_list[index] = card.card_count
                    temp_total += card.card_count

            temp_list.insert(0, item)
            temp_list.insert(1, round(temp_total/len(decks),1))
            card_count_list.append(temp_list)
            name_index = len(card_count_list)

        context['card_list'] = card_count_list
        context['format'] = Format.objects.filter(code=format_id).first()
        context['hero_name'] = hero_name

        return context

#this function is to be able to distinguish the priority in terms of sorting pitch numbers with no pitch that are equipments and non-equipments since the page would be sorting with ints and non-ints
def pitch_name(card):
    pitch = card.pitch
    if pitch == 0:
        if card.type == "Weapon" or card.type == "Equipment":
            return -1
        else:
            return pitch
    else:
        return pitch

def fetch_pitch_count(deck, pitch):
    return deck.cards.through.objects.filter(card__pitch=pitch).filter(deck=deck).aggregate(Sum('card_count'))['card_count__sum']

#function to fetch the most popular cards in relation to heroes or formats
def fetch_most_popular_cards(hero=None, format=None, class_type=None):
    cardinfo = CardInfo.objects.values("card").annotate(n=models.Sum("card_count"))
    if hero is not None:
        cardinfo = cardinfo.filter(deck__hero__name__icontains=hero)
    if format is not None:
        cardinfo = cardinfo.filter(deck__event__format__code=format)
    if class_type is not None:
        cardinfo = cardinfo.filter(card__card_class="Generic")
    return cardinfo.order_by('-n')

def get_card_percentage(hero=None, format=None, class_type=None):
    top_x_cards = fetch_most_popular_cards(hero, format, class_type)[:20]
    total_deck_count = Decklist.objects.count()
    if hero is not None:
        total_deck_count = Decklist.objects.filter(hero__name__icontains=hero).count()
    pop_list = []
    for card in top_x_cards:
        #fetch the number of decks that has the card in it
        deck_count = Decklist.objects.filter(cardInfo__card__card_id=card['card']).count()
        if hero is not None:
            deck_count = Decklist.objects.filter(hero__name__icontains=hero).filter(cardInfo__card__card_id=card['card']).count()
        pop_list.append((
            Card.objects.filter(card_id=card['card']).first(),
            "{:.2%}".format(deck_count/total_deck_count)
            ))
    pop_list.sort(key=lambda x:(len(x[1]), x[1]), reverse=True)
    return pop_list