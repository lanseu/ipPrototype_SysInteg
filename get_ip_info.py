import requests


def get_ip_info():
    # API URL to get IP and related information
    api_url = 'https://ipapi.co/json/'

    try:
        # Sending request to the API
        response = requests.get(api_url)
        response.raise_for_status()
        ip_info = response.json()

        # Displaying the IP information
        print("Public IPv4 Address: ", ip_info.get('ip'))
        print("City: ", ip_info.get('city'))
        print("Region: ", ip_info.get('region'))
        print("Country: ", ip_info.get('country_name'))
        print("ISP: ", ip_info.get('org'))
        print("ASN: ", ip_info.get('asn'))
        print("Latitude, Longitude: ", f"{ip_info.get('latitude')}, {ip_info.get('longitude')}")

        # Displaying Additional Information
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
