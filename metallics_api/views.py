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
from django.db.models import Sum

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
        if ((commodity == "Not Exist") or (commodity is None)):
            return JsonResponse({"Message:":"Comodity Not Exist. Please provide valid ID"})
        else:
            serializer = CommoditySerializer(commodity)
            return Response(serializer.data) 

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
                    if ((commodity == "Not Exist") or (commodity is None)):
                        response.append({"id":"{}".format(cid),"Message:":"Comodity Not Exist. Please provide valid ID"})
                    else: 
                        serializer = CommoditySerializer(commodity, data=row)
                        if serializer.is_valid():
                            serializer.save()
                            response.append(serializer.data)
                        else:
                            response.append({"id":"{}".format(cid),"Message:":"Invalid Inputs. Please provide valid inputs"})
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
    
    def check_element_existance(self):
        # Check unknown element already exist or not in composition by name if exist return id
        resp={"exist":False,"element_id":-1}
        try:
            get_unknown_element_obj = Chemical.objects.filter(name='Unknown').values('id')
            if len(get_unknown_element_obj)!=0:
                resp["exist"]=True
                resp["element_id"]=int(get_unknown_element_obj[0]['id'])
            return resp
        except Exception as errMsg:
            print("Exception: {}".format(errMsg))
            return resp

    def delete(self, request, format=None):
        # Delete composition entry by ID
        resp = {"Message":"Unknown Error"}
        try:
            commodity = request.data["commodity"]
            element = request.data["element"]
            # Check Composition Exist or Not
            composition = self.get_object(commodity,element)
            if ((composition == "Not Exist") or (composition is None)):
                resp["Message"] = "Composition record dose not exist to delete."
            else:
                # Get Current element percentage
                existing_sum_percentage = Composition.objects.filter(commodity=commodity,element=element).aggregate(Sum('percentage'))
                el_percentage = float(existing_sum_percentage['percentage__sum'])
                print("### : Current Element:{} ::::: Percentage: {}".format(element,el_percentage))

                # check unkown element existance in elements.
                un_element = self.check_element_existance()
                if un_element["exist"]: 
                    un_element_id = un_element["element_id"]
                    print("Unknown Element In Elements.. ID: {}".format(un_element_id))

                    if un_element_id != element:
                        # check unknown element exist in commodity if exist update percentage elase create & update percentage
                        composition_un = self.get_object(commodity, un_element_id)
                        print("composition_un ::::::: {}".format(composition_un))
                        if ((composition_un == "Not Exist") or (composition_un is None)):
                            # Get All elements Percentage
                            all_percentage=0.0
                            all_sum_percentage = Composition.objects.filter(commodity=commodity).exclude(element=element).aggregate(Sum('percentage'))
                            if all_sum_percentage['percentage__sum'] is None:
                                all_percentage=0.0
                            else:
                                all_percentage = float(all_sum_percentage['percentage__sum'])
                            print("All Percentage : {}".format(all_percentage))

                            # create unknown element and update percentage
                            un_el_data2={"commodity":commodity,"element":un_element_id,"percentage":float(100 - all_percentage)}
                            ce_serializer_new = CompositionSerializer(data=un_el_data2)
                            if ce_serializer_new.is_valid():
                                ce_serializer_new.save()
                                composition.delete()
                                resp["Message"] = "Composition Element Deleted, Unkown Element Added & Percentage Updated Successfully."
                        else:
                            un_el_compo = Composition.objects.filter(element=un_element_id).aggregate(Sum('percentage'))
                            un_el_percentage = float(un_el_compo['percentage__sum'])
                            print("Unknown Element Exist :::: Percentage: {}".format(un_el_percentage))

                            # Update Unknown Element Percentage
                            un_el_data={"commodity":commodity,"element":un_element_id,"percentage":float(el_percentage + un_el_percentage)}
                            ce_serializer = CompositionSerializer(composition_un, data=un_el_data)
                            if ce_serializer.is_valid():
                                ce_serializer.save()
                                composition.delete()
                                resp["Message"] = "Composition Element Deleted & Unkown Element Percentage Updated Successfully."
                    else:
                        resp["Message"] = "Unable to Remove Unknown Element. Try Another Element."
                else: 
                    resp["Message"] = "Unknown Element not Exist. Create Unknown Element than try."
            return Response({"commodity_id":"{}".format(commodity),"element_id":"{}".format(element),"Message":"{}".format(resp["Message"])})
        except Exception as errMsg:
            print("Exception: {}".format(errMsg))
            return Response(resp)


