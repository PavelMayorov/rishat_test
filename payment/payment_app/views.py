import os

from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from dotenv import load_dotenv
import stripe

from .models import Item


load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


class ItemView(TemplateView):
    template_name = 'item.html'

    def get_context_data(self, **kwargs) -> dict:
        item = Item.objects.get(id=self.kwargs['item_id'])
        context = super(ItemView, self).get_context_data()
        context.update({
            'item': item,
            'STRIPE_PUBLIC_KEY': os.getenv('STRIPE_PUBLIC_KEY'),
        })
        return context


class BuyView(View):
    def get(self, request, *args, **kwargs) -> JsonResponse:
        item = Item.objects.get(id=self.kwargs['item_id'])
        domain = os.getenv('YOUR_DOMAIN')
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'rub',
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain + 'success/',
            cancel_url=domain + 'cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
