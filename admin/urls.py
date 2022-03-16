from unicodedata import category
from django.urls import path

from admin.views import AddCategory, Category, CategoryView

urlpatterns = [
    path('addcategory/', AddCategory.as_view(), name='addcategory'),
    path('category/<int:id>/',Category.as_view(), name='category'),
    path('category_view/',CategoryView.as_view(), name='categoryview')
]
