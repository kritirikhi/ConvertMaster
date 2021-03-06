from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import MyConversion
from django.contrib.auth.decorators import *
import os
from datetime import datetime
from django.conf import settings
import pandas as pd
import csv
import json  
import xmltodict
import pprint
import dicttoxml



# =========================renders the landing page======================================
def index(request):
    return render(request,'index.html')

# ||+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++||
# ||                                                                                     ||
# ||                                                                                     ||
# ||                                                                                     ||
# ||                            CONVERSION CODE STARTS                                   ||
# ||                                                                                     ||
# ||                                                                                     ||
# ||+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++||
# 
# -------------------------------XML-TO-JSON----------------------------------------------
def xmlToJson(request):
    if request.method == 'POST':
        # Retrieveing the post data
        xml_data = request.POST['xml']
        
        #creating the file name based on date and time
        filename = ""
        name = datetime.now()
        filename += str(name.year)+str(name.month)+str(name.day)+str(name.hour)+str(name.minute)+str(name.second)+str(name.microsecond)

        # Creating the file name based on user 
        if request.user.is_authenticated or request.user.is_superuser:
            input_file_name = str(request.user) + '/' + filename + '.xml'
            output_file_name = str(request.user) + '/' + filename + '.json'
        else:
            input_file_name = filename + '.xml'
            output_file_name = filename + '.json'

        # Writing the post data to the input file
        saved_file = open(os.path.join(settings.MEDIA_ROOT, input_file_name), 'w')
        saved_file.write(xml_data)
        saved_file.close()

        # Converting XML to JSON
        with open('media/'+ input_file_name) as fd:
            doc = xmltodict.parse(fd.read())

        jsonFile = open(os.path.join(settings.MEDIA_ROOT, output_file_name), 'w')
        out = json.dumps(doc, indent=" ")
        jsonFile.write(out)
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(json.dumps(doc))
              
        # preparing JSON response data    
        response = dict()
        response['ans'] = out
        response['filename'] = filename
        
        # Removing the intermediate files if User is not Authenticated
        if request.user.is_superuser or request.user.is_authenticated:
            print('User is authenticated')
        else:
            os.remove(os.path.join(settings.MEDIA_ROOT, input_file_name))
            os.remove(os.path.join(settings.MEDIA_ROOT, output_file_name))

        # returning the JSON Response
        return JsonResponse(response, safe=False)
        
    else:
        return render(request,'convertEngine/xml_to_json.html')

# -------------------------------XML-TO-CSV----------------------------------------------
def xmlToCsv(request):
    if request.method == 'POST':
        # Retrieveing the post data
        xml_data = request.POST['xml']
        
        #creating the file name based on date and time
        filename = ""
        name = datetime.now()
        filename += str(name.year)+str(name.month)+str(name.day)+str(name.hour)+str(name.minute)+str(name.second)+str(name.microsecond)

        # Creating the file name based on user 
        if request.user.is_authenticated or request.user.is_superuser:
            input_file_name = str(request.user) + '/' + filename + '.xml'
            output_file_name = str(request.user) + '/' + filename + '.csv'
        else:
            input_file_name = filename + '.xml'
            output_file_name = filename + '.csv'

        # Writing the post data to the file
        
        saved_file = open(os.path.join(settings.MEDIA_ROOT, input_file_name), 'w')
        saved_file.write(xml_data)
        saved_file.close()
        
        # Converting XML to CSV
        with open('media/' + input_file_name) as fd:
            doc = xmltodict.parse(fd.read())
        out = json.dumps(doc)
        data = json.loads(out)

        x = data['csv_data']['row']
        data_df = pd.DataFrame(x)
        data_df.to_csv(os.path.join(settings.MEDIA_ROOT, output_file_name), index=False)

        data_csv = open('media/'+ output_file_name).read()
        
        # preparing JSON response data    
        response = dict()
        response['ans'] = data_csv
        response['filename'] = filename

        
        # Removing the intermediate files if User is not Authenticated
        if request.user.is_superuser or request.user.is_authenticated:
            print('User is authenticated')
        else:
            os.remove(os.path.join(settings.MEDIA_ROOT, input_file_name))
            os.remove(os.path.join(settings.MEDIA_ROOT, output_file_name))


        # returning the JSON Response
        return JsonResponse(response, safe=False)
    else:
        return render(request,'convertEngine/xml_to_csv.html')

