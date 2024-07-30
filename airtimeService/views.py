from django.shortcuts import render
import africastalking
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re

# Initialize Africa’s Talking at the module level to ensure it's done only once
africastalking.initialize(
    os.getenv("USERNAME"), os.getenv("API_KEY")
)


@csrf_exempt
def ussd(request):
    if request.method == 'POST':
        session_id = request.POST.get("sessionId", None)
        service_code = request.POST.get("serviceCode", None)
        phone_number = request.POST.get("phoneNumber", None)
        text = request.POST.get("text", "default")

        print("phone_number: ", phone_number)
        if text == "":
            response = "CON Welcome to Airtime Services: \n"
            response += "1. Buy Airtime \n"
            response += "2. Check balance"

        elif text == "1":
            # Minimum should be 5 shillings
            response = "CON Enter the amount(5 min)"
            print("text: ", text)

        elif len(text.split('*')) == 2:
            print("text2: ", text)

            if text.split('*')[1].isdigit() and int(text.split('*')[1]) >= 5:
                response = "CON Enter recipient(s) separated by commas"
            else:
                response = "END Your amount is incorrect"

        elif len(text.split('*')) == 3:
            print("text 3: ", text)

            recipients_text = text.split('*')[2]
            amount = text.split('*')[1]

            # Validate the recipients
            recipients = recipients_text.split(',')
            valid_recipients = []
            for r in recipients:
                if r.startswith('0'):
                    valid_recipients.append('+254' + r[1:])
                else:
                    valid_recipients.append(r)

            regex = re.compile(r'^\+254\d{9}$')
            valid_recipients = [
                r for r in valid_recipients if regex.fullmatch(r)]

            if valid_recipients:
                currency_code = "KES"
                try:
                    # Get the Airtime service
                    airtime = africastalking.Airtime
                    for recipient in valid_recipients:
                        airtime.send(phone_number=recipient,
                                     amount=amount, currency_code=currency_code)

                    response = "END Airtime sent successfully"
                except Exception as e:
                    response = f"END Failed to send airtime: {str(e)}"
            else:
                response = "END Invalid phone number(s) provided"

        elif text == "2":
            try:
                # Get the Application service
                application_service = africastalking.Application

                # Fetch application data
                app_data = application_service.fetch_application_data()

                # Extract the balance from the fetched data
                balance = app_data["UserData"]["balance"]

                # Send SMS to the requester
                sms = africastalking.SMS
                message = f"Your balance is {balance}"
                recipients = [phone_number]
                msg = sms.send(message, recipients)

                # Respond to the USSD request with the balance
                response = f"END Your balance is {balance}"
            except Exception as e:
                response = f"END Failed to retrieve balance: {str(e)}"

        else:
            response = "END Invalid choice"

        return HttpResponse(response)
