from django.contrib import admin
from .models import User, ChatSession, ResponseFeedback, RAGKnowledgeBase


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'mobile_number', 'place', 'preferred_language', 'skill_level', 'created_at')
    search_fields = ('user_name', 'email', 'place', 'preferred_language')
    list_filter = ('preferred_language', 'skill_level')


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_code', 'title', 'learner', 'tutoring_mode', 'messages_count', 'critical_thinking_score', 'status', 'created_at')
    search_fields = ('session_code', 'title', 'learner__user_name', 'tutoring_mode')
    list_filter = ('tutoring_mode', 'status')


@admin.register(ResponseFeedback)
class ResponseFeedbackAdmin(admin.ModelAdmin):
    list_display = ('learner', 'tutoring_topic', 'rating', 'confidence_gain', 'critical_thinking_encouraged', 'created_at')
    search_fields = ('learner__user_name', 'tutoring_topic')
    list_filter = ('rating', 'critical_thinking_encouraged')


@admin.register(RAGKnowledgeBase)
class RAGKnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('resource_name', 'domain', 'chunk_count', 'vector_engine', 'status', 'updated_at')
    search_fields = ('resource_name', 'domain', 'vector_engine')
    list_filter = ('domain', 'vector_engine', 'status')
