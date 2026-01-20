"""
Service d'envoi d'emails
En mode développement: affiche dans la console
En production: utilise SMTP Gmail
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service pour l'envoi d'emails via SMTP Gmail"""

    @staticmethod
    def _send_email(to_email: str, subject: str, body: str, html_body: str | None = None) -> bool:
        """
        Méthode interne pour envoyer un email

        Args:
            to_email: Email du destinataire
            subject: Sujet de l'email
            body: Corps du message en texte brut
            html_body: Corps du message en HTML (optionnel)

        Returns:
            True si l'email a été envoyé avec succès
        """
        # Mode développement: afficher dans la console
        if settings.app_env == "development":
            print("\n" + "=" * 60)
            print(f"📧 EMAIL (simulation - {settings.app_env})")
            print("=" * 60)
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print("-" * 60)
            print(body)
            print("=" * 60 + "\n")
            return True

        # Mode production: envoi via SMTP
        if not settings.smtp_user or not settings.smtp_password:
            logger.error("SMTP credentials not configured")
            return False

        try:
            # Créer le message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{settings.smtp_from_name} <{settings.smtp_user}>"
            msg["To"] = to_email

            # Ajouter le corps en texte brut
            msg.attach(MIMEText(body, "plain", "utf-8"))

            # Ajouter le corps HTML si fourni
            if html_body:
                msg.attach(MIMEText(html_body, "html", "utf-8"))

            # Connexion SMTP et envoi
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls()  # Sécuriser la connexion
                server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.smtp_user, to_email, msg.as_string())

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed. Check your credentials.")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    @staticmethod
    def send_invitation_email(
        to_email: str,
        inviter_name: str,
        task_title: str,
        invitation_token: str,
    ) -> bool:
        """
        Envoyer un email d'invitation

        Args:
            to_email: Email du destinataire
            inviter_name: Nom de la personne qui invite
            task_title: Titre de la tâche
            invitation_token: Token d'invitation

        Returns:
            True si l'email a été envoyé avec succès
        """
        invitation_link = f"{settings.frontend_url}/accept-invite?token={invitation_token}"

        subject = f"Invitation à rejoindre une tâche: {task_title}"

        body = f"""
Bonjour,

{inviter_name} vous invite à rejoindre la tâche "{task_title}".

Pour accepter cette invitation et créer votre compte, cliquez sur le lien suivant:
{invitation_link}

Ce lien expire dans 7 jours.

Cordialement,
L'équipe Task Manager
        """.strip()

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2563eb;">Invitation à rejoindre une tâche</h2>
        <p>Bonjour,</p>
        <p><strong>{inviter_name}</strong> vous invite à rejoindre la tâche "<strong>{task_title}</strong>".</p>
        <p>Pour accepter cette invitation et créer votre compte, cliquez sur le bouton ci-dessous:</p>
        <p style="text-align: center; margin: 30px 0;">
            <a href="{invitation_link}"
               style="background-color: #2563eb; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;">
                Accepter l'invitation
            </a>
        </p>
        <p style="color: #666; font-size: 14px;">Ce lien expire dans 7 jours.</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="color: #999; font-size: 12px;">
            Cordialement,<br>
            L'équipe Task Manager
        </p>
    </div>
</body>
</html>
        """.strip()

        return EmailService._send_email(to_email, subject, body, html_body)

    @staticmethod
    def send_welcome_email(to_email: str, first_name: str) -> bool:
        """
        Envoyer un email de bienvenue après inscription via invitation
        """
        subject = "Bienvenue sur Task Manager"

        body = f"""
Bonjour {first_name},

Votre compte a été créé avec succès sur Task Manager.

Vous pouvez maintenant vous connecter et voir les tâches qui vous sont assignées.

Connectez-vous ici: {settings.frontend_url}/login

Cordialement,
L'équipe Task Manager
        """.strip()

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2563eb;">Bienvenue sur Task Manager!</h2>
        <p>Bonjour <strong>{first_name}</strong>,</p>
        <p>Votre compte a été créé avec succès.</p>
        <p>Vous pouvez maintenant vous connecter et voir les tâches qui vous sont assignées.</p>
        <p style="text-align: center; margin: 30px 0;">
            <a href="{settings.frontend_url}/login"
               style="background-color: #2563eb; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;">
                Se connecter
            </a>
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="color: #999; font-size: 12px;">
            Cordialement,<br>
            L'équipe Task Manager
        </p>
    </div>
</body>
</html>
        """.strip()

        return EmailService._send_email(to_email, subject, body, html_body)

    @staticmethod
    def send_password_reset_email(to_email: str, reset_token: str) -> bool:
        """
        Envoyer un email de réinitialisation de mot de passe
        """
        reset_link = f"{settings.frontend_url}/reset-password?token={reset_token}"

        subject = "Réinitialisation de votre mot de passe"

        body = f"""
Bonjour,

Vous avez demandé la réinitialisation de votre mot de passe.

Cliquez sur le lien suivant pour définir un nouveau mot de passe:
{reset_link}

Ce lien expire dans 1 heure.

Si vous n'avez pas fait cette demande, ignorez cet email.

Cordialement,
L'équipe Task Manager
        """.strip()

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2563eb;">Réinitialisation de mot de passe</h2>
        <p>Bonjour,</p>
        <p>Vous avez demandé la réinitialisation de votre mot de passe.</p>
        <p>Cliquez sur le bouton ci-dessous pour définir un nouveau mot de passe:</p>
        <p style="text-align: center; margin: 30px 0;">
            <a href="{reset_link}"
               style="background-color: #2563eb; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;">
                Réinitialiser mon mot de passe
            </a>
        </p>
        <p style="color: #666; font-size: 14px;">Ce lien expire dans 1 heure.</p>
        <p style="color: #999; font-size: 12px;">
            Si vous n'avez pas fait cette demande, ignorez cet email.
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="color: #999; font-size: 12px;">
            Cordialement,<br>
            L'équipe Task Manager
        </p>
    </div>
</body>
</html>
        """.strip()

        return EmailService._send_email(to_email, subject, body, html_body)
