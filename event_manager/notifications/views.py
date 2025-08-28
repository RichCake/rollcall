from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def link_telegram_user(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        id = request.POST.get('id')
        
        user = get_object_or_404(get_user_model(), pk=id)
        user.telegram_chat_id = chat_id
        user.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

