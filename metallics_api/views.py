from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from .models import Chemical, Composition, Commodity
from .serializers import ChemicalSerializer, CompositionSerializer, CommoditySerializer
from django.http.response import JsonResponse
from rest_framework import viewsets

class GetComodityDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, id):
        # Check Comodity existance by id
        try:
            return Commodity.objects.get(id=id)
        except Commodity.DoesNotExist:
            return "Not Exist"
    
    def get(self, request, id, format=None):
        #Get Comodity by ID
        commodity = self.get_object(id)
        if commodity != "Not Exist":
            serializer = CommoditySerializer(commodity)
            return Response(serializer.data)
        else:
            return JsonResponse({"Message:":"Comodity Not Exist. Please provide valid ID"})

class UpdateComodityDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, id):
        # Check Comodity existance by id
        try:
            return Commodity.objects.get(id=id)
        except Commodity.DoesNotExist:
            return "Not Exist"
    def put(self, request, format=None):
        # Update Comodity by ID.
        try:
            response=[]
            resp_type = isinstance(request.data, list)
            if resp_type:
                for row in request.data:
                    cid=row["id"]
                    commodity = self.get_object(cid)
                    if commodity != "Not Exist":
                        serializer = CommoditySerializer(commodity, data=row)
                        if serializer.is_valid():
                            serializer.save()
                            response.append(serializer.data)
                        else:
                            response.append({"id":"{}".format(cid),"Message:":"Invalid Inputs. Please provide valid inputs"})
                    else: response.append({"id":"{}".format(cid),"Message:":"Comodity Not Exist. Please provide valid ID"})
                return Response(response)
            else:
                return Response({"Error":"Invalid Request Body. Please Provide List of JSON with valid inputs."})
        except Exception as errMsg:
            print("Exception: {}".format(errMsg))
            return Response({"Error":"Exception Occured while proccesing request."})

class RemoveChemicalComposition(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, commodity_id, element_id):
        # Check Composition existance by id
        try:
            return Composition.objects.filter(commodity=commodity_id, element=element_id).first()
        except Composition.DoesNotExist:
            return "Not Exist"
    def delete(self, request, format=None):
        # Delete composition entry by ID
        commodity = request.data["commodity"]
        element = request.data["element"]
        composition = self.get_object(commodity,element)
        if composition != "Not Exist":
            composition.delete()
            return Response({"commodity_id":"{}".format(commodity),"element_id":"{}".format(element),"Message":"Record deleted successfully"})
        else: return Response({"commodity_id":"{}".format(commodity),"element_id":"{}".format(element),"Message":"Record dose not exist."})
