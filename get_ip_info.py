import requests

def get_ip_info():
    # API URL to get geolocation and ISP information
    ipapi_url = 'https://ipapi.co/{ip}/json/'
    ipify_ipv4_url = 'https://api.ipify.org?format=json'
    ipify_ipv6_url = 'https://api64.ipify.org?format=json'

    try:
        # Get the public IPv4 address
        ipv4_response = requests.get(ipify_ipv4_url)
        ipv4 = ipv4_response.json().get('ip')

        # Get the public IPv6 address
        ipv6_response = requests.get(ipify_ipv6_url)
        ipv6 = ipv6_response.json().get('ip')

        # Fetch more details using the IPv4 address
        ipapi_response = requests.get(ipapi_url.format(ip=ipv4))
        ip_info = ipapi_response.json()

        # Display IPv4 and IPv6 information
        print("Public IPv4 Address: ", ipv4)
        print("Public IPv6 Address: ", ipv6)
        print("City: ", ip_info.get('city'))
        print("Region: ", ip_info.get('region'))
        print("Country: ", ip_info.get('country_name'))
        print("ISP: ", ip_info.get('org'))
        print("ASN: ", ip_info.get('asn'))
        print("Latitude, Longitude: ", f"{ip_info.get('latitude')}, {ip_info.get('longitude')}")

        # Display Additional Information
        print("\n--- Additional Location Information ---")
        print("Region Code: ", ip_info.get('region_code'))
        print("Continent Code: ", ip_info.get('continent_code'))
        print("Postal Code: ", ip_info.get('postal'))
        print("Timezone: ", ip_info.get('timezone'))
        print("UTC Offset: ", ip_info.get('utc_offset'))
        print("Languages: ", ip_info.get('languages'))
        print("Country Calling Code: ", ip_info.get('country_calling_code'))
        print("Currency: ", ip_info.get('currency'))

    # Error Handling
    except requests.RequestException as e:
        print(f"Error fetching IP information: {e}")

if __name__ == "__main__":
    get_ip_info()
