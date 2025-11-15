from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from .models import Notification
from .serializer import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar notificaciones.
    Permite:
    - Listar todas las notificaciones o filtrarlas por user_id
    - Crear nuevas notificaciones
    - Enviar notificaciones por correo y SMS al momento de crear
    """
    queryset = Notification.objects.all() 
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """
        Filtra notificaciones por user_id si se pasa como query param.
        Ejemplo: GET /api/notifications/?user_id=5
        """
        user_id = self.request.query_params.get("user_id")
        if user_id:
            return Notification.objects.filter(user_id=user_id)
        return Notification.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Crea una nueva notificación.
        Espera un JSON con: user_id, title, message, type
        Envía correo y SMS usando Twilio.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification = serializer.save()

        # Preparar datos para notificación
        notif_type = notification.type.lower()
        title = f"[{notif_type.upper()}] {notification.title}"
        message = notification.message

        # --- Envío de correo ---
        try:
            recipient = getattr(settings, "NOTIFICATION_EMAIL", None) #
            if recipient:
                send_mail(
                    subject=title,
                    message=message,
                    from_email=settings.NOTIFICATION_EMAIL,
                    recipient_list=[recipient],
                    fail_silently=False
                )
                print("Correo enviado correctamente.")
            else:
                print("NOTIFICATION_EMAIL no definido en settings.py")
        except Exception as e:
            print(f"Error al enviar correo: {e}")

        # --- Envío de SMS ---
        try:
            sid = getattr(settings, "TWILIO_ACCOUNT_SID", None)
            token = getattr(settings, "TWILIO_AUTH_TOKEN", None)
            from_number = getattr(settings, "TWILIO_PHONE_NUMBER", None)
            to_number = getattr(settings, "MY_PHONE_NUMBER", None)

            if sid and token and from_number and to_number:
                client = Client(sid, token)
                sms = client.messages.create(
                    body=f"{title}: {message}",
                    from_=from_number,
                    to=to_number
                )
                print(f"SMS enviado: SID {sms.sid}")
            else:
                print("Configuración de Twilio incompleta en settings.py")
        except Exception as e:
            print(f"Error al enviar SMS: {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)