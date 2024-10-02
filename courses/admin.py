from django.contrib import admin
from .models import Course, StudentCourse, CourseHold, StudyMaterial, TrainerAssignment, StudentFeedback

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_group_class', 'class_duration')
    filter_horizontal = ('trainers',)

@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'trainer', 'start_date', 'end_date')

@admin.register(CourseHold)
class CourseHoldAdmin(admin.ModelAdmin):
    list_display = ('student_course', 'start_date', 'end_date', 'status')

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('topic', 'course', 'student_course', 'created_by', 'expiry_date')

@admin.register(TrainerAssignment)
class TrainerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'course', 'start_date', 'end_date', 'start_time', 'end_time')

@admin.register(StudentFeedback)
class StudentFeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'feedback_type', 'status', 'created_at')