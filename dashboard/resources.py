from import_export import resources, fields
from import_export.widgets import DateWidget
from projects.models import ResearchProject
from publications.models import Publication
from team.models import TeamMember
from workshops.models import Workshop
from core.models import (
    Tutorial, ResearchNotice, TechnologyNotice, 
    CarouselImage, ImpactStory, ResearchHighlight, PolicyImpact
)

# Reuse or Define Resources

class ResearchProjectResource(resources.ModelResource):
    class Meta:
        model = ResearchProject
        import_id_fields = ('title',)
        skip_unchanged = True

class PublicationResource(resources.ModelResource):
    class Meta:
        model = Publication
        import_id_fields = ('title',)
        skip_unchanged = True

class TeamMemberResource(resources.ModelResource):
    class Meta:
        model = TeamMember
        import_id_fields = ('name',)
        skip_unchanged = True

class WorkshopResource(resources.ModelResource):
    class Meta:
        model = Workshop
        import_id_fields = ('title',)
        skip_unchanged = True

class TutorialResource(resources.ModelResource):
    class Meta:
        model = Tutorial
        import_id_fields = ('title',)
        skip_unchanged = True

class ImpactStoryResource(resources.ModelResource):
    class Meta:
        model = ImpactStory
        import_id_fields = ('title',)
        skip_unchanged = True

class ResearchNoticeResource(resources.ModelResource):
    class Meta:
        model = ResearchNotice
        import_id_fields = ('title',)
        skip_unchanged = True

class TechnologyNoticeResource(resources.ModelResource):
    class Meta:
        model = TechnologyNotice
        import_id_fields = ('title',)
        skip_unchanged = True
