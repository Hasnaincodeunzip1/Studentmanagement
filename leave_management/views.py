from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LeaveRequest, LeaveHistory
from .serializers import LeaveRequestSerializer, LeaveHistorySerializer
from core.permissions import IsTrainerOrAdminOrManager, IsAdminOrManager
from django.utils import timezone
from django.db.models import Sum
from django.db import transaction

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsTrainerOrAdminOrManager]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'MANAGER']:
            return LeaveRequest.objects.all()
        return LeaveRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        leave_days = (end_date - start_date).days + 1

        history = LeaveHistory.update_or_create_history(self.request.user, start_date)
        
        if leave_days > history.leaves_remaining:
            serializer.save(user=self.request.user, status='PENDING')
            return Response({
                "warning": "You have requested more leaves than your remaining balance. This may result in deductions.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        serializer.save(user=self.request.user, status='PENDING')

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrManager])
    def process_leave(self, request, pk=None):
        leave_request = self.get_object()
        action = request.data.get('action')
        remarks = request.data.get('remarks')

        if action not in ['approve', 'reject']:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            if action == 'approve':
                leave_request.status = 'APPROVED'
                start_date = leave_request.start_date
                end_date = leave_request.end_date
                leave_days = (end_date - start_date).days + 1

                history = LeaveHistory.update_or_create_history(leave_request.user, start_date)
                history.leaves_taken += leave_days
                history.leaves_remaining = max(0, history.leaves_remaining - leave_days)
                history.save()
            else:
                leave_request.status = 'REJECTED'

            leave_request.admin_remarks = remarks
            leave_request.save()

        serializer = self.get_serializer(leave_request)
        return Response(serializer.data)

class LeaveHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeaveHistorySerializer
    permission_classes = [IsTrainerOrAdminOrManager]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'MANAGER']:
            return LeaveHistory.objects.all()
        return LeaveHistory.objects.filter(user=user)

    @action(detail=False, methods=['get'])
    def current_month(self, request):
        today = timezone.now().date()
        history = LeaveHistory.update_or_create_history(request.user, today)
        serializer = self.get_serializer(history)
        return Response(serializer.data)