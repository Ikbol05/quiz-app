from django.shortcuts import render, redirect
from . import models
from random import choice, sample
from .models import Answer, AnswerDetail

def index(request):
    return render(request, 'index.html')


def quizList(request):
    images = [
        'https://st2.depositphotos.com/2769299/7314/i/450/depositphotos_73146775-stock-photo-a-stack-of-books-on.jpg',
        'https://img.freepik.com/free-photo/creative-composition-world-book-day_23-2148883765.jpg',
        'https://profit.pakistantoday.com.pk/wp-content/uploads/2018/04/Stack-of-books-great-education.jpg',
        'https://live-production.wcms.abc-cdn.net.au/73419a11ea13b52c6bd9c0a69c10964e?impolicy=wcms_crop_resize&cropH=1080&cropW=1918&xPos=1&yPos=0&width=862&height=485',
        'https://live-production.wcms.abc-cdn.net.au/398836216839841241467590824c5cf1?impolicy=wcms_crop_resize&cropH=2813&cropW=5000&xPos=0&yPos=0&width=862&height=485',
        'https://images.theconversation.com/files/45159/original/rptgtpxd-1396254731.jpg?ixlib=rb-4.1.0&q=45&auto=format&w=1356&h=668&fit=crop'
    ]
    
    quizes = models.Quiz.objects.filter(author=request.user)
    # images = sample(len(quizes), images)

    quizes_list = []

    for quiz in quizes:
        quiz.img = choice(images)
        quizes_list.append(quiz)

    return render(request, 'quiz-list.html', {'quizes':quizes_list})


def quizDetail(request, id):
    quiz = models.Quiz.objects.get(id=id)
    print(123)
    print(quiz.questions_count)
    return render(request, 'quiz-detail.html', {'quiz':quiz})


def createQuiz(request):
    if request.method == 'POST':
        quiz = models.Quiz.objects.create(
            name = request.POST['name'],
            amount = request.POST['amount'],
            author = request.user
        )
        return redirect('quizDetail', quiz.id)
    return render(request, 'quiz-create.html')


def questionCreate(request, id):
    quiz = models.Quiz.objects.get(id=id)
    return render(request, 'question-create.html', {'quiz':quiz})



def user_results(request):
    answers = Answer.objects.filter(author=request.user)
    context = {'answers': answers}
    return render(request, 'results.html', context)


def user_result_detail(request, pk):
    answer = Answer.objects.get(pk=pk)
    answer_details = AnswerDetail.objects.filter(answer=answer)
    correct_count = answer_details.filter(user_choice__correct=True).count()
    wrong_count = answer_details.filter(user_choice__correct=False).count()
    context = {
        'answer': answer,
        'answer_details': answer_details,
        'correct_count': correct_count,
        'wrong_count': wrong_count
    }
    return render(request, 'result_detail.html', context)


def owner_result_detail(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    answer_details = AnswerDetail.objects.filter(answer=answer)
    context = {
        'answer': answer,
        'answer_details': answer_details
    }
    return render(request, 'owner_result_detail.html', context)
