from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from .models import User
from .services.rag_service import get_rag_overview, get_tutoring_modes
from .services.analytics_service import get_learner_analytics, seed_demo_sessions_for_user


def home(request):
    """
    Landing router. Redirects authenticated learners to dashboard, otherwise login.
    """
    if 'user_id' in request.session:
        return redirect('dashboard')
    return redirect('login')


def register(request):
    """
    Learner Registration.
    Captures credentials, contact details, preferred programming track,
    skill level, and Socratic learning preferences.
    """
    if 'user_id' in request.session:
        return redirect('dashboard')

    if request.method == 'POST':
        user_name = request.POST.get('user_name', '').strip()
        password = request.POST.get('password', '')
        email = request.POST.get('email', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        place = request.POST.get('place', '').strip()
        preferred_language = request.POST.get('preferred_language', 'Python')
        skill_level = request.POST.get('skill_level', 'Beginner')
        learning_goal = request.POST.get(
            'learning_goal',
            'Master programming logic through step-by-step Socratic hints'
        ).strip()

        # Validation
        if not user_name or not password or not mobile_number or not place:
            return render(
                request,
                'users/register.html',
                {
                    'error': 'Please fill in all mandatory fieldsmarked with an asterisk (*).',
                    'form_data': request.POST,
                }
            )

        if User.objects.filter(user_name=user_name).exists():
            return render(
                request,
                'users/register.html',
                {
                    'error': f'Username "{user_name}" is already taken. Please select another.',
                    'form_data': request.POST,
                }
            )

        # Create learner profile
        user = User.objects.create(
            user_name=user_name,
            password=make_password(password),
            email=email if email else f"{user_name.lower()}@codetutor.edu",
            mobile_number=mobile_number,
            place=place,
            preferred_language=preferred_language,
            skill_level=skill_level,
            learning_goal=learning_goal,
        )

        # Initialize learner sessions and feedback analytics
        seed_demo_sessions_for_user(user)

        messages.success(request, f'Account created successfully for {user.user_name}! Please sign in.')
        return redirect('login')

    return render(request, 'users/register.html')


def login_view(request):
    """
    Learner Authentication.
    Validates hashed credentials and initializes a persistent session.
    """
    if 'user_id' in request.session:
        return redirect('dashboard')

    if request.method == 'POST':
        user_name = request.POST.get('user_name', '').strip()
        password = request.POST.get('password', '')

        if not user_name or not password:
            return render(
                request,
                'users/login.html',
                {
                    'error': 'Please enter both username and password.'
                }
            )

        try:
            user = User.objects.get(user_name=user_name)

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_name'] = user.user_name
                return redirect('dashboard')
            else:
                return render(
                    request,
                    'users/login.html',
                    {
                        'error': 'Invalid password. Please check your credentials and try again.'
                    }
                )
        except User.DoesNotExist:
            return render(
                request,
                'users/login.html',
                {
                    'error': f'No learner account found with username "{user_name}".'
                }
            )

    return render(request, 'users/login.html')


def dashboard(request):
    """
    Main CodeTutor-Athena Learner Dashboard.
    Provides complete learner profile details, active tutoring tracks,
    RAG knowledge base connection status, persistent session logs,
    feedback & confidence metrics, and Stage 1 onboarding completion notice.
    """
    if 'user_id' not in request.session:
        return redirect('login')

    try:
        user = User.objects.get(id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')

    # Handle quick profile track updates from the dashboard
    if request.method == 'POST' and 'update_track' in request.POST:
        user.preferred_language = request.POST.get('preferred_language', user.preferred_language)
        user.skill_level = request.POST.get('skill_level', user.skill_level)
        user.learning_goal = request.POST.get('learning_goal', user.learning_goal)
        user.save()
        messages.success(request, 'Learner tutoring profile updated successfully!')
        return redirect('dashboard')

    analytics = get_learner_analytics(user)
    rag_overview = get_rag_overview()
    tutoring_modes = get_tutoring_modes()

    context = {
        'user': user,
        'analytics': analytics,
        'rag_overview': rag_overview,
        'tutoring_modes': tutoring_modes,
    }

    return render(request, 'users/dashboard.html', context)


def logout_view(request):
    """
    Flushes the learner session and redirects to sign-in portal.
    """
    request.session.flush()
    return redirect('login')
