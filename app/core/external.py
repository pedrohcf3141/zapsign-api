from urllib.parse import urljoin
from requests import Session
import app.settings as config


class ZapSignError(Exception):
    pass


class SessionWithBaseURL(Session):
    def __init__(self, base_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    def request(self, method: str, url: str, **kwargs):
        modified_url = urljoin(self.base_url, url)
        return super().request(method, modified_url, **kwargs)


class ZapSignClient:
    _instance = None

    def __init__(self, AUTH_TOKEN: str):
        self.AUTH_TOKEN = AUTH_TOKEN
        self.BASE_URL = config.ZAPSIGN_API_URL
        self._session = self._get_session()

    @classmethod
    def get_instance(cls, AUTH_TOKEN: str = None):
        if cls._instance is None:
            cls._instance = cls(AUTH_TOKEN)
        return cls._instance

    def _get_session(self) -> SessionWithBaseURL:
        session = SessionWithBaseURL(self.BASE_URL)
        session.headers.update(
            {
                'Authorization': f'Bearer {self.AUTH_TOKEN}',
                'Content-Type': 'application/json',
            }
        )
        return session
