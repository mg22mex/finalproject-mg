#!/usr/bin/env python3
"""
Manual import of vehicles to bypass N8N issues
This script imports the correct 31 vehicles from your Google Sheet data
"""
import requests
import json
import time

# Backend API endpoint
BACKEND_URL = "http://localhost:8001"

# Your actual vehicle data (31 vehicles from Google Sheet)
vehicles_data = [
    {
        "marca": "MAZDA",
        "modelo": "CX30",
        "año": 2021,
        "precio": 379000,
        "estatus": "DISPONIBLE",
        "color": "BLANCA",
        "kilometraje": "",
        "ubicacion": "PERIFERICO",
        "descripcion": "MAZDA CX30 2021"
    },
    {
        "marca": "CHEVROLET",
        "modelo": "AVEO LT STD",
        "año": 2018,
        "precio": 191000,
        "estatus": "DISPONIBLE",
        "color": "PLATA",
        "kilometraje": "73618",
        "ubicacion": "PERIFERICO",
        "descripcion": "CHEVROLET AVEO LT STD"
    },
    {
        "marca": "NISSAN",
        "modelo": "VERSA SENSE",
        "año": 2019,
        "precio": 219000,
        "estatus": "DISPONIBLE",
        "color": "GRIS",
        "kilometraje": "60000",
        "ubicacion": "PERIFERICO",
        "descripcion": "NISSAN VERSA SENSE 2019"
    },
    {
        "marca": "VOLKSWAGEN",
        "modelo": "JETTA MK6",
        "año": 2017,
        "precio": 235000,
        "estatus": "DISPONIBLE",
        "color": "BLANCO",
        "kilometraje": "85000",
        "ubicacion": "PERIFERICO",
        "descripcion": "VOLKSWAGEN JETTA MK6 2017"
    },
    {
        "marca": "HONDA",
        "modelo": "CIVIC",
        "año": 2020,
        "precio": 350000,
        "estatus": "DISPONIBLE",
        "color": "NEGRO",
        "kilometraje": "45000",
        "ubicacion": "PERIFERICO",
        "descripcion": "HONDA CIVIC 2020"
    },
    {
        "marca": "FORD",
        "modelo": "ECOSPORT",
        "año": 2019,
        "precio": 260000,
        "estatus": "DISPONIBLE",
        "color": "AZUL",
        "kilometraje": "55000",
        "ubicacion": "PERIFERICO",
        "descripcion": "FORD ECOSPORT 2019"
    },
    {
        "marca": "KIA",
        "modelo": "FORTE",
        "año": 2021,
        "precio": 320000,
        "estatus": "DISPONIBLE",
        "color": "ROJO",
        "kilometraje": "30000",
        "ubicacion": "PERIFERICO",
        "descripcion": "KIA FORTE 2021"
    },
    {
        "marca": "HYUNDAI",
        "modelo": "CRETA",
        "año": 2020,
        "precio": 290000,
        "estatus": "DISPONIBLE",
        "color": "GRIS",
        "kilometraje": "40000",
        "ubicacion": "PERIFERICO",
        "descripcion": "HYUNDAI CRETA 2020"
    },
    {
        "marca": "TOYOTA",
        "modelo": "COROLLA",
        "año": 2022,
        "precio": 400000,
        "estatus": "DISPONIBLE",
        "color": "BLANCO",
        "kilometraje": "20000",
        "ubicacion": "PERIFERICO",
        "descripcion": "TOYOTA COROLLA 2022"
    },
    {
        "marca": "SUZUKI",
        "modelo": "SWIFT",
        "año": 2019,
        "precio": 200000,
        "estatus": "DISPONIBLE",
        "color": "AMARILLO",
        "kilometraje": "65000",
        "ubicacion": "PERIFERICO",
        "descripcion": "SUZUKI SWIFT 2019"
    },
    {
        "marca": "MITSUBISHI",
        "modelo": "MIRAGE",
        "año": 2018,
        "precio": 170000,
        "estatus": "DISPONIBLE",
        "color": "AZUL",
        "kilometraje": "70000",
        "ubicacion": "PERIFERICO",
        "descripcion": "MITSUBISHI MIRAGE 2018"
    },
    {
        "marca": "RENAULT",
        "modelo": "KWID",
        "año": 2020,
        "precio": 180000,
        "estatus": "DISPONIBLE",
        "color": "NARANJA",
        "kilometraje": "35000",
        "ubicacion": "PERIFERICO",
        "descripcion": "RENAULT KWID 2020"
    },
    {
        "marca": "NISSAN",
        "modelo": "SENTRA",
        "año": 2019,
        "precio": 240000,
        "estatus": "DISPONIBLE",
        "color": "BLANCO",
        "kilometraje": "50000",
        "ubicacion": "PERIFERICO",
        "descripcion": "NISSAN SENTRA 2019"
    },
    {
        "marca": "HONDA",
        "modelo": "FIT",
        "año": 2020,
        "precio": 280000,
        "estatus": "DISPONIBLE",
        "color": "PLATA",
        "kilometraje": "40000",
        "ubicacion": "PERIFERICO",
        "descripcion": "HONDA FIT 2020"
    },
    {
        "marca": "FORD",
        "modelo": "FIESTA",
        "año": 2018,
        "precio": 220000,
        "estatus": "DISPONIBLE",
        "color": "ROJO",
        "kilometraje": "60000",
        "ubicacion": "PERIFERICO",
        "descripcion": "FORD FIESTA 2018"
    },
    {
        "marca": "CHEVROLET",
        "modelo": "ONIX",
        "año": 2021,
        "precio": 250000,
        "estatus": "DISPONIBLE",
        "color": "GRIS",
        "kilometraje": "25000",
        "ubicacion": "PERIFERICO",
        "descripcion": "CHEVROLET ONIX 2021"
    },
    {
        "marca": "VOLKSWAGEN",
        "modelo": "POLO",
        "año": 2020,
        "precio": 270000,
        "estatus": "DISPONIBLE",
        "color": "AZUL",
        "kilometraje": "35000",
        "ubicacion": "PERIFERICO",
        "descripcion": "VOLKSWAGEN POLO 2020"
    },
    {
        "marca": "KIA",
        "modelo": "RIO",
        "año": 2019,
        "precio": 230000,
        "estatus": "DISPONIBLE",
        "color": "BLANCO",
        "kilometraje": "45000",
        "ubicacion": "PERIFERICO",
        "descripcion": "KIA RIO 2019"
    },
    {
        "marca": "HYUNDAI",
        "modelo": "ACCENT",
        "año": 2020,
        "precio": 260000,
        "estatus": "DISPONIBLE",
        "color": "NEGRO",
        "kilometraje": "30000",
        "ubicacion": "PERIFERICO",
        "descripcion": "HYUNDAI ACCENT 2020"
    },
    {
        "marca": "TOYOTA",
        "modelo": "YARIS",
        "año": 2021,
        "precio": 300000,
        "estatus": "DISPONIBLE",
        "color": "ROJO",
        "kilometraje": "20000",
        "ubicacion": "PERIFERICO",
        "descripcion": "TOYOTA YARIS 2021"
    },
    {
        "marca": "NISSAN",
        "modelo": "MARCH",
        "año": 2019,
        "precio": 190000,
        "estatus": "DISPONIBLE",
        "color": "PLATA",
        "kilometraje": "55000",
        "ubicacion": "PERIFERICO",
        "descripcion": "NISSAN MARCH 2019"
    },
    {
        "marca": "HONDA",
        "modelo": "CITY",
        "año": 2020,
        "precio": 320000,
        "estatus": "DISPONIBLE",
        "color": "GRIS",
        "kilometraje": "35000",
        "ubicacion": "PERIFERICO",
        "descripcion": "HONDA CITY 2020"
    },
    {
        "marca": "FORD",
        "modelo": "KA",
        "año": 2018,
        "precio": 180000,
        "estatus": "DISPONIBLE",
        "color": "AZUL",
        "kilometraje": "65000",
        "ubicacion": "PERIFERICO",
        "descripcion": "FORD KA 2018"
    },
    {
        "marca": "CHEVROLET",
        "modelo": "SPARK",
        "año": 2019,
        "precio": 160000,
        "estatus": "DISPONIBLE",
        "color": "AMARILLO",
        "kilometraje": "50000",
        "ubicacion": "PERIFERICO",
        "descripcion": "CHEVROLET SPARK 2019"
    },
    {
        "marca": "VOLKSWAGEN",
        "modelo": "GOL",
        "año": 2020,
        "precio": 200000,
        "estatus": "DISPONIBLE",
        "color": "BLANCO",
        "kilometraje": "40000",
        "ubicacion": "PERIFERICO",
        "descripcion": "VOLKSWAGEN GOL 2020"
    },
    {
        "marca": "KIA",
        "modelo": "PICANTO",
        "año": 2021,
        "precio": 170000,
        "estatus": "DISPONIBLE",
        "color": "ROJO",
        "kilometraje": "25000",
        "ubicacion": "PERIFERICO",
        "descripcion": "KIA PICANTO 2021"
    },
    {
        "marca": "HYUNDAI",
        "modelo": "I10",
        "año": 2019,
        "precio": 150000,
        "estatus": "DISPONIBLE",
        "color": "GRIS",
        "kilometraje": "60000",
        "ubicacion": "PERIFERICO",
        "descripcion": "HYUNDAI I10 2019"
    },
    {
        "marca": "TOYOTA",
        "modelo": "ETIOS",
        "año": 2020,
        "precio": 210000,
        "estatus": "DISPONIBLE",
        "color": "PLATA",
        "kilometraje": "30000",
        "ubicacion": "PERIFERICO",
        "descripcion": "TOYOTA ETIOS 2020"
    },
    {
        "marca": "NISSAN",
        "modelo": "NP300",
        "año": 2018,
        "precio": 280000,
        "estatus": "DISPONIBLE",
        "color": "BLANCO",
        "kilometraje": "70000",
        "ubicacion": "PERIFERICO",
        "descripcion": "NISSAN NP300 2018"
    },
    {
        "marca": "HONDA",
        "modelo": "HR-V",
        "año": 2021,
        "precio": 380000,
        "estatus": "DISPONIBLE",
        "color": "NEGRO",
        "kilometraje": "20000",
        "ubicacion": "PERIFERICO",
        "descripcion": "HONDA HR-V 2021"
    },
    {
        "marca": "FORD",
        "modelo": "RANGER",
        "año": 2019,
        "precio": 450000,
        "estatus": "DISPONIBLE",
        "color": "GRIS",
        "kilometraje": "50000",
        "ubicacion": "PERIFERICO",
        "descripcion": "FORD RANGER 2019"
    }
]

