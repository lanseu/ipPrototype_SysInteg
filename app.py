import speedtest
from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/api/get_ip_info', methods=['GET'])
# def get_ip_info():
#     # API URLs
#     ipapi_url = 'https://ipapi.co/{ip}/json/'
#     ipify_ipv4_url = 'https://api.ipify.org?format=json'
#     ipify_ipv6_url = 'https://api64.ipify.org?format=json'
#
#     try:
#         # Get public IPv4 address
#         ipv4_response = requests.get(ipify_ipv4_url)
#         ipv4_response.raise_for_status()  # Ensure request is successful
#         ipv4 = ipv4_response.json().get('ip')
#
#         # Get public IPv6 address
#         ipv6_response = requests.get(ipify_ipv6_url)
#         ipv6_response.raise_for_status()  # Ensure request is successful
#         ipv6 = ipv6_response.json().get('ip')
#
#         # Fetch more details using the IPv4 address
#         ipapi_response = requests.get(ipapi_url.format(ip=ipv4))
#         ipapi_response.raise_for_status()  # Ensure request is successful
#         ip_info = ipapi_response.json()
#
#         # Add IPv4 and IPv6 to the IP information response
#         ip_info['ipv4'] = ipv4
#         ip_info['ipv6'] = ipv6
#
#         return jsonify(ip_info), 200
#
#     except requests.RequestException as e:
#         return jsonify({'error': f"Error fetching IP information: {str(e)}"}), 500

@app.route('/api/get_ip_info', methods=['GET'])
def get_ip_info():
    # API URLs
    ipapi_url = 'https://ipapi.co/{ip}/json/'
    ipify_ipv4_url = 'https://api.ipify.org?format=json'
    ipify_ipv6_url = 'https://api64.ipify.org?format=json'

    try:
        # Get public IPv4 address
        ipv4_response = requests.get(ipify_ipv4_url)
        ipv4_response.raise_for_status()  # Ensure request is successful
        ipv4 = ipv4_response.json().get('ip')
        print("IPv4 Address: ", ipv4)  # Temporary print statement for testing

        # Get public IPv6 address
        ipv6_response = requests.get(ipify_ipv6_url)
        ipv6_response.raise_for_status()  # Ensure request is successful
        ipv6 = ipv6_response.json().get('ip')
        print("IPv6 Address: ", ipv6)  # Temporary print statement for testing

        # Fetch more details using the IPv4 address
        ipapi_response = requests.get(ipapi_url.format(ip=ipv4))
        ipapi_response.raise_for_status()  # Ensure request is successful
        ip_info = ipapi_response.json()

        # Perform speed test
        st = speedtest.Speedtest()
        st.get_best_server()  # Choose the best server based on ping

        # Get download and upload speeds (in Mbps)
        download_speed = st.download() / 1_000_000  # Convert from bps to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert from bps to Mbps
        ping = st.results.ping

        # Temporary print statements for speed test results
        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
        print(f"Ping: {ping:.2f} ms")

        # Add speed test results and IPs to the IP information
        ip_info['ipv4'] = ipv4
        ip_info['ipv6'] = ipv6
        ip_info['speed_test'] = {
            'download_speed_mbps': f"{download_speed:.2f}",
            'upload_speed_mbps': f"{upload_speed:.2f}",
            'ping_ms': f"{ping:.2f}"
        }

        return jsonify(ip_info), 200

    except requests.RequestException as e:
        return jsonify({'error': f"Error fetching IP information: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'error': f"Error performing speed test: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
