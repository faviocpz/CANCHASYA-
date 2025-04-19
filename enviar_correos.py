import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_mensajecorreo(destinatario, asunto, cuerpo):
    remitente = "canchasyainfo@gmail.com"
    contraseña = "jiht njzv gwak jkbd" 

    # Crear mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.send_message(mensaje)
        servidor.quit()
        return 1
    except Exception as e:
        print("Error:", e)
        return 0
