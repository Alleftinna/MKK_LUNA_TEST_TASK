import os

from starlette.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join("templates/")

# Указываем путь к шаблонам
templates = Jinja2Templates(directory=TEMPLATES_DIR)
