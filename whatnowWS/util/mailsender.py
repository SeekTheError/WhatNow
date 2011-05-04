from django.core.mail import send_mail

fromAdress='kuestions.kaist@gmail.com'

def sendMail(subject,message,toAdress)  :
  print message
  send_mail(subject, message , fromAdress, [toAdress], fail_silently=False)


