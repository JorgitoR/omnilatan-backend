from django.contrib import admin 

class AbstractNotificacionAdmin(admin.ModelAdmin):
	raw_id_fields = ('receiver', )
	list_display = ('receiver', 'actor', 'verb', 'level', 'read')
	list_filter = ('level', 'read', 'timestamp')

	def get_queryset(self, request):
		qs = super(AbstractNotificacionAdmin, self).get_queryset(request)
		return qs.prefetch_related('actor')