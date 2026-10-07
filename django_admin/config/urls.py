from django.contrib import admin

from django.urls import path

from store import views


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "analytics/",
        views.analytics
    ),

    path(
        "reports/sales.csv",
        views.sales_csv
    ),

    path(
        "reports/sales.pdf",
        views.sales_pdf
    )
]