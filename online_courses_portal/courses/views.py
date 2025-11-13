from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from .models import Course, Category
from .forms import CourseForm
from dashboard.decorators import instructor_required
from django.utils.decorators import method_decorator


@method_decorator(instructor_required, name='dispatch')
class MyCoursesListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/my_courses.html'
    context_object_name = 'courses'
    ordering = ['-created_at']

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user).select_related('category')


@method_decorator(instructor_required, name='dispatch')
class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:my_courses')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Course created successfully!')
        return super().form_valid(form)


@method_decorator(instructor_required, name='dispatch')
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:my_courses')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully!')
        return super().form_valid(form)


@method_decorator(instructor_required, name='dispatch')
class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:my_courses')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Course deleted successfully!')
        return super().delete(request, *args, **kwargs)


@method_decorator(instructor_required, name='dispatch')
class CourseTogglePublishView(LoginRequiredMixin, View):
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug, instructor=request.user)
        course.is_published = not course.is_published
        course.save()
        status = 'published' if course.is_published else 'unpublished'
        messages.success(request, f'Course {status} successfully!')
        return redirect('courses:my_courses')


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'page_obj'
    paginate_by = 12
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True).select_related('instructor', 'category')

        # Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(full_description__icontains=query)
            )

        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Course.objects.filter(is_published=True).select_related('instructor', 'category')