class AddChemicalComposition(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, commodity_id, element_id):
        # Check element already exist or not in composition by id
        try:
            return Composition.objects.filter(commodity=commodity_id, element=element_id).first()
        except Composition.DoesNotExist:
            return "Not Exist"

    def check_element_existance(self):
        # Check unknown element already exist or not in composition by name if exist return id
        resp={"exist":False,"element_id":-1}
        try:
            get_unknown_element_obj = Chemical.objects.filter(name='Unknown').values('id')
            if len(get_unknown_element_obj)!=0:
                resp["exist"]=True
                resp["element_id"]=int(get_unknown_element_obj[0]['id'])
            return resp
        except Exception as errMsg:
            print("Exception: {}".format(errMsg))
            return resp

    def post(self, request, format=None):
        permission_classes = (IsAuthenticated,)
        """
        Get Unkown element id if exist else create new element and get id.
        """
        resp = {}
        try:
            element = self.check_element_existance()
            un_element_id=None
            if not element["exist"]:
                dataa={"name":"Unknown"}
                ch_serializer = ChemicalSerializer(data=dataa)
                if ch_serializer.is_valid():
                    ch_serializer.save()
                    #print("##### New Element Created. Name: Unknown")
                    element_new = self.check_element_existance()
                    if element_new["exist"]: un_element_id = element_new["element_id"]
            else:
                un_element_id = element["element_id"]
                #print("##### Unknown Element Already Exist. ID: {}".format(un_element_id))

            if un_element_id:
                req_commodity = int(request.data["commodity"])
                req_element = int(request.data["element"])
                req_percentage = float(request.data["percentage"])
                if un_element_id != req_element:
                    # Check Element Existance and calculate percentage to get exact unkown percentage
                    un_exist=True
                    known_percentage=0
                    chk_un_composition = self.get_object(req_commodity,un_element_id)
                    if ((chk_un_composition == "Not Exist") or (chk_un_composition is None)):
                        un_exist=False
                        print("@@@@ Unknown Element Not In Composition")

                    chk_el_composition = self.get_object(req_commodity,req_element)
                    if ((chk_el_composition == "Not Exist") or (chk_el_composition is None)):
                        print("@@@@ Element Not In Composition")
                        if not un_exist:
                            print("@@@@ Element Not In Composition >> if not UN ")
                            existing_sum_percentage = Composition.objects.filter(commodity=req_commodity).aggregate(Sum('percentage'))
                            if existing_sum_percentage['percentage__sum'] is None:
                                known_percentage= req_percentage
                            else:
                                known_percentage = float(existing_sum_percentage['percentage__sum']) + req_percentage
                        else:
                            print("@@@@ Element Not In Composition >> UN exist")
                            existing_sum_percentage = Composition.objects.filter(commodity=req_commodity).exclude(element=un_element_id).aggregate(Sum('percentage'))
                            if existing_sum_percentage['percentage__sum'] is None:
                                known_percentage= req_percentage
                            else:
                                known_percentage = float(existing_sum_percentage['percentage__sum']) + req_percentage
                    else:
                        print("@@@@ Element In Composition")
                        if not un_exist:
                            print("@@@@ Element In Composition >> if not UN ")
                            existing_sum_percentage = Composition.objects.filter(commodity=req_commodity).exclude(element=req_element).aggregate(Sum('percentage'))
                            if existing_sum_percentage['percentage__sum'] is None:
                                known_percentage= req_percentage
                            else:
                                known_percentage = float(existing_sum_percentage['percentage__sum']) + req_percentage
                        else:
                            print("@@@@ Element In Composition >> UN exist")
                            existing_sum_percentage = Composition.objects.filter(commodity=req_commodity).exclude(element__in=[un_element_id,req_element]).aggregate(Sum('percentage'))
                            if existing_sum_percentage['percentage__sum'] is None:
                                known_percentage= req_percentage
                            else:
                                known_percentage = float(existing_sum_percentage['percentage__sum']) + req_percentage
     
                    unknown_percentage = float(100 - known_percentage)
                    print("@@@@ Known Percentage : {}".format(known_percentage))
                    print("@@@@ Unknown Percentage : {}".format(unknown_percentage))

                    if known_percentage > 100.00:
                        print("Sum of all elements more than 100% not allowd. {} %".format(known_percentage))
                        resp["Message"] = "Total Percentage is {}%. Its above 100% not allowd.".format(known_percentage)
                    else:
                        """
                        Create/ Update known Element with percentage
                        """
                        if ((chk_el_composition == "Not Exist") or (chk_el_composition is None)):
                            # Create New
                            kn_serializer_new = CompositionSerializer(data=request.data)
                            if kn_serializer_new.is_valid():
                                kn_serializer_new.save()
                                resp["known"] = "Element add successfully in composition with percentage."
                                print("@@@ Element Created Successfully.")
                        else:
                            # Update Existing
                            kn_serializer = CompositionSerializer(chk_el_composition, data=request.data)
                            if kn_serializer.is_valid():
                                kn_serializer.save()
                                resp["known"] = "Already Exist. Percentage Updated Successfully."
                                print("@@@ Element Percentage Updated Successfully.")

                        """
                        Create/ Update Unknown Element with percentage
                        """
                        un_el_data={"commodity":req_commodity,"element":un_element_id,"percentage":unknown_percentage}
                        
                        if ((chk_un_composition == "Not Exist") or (chk_un_composition is None)):
                            # Create New
                            ce_serializer_new = CompositionSerializer(data=un_el_data)
                            if ce_serializer_new.is_valid():
                                ce_serializer_new.save()
                                resp["unknown"] = "Element add successfully in composition with percentage."
                        else:
                            # Update Existing
                            un_el_data["id"]=un_element_id
                            ce_serializer = CompositionSerializer(chk_un_composition, data=un_el_data)
                            if ce_serializer.is_valid():
                                ce_serializer.save()
                                resp["unknown"] = "Already Exist. Percentage Updated Successfully."    
                else: 
                    resp["Message"]="Not Allowed to add/update unknown element."
            else:
                resp["Message"]="Unknown Element not exist to update composition"
            return JsonResponse(resp)
        except Exception as errMsg:
            print("Exception: {}".format(errMsg))
            resp["Message"]="Exception occured while add/update composition"
            return JsonResponse(resp) 
