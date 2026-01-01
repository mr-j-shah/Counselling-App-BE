"""
Mock email sending utility.
In production, replace this with actual email service (SendGrid, AWS SES, etc.)
"""

async def send_password_reset_email(email: str, reset_token: str) -> None:
    """
    Mock function to send password reset email.
    
    In production, this would:
    1. Generate reset link: https://yourapp.com/reset-password?token={reset_token}
    2. Send email via email service
    3. Handle errors appropriately
    
    Args:
        email: User's email address
        reset_token: The reset token to include in the link
    """
    reset_link = f"https://yourapp.com/reset-password?token={reset_token}"
    
    # Mock email sending - in production, use actual email service
    print(f"[MOCK EMAIL] Sending password reset email to {email}")
    print(f"[MOCK EMAIL] Reset link: {reset_link}")
    print(f"[MOCK EMAIL] Token: {reset_token}")
    print(f"[MOCK EMAIL] Email sent successfully!")
    
    # In production, you would do something like:
    # await email_service.send(
    #     to=email,
    #     subject="Password Reset Request",
    #     body=f"Click here to reset your password: {reset_link}"
    # )

