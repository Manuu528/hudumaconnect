from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import ServiceRequest


def home(request):
    return render(request, "requests_app/home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account was created successfully.")
        return redirect("dashboard")

    return render(request, "requests_app/register.html", {"form": form})


@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")

    items = ServiceRequest.objects.filter(citizen=request.user)

    return render(request, "requests_app/dashboard.html", {
        "requests_list": items,
        "total": items.count(),
        "pending": items.filter(status="pending").count(),
        "in_progress": items.filter(status="in_progress").count(),
        "resolved": items.filter(status="resolved").count(),
    })


@login_required
def submit_request(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":
        category = request.POST.get("category", "")
        location = request.POST.get("location", "").strip()
        description = request.POST.get("description", "").strip()
        image = request.FILES.get("image")

        valid_categories = {item[0] for item in ServiceRequest.CATEGORY_CHOICES}

        if category not in valid_categories or not location or not description:
            messages.error(request, "Complete all required fields correctly.")
        elif len(location) > 255 or len(description) > 5000:
            messages.error(request, "Your location or description is too long.")
        elif image and (
            image.size > 5 * 1024 * 1024
            or image.content_type not in {
                "image/jpeg", "image/png", "image/webp"
            }
        ):
            messages.error(
                request,
                "Use a JPEG, PNG, or WebP image no larger than 5 MB."
            )
        else:
            ServiceRequest.objects.create(
                citizen=request.user,
                category=category,
                location=location,
                description=description,
                image=image,
            )
            messages.success(request, "Your request was submitted.")
            return redirect("dashboard")

    return render(request, "requests_app/submit_request.html", {
        "categories": ServiceRequest.CATEGORY_CHOICES
    })


@login_required
def request_detail(request, pk):
    item = get_object_or_404(
        ServiceRequest.objects.select_related("citizen"), pk=pk
    )

    if item.citizen_id != request.user.id and not request.user.is_staff:
        raise PermissionDenied

    return render(request, "requests_app/request_detail.html", {
        "service_request": item
    })


def staff_required(view):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url="login"
    )(view)


@staff_required
def admin_dashboard(request):
    items = ServiceRequest.objects.select_related("citizen")

    status_filter = request.GET.get("status", "")
    category_filter = request.GET.get("category", "")
    search = request.GET.get("q", "").strip()

    valid_statuses = {item[0] for item in ServiceRequest.STATUS_CHOICES}
    valid_categories = {item[0] for item in ServiceRequest.CATEGORY_CHOICES}

    if status_filter in valid_statuses:
        items = items.filter(status=status_filter)

    if category_filter in valid_categories:
        items = items.filter(category=category_filter)

    if search:
        items = items.filter(
            Q(location__icontains=search)
            | Q(description__icontains=search)
            | Q(citizen__username__icontains=search)
            | Q(reference_number__icontains=search)
        )

    all_items = ServiceRequest.objects.all()

    return render(request, "requests_app/admin_dashboard.html", {
        "requests_list": items,
        "total": all_items.count(),
        "pending": all_items.filter(status="pending").count(),
        "in_progress": all_items.filter(status="in_progress").count(),
        "resolved": all_items.filter(status="resolved").count(),
        "statuses": ServiceRequest.STATUS_CHOICES,
        "categories": ServiceRequest.CATEGORY_CHOICES,
        "selected_status": status_filter,
        "selected_category": category_filter,
        "search": search,
    })


@staff_required
def update_status(request, pk):
    if request.method != "POST":
        return redirect("admin_dashboard")

    item = get_object_or_404(ServiceRequest, pk=pk)
    new_status = request.POST.get("status", "")
    valid_statuses = {value for value, label in ServiceRequest.STATUS_CHOICES}

    if new_status not in valid_statuses:
        messages.error(request, "Invalid status selected.")
    else:
        item.status = new_status
        item.save(update_fields=["status", "updated_at"])
        messages.success(request, "Request status updated.")

    return redirect("admin_dashboard")
