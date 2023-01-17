from flask import render_template, redirect, url_for, request
import requests
from solar import app
from solar.forms import Location_Form


@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/home')
def home():
    return redirect(url_for("home_page"))

@app.route('/solar_calculator')
def solar_calculator_page():
    return render_template("calculator.html")

@app.route('/test')
def test_page():
    #appliance_form=Appliance_Form()
    return render_template("test.html")

@app.route('/solar_insolation', methods=['GET', 'POST'])
def solar_insolation_page():
    Location_form = Location_Form()
    if request.method == "POST":
        baseURLGeoCoding = "https://maps.googleapis.com/maps/api/geocode/json?address="
        GeoCoding_API_Key = "Enter the API KEY"
        Solar_API_Key = "Enter the API Key"
        baseURLSolar = "https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key="
        
        AddressLineOne = request.form.get('AddressOne')
        AddressLineTwo = request.form.get('AddressTwo')
        AddressLineThree = request.form.get('Country')
        Address = AddressLineOne + "+" + AddressLineTwo + "+" + AddressLineThree
        
        Geodata = requests.get(baseURLGeoCoding + Address + "&key=" + GeoCoding_API_Key)
        Geodata = Geodata.json()

        EnteredAddress=["Not a valid Address"]
        Insolation =[]
        if Geodata['status'] == 'OK':
            print(Geodata["results"][0]["formatted_address"])
            EnteredAddress=[(Geodata["results"][0]["formatted_address"])]
            latitude = Geodata["results"][0]["geometry"]["location"]["lat"]
            longitude = Geodata["results"][0]["geometry"]["location"]["lng"]
            data = requests.get(baseURLSolar + Solar_API_Key + "&lat=" + str(latitude) +"&lon=" + str(longitude))
            data = data.json()
            print(data)
        
        
            if data["outputs"]["avg_dni"] == 'no data':
                pass
            else:
                Insolation.append(data["outputs"]["avg_dni"]["annual"]) 
                Insolation.append(data["outputs"]["avg_ghi"]['annual'])
                Insolation.append(data["outputs"]["avg_lat_tilt"]['annual'])
                print(data["outputs"]["avg_ghi"])
                print(data["outputs"]["avg_lat_tilt"])
                
            

        return render_template("solar_insolation.html", Location_Form = Location_form, EnteredAddress= EnteredAddress, Insolation =Insolation)

        

    if request.method == "GET":
        return render_template("solar_insolation.html", Location_Form = Location_form)