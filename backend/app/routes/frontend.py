from flask import Blueprint, send_from_directory
from pathlib import Path

# Path to the repository root -> parent of backend directory
ROOT_DIR = Path(__file__).resolve().parents[3]
FRONTEND_DIR = ROOT_DIR / 'frontend'

frontend_bp = Blueprint(
    'frontend', __name__,
    static_folder=str(FRONTEND_DIR),
    template_folder=str(FRONTEND_DIR)
)

@frontend_bp.route('/')
def index():
    """Serve the main index page."""
    return send_from_directory(frontend_bp.static_folder, 'index.html')


@frontend_bp.route('/<path:filename>')
def static_files(filename):
    """Serve frontend files for any other path."""
    return send_from_directory(frontend_bp.static_folder, filename)
