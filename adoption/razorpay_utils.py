import razorpay
from django.conf import settings
import json

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_razorpay_order(amount, currency='INR'):
    """Create a Razorpay order"""
    try:
        # Convert amount to paise (Razorpay expects amount in smallest currency unit)
        amount_in_paise = int(amount * 100)
        
        data = {
            'amount': amount_in_paise,
            'currency': currency,
            'payment_capture': 1  # Auto capture payment
        }
        
        order = client.order.create(data=data)
        return order
    except Exception as e:
        print(f"Razorpay order creation error: {e}")
        return None

def verify_razorpay_payment(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """Verify Razorpay payment signature"""
    try:
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        return client.utility.verify_payment_signature(params_dict)
    except Exception as e:
        print(f"Razorpay payment verification error: {e}")
        return False

def get_razorpay_payment_details(payment_id):
    """Get payment details from Razorpay"""
    try:
        payment = client.payment.fetch(payment_id)
        return payment
    except Exception as e:
        print(f"Error fetching payment details: {e}")
        return None