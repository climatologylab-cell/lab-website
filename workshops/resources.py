from import_export import resources
from .models import Workshop

class WorkshopResource(resources.ModelResource):
    class Meta:
        model = Workshop
        fields = ('id', 'title', 'description', 'event_date', 'link', 'is_active')
        import_id_fields = ('title', 'event_date')
