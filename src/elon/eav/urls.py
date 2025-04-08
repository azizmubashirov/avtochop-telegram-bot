from django.conf.urls import url
from . import views

urlpatterns = [

    url(r"^category/$", views.CategoryView.as_view(), name="category-create"),
    url(r"^category/(?P<pk>[0-9]+)/info/$", views.CategoryView.as_view(), name="category-info"),
    url(r"^tg/category/$", views.CategoryView.as_view(), name="tg-category-create"),
    url(r"^tg/category/(?P<pk>[0-9]+)/children/$", views.CategoryView.as_view(), name="tg-category-children"),

    url(r"^inputtype/$", views.InputTypeView.as_view(), name="input-type-create"),
    url(r"^inputtype/(?P<pk>[0-9]+)/info/$", views.InputTypeView.as_view(), name="input-type-info"),

    url(r"^entity/$", views.EntityView.as_view(), name="entity-create"),
    url(r"^entity/(?P<pk>[0-9]+)/info/$", views.EntityView.as_view(), name="entity-info"),

    url(r"^category-entity/$", views.CategoryEntityView.as_view(), name="category-entity-create"),
    url(r"^category-entity/(?P<pk>[0-9]+)/info/$", views.CategoryEntityView.as_view(), name="category-entity-info"),

    url(r"^attribute/$", views.AttributeView.as_view(), name="attribute-create"),
    url(r"^attribute/(?P<pk>[0-9]+)/info/$", views.AttributeView.as_view(), name="attribute-info"),

    url(r"^entity-attribute/$", views.EntityAttributeView.as_view(), name="entity-attribute-create"),
    url(r"^entity-attribute/(?P<pk>[0-9]+)/info/$", views.EntityAttributeView.as_view(), name="entity-attribute-info"),

    url(r"^value/$", views.ValueView.as_view(), name="value-create"),
    url(r"^value/(?P<pk>[0-9]+)/info/$", views.ValueView.as_view(), name="value-info"),

    url(r"^attribute-value/$", views.AttributeValueView.as_view(), name="attribute-value-create"),
    url(r"^attribute-value/(?P<pk>[0-9]+)/info/$", views.AttributeValueView.as_view(), name="attribute-value-info"),

    url(r"^category/steps/(?P<category_id>[0-9]+)/$", views.CategoryStepsView.as_view(), name="category-steps"),

]

