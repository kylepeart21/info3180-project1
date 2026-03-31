from app import app, db
from app.models import Property
from app.forms import PropertyForm
from flask import render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

###
# Routing for your application.
###

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about/')
def about():
    return render_template('about.html', name="Mary Jane")


@app.route('/properties')
def properties():
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)


@app.route('/properties/create', methods=['GET', 'POST'])
def create_property():
    form = PropertyForm()

    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)

        upload_folder = os.path.join('app/static/uploads')
        os.makedirs(upload_folder, exist_ok=True)

        photo_path = os.path.join(upload_folder, filename)
        photo.save(photo_path)

        new_property = Property(
            title=form.title.data,
            description=form.description.data,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            location=form.location.data,
            price=form.price.data,
            property_type=form.property_type.data,
            photo=filename
        )

        db.session.add(new_property)
        db.session.commit()

        flash('Property added successfully!', 'success')
        return redirect(url_for('properties'))

    return render_template('create_property.html', form=form)


@app.route('/properties/<int:id>')
def property_detail(id):
    property = Property.query.get_or_404(id)
    return render_template('property.html', property=property)


###
# Helpers
###

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text} - {error}", 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    return app.send_static_file(file_name + '.txt')


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404