# Import the necessary modules
import time
import json
import colorama
import datetime
import locale
from colorama import Fore, Style
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.billing.v20180709 import billing_client
from tencentcloud.billing.v20180709 import models as modelku
from tencentcloud.cvm.v20170312 import cvm_client, models as modelku2
from tencentcloud.cam.v20190116 import cam_client, models
import ctypes


# Initialize colorama
colorama.init()

def beautiful_input(prompt):
    print(f"{Fore.CYAN}\n=== {prompt} ==={Style.RESET_ALL}")
    value = input(f"{Fore.YELLOW}>> {Style.RESET_ALL}")
    return value

def set_cmd_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)
    
def checkinstance(cred):
    try:
        client2 = cvm_client.CvmClient(cred, "ap-singapore")
        request2 = modelku2.DescribeInstancesRequest()
        response2 = client2.DescribeInstances(request2)
        if response2.TotalCount > 0:
            print(f"\n{Fore.RED}======================= RESULT ALL INSTANCE ======================={Style.RESET_ALL}")
            print(response2)
            print(f"{Fore.RED}===================================================================={Style.RESET_ALL}\n")
        else:
            print("Instance Tidak Ditemukan, Silahkan Buat Instance dengan Server Singapore! (Atau Ketik 2)")
    except TencentCloudSDKException as err:
        # Handle API exception
        if err.code == "AuthFailure.InvalidSecretId" or err.code == "AuthFailure.InvalidSecretKey":
            print("Invalid Secret ID or Secret Key")
        else:
            print("Failed to retrieve user information:", err)
            
def create_instance(cred):
    # Specify the region and zone for the instance
    region = "ap-singapore"
    zone = "ap-singapore-3"

    # Create an instance request object
    request = modelku2.RunInstancesRequest()
    request.ImageId = "img-4ogcw28j"  # Specify the image ID
    request.InstanceType = "S5.MEDIUM2"  # Specify the instance type
    request.Placement = modelku2.Placement()
    request.Placement.Zone = zone  # Specify the zone
    request.InstanceCount = 1  # Specify the number of instances to create
    request.InternetAccessible = modelku2.InternetAccessible()
    request.InstanceChargeType = "POSTPAID_BY_HOUR"  # Pay-as-you-go billing type
    request.InternetAccessible.InternetMaxBandwidthOut = 1  # Specify the maximum outbound bandwidth
    
    request.SystemDisk = modelku2.SystemDisk()
    request.SystemDisk.DiskSize = 20  # Specify the system disk size in GB
    request.SystemDisk.DiskType = "CLOUD_PREMIUM"  # Specify the system disk type
    
    data_disk = modelku2.DataDisk()
    data_disk.DeleteWithInstance = True  # Delete the disk when the instance is terminated
    data_disk.DiskSize = 20  # Specify the data disk size in GB
    data_disk.DiskType = "CLOUD_PREMIUM"  # Specify the data disk type
    request.DataDisks = [data_disk]  # Add the data disk to the request

    # Set a password
    login_settings = modelku2.LoginSettings()
    login_settings.Password = "@Aqua1liter"  # Specify the desired password
    request.LoginSettings = login_settings

    # Create an instance client
    client = cvm_client.CvmClient(cred, region)

    try:
        # Send the request to create the instance
        response = client.RunInstances(request)

        # Check the response for errors
        if response.InstanceIdSet:
            # Retrieve the instance ID
            instance_id = response.InstanceIdSet[0]
            print("Successfully created instance:", instance_id)
        else:
            print("Failed to create the instance:", response)
    except TencentCloudSDKException as e:
        print("Error:", e)

def starting(cred, email_key):
    try:
        while True:
            try:
                now = datetime.datetime.now()
                #locale.setlocale(locale.LC_ALL, 'id_ID')  # Set the locale to Indonesian
                formatted_date = now.strftime("%A, %d %B %Y - %H:%M:%S WIB")
                # Create a client instance
                client = billing_client.BillingClient(cred, "ap-singapore")
                client2 = cvm_client.CvmClient(cred, "ap-singapore")
                client3 = cvm_client.CvmClient(cred, "ap-singapore")
                # Create the request object
                request = modelku.DescribeAccountBalanceRequest()
                request2 = modelku2.DescribeInstancesRequest()
                # Call the API
                response = client.DescribeAccountBalance(request)
                response2 = client2.DescribeInstances(request2)
                if response2.TotalCount > 0:  
                    if response.Balance > 20:
                        print(f'{Fore.GREEN}[*] [{formatted_date}] => {email_key} | Balance: {response.Balance} | RealBalance: {response.RealBalance} | CreditBalance: {response.CreditBalance} | RealCreditBalance: {response.RealCreditBalance} | Instance ID: {response2.InstanceSet[0].InstanceId}{Style.RESET_ALL}')
                        request3 = modelku2.TerminateInstancesRequest()
                        request3.from_json_string(json.dumps({"InstanceIds": [response2.InstanceSet[0].InstanceId]}))
                        response3 = client3.TerminateInstances(request3)
                        print(response3)
                        print("Instance termination successful.")
                        break
                    else:
                        print(f'{Fore.YELLOW}[*] [{formatted_date}] => {email_key} | Balance: {response.Balance} | RealBalance: {response.RealBalance} | CreditBalance: {response.CreditBalance} | RealCreditBalance: {response.RealCreditBalance} | Instance ID: {response2.InstanceSet[0].InstanceId}{Style.RESET_ALL}')
                    time.sleep(5)
                else:
                    print("Instance Tidak Ditemukan, Silahkan Buat Instance dengan Server Singapore!")
                    break
            except TencentCloudSDKException as err:
                # Handle API exception
                if err.code == "AuthFailure.InvalidSecretId" or err.code == "AuthFailure.InvalidSecretKey":
                    print("Invalid Secret ID or Secret Key")
                    break
                else:
                    print("Failed to retrieve user information:", err)
                    break
    except TencentCloudSDKException as err:
        # Handle API exception
        if err.code == "AuthFailure.InvalidSecretId" or err.code == "AuthFailure.InvalidSecretKey":
            print("Invalid Secret ID or Secret Key")
        else:
            print("Failed to retrieve user information:", err)
            
