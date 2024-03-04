# File: run.py

from app import create_app, db

# Create the Flask application
app = create_app()

# Create all database tables
with app.app_context():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