# -------------------------------CSV-TO-JSON----------------------------------------------
def csvToJson(request):
    if request.method == 'POST':
        # Retrieveing the post data
        csv_data = request.POST['csv']
        
        #creating the file name based on time
        filename = ""
        name = datetime.now()
        filename += str(name.year)+str(name.month)+str(name.day)+str(name.hour)+str(name.minute)+str(name.second)+str(name.microsecond)

        # Creating the file name based on user 
        if request.user.is_authenticated or request.user.is_superuser:
            input_file_name = str(request.user) + '/' + filename + '.csv'
            output_file_name = str(request.user) + '/' + filename + '.json'
        else:
            input_file_name = filename + '.csv'
            output_file_name = filename + '.json'

        # Writing the post data to the file

        saved_file = open(os.path.join(settings.MEDIA_ROOT, input_file_name), 'w')
        saved_file.write(csv_data)
        saved_file.close()

        # Converting the csv file to the json format

        csvfile = open(os.path.join(settings.MEDIA_ROOT, input_file_name), 'r' )  
        reader = csv.DictReader(csvfile)   
        out = json.dumps( [ row for row in reader ],indent=" " )
        jsonfile = open(os.path.join(settings.MEDIA_ROOT, output_file_name), 'w')  
        jsonfile.write(out)
        jsonfile.close()
        
        # preparing JSON response data    
        response = dict()
        response['ans'] = out
        response['filename'] = filename

        
        # Removing the intermediate files if User is not Authenticated
        if request.user.is_superuser or request.user.is_authenticated:
            print('User is authenticated')
        else:
            os.remove(os.path.join(settings.MEDIA_ROOT, input_file_name))
            os.remove(os.path.join(settings.MEDIA_ROOT, output_file_name))


        # returning the JSON Response
        return JsonResponse(response, safe=False)

    else:
        return render(request,'convertEngine/csv_to_json.html')

# -------------------------------CSV-TO-XML----------------------------------------------
def csvToXml(request):
    if request.method == 'POST':
        # Retrieveing the post data
        csv_data = request.POST['csv']
        # print('csv data recieved')
        #creating the file name based on time
        filename = ""
        name = datetime.now()
        filename += str(name.year)+str(name.month)+str(name.day)+str(name.hour)+str(name.minute)+str(name.second)+str(name.microsecond)
        # print('filename created')
        # print(filename)

        # Creating the file name based on user 
        if request.user.is_authenticated or request.user.is_superuser:
            input_file_name = str(request.user) + '/' + filename + '.csv'
            output_file_name = str(request.user) + '/' + filename + '.xml'
        else:
            input_file_name = filename + '.csv'
            output_file_name = filename + '.xml'

        # Writing the post data to the file
       
        saved_file = open(os.path.join(settings.MEDIA_ROOT, input_file_name), 'w')
        saved_file.write(csv_data)
        saved_file.close()
        print(input_file_name)
        
    
        csvData = csv.reader(open('media/'+ input_file_name))
        # csvData = open('media/'+input_file_name)
        # csvData = csv.reader(csvData)
        xmlData = open(os.path.join(settings.MEDIA_ROOT, output_file_name), 'w')
        xmlData.write('<?xml version="1.0"?>' + "\n")
        # there must be only one top-level tag
        xmlData.write('<csv_data>' + "\n")
        
        rowNum = 0
        for row in csvData:
            if rowNum == 0:
                tags = row
                # replace spaces w/ underscores in tag names
                for i in range(len(tags)):
                    tags[i] = tags[i].replace(' ', '_')
            else: 
                xmlData.write('<row>' + "\n")
                for i in range(len(tags)):
                    xmlData.write('    ' + '<' + tags[i] + '>' + row[i] + '</' + tags[i] + '>' + "\n")
                xmlData.write('</row>' + "\n")
                    
            rowNum +=1

        xmlData.write('</csv_data>' + "\n")
        xmlData.close()

        data_xml = open('media/'+ output_file_name).read()
        
        # preparing JSON response data    
        response = dict()
        response['ans'] = data_xml
        response['filename'] = filename

        
        # Removing the intermediate files if User is not Authenticated
        if request.user.is_superuser or request.user.is_authenticated:
            print('User is authenticated')
        else:
            os.remove(os.path.join(settings.MEDIA_ROOT, input_file_name))
            os.remove(os.path.join(settings.MEDIA_ROOT, output_file_name))


        # returning the JSON Response
        return JsonResponse(response, safe=False)
       
    else:
        return render(request,'convertEngine/csv_to_xml.html')

