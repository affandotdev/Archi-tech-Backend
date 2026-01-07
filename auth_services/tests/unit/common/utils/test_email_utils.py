from unittest.mock import patch

import pytest
from django.conf import settings
from src.common.utils.email_utils import send_otp_email


@pytest.mark.unit
@patch("src.common.utils.email_utils.send_mail")
def test_send_otp_email_calls_backend(mock_send_mail):
    """Test that send_otp_email correctly calls Django's send_mail with right params."""
    # Arrange
    email = "test@example.com"
    otp = "123456"
    purpose = "login"

    # Mock settings to ensure predictable from_email
    with patch.object(settings, "DEFAULT_FROM_EMAIL", "noreply@test.com"):
        # Act
        send_otp_email(email, otp, purpose)

    # Assert
    mock_send_mail.assert_called_once()
    args, kwargs = mock_send_mail.call_args

    subject = args[0]
    message = args[1]
    from_email = args[2]
    recipient_list = args[3]

    assert "noreply@test.com" in subject
    assert purpose in subject
    assert otp in message
    assert "noreply@test.com" == from_email
    assert [email] == recipient_list
    assert kwargs["fail_silently"] is False
