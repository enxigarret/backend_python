from unittest.mock import MagicMock, patch

from sqlmodel import select
from app.test_pre_start import init,logger

def test_init_success_connection() -> None:

    engine_mock = MagicMock()
    session_mock = MagicMock()
    session_mock.__enter__.return_value = session_mock
    #select 1 statement only check
    select1 = select(1)
    with (
        patch("app.test_pre_start.Session", return_value=session_mock) as session_patch,
        patch("app.test_pre_start.select", return_value=select1) as select_patch,
        patch("app.test_pre_start.logger") as logger_patch
    ):
        try:
            init(engine_mock)
            connection_successful = True
        except Exception as e:
            connection_successful = False
        assert connection_successful,(
            "Expected database connection to succeed, but it failed."
        )
        session_mock.exec.assert_called_once_with(select1)