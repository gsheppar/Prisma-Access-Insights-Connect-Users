#!/usr/bin/env python3
import requests
import sys
import os
import json
import prisma_settings
                                  
try:
    from prisma_settings import INSIGHTS_API

except ImportError:
    INSIGHTS_API = None
                     
def go():
        
    if not INSIGHTS_API:
        print("Please configure an Insights API Key")
        return
    current_connected_users()

def current_connected_users():
    
    tenant_url = "https://pa-staging02.api.prismaaccess.com/api/sase/v1.0/jwt/tenant/1229033719"
    headers = {'Content-type': 'application/json', 'Authorization': 'ApiKey ' + INSIGHTS_API}
    
    api_request = requests.post(url=tenant_url,headers=headers)
    api_response = api_request.json()
    token = api_response["token"]

    
    data = {"count":10000}
    
    tenant_url = "https://pa-staging02.api.prismaaccess.com/api/sase/v1.0/resource/tenant/1229033719/custom/query/gp_mobileusers/current_connected_user_list"
    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}
    
    api_request = requests.post(url=tenant_url,headers=headers, json=data)
    if api_request:
        api_response = api_request.json()
        users = api_response["data"]
        if users:
            for item in users:
                print(item)
        else:
            print("No current users found")
    else:
        print("API query failed to get current users lists")
    
    return()

if __name__ == "__main__":
    go()