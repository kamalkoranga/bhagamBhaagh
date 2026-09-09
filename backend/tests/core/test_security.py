from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.config import settings
from app.core.security import (
    MAX_BCRYPT_BYTES,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_password_returns_different_hash_for_same_password(self):
        password = "my-secret-password"

        first_hash = hash_password(password)
        second_hash = hash_password(password)

        assert first_hash != second_hash

    def test_hash_password_does_not_return_plain_password(self):
        password = "my-secret-password"

        password_hash = hash_password(password)

        assert password_hash != password

    def test_verify_password_returns_true_for_correct_password(self):
        password = "my-secret-password"
        password_hash = hash_password(password)

        assert verify_password(password, password_hash) is True

    def test_verify_password_returns_false_for_wrong_password(self):
        password = "my-secret-password"
        password_hash = hash_password(password)

        assert verify_password("wrong-password", password_hash) is False

    def test_password_longer_than_bcrypt_limit_is_truncated(self):
        password = "a" * (MAX_BCRYPT_BYTES + 20)
        truncated_password = password[:MAX_BCRYPT_BYTES]

        password_hash = hash_password(password)

        assert verify_password(password, password_hash) is True
        assert verify_password(truncated_password, password_hash) is True

    def test_unicode_password_is_verified(self):
        password = "pässwörd-🔐"

        password_hash = hash_password(password)

        assert verify_password(password, password_hash) is True


class TestAccessToken:
    def test_create_access_token_contains_subject(self):
        user_id = "user-123"

        token = create_access_token(user_id)
        payload = decode_access_token(token)

        assert payload is not None
        assert payload["sub"] == user_id

    def test_create_access_token_contains_expiration(self):
        token = create_access_token("user-123")
        payload = decode_access_token(token)

        assert payload is not None
        assert "exp" in payload

    def test_create_access_token_contains_additional_claims(self):
        additional_claims = {
            "role": "admin",
            "email": "admin@example.com",
        }

        token = create_access_token(
            "user-123",
            additional_claims=additional_claims,
        )

        payload = decode_access_token(token)

        assert payload is not None
        assert payload["sub"] == "user-123"
        assert payload["role"] == "admin"
        assert payload["email"] == "admin@example.com"

    def test_create_access_token_converts_subject_to_string(self):
        token = create_access_token(123)

        payload = decode_access_token(token)

        assert payload is not None
        assert payload["sub"] == "123"

    def test_create_access_token_can_be_decoded(self):
        token = create_access_token("user-123")

        payload = decode_access_token(token)

        assert payload is not None
        assert payload["sub"] == "user-123"


class TestAccessTokenDecoding:
    def test_decode_access_token_returns_none_for_invalid_token(self):
        invalid_token = "this-is-not-a-valid-jwt"

        payload = decode_access_token(invalid_token)

        assert payload is None

    def test_decode_access_token_returns_none_for_token_with_wrong_secret(self):
        payload = {"sub": "user-123"}

        token = jwt.encode(
            payload,
            "wrong-secret",
            algorithm=settings.JWT_ALGORITHM,
        )

        result = decode_access_token(token)

        assert result is None

    def test_decode_access_token_returns_none_for_expired_token(self):
        expired_time = datetime.now(UTC) - timedelta(minutes=5)

        token = jwt.encode(
            {
                "sub": "user-123",
                "exp": expired_time,
            },
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

        result = decode_access_token(token)

        assert result is None

    def test_decode_access_token_returns_payload_for_valid_token(self):
        token = create_access_token("user-123")

        payload = decode_access_token(token)

        assert payload is not None
        assert payload["sub"] == "user-123"
