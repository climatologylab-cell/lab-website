from import_export import resources, fields
from import_export.widgets import DateWidget
from .models import ResearchProject

class ResearchProjectResource(resources.ModelResource):
    """Import/Export resource for ResearchProject - optimized for current model"""
    
    # Map CSV columns to model fields (only fields that exist in model)
    title = fields.Field(attribute='title', column_name='TOPIC')
    description = fields.Field(attribute='description', column_name='DESCRIPTION')
    funding_agency = fields.Field(attribute='funding_agency', column_name='FUNDING AGENCY')
    grant_amount = fields.Field(attribute='grant_amount', column_name='GRANT AMOUNT')
    collaborators = fields.Field(attribute='collaborators', column_name='OTHER OFFICERS / COLLABORATORS')
    partner_institutions = fields.Field(attribute='partner_institutions', column_name='PARTNER INSTITUTIONS')
    start_date = fields.Field(attribute='start_date', column_name='START DATE', widget=DateWidget(format='%d %b %Y'))
    end_date = fields.Field(attribute='end_date', column_name='END DATE', widget=DateWidget(format='%d %b %Y'))
    status = fields.Field(attribute='status', column_name='STATUS')
    role = fields.Field(attribute='role', column_name='ROLE')
    project_type = fields.Field(attribute='project_type', column_name='PROJECT TYPE')

    class Meta:
        model = ResearchProject
        import_id_fields = ('title',)  # Use title as unique identifier for updates
        fields = (
            'title', 
            'description', 
            'funding_agency', 
            'grant_amount',
            'collaborators', 
            'partner_institutions',
            'start_date', 
            'end_date',
            'status',
            'role',
            'project_type',
            'is_active'
        )
        skip_unchanged = True
        report_skipped = True