# Menu layout
if __name__ == '__main__':
    set_cmd_title("Tencent Bot V 1.0 by t.me/starfz")
    ascii_banner =  """

████████╗░█████╗░███╗░░██╗░██████╗░░██████╗███████╗███╗░░██╗░██████╗░
╚══██╔══╝██╔══██╗████╗░██║██╔════╝░██╔════╝██╔════╝████╗░██║██╔════╝░
░░░██║░░░██║░░██║██╔██╗██║██║░░██╗░╚█████╗░█████╗░░██╔██╗██║██║░░██╗░
░░░██║░░░██║░░██║██║╚████║██║░░╚██╗░╚═══██╗██╔══╝░░██║╚████║██║░░╚██╗
░░░██║░░░╚█████╔╝██║░╚███║╚██████╔╝██████╔╝███████╗██║░╚███║╚██████╔╝
░░░╚═╝░░░░╚════╝░╚═╝░░╚══╝░╚═════╝░╚═════╝░╚══════╝╚═╝░░╚══╝░╚═════╝░

████████╗███████╗██████╗░███╗░░░███╗██╗███╗░░██╗░█████╗░████████╗███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗░████║██║████╗░██║██╔══██╗╚══██╔══╝██╔════╝
░░░██║░░░█████╗░░██████╔╝██╔████╔██║██║██╔██╗██║███████║░░░██║░░░█████╗░░
░░░██║░░░██╔══╝░░██╔══██╗██║╚██╔╝██║██║██║╚████║██╔══██║░░░██║░░░██╔══╝░░
░░░██║░░░███████╗██║░░██║██║░╚═╝░██║██║██║░╚███║██║░░██║░░░██║░░░███████╗
░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝

██╗░░░██╗░░███╗░░░░░░█████╗░
██║░░░██║░████║░░░░░██╔══██╗
╚██╗░██╔╝██╔██║░░░░░██║░░██║
░╚████╔╝░╚═╝██║░░░░░██║░░██║
░░╚██╔╝░░███████╗██╗╚█████╔╝
░░░╚═╝░░░╚══════╝╚═╝░╚════╝░        
"""
    print(f"{Fore.LIGHTCYAN_EX} {ascii_banner} {Style.RESET_ALL} \n=========> {Fore.YELLOW}Version: 1.0 created by t.me/starfz {Style.RESET_ALL} <========= \n")
    try:
        email_key = beautiful_input("Masukkan Email: ")
        id_key = beautiful_input("Masukkan Secret Id: ")
        sec_key = beautiful_input("Masukkan Secret Key: ")
        creds = credential.Credential("IKIDWt3z1c8TwDJF1czKbfWL5bv1sl4C6Wji", "sWv64o57uYx72lGk02pO9h3KOEwRjuuh")
        clientx = billing_client.BillingClient(creds, "ap-singapore")
        requestx = modelku.DescribeAccountBalanceRequest()
        responsex = clientx.DescribeAccountBalance(requestx)
        while True:
            print("\nMenu Information:")
            print("1. Check Available Instance")
            print("2. Create Instance")
            print("3. Auto Terminate (If Get 30$)")
            print("4. Quit")
            choice = beautiful_input("Enter your choice (1-3): ")

            if choice == "1":
                checkinstance(creds)
            elif choice == "2":
                create_instance(creds)
            elif choice == "3":
                starting(creds, email_key)
            elif choice == "4":
                print("Anda Keluar..")
                break
            else:
                print("\nInvalid choice. Please enter a valid option (1-3).\n")
    except TencentCloudSDKException as err:
        # Handle API exception
        if err.code == "AuthFailure.InvalidSecretId" or err.code == "AuthFailure.InvalidSecretKey":
            print("Invalid Secret ID or Secret Key")
        else:
            print("Failed to retrieve user information, Invalid Secret ID or Secret Key.", err)