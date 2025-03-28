from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Client, Task
from .serializers import UserSerializer, ClientSerializer,TaskSerializer
from .permissions import IsManager


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request, pk):
        if pk:
            user = CustomUser.objects.get(id=pk)
            ser = UserSerializer(user)
            return Response(ser.data)
        users = CustomUser.objects.filter(is_manager=False)
        ser = UserSerializer(users, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = UserSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=400)


class GetMe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        ser = UserSerializer(user)
        return Response(ser.data)


class ClientAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if pk:
            client = Client.objects.get(id=pk)
            if request.user.is_manager or client.created_by == request.user:
                ser = ClientSerializer(client)
                return Response(ser.data)
            return Response({"error": "Permission denied"}, status=403)
        
        if request.user.is_manager:
            clients = Client.objects.all()
        else:
            clients = Client.objects.filter(created_by=request.user)
        
        ser = ClientSerializer(clients, many=True)
        return Response(ser.data)

    def post(self, request):
        if not request.user.is_manager:
            return Response({"error": "Only managers can create clients"}, status=403)
        
        ser = ClientSerializer(data=request.data)
        if ser.is_valid():
            ser.save(created_by=request.user)
            return Response(ser.data)
        return Response(ser.errors, status=400)

    def patch(self, request, pk):
        client = Client.objects.get(id=pk)
        if not request.user.is_manager:
            return Response({"error": "Only managers can edit clients"}, status=403)
        
        ser = ClientSerializer(client, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=400)

    def delete(self, request, pk):
        client = Client.objects.get(id=pk)
        if not request.user.is_manager:
            return Response({"error": "Only managers can delete clients"}, status=403)
        
        client.delete()
        return Response({"message": "Client deleted successfully"})


class TaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            task = Task.objects.get(id=pk)
            if request.user.is_manager or task.assigned_to == request.user:
                ser = TaskSerializer(task)
                return Response(ser.data)
            return Response({"error": "Permission denied"}, status=403)
        
        if request.user.is_manager:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(assigned_to=request.user)
        
        ser = TaskSerializer(tasks, many=True)
        return Response(ser.data)

    def post(self, request):
        if not request.user.is_manager:
            return Response({"error": "Only managers can create tasks"}, status=403)
        
        ser = TaskSerializer(data=request.data)
        if ser.is_valid():
            ser.save(created_by=request.user)
            return Response(ser.data)
        return Response(ser.errors, status=400)
    
    def patch(self, request, pk):
        task = Task.objects.get(id=pk)
        if not request.user.is_manager and task.assigned_to != request.user:
            return Response({"error": "Permission denied"}, status=403)
        
        ser = TaskSerializer(task, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=400)

    def delete(self, request, pk):
        task = Task.objects.get(id=pk)
        if not request.user.is_manager:
            return Response({"error": "Only managers can delete tasks"}, status=403)
        
        task.delete()
        return Response({"message": "Task deleted successfully"})