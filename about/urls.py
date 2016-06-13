from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView

app_name = 'about'

urlpatterns = [
    url(r'^$',
        RedirectView.as_view(url=reverse_lazy('about:this_site')),
        name='index'),
    url(r'^this-site/$',
        TemplateView.as_view(template_name='about/this_site.html'),
        name='this_site'),
    url(r'^us/$',
        TemplateView.as_view(template_name='about/us.html'), name='us'),
    url(r'^privacy/$',
        TemplateView.as_view(template_name='about/privacy.html'),
        name='privacy'),
    url(r'^terms/$',
        TemplateView.as_view(template_name='about/terms.html'),
        name='terms'),
    url(r'^contact/$',
        TemplateView.as_view(template_name='about/contact.html'),
        name='contact'),
]
