from django.shortcuts import redirect, render
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe.error

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def checkout(request):
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items = [
                {
                    'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'T-shirt',
                        },
                        'unit_amount': 2000,  # Amount in cents (20 USD)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/')
        )
        return redirect(checkout_session.url, code=303)
    return render(request,'checkout.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header =request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status = 400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status = 400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print('Payment was successful!')

    return JsonResponse({'status': 'success'}, status=200)
    
    

def success(request):
    return render(request,'success.html')
def cancel(request):
    return render(request,'cancel.html')
