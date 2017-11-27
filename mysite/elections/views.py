from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404
from .models import Candidate, Poll, Choice

# Create your views here.

import datetime
from django.db.models import Sum

def index(request):
	candidates = Candidate.objects.all()
	context = {'candidates':candidates}
	return render(request, 'elections/index.html', context)
"""

def index(request):
    candidates = Candidate.objects.all() #Candidate에 있는 모든 객체를 불러옵니다
    str = "" #마지막에 return해 줄 문자열입니다.
    for candidate in candidates:
        str += "{}기호 {}번 ({})<BR>".format(candidate.name, candidate.party_number, candidate.area) #<BR>은 html에서 다음 줄로 이동하기 위해 쓰입니다.
        str += candidate.introduction + "<P>" #<P>는 html에서 단락을 바꾸기 위해 쓰입니다.
    return HttpResponse(str)
"""
def candidates(request, name):
    candidate = get_object_or_404(Candidate, name = name)
    #try:
    #    candidate = Candidate.objects.get(name = name)
    #except:
    #    return HttpResponseNotFound("없는 페이지 입니다.")
    #    raise Http404
    return HttpResponse(candidate.name)

def areas(request, area):
    today = datetime.datetime.now()
    try :
        poll = Poll.objects.get(area = area, start_date__lte = today, end_date__gte=today) # get에 인자로 조건을 전달해줍니다. 
        candidates = Candidate.objects.filter(area = area) # Candidate의 area와 매개변수 area가 같은 객체만 불러오기
    except:
        poll = None
        candidates = None
    context = {'candidates': candidates,
    'area' : area,
    'poll' : poll }
    return render(request, 'elections/area.html', context)


def polls(request, poll_id):
    poll = Poll.objects.get(pk = poll_id)
    selection = request.POST['choice']

    try: 
        choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
        choice.save()

    return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):
    candidates = Candidate.objects.filter(area = area)
    polls = Poll.objects.filter(area = area)
    poll_results = []
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date
        total_votes = Choice.objects.filter(poll_id = poll.id).aggregate(Sum('votes'))

        print("#######",total_votes)
        result['total_votes'] = total_votes['votes__sum']
        rates = []
        for candidate in candidates:
            try:
                choice = Choice.objects.get(poll_id = poll.id,
                    candidate_id = candidate.id)
                rates.append(
                    round(choice.votes * 100 /result['total_votes'],1)
                )
            except:
                rates.append(0)

        result['rates'] = rates
        poll_results.append(result)

    context = {'candidates':candidates, 'area':area,
    'poll_results' : poll_results}
    return render(request, 'elections/result.html', context)
