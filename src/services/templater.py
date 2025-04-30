from jinja2 import Environment, FileSystemLoader
from src.core.models.dtos import CVSchema

def render_latex(cv_data: CVSchema) -> str:
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('cv_template.tex.jinja')
    return template.render(cv=cv_data)
