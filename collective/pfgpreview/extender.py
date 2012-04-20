from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from collective.pfgpreview.i18n import _
from Products.Archetypes import atapi
from Products.PloneFormGen.interfaces import IPloneFormGenForm


class ExStringField(ExtensionField, atapi.StringField):
    """An extender string field."""


class ExTextField(ExtensionField, atapi.TextField):
    """An extender string field."""


class FormFolderExtender(object):
    adapts(IPloneFormGenForm)
    implements(ISchemaExtender)

    fields = [
        ExStringField('previewTitle',
            schemata='preview',
            required=False,
            searchable=True,
            primary=False,
            default=u'Please review your submission',
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u'Title'),
            ),
        ),

        ExStringField('confirmButton',
            schemata='preview',
            required=False,
            searchable=False,
            primary=False,
            default=u'Confirm',
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u'Confirm button label'),
            ),
        ),

        ExStringField('backButton',
            schemata='preview',
            required=False,
            searchable=False,
            primary=False,
            default=u'Back',
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u'Back button label'),
            ),
        ),

        ExTextField('previewPrologue',
            schemata='preview',
            required=False,
            searchable=True,
            primary=False,
            default=u'',
            storage=atapi.AnnotationStorage(),
            validators=('isTidyHtmlWithCleanup',),
            allowable_content_types=('text/html',),
            default_output_type='text/x-html-safe',
            widget=atapi.RichWidget(
                description='Displayed below header.',
                label=u'Prologue',
                rows=25,
                allow_file_upload=False),
        ),

        ExTextField('previewEpilogue',
            schemata='preview',
            required=False,
            searchable=True,
            primary=False,
            default=u'',
            storage=atapi.AnnotationStorage(),
            validators=('isTidyHtmlWithCleanup',),
            allowable_content_types=('text/html',),
            default_output_type='text/x-html-safe',
            widget=atapi.RichWidget(
                description='Displayed below form preview.',
                label=u'Epilogue',
                rows=25,
                allow_file_upload=False),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
