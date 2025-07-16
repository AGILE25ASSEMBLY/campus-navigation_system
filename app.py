import os
import logging
from flask import Flask, render_template, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from navigation import CampusNavigator

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_dev")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize navigation system
navigator = CampusNavigator()

@app.route('/')
def index():
    """Main page with navigation form"""
    locations = navigator.get_all_locations()
    return render_template('index.html', locations=locations)

@app.route('/navigate', methods=['POST'])
def navigate():
    """Handle navigation request"""
    start = request.form.get('start', '').strip().lower()
    destination = request.form.get('destination', '').strip().lower()
    
    if not start or not destination:
        return render_template('directions.html', 
                             error="Please provide both starting point and destination")
    
    # Get directions
    directions = navigator.get_directions(start, destination)
    
    if directions['success']:
        return render_template('directions.html', 
                             directions=directions['directions'],
                             start=start.title(),
                             destination=destination.title())
    else:
        return render_template('directions.html', 
                             error=directions['error'])

@app.route('/api/locations')
def api_locations():
    """API endpoint to get all locations"""
    return jsonify(navigator.get_all_locations())

@app.route('/api/search')
def api_search():
    """API endpoint to search locations"""
    query = request.args.get('q', '').strip().lower()
    locations = navigator.search_locations(query)
    return jsonify(locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
