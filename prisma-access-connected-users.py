#!/usr/bin/env python3
import requests
import sys
import os
import json
import csv 
import prisma_settings
from datetime import datetime
                                  
try:
    from prisma_settings import INSIGHTS_API
    from prisma_settings import TENANT_ID

except ImportError:
    INSIGHTS_API = None
    TENANT_ID = None
                     
def go():
        
    if not INSIGHTS_API:
        print("Please configure an Insights API Key")
        return
    if not TENANT_ID:
        print("Please configure an Tenant ID")
        return
    current_connected_users()

def current_connected_users():
    
    tenant_url = "https://pa-staging02.api.prismaaccess.com/api/sase/v1.0/jwt/tenant/" + TENANT_ID
    headers = {'Content-type': 'application/json', 'Authorization': 'ApiKey ' + INSIGHTS_API}
    
    api_request = requests.post(url=tenant_url,headers=headers)
    api_response = api_request.json()
    token = api_response["token"]

    
    data = {"count":10000}
    
    tenant_url = "https://pa-staging02.api.prismaaccess.com/api/sase/v1.0/resource/tenant/" + TENANT_ID + "/custom/query/gp_mobileusers/current_connected_user_list"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    
    api_request = requests.post(url=tenant_url,headers=headers, json=data)
    if api_request:
        api_response = api_request.json()
        users = api_response["data"]
        if users:
            
            print("Found " + str(len(users)) + " connected users")
            
            csv_columns = []
            for key in users[0]:
                csv_columns.append(key)
                
            time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    
            csv_file = "connected_users_" + time + ".csv"
            try:
                with open(csv_file, 'w', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    writer.writeheader()
                    for data in users:
                        try:
                            writer.writerow(data)
                        except:
                            print("Failed to write data for row")
                    print("Saved " + csv_file + " file")
            except IOError:
                print("CSV Write Failed")
        else:
            print("No connected users found")
    else:
        print("API query failed to get current connected users lists")
    
    return()

if __name__ == "__main__":
    go()