from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@csrf_exempt
def chanmq_input(request, host):
    """
    listens for transhumus.output.chanmq
    """
    async_to_sync(get_channel_layer().group_send)('chanmq', {'type': 'chanmq', 'data': request.POST})
    return JsonResponse({})
