import json
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from fyers_apiv3.FyersWebsocket.data_ws import FyersDataSocket
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from fyers_apiv3.FyersWebsocket import order_ws
from django.conf import settings
from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws
import hashlib
import requests
import hashlib
import requests
from channels.generic.websocket import WebsocketConsumer
from fyers_apiv3.FyersWebsocket import order_ws
from django.conf import settings

from fyersapi.views import get_data_instance
import time

class FyersPositionDataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # Generate app_id_hash
        self.app_id = settings.FYERS_APP_ID
        secret_key = settings.FYERS_SECRET_ID
        app_id_hash = self.generate_app_id_hash(self.app_id, secret_key)
        pin = "2255"
        session = self.scope["session"]
        refresh_token = session.get("refresh_token")

        url = "https://api-t1.fyers.in/api/v3/validate-refresh-token"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "grant_type": "refresh_token",
            "appIdHash": app_id_hash,
            "refresh_token": refresh_token,
            "pin": pin
        }

        response = requests.post(url, headers=headers, json=data)
        json_response = response.json()
        if response.status_code == 200:
            json_response = response.json()
            access_token = json_response.get("access_token")
            access_token = self.app_id + ":" + access_token

            self.fyers = order_ws.FyersOrderSocket(
                access_token=access_token,  # Your access token for authenticating with the Fyers API.
                write_to_file=False,        # A boolean flag indicating whether to write data to a log file or not.
                log_path="",                # The path to the log file if write_to_file is set to True (empty string means current directory).
                on_connect=self.onopen,          # Callback function to be executed upon successful WebSocket connection.
                on_close=self.onclose,           # Callback function to be executed when the WebSocket connection is closed.
                on_error=self.onerror,           # Callback function to handle any WebSocket errors that may occur.
                on_positions=self.onPosition,    # Callback function to handle position-related events from the WebSocket.
            )
            self.fyers.connect()
        else:
            #print("Error:", response.text)
            self.send(text_data=f"Error: {response.text}")

    def disconnect(self, close_code):
        self.close()

    def onopen(self):
        data_type = "OnPositions"
        self.fyers.subscribe(data_type=data_type)
        self.fyers.keep_running()

    def onPosition(self, message):
        #print("Position Response:", message)
        self.send(text_data=f"Position Response: {message}")

    def onerror(self, message):
        #print("Error:", message)
        self.send(text_data=f"Error: {message}")

    def onclose(self, message):
        #print("Connection closed:", message)
        self.send(text_data=f"Connection closed: {message}")

    @staticmethod
    def generate_app_id_hash(client_id, secret_key):
        concatenated_string = f"{client_id}:{secret_key}"
        hash_object = hashlib.sha256(concatenated_string.encode())
        return hash_object.hexdigest()

# from channels.generic.websocket import WebsocketConsumer
# import hashlib
# import requests
# import json

class FyersIndexDataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.last_keyword = self.scope['url_route']['kwargs']['last_keyword']  # Extract the last keyword from URL
        #print("last_keywordlast_keyword", self.last_keyword)
        self.symbols = ["NSE:" + self.last_keyword + "-INDEX"]
        # Generate app_id_hash
        self.app_id = settings.FYERS_APP_ID
        secret_key = settings.FYERS_SECRET_ID
        app_id_hash = self.generate_app_id_hash(self.app_id, secret_key)
        pin = "2255"
        session = self.scope["session"]
        refresh_token = session.get("refresh_token")
        

        url = "https://api-t1.fyers.in/api/v3/validate-refresh-token"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "grant_type": "refresh_token",
            "appIdHash": app_id_hash,
            "refresh_token": refresh_token,
            "pin": pin
        }

        response = requests.post(url, headers=headers, json=data)
        json_response = response.json()
        if response.status_code == 200:
            json_response = response.json()
            self.access_token = json_response.get("access_token")
            self.getoptionsymbols = self.getOptionStrikes()
            # #print("=================================================", self.getoptionsymbols)
            # Connect to FyersOrderSocket with the new access token
            self.fyers = data_ws.FyersDataSocket(
                access_token=self.access_token,       # Access token in the format "appid:accesstoken"
                log_path="",                     # Path to save logs. Leave empty to auto-create logs in the current directory.
                litemode=True,                  # Lite mode disabled. Set to True if you want a lite response.
                write_to_file=False,              # Save response in a log file instead of #printing it.
                reconnect=True,                  # Enable auto-reconnection to WebSocket on disconnection.
                on_connect=self.on_open,               # Callback function to subscribe to data upon connection.
                on_close=self.on_close,                # Callback function to handle WebSocket connection close events.
                on_error=self.on_error,                # Callback function to handle WebSocket errors.
                on_message=self.on_message             # Callback function to handle incoming messages from the WebSocket.
            )

            self.fyers.connect()
        else:
            #print("Error:", response.text)
            self.send(text_data=f"Error: {response.text}")

    def disconnect(self, close_code):
        # Unsubscribe from symbols when disconnecting WebSocket
        #print("Disconnecting WebSocket")
        #print("***********************", self.allsymbols)
        data_type = "SymbolUpdate"
        self.fyers.unsubscribe(symbols=self.allsymbols, data_type=data_type)
        # Close the WebSocket connection
        self.close()

    def on_open(self):
        """
        Callback function to subscribe to data type and symbols upon WebSocket connection.

        """
        # Specify the data type and symbols you want to subscribe to
        data_type = "SymbolUpdate"
        self.allsymbols = self.symbols+self.getoptionsymbols

        #print("self.allsymbolsself.allsymbols", self.allsymbols)

        # Subscribe to the specified symbols and data type
        self.fyers.subscribe(symbols=self.allsymbols, data_type=data_type)
        # Keep the socket running to receive real-time data
        self.fyers.keep_running()

    def on_message(self, message):
        #print("Message:", message)
        self.send(text_data=f"{message}")

    def on_error(self, message):
        #print("Error:", message)
        self.send(text_data=f"Error: {message}")

    def on_close(self, message):
        #print("Connection closed:", message)
        data_type = "SymbolUpdate"
        self.fyers.unsubscribe(symbols=self.allsymbols, data_type=data_type)
        self.send(text_data=f"Connection closed: {message}")

    @staticmethod
    def generate_app_id_hash(client_id, secret_key):
        concatenated_string = f"{client_id}:{secret_key}"
        hash_object = hashlib.sha256(concatenated_string.encode())
        return hash_object.hexdigest()
    
    def getOptionStrikes(self):
        response=None
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        self.fyers = fyersModel.FyersModel(client_id=self.app_id, is_async=False, token=self.access_token, log_path="")
        #print("self.symbolsself.symbols", type(self.symbols))
        self.ce_symbols=[]
        self.pe_symbols=[]
      
        data = {
            "symbol": self.symbols[0],
            "strikecount": 1,
        }
        try:
            self.expiry_response = self.fyers.optionchain(data=data)
            first_expiry_ts = self.expiry_response['data']['expiryData'][0]['expiry']
            # first_expiry_date = expiry_response['data']['expiryData'][0]['date']
            # return render(request, template, context)
            if first_expiry_ts:
                options_data = {
                    "symbol":self.symbols[0],
                    "strikecount": 2,
                    "timestamp": first_expiry_ts
                }

                response = self.fyers.optionchain(data=options_data)
                # Filter optionsChain data for option type 'PE'
                pe_options = [option for option in response['data']['optionsChain'] if option['option_type'] == 'PE']
                # Sort the filtered data by strike_price in ascending order
                pe_options_sorted = sorted(pe_options, key=lambda x: x['strike_price'], reverse=True)
                #print("**************************************")
                # #print(pe_options_sorted)
                self.pe_symbols = [option['symbol'] for option in pe_options_sorted]
                #print("**************************************")



                # Filter optionsChain data for option type 'CE'
                ce_options = [option for option in response['data']['optionsChain'] if option['option_type'] == 'CE']
                # Sort the filtered data by strike_price in ascending order
                ce_options_sorted = sorted(ce_options, key=lambda x: x['strike_price'])
                #print("**************************************")
                # #print(ce_options_sorted)
                self.ce_symbols = [option['symbol'] for option in ce_options_sorted]
                symbol_list =  self.ce_symbols + self.pe_symbols
                #print("**************************************")
                return symbol_list
            

        except (KeyError, AttributeError, IndexError) as e:
            # Handle the error gracefully
            error_message = f'Error occurred: {str(e)}'
            #print("Error occurred while fetching expiry data:", error_message)
          
        return response

    def receive(self, text_data):
        # Parse the incoming message
        message = json.loads(text_data)
        action = message.get('action')

        # Check if the client requested a disconnect action
        if action == 'disconnect':
            # Unsubscribe from symbols when disconnecting WebSocket
            data_type = "SymbolUpdate"
            self.fyers.unsubscribe(symbols=self.allsymbols, data_type=data_type)
            # Close the WebSocket connection
            self.close()

    




