import csv

from django.http import (
    HttpResponse,
    JsonResponse
)

from django.db.models import (
    Sum,
    Count
)

from reportlab.pdfgen import canvas

from .models import (
    Order,
    Product
)


def analytics(request):

    sales = Order.objects.filter(
        payment_status="paid"
    ).aggregate(
        revenue=Sum("total"),
        orders=Count("id")
    )

    top_products = list(
        Product.objects
        .order_by("-popularity")
        .values(
            "id",
            "name",
            "popularity"
        )[:10]
    )

    low_stock = list(
        Product.objects
        .filter(
            stock__lte=10,
            is_active=True
        )
        .values(
            "id",
            "name",
            "stock"
        )
        .order_by("stock")
    )

    return JsonResponse({

        "total_revenue":
            sales["revenue"] or 0,

        "total_orders":
            sales["orders"] or 0,

        "top_products":
            top_products,

        "low_stock":
            low_stock
    })


def sales_csv(request):

    response = HttpResponse(
        content_type="text/csv"
    )

    response[
        "Content-Disposition"
    ] = (
        'attachment; '
        'filename="sales_report.csv"'
    )

    writer = csv.writer(
        response
    )

    writer.writerow([
        "Order ID",
        "Customer",
        "Total",
        "Payment Status",
        "Order Status",
        "Created"
    ])

    orders = (
        Order.objects
        .select_related("customer")
        .order_by("-created_at")
    )

    for order in orders:

        writer.writerow([
            order.id,
            order.customer.email,
            order.total,
            order.payment_status,
            order.order_status,
            order.created_at
        ])

    return response


def sales_pdf(request):

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        'attachment; '
        'filename="sales_report.pdf"'
    )

    pdf = canvas.Canvas(
        response
    )

    pdf.setTitle(
        "Sales Report"
    )

    pdf.drawString(
        50,
        800,
        "Smart E-Commerce Sales Report"
    )

    y = 770

    orders = (
        Order.objects
        .select_related("customer")
        .order_by("-created_at")[:40]
    )

    for order in orders:

        text = (
            f"Order #{order.id} | "
            f"{order.customer.email} | "
            f"{order.total} | "
            f"{order.payment_status}"
        )

        pdf.drawString(
            50,
            y,
            text
        )

        y -= 18

        if y < 50:

            pdf.showPage()

            y = 800

    pdf.save()

    return response
