import razorpay

keyid = 'rzp_live_8iKdUKGqRVttUs'
keySecret = 'utpgdTG6iY9OXcRVwZ6pepLu'

client = razorpay.Client(auth=(keyid, keySecret))

data = {
    'amount': 100 * 100,
    'currency': "INR",
    'receipt': 'feelfreetocode12',
    'notes': {
        "name": "Virendra",
        "Payment_for": "Gold Membership",
    }
}

order = client.order.create(data=data)

print(order)
