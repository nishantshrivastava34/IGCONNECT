from django.shortcuts import render
from django.http import	HttpResponse 
from django.shortcuts import render , get_object_or_404 , redirect
from .models import Question,Answer,Qcomment ,Acomment
from django.utils import timezone
from django.contrib.auth.models import User
'''#This will show recent questions , signup ,signin options 
(no of answers, no of votes,no of comments,time published , published by ,) for questions '''
def index(request): #This request object contains meta data about request
   	if request.user.is_authenticated() == True:
	    latest_question_list = Question.objects.order_by('-pub_time')[:10]
	    context = {'latest_question_list': latest_question_list}
	    return render(request, 'index.html', context) #This return a response object
	else:
		return redirect('/authent')

'''This will show particular question text , publishion time of question ,
user who published , Commenting on question ,show comments , upvotes , downvote on question.


Show Top answers with upvotes 
votes on answers
comments on answers
add answers.'''
def detail(request,question_id):

	question = get_object_or_404(Question, pk=question_id)
	answer_dict = question.answer_set.all().order_by( '-upvotes')[:10]
	qcomment_dict = question.qcomment_set.all().order_by('-qcomment_time')[:10]
	

	if request.method == 'POST':

		if 'ans_text' in request.POST :
			answer_text = request.POST['ans_text']
			answer_time = timezone.now()
			answer = Answer(question = question , answer_text = answer_text , answer_time = answer_time ,  upvotes = 0, downvotes = 0, auser = request.user)
			answer.save()
			return render(request , 'detail.html' , {'answer_dict' : answer_dict , 'question' : question})
		elif 'ques_comm_text' in request.POST :
			cquestion_text = request.POST['ques_comm_text']
			cquestion = Qcomment( cquestion = question ,qcomment_text = cquestion_text , qcomment_time = timezone.now() , qcuser = request.user)
			cquestion.save()
			return render(request , 'detail.html' , {'qcomment_dict' : answer_dict , 'question' : question})
		

	else:
		return render(request , 'detail.html' , {'answer_dict' : answer_dict , 'question' : question , 'qcomment_dict' : qcomment_dict} )

