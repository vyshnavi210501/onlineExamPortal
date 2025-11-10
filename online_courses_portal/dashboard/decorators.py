from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator to restrict access based on user roles.
    allowed_roles: list of allowed role strings (e.g., ['instructor', 'admin'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect('login')
            if request.user.role not in allowed_roles:
                messages.error(request, "You don't have permission to access this page.")
                # Redirect to appropriate dashboard based on role
                if request.user.role == 'instructor':
                    return redirect('instructor_dashboard')
                elif request.user.role == 'student':
                    return redirect('student_dashboard')
                else:
                    return redirect('admin_dashboard')  # Assuming admin has a dashboard
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Specific role decorators for convenience
def instructor_required(view_func):
    return role_required(['instructor'])(view_func)

def student_required(view_func):
    return role_required(['student'])(view_func)

def admin_required(view_func):
    return role_required(['admin'])(view_func)

def instructor_or_admin_required(view_func):
    return role_required(['instructor', 'admin'])(view_func)

def student_or_admin_required(view_func):
    return role_required(['student', 'admin'])(view_func)