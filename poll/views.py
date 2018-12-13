from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from poll.models import Question
# Create your views here.

def index(request):
    # 템플릿에게 넘겨줄 객체의 이름
    # Question 테이블 객체에서 pub_date 컬럼의 역순으로 정렬하여 5개의 최근 Question 객체를 가져와서 만듦
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    # 템플릿에 넘겨주는 방식은 파이썬 사전 타입으로 템플릿에 사용될 변수명과그 변수명에 해당하는 객체를 매핑하는 사전.
    # context 변수를 만들어서 이를 render() 함수에 보냄
    context = {'latest_question_list': latest_question_list}
    # render 함수는 템플릿 파일인 poll/index.html 에 context 변수를 적용해서 사용자에게 보여줄 최종 HTML 텍스트를 만듦.
    # 이를 담아서 HttpResponse 객체를 반환함.
    # index 뷰 함수는 최종적으로 클라이언트에게 응답할 데이터인 HttpResponse 객체를 반환함.
    return render(request, 'poll/index.html', context)

def detail(request, question_id):
    # 첫 번째 인자는 모델 클래스이고, 두 번째 인자부터는 검색 조건을 여러 개 사용할 수 있다.
    # Question 모델 클래스로 부터 pk=question_id 검색 조건에 맞는 객체를 조회한다.
    # 조건에 맞는 객체가 없으면 Http404 exception을 발생시킴.
    question = get_object_or_404(Question, pk=question_id)
    # 템플릿에게 넘겨주는 컨텍스트 사전을 render() 함수의 인자로 직접 써주고 있다.
    # 템플릿 파일에서는 question이란 변수를 사용할 수 있게 됨.
    return render(request, 'poll/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Choice 테이블을 검색조건 request.POST['choice']를 이용해서 검색함.
        # request.POST['choice'] 는 폼 데이터에서 키가 'choice' 에 해당하는 값인 choice.id를 스트링으로 리턴함.      
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # URLConf 는 일반적으로 URL 스트링과 뷰를 매핑한 각 라인을 URL 패턴이라 하고 이름을 하나씩 부여함.
        # 그런데 reverse() 함수를 사용하여 URL 패턴명으로 부터 URL 스트링을 구할 수도 있음.
        # reverse() 함수의 첫번째 인자로 URL 패턴의 이름, URL 스트링에 사용될 파라미터 두 개의 인자를 받음.
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {'question': question})