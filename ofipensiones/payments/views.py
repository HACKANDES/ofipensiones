from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OfipensionesLog, TermPayment, Bill
from .serializers import PaymentReceiptSerializer, BillSerializer

# from authlib.integrations.django_oauth2 import ResourceProtector

# require_auth = ResourceProtector()

import time
from datetime import timedelta


# @require_auth(None)
class PaymentReceiptList(APIView):
    def get(self, request):
        s = time.time()
        payment_receipts = TermPayment.objects.all()
        serializer = PaymentReceiptSerializer(payment_receipts, many=True)
        e = time.time()

        delta = timedelta(seconds=e - s)

        OfipensionesLog(operation_name="payment_receipt_list", time_taken=delta).save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class BillList(APIView):
    def get(self, request):
        s = time.time()
        bill = Bill.objects.all()
        serializer = BillSerializer(bill, many=True)
        e = time.time()

        delta = timedelta(seconds=e - s)
        OfipensionesLog(operation_name="bill_list", time_taken=delta).save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        s = time.time()
        serializer = BillSerializer(data=request.data)

        if not serializer.is_valid():
            e = time.time()
            delta = timedelta(seconds=e - s)
            OfipensionesLog(
                operation_name="bill_create_failed", time_taken=delta
            ).save()

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        e = time.time()

        delta = timedelta(seconds=e - s)
        OfipensionesLog(operation_name="bill_create", time_taken=delta).save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BillDetail(APIView):
    def get_object(self, pk):
        try:
            return Bill.objects.get(pk=pk)
        except Bill.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        s = time.time()
        bill = self.get_object(pk)
        if bill is None:
            e = time.time()
            delta = timedelta(seconds=e - s)
            OfipensionesLog(
                operation_name="bill_get_not_found", time_taken=delta
            ).save()

            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BillSerializer(bill)
        e = time.time()

        delta = timedelta(seconds=e - s)
        OfipensionesLog(operation_name="bill_get", time_taken=delta).save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        s = time.time()
        bill = self.get_object(pk)
        if bill is None:
            e = time.time()
            delta = timedelta(seconds=e - s)
            OfipensionesLog(
                operation_name="bill_put_not_found", time_taken=delta
            ).save()

            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BillSerializer(bill, data=request.data)

        if not serializer.is_valid():
            e = time.time()
            delta = timedelta(seconds=e - s)
            OfipensionesLog(operation_name="bill_put_failed", time_taken=delta).save()

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        e = time.time()
        delta = timedelta(seconds=e - s)
        OfipensionesLog(operation_name="bill_put", time_taken=delta).save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        s = time.time()
        bill = self.get_object(pk)
        if bill is None:
            e = time.time()
            delta = timedelta(seconds=e - s)
            OfipensionesLog(
                operation_name="bill_delete_not_found", time_taken=delta
            ).save()

            return Response(status=status.HTTP_404_NOT_FOUND)

        bill.delete()
        e = time.time()
        delta = timedelta(seconds=e - s)
        OfipensionesLog(operation_name="bill_delete", time_taken=delta).save()

        return Response(status=status.HTTP_204_NO_CONTENT)
