
from django.urls import path 
from .views import *

urlpatterns = [
    path('Home/', Home , name = 'Home') , 
    path('Form/', form , name = 'form') ,
    path('CV/', CV , name = 'CV') ,  
    path('contact/', contact , name = 'contact') , 
    path('carusel/', carusel , name = 'carusel') ,
    path('projects/',ListProjects.as_view(),name='projects'),
    path('advanced/<int:id>',advanced,name='advanced'),
    path('projects/project_books/',project_books,name='project_books'),
    path('projects/project_calculator/',project_calculator,name='project_calculator'),
    path('projects/project_pyramid/',project_pyramid,name='project_pyramid'),
    path('projects/project_orders/',project_orders,name='project_orders'),
    path('projects/project_phone_book/',project_phone_book,name='project_phone_book'),
    path('projects/project_tests/',project_tests,name='project_tests'),
    path('projects/project_diamonds',project_diamonds,name='project_diamonds'),
    path('projects/project_REGEX/',project_REGEX,name='project_REGEX'),
    path('projects/project_nested_func/',project_nested_func,name='project_nested_func'),
    path('projects/project_generator_copy/',project_generator_copy,name='project_generator_copy'),
    path('projects/project_OOP/',project_OOP,name='project_OOP'),
    path('projects/project_myLibrary/',project_myLibrary,name='project_myLibrary'),
    path('projects/project_react_products/',project_react_products,name='projects/project_react_products')
]

