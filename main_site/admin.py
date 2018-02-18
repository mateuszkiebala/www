from django.contrib import admin
from .models import Province, Commune, Candidate, Voting, CommuneType, InhabitantsRange


def number_of_candidates():
    return Candidate.objects.count()


class CommuneInLine(admin.TabularInline):
    model = Commune
    extra = 3


class ProvinceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Province', {'fields': ['name']}),
    ]
    inlines = [CommuneInLine]


class VotingInLine(admin.TabularInline):
    model = Voting
    extra = number_of_candidates()


class CandidateAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Candidate', {'fields': ['name', 'surname']})
    ]

    # We can add only two candidates.
    def has_add_permission(self, request):
        if number_of_candidates() >= 2:
            return False
        else:
            return True


class VotingAdmin(admin.ModelAdmin):
    # This class only display votings.
    list_display = ('candidate', 'commune', 'votes')
    list_filter = ['candidate', 'commune']

    # Disable editing votings.
    readonly_fields = ['candidate', 'commune', 'votes']
    search_fields = ['candidate', 'commune']

    # Disable ability to add votings outside the commune.
    def has_add_permission(self, request):
        return False


class CommuneAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    list_filter = ['province']
    inlines = [VotingInLine]


class RangeAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Province, ProvinceAdmin)
admin.site.register(Commune, CommuneAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Voting, VotingAdmin)
admin.site.register(CommuneType)
admin.site.register(InhabitantsRange, RangeAdmin)
