from pathlib import Path
from dynaconf import Dynaconf

_CONFIG_DIR = Path(__file__).parent  # always points to config/

settings = Dynaconf(
    settings_files=[str(_CONFIG_DIR / "settings.toml")],
    secrets=[str(_CONFIG_DIR / ".secrets.toml")],
    environments=True,
    env_switcher="ENV_FOR_DYNACONF",
)