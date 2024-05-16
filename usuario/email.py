from django.core.mail import send_mail

def send_email_token(email,token):
    try:
        subject = 'Bienvenido a Descuentos Catamarca'
        message = f'Ingresa el token de seguridad completar tu registro:  {token}' #http://127.0.0.1/verify/{token}/'
        email_from = 'Descuentos Catamarca <guitarra327373@gmail.com>'
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )

    except Exception as e:
        return False
    
    return True