# -------------------------------JSON-TO-CSV----------------------------------------------
def jsonToCsv(request):
    if request.method == 'POST':
        # Retrieveing the post data
        json_data = request.POST['json']
        
        #creating the file name based on time
        filename = ""
        name = datetime.now()
        filename += str(name.year)+str(name.month)+str(name.day)+str(name.hour)+str(name.minute)+str(name.second)+str(name.microsecond)

        # Creating the file name based on user 
        if request.user.is_authenticated or request.user.is_superuser:
            input_file_name = str(request.user) + '/' + filename + '.json'
            output_file_name = str(request.user) + '/' + filename + '.csv'
        else:
            input_file_name = filename + '.json'
            output_file_name = filename + '.csv'
        
        # Writing the post data to the file

        saved_file = open(os.path.join(settings.MEDIA_ROOT, input_file_name), 'w')
        saved_file.write(json_data)
        saved_file.close()

        # Converting JSON to CSV
        
        data_df = pd.read_json('media/' + input_file_name, orient='records')
        data_df.to_csv(os.path.join(settings.MEDIA_ROOT, output_file_name), index=False)

        data_csv = open('media/'+ output_file_name).read()

        # preparing JSON response data    
        response = dict()
        response['ans'] = data_csv
        response['filename'] = filename

        
        # Removing the intermediate files if User is not Authenticated
        if request.user.is_superuser or request.user.is_authenticated:
            print('User is authenticated')
        else:
            os.remove(os.path.join(settings.MEDIA_ROOT, input_file_name))
            os.remove(os.path.join(settings.MEDIA_ROOT, output_file_name))

        # returning the JSON Response
        return JsonResponse(response, safe=False)
    else:
        return render(request,'convertEngine/json_to_csv.html')

# -------------------------------JSON-TO-XML----------------------------------------------
def jsonToXml(request):
    if request.method == 'POST':
        # Retrieveing the post data
        json_data = request.POST['json']
        
        #creating the file name based on time
        filename = ""
        name = datetime.now()
        filename += str(name.year)+str(name.month)+str(name.day)+str(name.hour)+str(name.minute)+str(name.second)+str(name.microsecond)
        
        # Creating the file name based on user 
        if request.user.is_authenticated or request.user.is_superuser:
            input_file_name = str(request.user) + '/' + filename + '.json'
            output_file_name = str(request.user) + '/' + filename + '.xml'
        else:
            input_file_name = filename + '.json'
            output_file_name = filename + '.xml'

        # Writing the post data to the file
        saved_file = open(os.path.join(settings.MEDIA_ROOT, input_file_name), 'w')
        saved_file.write(json_data)
        saved_file.close()

        # Converting JSON to XML
        data = open('media/' + input_file_name, 'r').read()
        data = json.loads(data)

        out = open(os.path.join(settings.MEDIA_ROOT, output_file_name), 'w')
        out.write(xmltodict.unparse(data, pretty=True))

        # preparing JSON response data    
        response = dict()
        response['ans'] = str(xmltodict.unparse(data, pretty=True))
        response['filename'] = filename
        
        # Removing the intermediate files if User is not Authenticated
        if request.user.is_superuser or request.user.is_authenticated:
            print('User is authenticated')
        else:
            os.remove(os.path.join(settings.MEDIA_ROOT, input_file_name))
            os.remove(os.path.join(settings.MEDIA_ROOT, output_file_name))

        # returning the JSON Response
        return JsonResponse(response, safe=False)
    else:
        return render(request,'convertEngine/json_to_xml.html')

