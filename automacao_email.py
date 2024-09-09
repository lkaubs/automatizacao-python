import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from consts import *

def enviaEmail(html, assunto):
    servidor_smtp = 'smtp.office365.com'
    porta_smtp = 587

    # Crie a mensagem do e-mail
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    msg['Subject'] = assunto

    # Anexe o corpo HTML
    msg.attach(MIMEText(html, 'html'))
    try:

        servidor = smtplib.SMTP(servidor_smtp, porta_smtp)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA)
        servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        servidor.quit()
        print("E-mail enviado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao enviar e-mail: {str(e)}")