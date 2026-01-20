"""
Service d'envoi d'emails
En mode développement: affiche dans la console
En production: utiliser un vrai service SMTP
"""

import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service pour l'envoi d'emails"""

    @staticmethod
    def send_invitation_email(
        to_email: str,
        inviter_name: str,
        task_title: str,
        invitation_token: str,
        base_url: str = "http://localhost:3000"
    ) -> bool:
        """
        Envoyer un email d'invitation

        Args:
            to_email: Email du destinataire
            inviter_name: Nom de la personne qui invite
            task_title: Titre de la tâche
            invitation_token: Token d'invitation
            base_url: URL de base de l'application frontend

        Returns:
            True si l'email a été envoyé avec succès
        """
        invitation_link = f"{base_url}/accept-invite?token={invitation_token}"

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

        # Mode développement: afficher dans la console
        if settings.app_env == "development":
            logger.info("=" * 60)
            logger.info("EMAIL SIMULATION (dev mode)")
            logger.info("=" * 60)
            logger.info(f"To: {to_email}")
            logger.info(f"Subject: {subject}")
            logger.info("-" * 60)
            logger.info(body)
            logger.info("=" * 60)

            # Afficher aussi dans la console standard
            print("\n" + "=" * 60)
            print("📧 EMAIL INVITATION (simulation)")
            print("=" * 60)
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print("-" * 60)
            print(body)
            print("=" * 60 + "\n")

            return True

        # Mode production: implémenter l'envoi réel
        # TODO: Ajouter l'intégration avec un service SMTP ou API email
        # Exemple avec SMTP:
        # import smtplib
        # from email.mime.text import MIMEText
        # ...

        logger.warning("Email service not configured for production")
        return False

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

Cordialement,
L'équipe Task Manager
        """.strip()

        if settings.app_env == "development":
            print("\n" + "=" * 60)
            print("📧 EMAIL BIENVENUE (simulation)")
            print("=" * 60)
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print("-" * 60)
            print(body)
            print("=" * 60 + "\n")
            return True

        return False