# ||+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++||
# ||                                                                                     ||
# ||                                                                                     ||
# ||                                                                                     ||
# ||                            CONVERSION CODE ENDS                                     ||
# ||                                                                                     ||
# ||                                                                                     ||
# ||+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++||


# # ==========================DOCUMENTATION================================================
def documentation(request):
    return render(request, 'convertEngine/doc.html')

# ====================shows previous convertions for logined users==========================
def saveconversion(request):
    if request.method == 'POST':
        filename = request.POST['filename']
        original = request.POST['original']
        converted = request.POST['converted']
        convName = request.POST['convName']
        conversion = MyConversion(user=request.user,filename=filename,original=original,converted=converted,convName=convName)
        conversion.save()
        return JsonResponse({'ans':'Consverion Success'}, safe=False)

# ====================shows previous convertions for logined users==========================

@login_required
def myconversions(request):
    
    myconversion=MyConversion.objects.all().filter(user=request.user)
    
    x=[]
    for obj in myconversion:
        d={}
        d['filename']=obj.filename 
        d['converted']=obj.converted
        d['original'] = obj.original
        d['convName'] = obj.convName
        downloadlink='/media/' + str(obj.user.username) +'/'+ str(obj.filename) + '.' + str(obj.converted)
        d['downloadlink']=downloadlink
        x.append(d)

    context={
        'mydata':x
    }

    return render(request,'convertEngine/myconversions.html',context)

#===================view of only one specific conversion=================================

@login_required
def SingleConversionView(request):

    if request.method =='POST':

        original=request.POST['original']
        converted=request.POST['converted']
        convName=request.POST['convName']
        filename=request.POST['filename']

        singleconversion=MyConversion.objects.all().filter(user=request.user,filename=filename,convName=convName)
        
        #saved_file = open(os.path.join(settings.MEDIA_ROOT, input_file_name), 'w')
        # input_file_name = str(request.user) + '/' + filename + '.csv'
        # saved_file = open(os.path.join(settings.MEDIA_ROOT, input_file_name), 'w')
        
        
        originalfilename=str(request.user)+ '/' + str(filename) + '.' + str(original)
        originalfile = open(os.path.join(settings.MEDIA_ROOT,originalfilename),'r').read()

        
        convertedfilename=str(request.user) + '/' + str(filename) + '.' + str(converted)
        convertedfile=open(os.path.join(settings.MEDIA_ROOT,convertedfilename),'r').read()

        context={
            'originalfile':originalfile,
            'convertedfile':convertedfile,
            'converted':converted,
            'original':original,
           
        }
    return render (request,'convertEngine/SingleConversionView.html',context)

# ===========================TEST FUNC===============================
def test(request):
    pass
    # x = "Hello world"
    # # user = request.session['User']
    # filename = '6-06-2019'
    # #form = "<form action=\"{% url 'save' %}\"" + ' method="post"><input type="hidden" value="JSON" name=\'original\'><input type="hidden" value="XML" name=\'converted\'><input type="hidden" value="kriti/20197205457858905" id="ilename" name="filename"><input type="hidden" name="convName" value="Enter Conversion Name"><input type="submit" class="btn btn-primary" value="Save conversion"></form>'
    # filepath = '/media/kriti/201971863836316660.json'
    # filepath = '/media/images/logo_short.png'
    # return render(request,'test.html')