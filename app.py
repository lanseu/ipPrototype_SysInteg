import asyncio
from flask import Flask, render_template, jsonify
import aiohttp
import speedtest
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Create a ThreadPoolExecutor for the speedtest to run asynchronously
executor = ThreadPoolExecutor(max_workers=2)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_ip_info():
    ipapi_url = 'https://ipapi.co/{ip}/json/'
    ipify_ipv4_url = 'https://api.ipify.org?format=json'
    ipify_ipv6_url = 'https://api64.ipify.org?format=json'

    async with aiohttp.ClientSession() as session:
        # Fetch both IPv4 and IPv6 addresses asynchronously
        ipv4_task = fetch(session, ipify_ipv4_url)
        ipv6_task = fetch(session, ipify_ipv6_url)

        ipv4_response, ipv6_response = await asyncio.gather(ipv4_task, ipv6_task)
        ipv4 = ipv4_response.get('ip')
        ipv6 = ipv6_response.get('ip')

        # Fetch IP details using IPv4
        ipapi_response = await fetch(session, ipapi_url.format(ip=ipv4))
        ip_info = ipapi_response

        return ipv4, ipv6, ip_info

def run_speedtest():
    st = speedtest.Speedtest()
    st.get_best_server()  # Choose the best server based on ping
    download_speed = st.download() / 1_000_000  # Convert from bps to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert from bps to Mbps
    ping = st.results.ping  # Get the ping (in ms)
    
    return download_speed, upload_speed, ping

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_ip_info')
async def handle_get_ip_info():
    try:
        # Get IP information asynchronously
        ipv4, ipv6, ip_info = await get_ip_info()

        # Run speedtest in a separate thread to avoid blocking the main thread
        download_speed, upload_speed, ping = await asyncio.get_event_loop().run_in_executor(executor, run_speedtest)

        # Return IP information as JSON
        return jsonify({
            'ipv4': ipv4,
            'ipv6': ipv6,
            'city': ip_info.get('city'),
            'region': ip_info.get('region'),
            'country': ip_info.get('country_name'),
            'isp': ip_info.get('org'),
            'asn': ip_info.get('asn'),
            'latitude': ip_info.get('latitude'),
            'longitude': ip_info.get('longitude'),
            'region_code': ip_info.get('region_code'),
            'continent_code': ip_info.get('continent_code'),
            'postal_code': ip_info.get('postal'),
            'timezone': ip_info.get('timezone'),
            'utc_offset': ip_info.get('utc_offset'),
            'languages': ip_info.get('languages'),
            'country_calling_code': ip_info.get('country_calling_code'),
            'currency': ip_info.get('currency'),
            'download_speed': f"{download_speed:.2f} " if isinstance(download_speed, (int, float)) else download_speed,
            'upload_speed': f"{upload_speed:.2f}" if isinstance(upload_speed, (int, float)) else upload_speed,
            'ping': f"{ping:.2f} " if isinstance(ping, (int, float)) else ping
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
