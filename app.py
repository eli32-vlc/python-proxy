from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Function to handle requests and proxy them
def proxy_request(url):
    # Extract method and headers
    method = request.method
    headers = {key: value for key, value in request.headers if key != 'Host'}

    # Forward the request to the target URL
    if method == 'GET':
        resp = requests.get(url, headers=headers, params=request.args)
    elif method == 'POST':
        resp = requests.post(url, headers=headers, data=request.data)
    elif method == 'PUT':
        resp = requests.put(url, headers=headers, data=request.data)
    elif method == 'DELETE':
        resp = requests.delete(url, headers=headers, data=request.data)
    else:
        return Response("Method not allowed", status=405)

    # Return the response to the client
    return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))

@app.route('/<path:url>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(url):
    # Construct the full URL
    full_url = f"http://{url}"

    # Proxy the request
    return proxy_request(full_url)

if __name__ == '__main__':
    app.run(debug=True)
