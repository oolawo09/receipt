from app import app, db  # noqa:F401
from app.models import Receipt, Item


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Receipt': Receipt, 'Item': Item}