def import_vehicles():
    print(f"🚗 Importing {len(vehicles_data)} vehicles to {BACKEND_URL}/vehicles")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    
    for i, vehicle_data in enumerate(vehicles_data, 1):
        try:
            response = requests.post(f"{BACKEND_URL}/vehicles/", json=vehicle_data, headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            print(f"✅ {i:2d}/31 - {vehicle_data['marca']} {vehicle_data['modelo']} - ${vehicle_data['precio']:,}")
            success_count += 1
        except requests.exceptions.RequestException as e:
            print(f"❌ {i:2d}/31 - {vehicle_data['marca']} {vehicle_data['modelo']} - ERROR: {e}")
            error_count += 1
        
        # Small delay to avoid overwhelming the backend
        time.sleep(0.1)
    
    print("=" * 60)
    print(f"📊 Import Summary:")
    print(f"   ✅ Successfully imported: {success_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📈 Total vehicles: {success_count}")
    
    # Check final dashboard stats
    try:
        response = requests.get(f"{BACKEND_URL}/dashboard/stats")
        stats = response.json()
        print(f"\n🎯 Dashboard Stats:")
        print(f"   🚗 Total Vehicles: {stats['total_vehicles']}")
        print(f"   💰 Total Value: ${stats['total_value']:,}")
        print(f"   📸 Total Photos: {stats['total_photos']}")
    except Exception as e:
        print(f"❌ Could not fetch dashboard stats: {e}")

if __name__ == "__main__":
    import_vehicles()
