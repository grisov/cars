from typing import List
import os
from pydantic import AnyHttpUrl
from app.core.config import settings


def test_environment_variables() -> None:
    """Check environment variables."""
    variables = {
        "DOMAIN": str,
        "HOSTNAME": str,
        "SERVER_HOST": AnyHttpUrl,
        "BACKEND_CORS_ORIGINS": List,
        "INSTALL_DEV": bool,
        "PROJECT_NAME": str,
    }
    for var in variables:
        assert os.getenv(var) is not None, "The variable is exists in the environment and is not empty"
        if var not in ["DOMAIN", "INSTALL_DEV"]:
            value = getattr(settings, var)
            assert value is not None, "The parameter of the same name is available in the settings object"
            assert isinstance(value, variables[var]), "The parameter contains the corresponding data type"
        else:
            assert hasattr(settings, var) == False, "There is no parameter with the appropriate name in the settings object"
    # Some additional clarifications
    assert settings.HOSTNAME == os.getenv("DOMAIN"), "HOSTNAME and DOMAIN are match"
    assert os.getenv("DOMAIN") in settings.SERVER_HOST, "The server host contains the domain name"  # type: ignore
    assert isinstance(settings.API_V1_STR, str), "This prefix is defined only in the settings object"
    if os.getenv("DOMAIN") == "localhost":
        assert os.getenv("INSTALL_DEV") == "true", "Variable value only on localhost"
    else:
        assert os.getenv("INSTALL_DEV") == "false", "The variable value when using the container on the production"
