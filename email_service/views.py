from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

# Create your views here.

class TramcoContact(APIView):
    def post(self, request):
        data=request.data

        message_content = data.get('message')
        if not message_content: 
            message_content = "No additional message provided"

        subject = f"New Contact Request from {data.get('name', 'Unknown')}"
        message = (
                f"Name: {data['name']}\n"
                f"Email: {data['email']}\n"
                f"Phone: {data['phone']}\n"
                f"Message:\n{message_content}"
            )
        try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='no-reply@mergemechano.com',
                    recipient_list=["richardpaulson22@gmail.com"], 
                    fail_silently=False,
                )
                return Response({"success": True, "message": "Email sent successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
                return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)