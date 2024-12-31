"""
Utility functions for email testing and validation
"""
import os
import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage, send_mail, get_connection
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.utils import timezone

logger = logging.getLogger(__name__)

@dataclass
class EmailTestResult:
    """Data class to store email test results"""
    success: bool
    timestamp: datetime
    message: str
    error_details: Optional[str] = None
    smtp_response: Optional[str] = None

class EmailTestingError(Exception):
    """Custom exception for email testing errors"""
    pass

def verify_email_settings() -> Dict[str, Any]:
    """
    Verify that all required email settings are configured
    
    Returns:
        Dict containing email configuration status
    """
    required_settings = [
        'EMAIL_BACKEND',
        'EMAIL_HOST',
        'EMAIL_PORT',
        'EMAIL_USE_TLS',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'DEFAULT_FROM_EMAIL'
    ]
    
    config_status = {}
    for setting in required_settings:
        value = getattr(settings, setting, None)
        # Mask password in results
        if setting == 'EMAIL_HOST_PASSWORD':
            config_status[setting] = bool(value)
        else:
            config_status[setting] = value
    
    return config_status

def test_smtp_connection() -> EmailTestResult:
    """
    Test SMTP connection without sending email
    
    Returns:
        EmailTestResult object with connection test results
    """
    try:
        connection = get_connection(fail_silently=False)
        connection.open()
        connection.close()
        return EmailTestResult(
            success=True,
            timestamp=timezone.now(),
            message="SMTP connection successful",
        )
    except Exception as e:
        logger.error(f"SMTP connection test failed: {str(e)}")
        return EmailTestResult(
            success=False,
            timestamp=timezone.now(),
            message="SMTP connection failed",
            error_details=str(e)
        )

def send_test_email(
    to_email: str,
    from_email: Optional[str] = None,
    subject: str = "Test Email",
    use_template: bool = False
) -> EmailTestResult:
    """
    Send a test email and return the result
    
    Args:
        to_email: Recipient email address
        from_email: Sender email address (defaults to DEFAULT_FROM_EMAIL)
        subject: Email subject line
        use_template: Whether to use HTML template for test email
    
    Returns:
        EmailTestResult object with send results
    """
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL

    try:
        # Verify email settings first
        config_status = verify_email_settings()
        missing_settings = [k for k, v in config_status.items() if not v]
        if missing_settings:
            raise EmailTestingError(
                f"Missing email configuration: {', '.join(missing_settings)}"
            )

        # Prepare email content
        context = {
            'timestamp': timezone.now(),
            'to_email': to_email,
            'config_status': config_status
        }

        if use_template:
            # Using HTML template
            html_message = render_to_string('email/test_email.html', context)
            text_message = render_to_string('email/test_email.txt', context)
        else:
            # Simple text message
            text_message = (
                f"This is a test email sent at {timezone.now()}\n"
                f"From: {from_email}\n"
                f"To: {to_email}\n"
                f"Email configuration status:\n"
                f"{'\n'.join(f'{k}: {v}' for k, v in config_status.items())}"
            )
            html_message = None

        # Create email message
        email = EmailMessage(
            subject=subject,
            body=text_message,
            from_email=from_email,
            to=[to_email],
        )
        
        if html_message:
            email.content_subtype = "html"
            email.body = html_message

        # Send email and capture SMTP response
        response = email.send(fail_silently=False)

        logger.info(f"Test email sent successfully to {to_email}")
        return EmailTestResult(
            success=True,
            timestamp=timezone.now(),
            message="Email sent successfully",
            smtp_response=str(response)
        )

    except ImproperlyConfigured as e:
        error_msg = "Email settings are not configured properly"
        logger.error(f"{error_msg}: {str(e)}")
        return EmailTestResult(
            success=False,
            timestamp=timezone.now(),
            message=error_msg,
            error_details=str(e)
        )

    except Exception as e:
        error_msg = f"Error sending email: {str(e)}"
        logger.error(error_msg)
        return EmailTestResult(
            success=False,
            timestamp=timezone.now(),
            message="Failed to send email",
            error_details=str(e)
        )

def run_comprehensive_email_test(to_email: str) -> Dict[str, EmailTestResult]:
    """
    Run a comprehensive email test including configuration verification,
    SMTP connection test, and test email sending
    
    Args:
        to_email: Email address to send test email to
    
    Returns:
        Dictionary containing results of all tests
    """
    results = {
        'config': None,
        'smtp': None,
        'send': None
    }

    try:
        # Test configuration
        config = verify_email_settings()
        results['config'] = EmailTestResult(
            success=all(config.values()),
            timestamp=timezone.now(),
            message="Configuration verification complete",
            error_details=None if all(config.values()) else f"Missing settings: {[k for k, v in config.items() if not v]}"
        )

        # Test SMTP connection
        results['smtp'] = test_smtp_connection()

        # Only proceed with sending if previous tests passed
        if results['config'].success and results['smtp'].success:
            results['send'] = send_test_email(to_email)
        else:
            results['send'] = EmailTestResult(
                success=False,
                timestamp=timezone.now(),
                message="Skipped due to previous test failures",
                error_details="Configuration or SMTP test failed"
            )

    except Exception as e:
        logger.error(f"Comprehensive email test failed: {str(e)}")
        for key in results:
            if results[key] is None:
                results[key] = EmailTestResult(
                    success=False,
                    timestamp=timezone.now(),
                    message=f"Test failed during {key} phase",
                    error_details=str(e)
                )

    return results
