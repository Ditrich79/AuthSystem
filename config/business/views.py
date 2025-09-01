from rest_framework.views import APIView
from rest_framework.response import Response
from access_control.permissions import permission_required

class ProductListView(APIView):
    @permission_required('products', 'read')
    def get(self, request):
        mock_products = [
            {"id": 1, "name": "Laptop", "price": 1000},
            {"id": 2, "name": "Mouse", "price": 25}
        ]
        return Response(mock_products)

    @permission_required('products', 'create')
    def post(self, request):
        return Response({'message': 'Product created'}, status=201)

class OrderListView(APIView):
    @permission_required('orders', 'read', own_only=True)
    def get(self, request):
        mock_orders = [{"id": 1, "product": "Laptop", "owner": request.user.id}]
        return Response(mock_orders)
