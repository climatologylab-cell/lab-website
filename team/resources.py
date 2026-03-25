from import_export import resources
from .models import TeamMember

class TeamMemberResource(resources.ModelResource):
    class Meta:
        model = TeamMember
        fields = ('id', 'name', 'role', 'email', 'bio', 'linkedin_url', 'google_scholar_url', 'order', 'is_active')
        import_id_fields = ('email',)
