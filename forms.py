from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from models import Provider 


class ProviderForm(FlaskForm):
    name = StringField('Provider Name', 
                      validators=[
                          DataRequired(message="Name is required"),
                          Length(min=2, max=100, message="Name must be between 2 and 100 characters")
                      ])
    
    location = StringField('Location', 
                         validators=[
                             DataRequired(message="Location is required"),
                             Length(max=100, message="Location must be less than 100 characters")
                         ])
    
    category = StringField('Category', 
                         validators=[
                             DataRequired(message="Category is required"),
                             Length(max=50, message="Category must be less than 50 characters")
                         ])
    
    status = SelectField('Status',
                        choices=[
                            ('Active', 'Active'),
                            ('Inactive', 'Inactive')
                        ],
                        validators=[
                            DataRequired(message="Status is required")
                        ])
    
    submit = SubmitField('Save Provider')

    def __init__(self, *args, **kwargs):
        # Get the provider_id from kwargs and remove it
        self.provider_id = kwargs.pop('provider_id', None)
        super(ProviderForm, self).__init__(*args, **kwargs)

    def validate_status(self, field):
        if field.data not in ['Active', 'Inactive']:
            raise ValidationError('Status must be either Active or Inactive')
        
    def validate_name(self, field):
        query = Provider.query.filter_by(
            name=field.data,
            location=self.location.data
        )
        
        # If this is an edit (provider_id exists), exclude the current provider from the check
        if self.provider_id:
            query = query.filter(Provider.id != self.provider_id)
            
        existing_provider = query.first()
        
        if existing_provider:
            raise ValidationError(f'Provider with name "{field.data}" at location "{self.location.data}" already exists.')

# class ProviderForm(FlaskForm):
#     name = StringField('Provider Name', 
#                       validators=[
#                           DataRequired(message="Name is required"),
#                           Length(min=2, max=100, message="Name must be between 2 and 100 characters")
#                       ])
    
#     location = StringField('Location', 
#                          validators=[
#                              DataRequired(message="Location is required"),
#                              Length(max=100, message="Location must be less than 100 characters")
#                          ])
    
#     category = StringField('Category', 
#                          validators=[
#                              DataRequired(message="Category is required"),
#                              Length(max=50, message="Category must be less than 50 characters")
#                          ])
    
#     status = SelectField('Status',
#                         choices=[
#                             ('Active', 'Active'),     #(value, label)
#                             ('Inactive', 'Inactive')
#                         ],
#                         validators=[
#                             DataRequired(message="Status is required")
#                         ])
    
#     submit = SubmitField('Save Provider')


#     #The function name validate_status is special
#     #WTForms looks for methods starting with validate_ followed by the field name
#     def validate_status(self, field):
#         if field.data not in ['Active', 'Inactive']:
#             raise ValidationError('Status must be either Active or Inactive')
        
#     def validate_name(self, field):
#         # Check for existing provider with same name and location
#         existing_provider = Provider.query.filter_by(
#             name=field.data,
#             location=self.location.data  #self is form object
#         ).first()
        
#         if existing_provider:
#             raise ValidationError(f'Provider with name "{field.data}" at location "{self.location.data}" already exists.')
        


class CSVUploadForm(FlaskForm):
    file = FileField('CSV File', 
                    validators=[
                        FileRequired(message="Please select a file"),
                        FileAllowed(['csv'], message='Only CSV files are allowed')
                    ])
    submit = SubmitField('Upload CSV')

    def validate_file(self, field):
        #if user uploads a file, proceed
        if field.data:
            # Read the first few lines to check for duplicates
            try:
                file_content = field.data.stream.read().decode("UTF8") #read file streams and decode into string utf-8
                field.data.stream.seek(0)  # Reset file pointer at beginning
                
                # If the file contains only whitespace or is completely empty, raise an error.
                if not file_content.strip():
                    raise ValidationError('The CSV file is empty')
                
                # You could add more specific CSV validation here
                # Grabs first line which are headers, remove white spaces and split by comma
                headers = file_content.split('\n')[0].strip().split(',')
                required_headers = {'name', 'location', 'category', 'status'}
                if not required_headers.issubset(set(headers)):
                    raise ValidationError('CSV file must contain name, location, category, and status columns')
                
            except UnicodeDecodeError:
                raise ValidationError('Invalid CSV file format')
            except Exception as e:
                raise ValidationError(f'Error processing CSV file: {str(e)}')
