import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Creates a Stripe Checkout Session for upgrading to PRO membership.
        """
        price_id = request.data.get("price_id", settings.STRIPE_PRICE_ID)

        if not price_id:
            return Response(
                {"error": "Price ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                mode="subscription",
                # This is CRITICAL: It tells the webhook WHO paid.
                client_reference_id=request.user.id,
                # These URLs redirect the user after they pay or cancel
                success_url=settings.FRONTEND_URL + "/dashboard?success=true",
                cancel_url=settings.FRONTEND_URL + "/dashboard?canceled=true",
                customer_email=request.user.email,
            )
            return Response({"url": checkout_session.url})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Listens for Stripe webhooks to update user subscription status automatically.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    event = None

    try:
        # 1. Verify that the request actually came from Stripe
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature (potential hacker)
        return HttpResponse(status=400)

    # 2. Handle the specific event: Checkout Session Completed
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_id = session.get("client_reference_id")
        stripe_customer_id = session.get("customer")
        stripe_subscription_id = session.get("subscription")

        try:
            user = User.objects.get(id=user_id)

            user.stripe_customer_id = stripe_customer_id
            user.stripe_subscription_id = stripe_subscription_id
            user.is_pro_member = True

            user.save()
            print(f"✅ User {user.email} upgraded to PRO.")

        except User.DoesNotExist:
            print(f"⚠️ User with ID {user_id} not found during webhook.")
            return HttpResponse(status=404)

    # 3. Handle Subscription Deletion (Churn)
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        stripe_customer_id = subscription.get("customer")

        try:
            user = User.objects.get(stripe_customer_id=stripe_customer_id)
            user.is_pro_member = False
            user.save()
            print(f"❌ User {user.email} subscription ended.")
        except User.DoesNotExist:
            pass

    return HttpResponse(status=200)
