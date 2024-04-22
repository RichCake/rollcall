from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404


def link_telegram_user(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        username = request.POST.get('username')
        
        user = get_object_or_404(get_user_model(), username=username)
        user.telegram_chat_id = chat_id
        user.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

