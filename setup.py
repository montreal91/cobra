
from setuptools import setup


setup(
    name="Cobra",
    options={
        "build_apps": {
            "include_patterns": [
                "data/fonts/*.ttf",
                "data/models/*.egg",
                "data/sprites/*.png",
            ],
            "gui_apps": {
                "Cobra": "main.py",
            },
            "log_filename": "$USER_APPDATA/Cobra/output.log",
            "log_append": False,
            "plugins": [
                "pandagl",
            ],
        },
    },
)
