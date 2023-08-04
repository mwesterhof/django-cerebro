from django.contrib import admin, messages

from .models import Classifier, ClassifierFeature, ClassifierSample, DataPoint


class ClassifierSampleInline(admin.TabularInline):
    extra = 0
    model = ClassifierSample


class ClassifierFeatureInline(admin.TabularInline):
    extra = 0
    model = ClassifierFeature


class ClassifierAdmin(admin.ModelAdmin):
    inlines = [ClassifierSampleInline, ClassifierFeatureInline]
    readonly_fields = ['training_warnings']
    actions = ['train']
    list_display = ['__str__', 'data_count', 'training_success']

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

    def data_count(self, instance):
        return instance.data_points.count()

    def training_success(self, instance):
        return not bool(instance.training_warnings)
    training_success.boolean = True


class DataPointAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'config')
    list_filter = ('config',)


admin.site.register(Classifier, ClassifierAdmin)
admin.site.register(DataPoint, DataPointAdmin)
