from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AccessRoleRule
from .serializers import AccessRoleRuleSerializer
from .permissions import permission_required


class AccessRuleListView(APIView):
    @permission_required('access_rules', 'read')
    def get(self, request):
        rules = AccessRoleRule.objects.all()
        return Response(AccessRoleRuleSerializer(rules, many=True).data)

    @permission_required('access_rules', 'create')
    def post(self, request):
        serializer = AccessRoleRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccessRuleDetailView(APIView):
    @permission_required('access_rules', 'update')
    def put(self, request, pk):
        try:
            rule = AccessRoleRule.objects.get(pk=pk)
        except AccessRoleRule.DoesNotExist:
            return Response({'error': 'Rule not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccessRoleRuleSerializer(rule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_required('access_rule', 'delete')
    def delete(self, request, pk):
        try:
            rule = AccessRoleRule.objects.get(pk=pk)
        except AccessRoleRule.DoesNotExist:
            return Response({'error': 'Rule not found'}, status=status.HTTP_404_NOT_FOUND)

        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)