from decimal import Decimal

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from .models import ReportingPeriod, Timecard, TimecardObject, Targets, HolidayPrefills
from employees.models import UserData

class ReportingPeriodListFilter(admin.SimpleListFilter):
    parameter_name = 'reporting_period'
    title = 'Reporting Period'

    def lookups(self, request, model_admin):
        data = ReportingPeriod.objects.distinct().values_list('start_date')

        return [(p[0], p[0]) for p in data]

    def queryset(self, request, queryset):
        return queryset


class TimecardObjectFormset(BaseInlineFormSet):
    def clean(self):
        """
        Check to ensure the proper number of hours are entered.
        """

        super(TimecardObjectFormset, self).clean()

        if any(self.errors):
            return

        hours = Decimal(0.0)
        aws_eligible = UserData.objects.get(
            user__id=self.instance.user_id).is_aws_eligible
        min_working_hours = self.instance.reporting_period.min_working_hours
        max_working_hours = self.instance.reporting_period.max_working_hours

        for unit in self.cleaned_data:
            try:
                hours = hours + unit['hours_spent']
            except KeyError:
                pass

        if hours > max_working_hours and not aws_eligible:
            raise ValidationError(
                'You have entered more than %s hours' % max_working_hours
            )

        if hours < min_working_hours and not aws_eligible:
            raise ValidationError(
                'You have entered fewer than %s hours' % min_working_hours
            )


class ReportingPeriodAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date',)
    filter_horizontal = ['holiday_prefills', ]


class TimecardObjectInline(admin.TabularInline):
    formset = TimecardObjectFormset
    model = TimecardObject
    readonly_fields = [
        'submitted',
        'grade',
        'revenue_profit_loss_account',
        'expense_profit_loss_account'
    ]


class TimecardAdmin(admin.ModelAdmin):
    inlines = (TimecardObjectInline,)
    list_display = ('user', 'reporting_period',)
    list_filter = (ReportingPeriodListFilter, 'reporting_period',)
    search_fields = ['user__username', 'reporting_period__start_date', 'reporting_period__end_date',]


admin.site.register(HolidayPrefills)
admin.site.register(ReportingPeriod, ReportingPeriodAdmin)
admin.site.register(Timecard, TimecardAdmin)
admin.site.register(Targets)
