from django.contrib import admin, messages

from .models import ClassifierConfig, ClassifierFeature, ClassifierSample, DataPoint


class ClassifierSampleInline(admin.TabularInline):
    model = ClassifierSample


class ClassifierFeatureInline(admin.TabularInline):
    model = ClassifierFeature


class ClassifierConfigAdmin(admin.ModelAdmin):
    inlines = [ClassifierSampleInline, ClassifierFeatureInline]
    readonly_fields = ['training_warnings']
    actions = ['train']

    fieldsets = [
        (
            None, {
                'fields': ['name', 'slug', 'short_description', 'training_warnings'],
            },
        ),
        (
            "Neural net design", {
                'fields': [
                    'hidden_layer_sizes',
                    'activation',
                    'solver',
                ]
            }
        ),
        (
            "Algorithm variables", {
                'classes': ['collapse'],
                'fields': [
                    'alpha',
                    'batch_size',
                    'learning_rate',
                    'learning_rate_init',
                    'power_t',
                    'max_iter',
                    'tol',
                    'momentum',
                    'nesterovs_momentum',
                    'validation_fraction',
                    'beta_1',
                    'beta_2',
                    'epsilon',
                    'n_iter_no_change',
                    'max_fun',
                ]
            }
        ),
        (
            "Configuration", {
                'classes': ['collapse'],
                'fields': [
                    'shuffle',
                    'random_state',
                    'verbose',
                    'warm_start',
                    'early_stopping',
                ]
            }
        ),
    ]

    @admin.action(description="Train this classifier on available data")
    def train(self, request, queryset):
        for obj in queryset:
            obj.train()
        messages.success(request, "training done")


class DataPointAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'config')
    list_filter = ('config',)


admin.site.register(ClassifierConfig, ClassifierConfigAdmin)
admin.site.register(DataPoint, DataPointAdmin)
