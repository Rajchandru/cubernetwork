
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer

class AccountDetailView(APIView):
    serializer_class=AccountSerializer
    def get(self, request, pk=None):
        if pk:
            try:
                account = Account.objects.get(pk=pk)
                serializer = AccountSerializer(account)
                return Response(serializer.data)
            except Account.DoesNotExist:
                return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            accounts = Account.objects.all()
            serializer = AccountSerializer(accounts, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DestinationAPIView(APIView):
    serializer_class=DestinationSerializer
    def get(self, request, pk=None):
        if pk:
            try:
                destination = Destination.objects.get(pk=pk)
                serializer = DestinationSerializer(destination)
                return Response(serializer.data)
            except Destination.DoesNotExist:
                return Response({'error': 'Destination not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            destinations = Destination.objects.all()
            serializer = DestinationSerializer(destinations, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            destination = Destination.objects.get(pk=pk)
        except Destination.DoesNotExist:
            return Response({'error': 'Destination not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DestinationSerializer(destination, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            destination = Destination.objects.get(pk=pk)
        except Destination.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        destination.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DestinationListByAccount(APIView):
    def get(self, request, account_id):
        print("account_id",account_id)
        destinations = Destination.objects.filter(account_id=account_id)
        
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)

class IncomingData(APIView):
    def post(self, request):
        data = request.data
        print("data",data)
        headers = request.headers
        print("headers",headers)
        print("typeheaders",type(headers))

        # Validate incoming data and headers
        if not data or not headers.get('Content-Type') == 'application/json':
            print("jason data")
            return Response({'message': 'Invalid Data'}, status=400)
        if 'CL-XTOKEN' not in headers:
            
            return Response({'message': 'Unauthenticated'}, status=401)

        # Identify account using app secret token
        app_secret_token = headers['CL-XTOKEN']
        print("app_secret_token",app_secret_token)
        try:
            account = Account.objects.get(app_secret_token=app_secret_token)
        except Account.DoesNotExist:
            return Response({'message': 'Invalid App Secret Token'}, status=401)

        # Send data to destinations associated with the account
        destinations = Destination.objects.filter(account=account)
        for destination in destinations:
            print('destinations',destination)
            # Implement logic to send data to each destination using HTTP client

        return Response({'message': 'Data sent to destinations'}, status=200)
