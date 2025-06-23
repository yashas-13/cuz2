# Allow running the app either as ``python run.py`` from the ``backend`` folder
# or via ``python -m backend.run`` from the project root. Importing using the
# absolute package path avoids issues with relative imports.
from backend.app import create_app

app = create_app()

if __name__ == '__main__':
    # Allow overriding port via the ``PORT`` environment variable. This helps
    # avoid conflicts if port 5000 is already in use when testing.
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
