from unittest.mock import MagicMock, patch

import pytest
from src.common.utils.otp_utils import (OTP_LENGTH, create_email_otp,
                                        generate_otp)


@pytest.mark.unit
def test_generate_otp_length_and_content():
    """Test that generated OTP is of correct length and contains only digits."""
    otp = generate_otp()
    assert len(otp) == OTP_LENGTH
    assert otp.isdigit()


@pytest.mark.unit
@patch("src.common.utils.otp_utils.EmailOTP.objects.create")
def test_create_email_otp(mock_create):
    """Test creating an email OTP without touching the database."""
  
    email = "test@example.com"
    purpose = "login"
    mock_obj = MagicMock()
    mock_create.return_value = mock_obj

   
    result = create_email_otp(email, purpose)

  
    assert result == mock_obj
    mock_create.assert_called_once()


    args, kwargs = mock_create.call_args
    assert kwargs["email"] == email
    assert kwargs["purpose"] == purpose
    assert "otp" in kwargs
    assert "expires_at" in kwargs
