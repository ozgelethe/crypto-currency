import time
import threading
import requests
import pytest
from flask import Flask
from flask.testing import FlaskClient

# Import the app and socketio from your app.py
from app import app, socketio, get_currency_values

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client

@pytest.fixture
def socketio_client():
    client = socketio.test_client(app)
    return client

def wait_for_event(socketio_client, event_name, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        received_events = socketio_client.get_received()
        for event in received_events:
            if event['name'] == event_name:
                return event['args'][0]
        time.sleep(0.1)
    raise TimeoutError(f"Timed out waiting for '{event_name}' event")

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'WebSocket Example' in response.data

def test_currency_update(socketio_client):
    # Emit a test event to the app and check if the BTC value is updated
    socketio_client.emit('request', {'data': 'test'})

    # Wait for the 'update_currencies' event
    data = wait_for_event(socketio_client, 'update_currencies')
    print("Received Data:", data)  # Add this line to print the received data
    assert data is not None

    initial_btc_value = data['BTC']

    time.sleep(7)  # Adjust the timing as needed

    # Wait for the 'update_currencies' event after the second update
    data = wait_for_event(socketio_client, 'update_currencies')
    print("Received Data:", data)  # Add this line to print the received data
    assert data is not None

    updated_btc_value = data['BTC']

    assert initial_btc_value is not None
    assert updated_btc_value is not None
    assert initial_btc_value != 'Loading...'
    assert updated_btc_value != 'Loading...'
    assert initial_btc_value != updated_btc_value
