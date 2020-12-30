from main import ma
from models.JobSalary import JobSalary
from marshmallow.validate import Length, Range
from datetime import datetime

class JobSalarySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = JobSalary
    
    title = ma.String(required=True, validate=Length(min=1))
    lower_quartile = ma.Integer(required=True, validate=Range(min=0.0))
    median = ma.Integer(required=True, validate=Range(min=0.0))
    upper_quartile = ma.Integer(required=True, validate=Range(min=0.0))
    avg_years_experience = ma.Float(required=True, validate=Range(min=0.0, max=50.0))
    last_updated = ma.String(required=True,nullable=False, default=datetime.utcnow)


job_salary_schema = JobSalarySchema()
job_salary_schemas = JobSalarySchema(many=True)