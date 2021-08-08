
from wagtail.core.models import Page,Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel,InlinePanel,MultiFieldPanel,FieldRowPanel
from django.db import models
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from .blocks import TwoColumnBlock
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

#class AboutUs(Page):
    #intro = RichTextField(blank=True)
    #search_fields = Page.search_fields + [
#   index.SearchField('intro'),
#]
#   content_panels = Page.content_panels + [

#       FieldPanel('intro', classname="full"),
#       InlinePanel('gallery_images', label="Gallery images"),

   # ]

class AboutUs(Page):
    template="home/about_us.html "
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('intro', blocks.RichTextBlock()),
        ('two_columns', TwoColumnBlock()),
        ('image', ImageChooserBlock(icon="image")),

    ],null=True,blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]



#class AboutUsGalleryImage(Orderable):
   # page = ParentalKey(AboutUs, on_delete=models.CASCADE, related_name='gallery_images')
    #image = models.ForeignKey(
    #    'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
   # )
   # caption = models.CharField(blank=True, max_length=250)

  #  panels = [
     #   ImageChooserPanel('image'),
     #   FieldPanel('caption'),
    #]

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='custom_form_fields')

class FormPage(AbstractEmailForm):
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('custom_form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email Notification Config"),
    ]

    def get_form_fields(self):
        return self.custom_form_fields.all()