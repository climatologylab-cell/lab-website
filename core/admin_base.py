from import_export.admin import ImportExportModelAdmin

class BaseAdmin(ImportExportModelAdmin):
    """
    Base admin class that adds Import/Export functionality.
    Inherit from this class instead of admin.ModelAdmin.
    """
    pass
