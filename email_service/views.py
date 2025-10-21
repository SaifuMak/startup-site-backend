from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail,EmailMessage
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *

# Create your views here.


def send_email_with_attachment(email,subject,message,recipient_email,from_email,attachment):
     
     message = message
     from_email = from_email
    #  recipient_email = ['richardpaulson22@gmail.com']
     recipient_email = [recipient_email]
     reply_to=[email] if email else []


     email_message = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_email,  # Email will be sent to this address
        reply_to=reply_to  # Reply-to will be set correctly
    )

     if attachment:
        email_message.attach(attachment.name, attachment.read(), attachment.content_type)

     email_message.send()
    #  send_mail(subject,message,from_email, recipient_email)


class TramcoContact(APIView):
    def post(self, request):
        data=request.data

        message_content = data.get('message')
        phone_no = data.get('phone')

        if not message_content: 
            message_content = "No additional message provided"
        
        if not phone_no: 
            phone_no = "not provided"

        subject = f"New Contact Request from {data.get('name', 'Unknown')}"

        message = (
                f"Name: {data['name']}\n"
                f"Email: {data['email']}\n"
                f"Phone: {phone_no}\n"
                f"Message: {message_content}\n"
            )
        try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='no-reply@mergemechano.com',
                    recipient_list=["richardpaulson22@gmail.com"], 
                    fail_silently=False,
                )
                return Response({"success": True, "message": "Message received! Our team will contact you soon."}, status=status.HTTP_200_OK)
        except Exception as e:
                return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TramcoCareerEmailAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser) 

    def post(self, request, *args, **kwargs):
        # print(request.data,'---------------------------------')
        # return Response('success', status=status.HTTP_200_OK)

        serializer = CareerFormSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Extract individual values, default to None if not present
            role = validated_data.get("role", None)
            name = validated_data.get("name", None)
            email = validated_data.get("email", None)
            phone = validated_data.get("phone", None)
            current_city = validated_data.get("current_city", None)
            experience_years = validated_data.get("experience_years", None)
            experience_months = validated_data.get("experience_months", None)
            preferred_location = validated_data.get("preferred_location", None)
            other_location = validated_data.get("other_location", None)
            resume = validated_data.get("resume", None)  # File object

            subject = 'Interested in Career Opportunities at Tramco'

            experience_text = []
            if experience_years > 0:
                experience_text.append(f"{experience_years} years")
            if experience_months > 0:
                experience_text.append(f"{experience_months} months")

            experience_statement = " and ".join(experience_text) if experience_text else "no"

            message = f"""
                    Dear Hiring Team,

                    I am excited to apply for the role of {role}. My name is {name}, and you can reach me at {email} or {phone}.

                    I am currently based in {current_city} and have {experience_statement} professional experience in this field.

                    I am particularly interested in working in {other_location if preferred_location == "Other" else preferred_location}, and I believe my skills and knowledge make me a great fit for this role.

                    {"I have attached my resume for your review." if resume else ""} I look forward to the opportunity to discuss my application further.

                    Best regards,  
                    {name}
                    """
            recipient_mail = 'richardpaulson22@gmail.com'
            from_mail = 'no-reply@mergemechano.com'

            try: 
               send_email_with_attachment(email,subject,message, recipient_mail,from_mail,attachment = resume if resume else None,)

               return Response('success email has been sent', status=status.HTTP_200_OK)

            except Exception as e:
                print(str(e))
                return Response('something went wrong',  status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)