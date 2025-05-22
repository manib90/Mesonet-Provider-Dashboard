import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import csv
from io import StringIO
from models import db, Provider
from forms import ProviderForm, CSVUploadForm
from sqlalchemy import func
from datetime import datetime, timedelta


#app = Flask(__name__)
app = Flask(__name__, instance_path="/tmp") 

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
#where to create/find the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['Database']
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_URL', 'sqlite:///providers.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Connects Flask-SQLAlchemy instance to Flask application
db.init_app(app)

# Create database tables, also creates only those table that doesnot exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('list_providers'))

@app.route('/providers')
def list_providers():
    providers = Provider.query.all()
    return render_template('providers/list.html', providers=providers)

@app.route('/providers/new', methods=['GET', 'POST'])
def new_provider():
    form = ProviderForm()
    if form.validate_on_submit():
        try:
            # Check for existing provider
            existing_provider = Provider.query.filter_by(
                name=form.name.data,
                location=form.location.data
            ).first()

            if existing_provider:
                flash('A provider with this name and location already exists.', 'error')
                return render_template('providers/add.html', form=form)
            
            provider = Provider(
                name=form.name.data,
                location=form.location.data,
                category=form.category.data,
                status=form.status.data
            )
            db.session.add(provider)
            db.session.commit()
            flash('Provider added successfully!', 'success')
            return redirect(url_for('list_providers'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the provider.', 'danger')
    return render_template('providers/new.html', form=form)

@app.route('/providers/<int:id>/edit', methods=['GET', 'POST'])
def edit_provider(id):
    provider = Provider.query.get_or_404(id) #retrieves data by id
    form = ProviderForm(obj=provider)        #pre-fills the form by provider data fetched
    
    if form.validate_on_submit():
        try:
            provider.name = form.name.data
            provider.location = form.location.data
            provider.category = form.category.data
            provider.status = form.status.data
            db.session.commit()
            flash('Provider updated successfully!', 'success')
            return redirect(url_for('list_providers'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the provider.', 'danger')
    
    return render_template('providers/edit.html', form=form, provider=provider)

@app.route('/providers/<int:id>/delete', methods=['GET', 'POST'])
def delete_provider(id):
    provider = Provider.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(provider)
        db.session.commit()
        flash('Provider deleted successfully!', 'success')
        return redirect(url_for('list_providers'))
    return render_template('providers/delete.html', provider=provider)


@app.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    form = CSVUploadForm()
    if form.validate_on_submit():
        csv_file = request.files['file'] #get uploaded file from the form
        # StringIO: Creates in-memory text stream
        # decode("UTF8"): Converts bytes to text
        stream = StringIO(csv_file.stream.read().decode("UTF8"), newline=None)
        # Creates CSV reader that maps to dictionaries, using the headers as keys
        csv_reader = csv.DictReader(stream)
        
        # Initialize counters
        added_count = 0
        error_count = 0
        duplicate_count = 0
        
        # Validate headers
        if not csv_reader.fieldnames:
            flash('Invalid CSV file: No headers found', 'error')
            return redirect(url_for('upload_csv'))

        required_columns = {'name', 'location', 'category', 'status'}
        headers = set(csv_reader.fieldnames)  # Now we know fieldnames is not None
        
        if not required_columns.issubset(headers):
            flash('Invalid CSV format. Required columns: name, location, category, status', 'error')
            return redirect(url_for('upload_csv'))

        # Process each row
        for row in csv_reader:
            try:
                # Check if provider already exists
                existing_provider = Provider.query.filter_by(
                    name=row['name'],
                    location=row['location']
                ).first()

                if existing_provider:
                    duplicate_count += 1
                    continue

                # Validate status
                if row['status'] not in ['Active', 'Inactive']:
                    error_count += 1
                    continue

                # Create new provider
                provider = Provider(
                    name=row['name'],
                    location=row['location'],
                    category=row['category'],
                    status=row['status']
                )
                db.session.add(provider)
                added_count += 1

            except Exception as e:
                error_count += 1

        # Commit all valid entries
        try:
            db.session.commit()
            flash(f'Successfully added {added_count} providers. '
                  f'{duplicate_count} duplicates skipped. '
                  f'{error_count} entries had errors.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while saving to database.', 'error')
        
        return redirect(url_for('list_providers'))
    
    return render_template('upload.html', form=form)


@app.route('/dashboard')
def dashboard():
    # Get Active vs Inactive count
    status_counts = db.session.query(
        Provider.status, 
        func.count(Provider.id)
    ).group_by(Provider.status).all()
    
    # Convert to format needed for Chart.js
    status_labels = [status for status, _ in status_counts]
    status_data = [count for _, count in status_counts]
    
    # Get providers added over time (last 7 days)
    today = datetime.now()
    seven_days_ago = today - timedelta(days=7)
    
    daily_counts = db.session.query(
        func.date(Provider.created_at),
        func.count(Provider.id)
    ).filter(
        Provider.created_at >= seven_days_ago
    ).group_by(
        func.date(Provider.created_at)
    ).all()
    
    # Prepare data for timeline chart
    dates = [(seven_days_ago + timedelta(days=x)).strftime('%Y-%m-%d') 
             for x in range(8)]
    counts_dict = dict(daily_counts)
    timeline_data = [counts_dict.get(date, 0) for date in dates]
    
    return render_template(
        'dashboard.html',
        status_labels=status_labels,
        status_data=status_data,
        timeline_labels=dates,
        timeline_data=timeline_data
    )

if __name__ == '__main__':
    app.run(debug=True)
