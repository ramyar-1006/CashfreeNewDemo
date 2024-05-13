from flask import Flask, request, render_template, redirect, url_for
import requests
import uuid

app = Flask(__name__)
order_counter = 1

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Form</title>
    <style>

      /* CSS for button */
        #placeOrderBtn {
            background-color: #800080; /* Purple */
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }

        #placeOrderBtn:hover {
            background-color: #6a006a; /* Darker purple on hover */
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }
        form {
            max-width: 400px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        label {
            color: #333;
            font-weight: bold;
            margin-bottom: 5px;
            display: block;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            margin-bottom: 10px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }

          #fillDetailsLabel {
            text-align: center;
            font-weight: bold;
            color: #800080; /* Purple */
        }
    </style>
</head>
<body>
        <form action="/place_order" method="post" name="Fill Details">
        <label id="fillDetailsLabel" for="customer_id">Fill Details To Place An Order</label><br><br>

 <form action="/place_order" method="post" name="Fill Details">
<label for="customer_id">Customer ID:</label>
<input type="text" id="customer_id" name="customer_id"><br>

<label for="customer_phone">Customer Phone:</label>
<input type="text" id="customer_phone" name="customer_phone"><br>

<label for="customer_email">Customer Email:</label>
<input type="text" id="customer_email" name="customer_email"><br>

<label for="customer_name">Customer Name:</label>
<input type="text" id="customer_name" name="customer_name"><br>

<label for="order_amount">Order Amount:</label>
<input type="text" id="order_amount" name="order_amount"><br>

<label for="order_currency">Order Currency:</label>
<select id="order_currency" name="order_currency">
    <option value="INR">INR (Indian Rupees)</option>
</select><br>
<br>
    <input type="submit" id="placeOrderBtn" value="Place Order">
    </form>
</body>
</html>
    '''

@app.route('/place_order', methods=['POST'])
def place_order():
    global order_counter
    customer_id = request.form['customer_id']
    customer_phone = request.form['customer_phone']
    customer_email = request.form['customer_email']
    customer_name = request.form['customer_name']
    order_amount = request.form['order_amount']
    order_currency = request.form['order_currency']
    
    # Generate a unique order ID using UUID
    '''order_id = f"playstation_purchase_{order_counter}"
    order_counter += 2
    print (order_id)'''

    order_id = str(uuid.uuid4())
    return_url = url_for('thank_you', order_id=order_id, _external=True)

    
    url = "https://sandbox.cashfree.com/pg/orders"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-version": "2023-08-01",
        "x-client-id": "<X-Client-ID>",
        "x-client-secret": "<X-Client- Secret>"
    }
    data = {
        "customer_details": {
            "customer_id": customer_id,
            "customer_phone": customer_phone,
            "customer_email": customer_email,
            "customer_name": customer_name
        },
        "order_amount": order_amount,
        "order_currency": "INR",
        "order_id": order_id,
     
        "order_meta": {
            "return_url": f"http://127.0.0.1:5000/thank_you?order_id={order_id}"
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        api_response = response.json()
        payment_session_id = api_response.get('payment_session_id')
        return render_template('checkout.html',
                               payment_session_id=payment_session_id,
                               customer_id=customer_id,
                               customer_phone=customer_phone,
                               customer_email=customer_email,
                               customer_name=customer_name,
                               order_amount=order_amount,
                               order_currency=order_currency,
                               order_id=order_id)
    else:
        return f'Error: {response.status_code}, {response.text}'
@app.route('/thank_you')
def thank_you():
    order_id = request.args.get('order_id')
    customer_id = request.args.get('customer_id')
    customer_phone = request.args.get('customer_phone')
    customer_email = request.args.get('customer_email')
    customer_name = request.args.get('customer_name')
    order_amount = request.args.get('order_amount')
    order_currency = request.args.get('order_currency')
    
    return f'''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
            color: #800080; /* Purple */
        }}
        .container {{
            max-width: 800px;
            margin: auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            text-align: center;
        }}
        p {{
            text-align: center;
            font-size: 18px;
        }}
        .order-details {{
            margin-top: 20px;
        }}
        .order-details p {{
            font-size: 16px;
            margin: 5px;
        }}
        .order-details p strong {{
            color: #000;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Thank You!</h1>
        <p>Your Order Has been placed</p>
        <p>Your order ID Is: <strong>{order_id}</strong></p>
    </div>
</body>
</html>
    '''
   

if __name__ == '__main__':
    app.run(debug=True)
