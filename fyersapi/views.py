from decimal import Decimal
import json
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from account.models import CommonConfig
from fyers_apiv3 import fyersModel
import webbrowser
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from .models import OpenOrderTempData, TradingData
import datetime
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import TradingData
from django.utils import timezone
from django.db.models import Q
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import EOD_DataForm, SOD_DataForm, TradingConfigurationsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class Brokerconfig(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request, *args, **kwargs):
        template = "trading_tool/html/index.html"
        context = {}
        return render(request, template, context)
    
def brokerconnect(request):
    # Get client_id and secret_key from settings.py
    client_id = settings.FYERS_APP_ID
    secret_key = settings.FYERS_SECRET_ID
    redirect_uri = settings.FYERS_REDIRECT_URL+"/dashboard"
    # Replace these values with your actual API credentials
    # redirect_uri = "https://tradewithappz.co.in/dashboard"
    # redirect_uri = "https://aabe-2405-201-f007-417b-7d9c-6736-527b-61a6.ngrok-free.app/dashboard"
    response_type = "code"  
    state = "sample_state"
    # Create a session model with the provided credentials
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type
    )
    # Generate the auth code using the session model
    response = session.generate_authcode()
    # #print the auth code received in the response
    # You can redirect to another page or render a template after #printing
    return redirect(response)  # Assuming 'home' is the name of a URL pattern you want to redirect to



def get_accese_token(request):
    # return redirect('some_redirect_url')
    # Get client_id and secret_key from settings.py
    client_id = settings.FYERS_APP_ID
    secret_key = settings.FYERS_SECRET_ID
    redirect_uri = settings.FYERS_REDIRECT_URL+"/dashboard"
    # redirect_uri = "https://tradewithappz.co.in/dashboard"
    # redirect_uri = "https://aabe-2405-201-f007-417b-7d9c-6736-527b-61a6.ngrok-free.app/dashboard"
    response_type = "code" 
    grant_type = "authorization_code"  
    # The authorization code received from Fyers after the user grants access
    # auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MTEyNzg2NDgsImV4cCI6MTcxMTMwODY0OCwibmJmIjoxNzExMjc4MDQ4LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJZUzA1MTQxIiwib21zIjoiSzEiLCJoc21fa2V5IjoiNGQ0OWQzMzA2MmM4YzMyOTA4OGEyMzZkMWVkZDI0MDhhODYyY2QyZDdlMmI2M2Y4NjI3N2JkZGUiLCJub25jZSI6IiIsImFwcF9pZCI6Ikg5TzQwNlhCWFciLCJ1dWlkIjoiNTdhYzQ2MmM0YzkxNGI0MzlmMGY3OTc3MGRmMDM0YTEiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.RhnYqWn9hqR5X_yg5wHKcOGCkGFnAb4Ms2xbToDMPAw"
    auth_code = request.session.get(' ')
    # Create a session object to handle the Fyers API authentication and token generation
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key, 
        redirect_uri=redirect_uri, 
        response_type=response_type, 
        grant_type=grant_type
    )
    #print("sessionsession", session)
    # Set the authorization code in the session object
    session.set_token(auth_code)
    # Generate the access token using the authorization code
    response = session.generate_token()
    #print("responseresponse", response)
    # #print the response, which should contain the access token and other details
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    if access_token:
        return access_token

    else:
        return None
        

def get_accese_token_store_session(request):
    # return redirect('some_redirect_url')
    # Get client_id and secret_key from settings.py
    client_id = settings.FYERS_APP_ID
    secret_key = settings.FYERS_SECRET_ID
    redirect_uri = settings.FYERS_REDIRECT_URL+"/dashboard"
    # redirect_uri = "https://tradewithappz.co.in/dashboard"
    # redirect_uri = "https://aabe-2405-201-f007-417b-7d9c-6736-527b-61a6.ngrok-free.app/dashboard"
    response_type = "code" 
    grant_type = "authorization_code"  
    # The authorization code received from Fyers after the user grants access
    # auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MTEyNzg2NDgsImV4cCI6MTcxMTMwODY0OCwibmJmIjoxNzExMjc4MDQ4LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJZUzA1MTQxIiwib21zIjoiSzEiLCJoc21fa2V5IjoiNGQ0OWQzMzA2MmM4YzMyOTA4OGEyMzZkMWVkZDI0MDhhODYyY2QyZDdlMmI2M2Y4NjI3N2JkZGUiLCJub25jZSI6IiIsImFwcF9pZCI6Ikg5TzQwNlhCWFciLCJ1dWlkIjoiNTdhYzQ2MmM0YzkxNGI0MzlmMGY3OTc3MGRmMDM0YTEiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.RhnYqWn9hqR5X_yg5wHKcOGCkGFnAb4Ms2xbToDMPAw"
    auth_code = request.session.get('auth_code')
    # Create a session object to handle the Fyers API authentication and token generation
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key, 
        redirect_uri=redirect_uri, 
        response_type=response_type, 
        grant_type=grant_type
    )
    # Set the authorization code in the session object
    session.set_token(auth_code)
    # Generate the access token using the authorization code
    response = session.generate_token()
    # #print the response, which should contain the access token and other details
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    if access_token and refresh_token:
        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token
        obj, created = CommonConfig.objects.update_or_create(
                param='access_token',
                defaults={"value": access_token}
            )
    else:
        #print("access_token or refresh_token missing")
        pass
    # You can redirect to another page or render a template after #printing
    return redirect('dashboard')  # Assuming 'home' is the name of a URL pattern you want to redirect to



def close_all_positions(request):
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')
    
    if not access_token:
        return redirect('dashboard')
    
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
    order_data = fyers.orderbook()

    # Collect order IDs with status 6 using list comprehension
    orders_with_status_6 = [{"id": order.get("id")} for order in order_data["orderBook"] if order["status"] == 6]

    if orders_with_status_6:
        order_cancel_response = fyers.cancel_basket_orders(data=orders_with_status_6)
        messages.success(request, order_cancel_response)
    else:
        messages.success(request, "No pending orders to cancel.")

    # Exit positions
    data = {
        "segment": [11],
        "side": [1],
        "productType": ["INTRADAY"]
    }
    response = fyers.exit_positions(data=data)

    if 'message' in response:
        message = response['message']
        messages.success(request, message)
        OpenOrderTempData.objects.all().delete()
        return JsonResponse({'message': message, 'code': response['code']})
    else:
        message = "Error: Response format is unexpected"
        messages.error(request, message)
        return JsonResponse({'message': message, 'code': response['code']})


def get_data_instance(request):
    context={}
    template="trading_tool/html/profile_view.html"
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')
    if access_token:
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
        # Return the response received from the Fyers API
        return fyers
    else:
        #print("noithing here")
        # return redirect('dashboard')  
        # Handle the case where access_token is not found in the session
        pass
    return None


class ProfileView(LoginRequiredMixin, View):
  login_url = '/login'
  def get(self, request):
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')

    if access_token:
      fyers = fyersModel.FyersModel(
        client_id=client_id, 
        is_async=False, 
        token=access_token,
        log_path=""
      )
      response = fyers.get_profile()
      context = response
      return render(request, 'trading_tool/html/profile_view.html', context)
    
    else:
      #print("no access token")
      return render(request, 'trading_tool/html/profile_view.html')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import SOD_DataForm
from .models import SOD_EOD_Data  # Import your model

class SOD_ReportingView(LoginRequiredMixin, FormView):
    login_url = '/login'
    template_name = 'trading_tool/html/sod_form.html'
    form_class = SOD_DataForm
    success_url = reverse_lazy('dashboard')

    def get_initial_data(self):
        initial = super().get_initial()
        # Retrieve slug data from URL parameters
        # Load initial value for week_no
        data_instance = get_data_instance(self.request)
        fund_data = data_instance.funds()
        #print("fund_datafund_data", fund_data)
        current_date = datetime.date.today()

        # calculate the slippage 
        initial_week_no = current_date.isocalendar()[1]
        initial['week_no'] = initial_week_no
        total_balance = 0

        for item in fund_data.get('fund_limit', []):
            if item.get('title') == 'Total Balance':
                total_balance = item.get('equityAmount')
                break
        #print("Total Balance:", total_balance)
        initial['trading_date'] = current_date
        initial['opening_balance'] = total_balance

        previous_date = current_date - datetime.timedelta(days=1)
        #print("previous_date", previous_date)
        previous_date_data =SOD_EOD_Data.objects.filter(trading_date=previous_date).exists()
        if previous_date_data:
            previous_date_data = SOD_EOD_Data.objects.filter(trading_date=previous_date).first()
            prev_day_slippage = float(total_balance) -   float(previous_date_data.closing_balance)
            # calculate overall expense 
            turnover = previous_date_data.opening_balance + previous_date_data.day_p_and_l + previous_date_data.withdrwal_amount
            turnover = turnover-previous_date_data.withdrwal_amount
            #print("turnoverturnoverturnover", turnover)
            actual_expense = float(turnover) - total_balance
            actual_benefit = float(previous_date_data.day_p_and_l) - float(actual_expense)
            previous_date_data.actual_expense = actual_expense
            previous_date_data.actual_benefit = actual_benefit
            previous_date_data.save()
            initial['prev_day_slippage'] = prev_day_slippage
   
        return initial

    def get_initial(self):
        return self.get_initial_data()

    def form_valid(self, form):
        # Check if a record with the same trading_date already exists
        trading_date = form.cleaned_data.get('trading_date')
        if SOD_EOD_Data.objects.filter(trading_date=trading_date).exists():
            return JsonResponse({'error': 'A record for this trading date already exists.'}, status=400)
        form.save()
        return JsonResponse({'success': 'Form submitted successfully.'})

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SOD_EOD_Data
import datetime
@csrf_exempt
def fetch_date_data(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        
        date_obj = datetime.datetime.strptime(date_str, '%d-%m-%Y')
        #print("date_strdate_strdate_str", date_obj)
        
        data_instance = SOD_EOD_Data.objects.filter(trading_date=date_obj).first()
        data_instance = SOD_EOD_Data.objects.filter(trading_date=date_obj).first()
        #print("data_instancedata_instance", data_instance)
        
        if data_instance:
            data = {
                'trading_date': data_instance.trading_date,
                'opening_balance': data_instance.opening_balance,
                'closing_balance': data_instance.closing_balance,
                'day_exp_brokerage': data_instance.day_exp_brokerage,
                'day_order_count': data_instance.day_order_count,
                'day_p_and_l': data_instance.day_p_and_l,
                'actual_expense': data_instance.actual_expense,
                'actual_benefit': data_instance.actual_benefit,
                'notes': data_instance.notes,
       
                # 'some_other_field': data_instance.some_other_field,
                # # Add other fields as necessary
            }
            #print("datadatadata", data)
            return JsonResponse({'data': data}, status=200)
        else:
            return JsonResponse({'error': 'No data found for the given date'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.http import JsonResponse
from django.utils import timezone
from collections import defaultdict
from datetime import timedelta
from .models import SOD_EOD_Data

def daily_candle_overview(request):
    fifteen_days_ago = timezone.now() - timedelta(days=15)
    # Query the database for SOD_EOD_Data objects within the past 15 days
    data_objects = SOD_EOD_Data.objects.filter(trading_date__gte=fifteen_days_ago)
    
    if data_objects.exists():
        # Create a defaultdict to store balance data for each date
        balance_data = defaultdict(list)
        
        # Iterate through the data_objects and collect opening and closing balance data
        for obj in data_objects:
            trading_date = obj.trading_date.strftime('%Y-%m-%d')
            # Append opening balance twice and closing balance twice
            balance_data[trading_date].extend([float(obj.opening_balance), float(obj.opening_balance), float(obj.closing_balance), float(obj.closing_balance)])
        
        # Format the data into the desired format
        formatted_data = []
        for date, balances in balance_data.items():
            print("balancesbalances", balances)
            formatted_data.append({'x': date, 'y': balances})

        print("formatted_dataformatted_data", formatted_data)
        
        return JsonResponse(formatted_data, safe=False)

    else:
        return JsonResponse({'error': 'No data found within the past 15 days'}, status=404)
    


# ---------------------------------------------------------------------------------------------------------------------------

from django.http import JsonResponse
def update_data_instance(request):
    context = {}
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')
    total_order_status=0

    if access_token:
        data_instance = get_data_instance(request)
        # fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
        positions_data = data_instance.positions()
        order_data = data_instance.orderbook()
        fund_data = data_instance.funds()
        if "orderBook" in order_data:
            total_order_status = sum(1 for order in order_data["orderBook"] if order["status"] == 2)
        # Process the response and prepare the data
        data = { 'positions': positions_data,
                'total_order_status': total_order_status ,
                'fund_data': fund_data,
                'order_data': order_data
                }  # Modify this according to your response structure
        
        # print("datadatadata", data)
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Access token not found'}, status=400)
    
# ---------------------------------------------------------------------------------------------------------------------------

from django.views.generic import TemplateView

class CandleOverviewView(TemplateView):
    template_name = 'trading_tool/html/candle_overview.html'


class EOD_ReportingView(LoginRequiredMixin, FormView):
    login_url = '/login'
    template_name = 'trading_tool/html/eod_form.html'
    form_class = EOD_DataForm
    success_url = reverse_lazy('dashboard')

    def get_initial_data(self):
        initial = super().get_initial()
        # Retrieve slug data from URL parameters
        # Load initial value for week_no
        data_instance = get_data_instance(self.request)
        fund_data = data_instance.funds()
        order_data = data_instance.orderbook()
        total_order_status = sum(1 for order in order_data["orderBook"] if order["status"] == 2)
        total_balance = 0
        realised_profit = 0
        total_order_status = 0  
        confData = TradingConfigurations.objects.order_by('-last_updated').first()
        cost = confData.capital_limit_per_order
        tax = calculate_tax(cost)
        default_brokerage = settings.DEFAULT_BROKERAGE + tax
        # default_brokerage = settings.DEFAULT_BROKERAGE
        exp_brokerage = default_brokerage * total_order_status

        for item in fund_data.get('fund_limit', []):
            if item.get('title') == 'Total Balance':
                total_balance = item.get('equityAmount')
            if item.get('title') == 'Realized Profit and Loss':
                realised_profit = item.get('equityAmount')
                break

        initial['day_exp_brokerage'] = exp_brokerage
        initial['day_order_count'] = total_order_status
        initial['day_p_and_l'] = realised_profit
        initial['closing_balance'] = total_balance
        return initial

    def get_initial(self):
        return self.get_initial_data()

    def form_valid(self, form):
        # Check if a record with the same trading_date already exists
        trading_date = datetime.date.today()
        existing_instance = SOD_EOD_Data.objects.filter(trading_date=trading_date).first()
        #print("existing_instance", existing_instance)
        
        if existing_instance:
            # If a record exists, update the existing instance with the form data
            for field in form.Meta.fields:
                setattr(existing_instance, field, form.cleaned_data[field])
            existing_instance.save()
            return JsonResponse({'success': 'Form data updated successfully.'})
        else:
            # If no record exists, save the form data as a new instance
            form.save()
            return JsonResponse({'success': 'Form submitted successfully.'})

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)


import calendar
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.conf import settings  


class TradingCalenderView(LoginRequiredMixin, View):
    login_url = '/login'

    def get_first_last_dates(self, year, month):
        first_date = datetime.datetime(year, month, 1).strftime('%Y-%m-%d')
        last_date = (datetime.datetime(year, month, calendar.monthrange(year, month)[1])
                     .strftime('%Y-%m-%d'))
        return first_date, last_date

    def get(self, request):
        client_id = settings.FYERS_APP_ID
        access_token = request.session.get('access_token')

        if access_token:
            fyers = fyersModel.FyersModel(
                client_id=client_id, 
                is_async=False, 
                token=access_token,
                log_path=""
            )
            response = fyers.get_profile()

            # Get current month calendar
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            cal = calendar.monthcalendar(year, month)
            month_name = calendar.month_name[month]
            first_date, last_date = self.get_first_last_dates(year, month)

            date_wise_data = SOD_EOD_Data.objects.filter(trading_date=now).first()



            if request.is_ajax():
                # If the request is AJAX and it's for the previous month data
                year = request.GET.get('year')
                month = request.GET.get('month')
                if  'prev_month' in request.GET:
                    year, month = self.calculate_previous_month(int(year), int(month))  # Function to calculate the previous month
                elif 'next_month' in request.GET:
                    year, month = self.calculate_next_month(int(year), int(month))  # Function to calculate the previous month
                elif 'current_month' in request.GET:
                    year = int(year)
                    month = int(month)
                    # year, month = self.calculate_next_month(int(year), int(month))  # Function to calculate the previous month
                print('yearyearyearyearyearyearyearyearyear', year, type(year))
                print('month', month, type(month))

                cal = calendar.monthcalendar(year, month)
                month_name = calendar.month_name[month]
                first_date, last_date = self.get_first_last_dates(year, month)
                # Iterate over each week in the calendar data
                for week in cal:
                    # Check if the first day of the week is valid
                    if week[6]  != 0:
                        # If the first day is None, indicating days outside the month, find the first valid day
                        for day in week:
                            if day  != 0:
                                week_number = self.get_week_of_year(year, month, day)
                                week.append(week_number)
                                break
                    else:
                        # Calculate week number for the first day of the week
                        week_number = self.get_week_of_year(year, month, week[0])
                        # Append week number to the week list
                        week.append(week_number)

                profit_data = SOD_EOD_Data.objects.filter(trading_date__range=[first_date, last_date])
                profit_data_dict = {entry['trading_date'].strftime('%d-%m-%Y'): entry['day_p_and_l'] for entry in profit_data.values('trading_date', 'day_p_and_l')}            
                #print("profit_data_dict", profit_data_dict)

                combined_list = []
                for row in cal:
                    combined_row = []
                    counter=1
                    for i, item in enumerate(row):
                        limit = len(row)
                        if i == limit:
                            combined_row.append(item)  
                            #print("combined_row", combined_row)
                            # Append the last item as is
                        elif isinstance(item, int):
                                date_key = f"{item:02d}-{month:02d}-{year}"  # Construct the date dynamically
                                if date_key in profit_data_dict:
                                    #print('date_key', date_key, item)
                                    combined_row.append({counter:[item ,float(profit_data_dict[date_key])]})  # Change Decimal to float
                                else:
                                    #print('date_key11', date_key, item)
                                    combined_row.append({counter:[item , 0.00]})  # Change Decimal to float
                        else:
                            #print('date_key12', date_key, item)
                            #print("ppppppppp", i, item)
                            combined_row.append(item)
                        counter +=1
                    combined_list.append(combined_row)
                    for sublist in combined_list:
                        sublist_sum = 0
                        for d in sublist:
                            for key, value in d.items():
                                if key in range(1, 6):  # Check if the key is between 1 and 5
                                    sublist_sum += value[1]  # Add the second element of the value
                                if key == 8:
                                    value[1] = sublist_sum

                    #print("combined_listcombined_list", combined_list)

                return JsonResponse({'calendar': combined_list, 'month_name': month_name, 'month': month, 'year': year, 'first_date': first_date, 'last_date': last_date, 'now' : now})
            


            
            # Iterate over each week in the calendar data
            for week in cal:
                # Check if the first day of the week is valid
                if week[6]  != 0:
                    # If the first day is None, indicating days outside the month, find the first valid day
                    for day in week:
                        # sod_eod_data = SOD_EOD_Data.object.filter()
                        if day  != 0:
                            week_number = self.get_week_of_year(year, month, day)
                            week.append(week_number)
                            break
                else:
                    # Calculate week number for the first day of the week
                    week_number = self.get_week_of_year(year, month, week[0])
                    # Append week number to the week list
                    week.append(week_number)

            profit_data = SOD_EOD_Data.objects.filter(trading_date__range=[first_date, last_date])
            profit_data_dict = {entry['trading_date'].strftime('%d-%m-%Y'): entry['day_p_and_l'] for entry in profit_data.values('trading_date', 'day_p_and_l')}            
            #print("profit_data_dict", profit_data_dict)

            combined_list = []
            for row in cal:
                combined_row = []
                counter=1
                for i, item in enumerate(row):
                    limit = len(row)
                    if i == limit:
                        combined_row.append(item)  
                        #print("combined_row", combined_row)
                        # Append the last item as is
                    elif isinstance(item, int):
                            date_key = f"{item:02d}-{month:02d}-{year}"  # Construct the date dynamically
                            if date_key in profit_data_dict:
                                #print('date_key', date_key, item)
                                combined_row.append({counter:[item ,float(profit_data_dict[date_key])]})  # Change Decimal to float
                            else:
                                #print('date_key11', date_key, item)
                                combined_row.append({counter:[item , 0.00]})  # Change Decimal to float
                    else:
                        #print('date_key12', date_key, item)
                        #print("ppppppppp", i, item)
                        combined_row.append(item)
                    counter +=1
                combined_list.append(combined_row)
                for sublist in combined_list:
                    sublist_sum = 0
                    for d in sublist:
                        for key, value in d.items():
                            if key in range(1, 6):  # Check if the key is between 1 and 5
                                sublist_sum += value[1]  # Add the second element of the value
                            if key == 8:
                                value[1] = sublist_sum


                






            # for date, profit in profit_data_dict.items():
            #     day = int(date.split('-')[0])
            #     for row in cal:
            #         if day in row[:-1]:  # Exclude the last element of the sublist
            #             index = row.index(day)
            #             row[index] = f"{day}:{profit}"




            context = {
                'calendar': combined_list, 
                'month_name': month_name,
                'month': month,
                'year': year,
                'first_date': first_date,
                'last_date': last_date,
                'now' : now,
                'now_date': now.day,
                'now_month': now.month,
                'now_year': now.year,
                'date_wise_data' : date_wise_data,
                'profit_data_dict': profit_data_dict
            }
            return render(request, 'trading_tool/html/calender_view.html', context)
        
        else:
            #print("no access token")
            return render(request, 'trading_tool/html/calender_view.html')

    def calculate_next_month(self, year, month):
        # Calculate the next month
        month += 1
        if month > 12:
            # If the current month is December, go to the next year and set the month to January
            year += 1
            month = 1
        return year, month
    
    def calculate_previous_month(self, year, month):
        # Calculate the previous month
        month -= 1
        if month == 0:
            # If the current month is January, go to the previous year
            year -= 1
            month = 12

        return year, month

    def get_week_of_year(self, year, month, day):
        # Calculate the nth week of the year if the day is valid for the month
        if 1 <= day <= calendar.monthrange(year, month)[1]:
            week_number = datetime.datetime(year, month, day).isocalendar()[1]
            return week_number
        else:
            return None  # Return None if the day is outside the valid range for the month


from django.http import JsonResponse
class OrderHistory(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        context = {}
        data_instance = get_data_instance(request)
        order_data = data_instance.orderbook()
        page_count = 10

        # Ensure order_data is a list or a queryset
        if not isinstance(order_data, list):
            # If order_data is not a list, assume it's a dictionary and extract the 'orderBook' key
            order_data = order_data.get('orderBook', [])
            order_data = sorted(order_data, key=lambda x: x['slNo'], reverse=True)

            # Map status values to their descriptions
            for order in order_data:
                order['status_description'] = settings.STATUS_DESCRIPTIONS.get(order.get('status', 'Unknown'))

        if request.is_ajax():
            load_more = request.GET.get('load_more', None)
            if load_more:
                page_count=200


        paginator = Paginator(order_data, page_count)  # Show 20 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if request.is_ajax():
            # If the request is AJAX, fetch the filter value and filter the queryset

            status_filter = request.GET.get('status', None)  # Assuming AJAX passes 'status' parameter for filtering
            print("status_filterstatus_filter", status_filter)
         
            
            # Get the current page's data
            current_page_data = list(page_obj)
            filtered_data=[]

            print("current_page_datacurrent_page_data", current_page_data)

            # Filter the current page's data based on the status
            if status_filter:
                filtered_data = [order for order in current_page_data if order.get('status') == int(status_filter)]
                print("filtered_datafiltered_datafiltered_data", filtered_data)
            else:
                filtered_data = current_page_data

            # Create a new paginator for the filtered data
            filtered_paginator = Paginator(filtered_data, page_count )
            filtered_page_number = request.GET.get('page')
            filtered_page_obj = filtered_paginator.get_page(filtered_page_number)

            # Return the filtered data as JSON response
            return render(request, 'trading_tool/html/order_ajaxtemp.html', {'order_history_data': filtered_page_obj})

        # Otherwise, return the entire rendered page
        context['order_history_data'] = page_obj
        return render(request, 'trading_tool/html/order_history.html', context)
    

from django.http import JsonResponse
class TransactionHistory(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        context = {}
        get_transaction_data =SOD_EOD_Data.objects.filter(
                                    Q(withdrwal_amount__gt=0) | Q(withdrwal_amount__lt=0) |
                                    Q(deposit_amount__gt=0) | Q(deposit_amount__lt=0)
                                ).order_by('-trading_date')
        context['get_transaction_data'] = get_transaction_data
        return render(request, 'trading_tool/html/transaction_history.html', context)


class OptionChainView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, slug):
        context = {}
        template = 'trading_tool/html/optionchainview.html'
        data_instance = get_data_instance(request)
        conf_data = TradingConfigurations.objects.order_by('-last_updated').first()

        forward_trailing_points = conf_data.forward_trailing_points
        reverse_trailing_points = conf_data.reverse_trailing_points
        scalping_mode = conf_data.scalping_mode
        cost = conf_data.scalping_amount_limit if scalping_mode else conf_data.capital_limit_per_order
        stoploss_percentage = conf_data.scalping_stoploss if scalping_mode else conf_data.default_stoploss
        exchange = "BSE:" if slug == "SENSEX" else "NSE:"

        data = {"symbol": f"{exchange}{slug}-INDEX", "strikecount": 2}

        try:
            expiry_response = data_instance.optionchain(data=data)
            order_data = data_instance.orderbook()
            total_order_status = sum(1 for order in order_data.get("orderBook", []) if order["status"] == 2)
            positions_data = data_instance.positions()

            tax = calculate_tax(cost)
            default_brokerage = settings.DEFAULT_BROKERAGE + tax
            exp_brokerage = default_brokerage * total_order_status
            trading_config = TradingConfigurations.objects.order_by('-last_updated').first()
            order_limit = trading_config.max_trade_count
            exp_brokerage_limit = order_limit * default_brokerage

            first_expiry_ts = expiry_response['data']['expiryData'][0]['expiry']
            first_expiry_date = expiry_response['data']['expiryData'][0]['date']
        except (KeyError, AttributeError, IndexError) as e:
            error_message = f'Error occurred: {str(e)}'
            messages.error(request, error_message)
            return redirect('login')

        options_data = {"symbol": f"{exchange}{slug}-INDEX", "strikecount": 2, "timestamp": first_expiry_ts}

        try:
            response = data_instance.optionchain(data=options_data)
        except AttributeError as e:
            error_message = f'Error occurred while fetching options data: {str(e)}'
            messages.error(request, error_message)
            return render(request, template, context)

        pe_options = [option for option in response['data']['optionsChain'] if option['option_type'] == 'PE']
        pe_options_sorted = sorted(pe_options, key=lambda x: x['strike_price'], reverse=True)

        for index, option in enumerate(pe_options_sorted, start=1):
            option['serial_number'] = index
            option['lot_cost'] = int(option['ltp']) * get_default_lotsize(slug)

        ce_options = [option for option in response['data']['optionsChain'] if option['option_type'] == 'CE']
        ce_options_sorted = sorted(ce_options, key=lambda x: x['strike_price'])

        for index, option in enumerate(ce_options_sorted, start=1):
            option['serial_number'] = index
            option['lot_cost'] = int(option['ltp']) * get_default_lotsize(slug)

        actual_profit = round(float(positions_data['overall']['pl_realized']) - float(exp_brokerage), 2)
        reward_ratio = conf_data.reward_ratio
        exp_loss = (cost * stoploss_percentage) / 100
        exp_profit_percentage = stoploss_percentage * reward_ratio
        exp_profit = (cost * exp_profit_percentage) / 100

        day_max_loss = -conf_data.max_loss
        super_trader_threshold = exp_brokerage_limit * reward_ratio * 2

        # max_serial_number = len(pe_options_sorted) * 2 - 1
        # atm_index = (max_serial_number // 2) + 1

        atm_index = len(pe_options_sorted) // 2  # Calculate the ATM index









        context.update({
            'access_token': request.session.get('access_token'),
            'forward_trailing_points': forward_trailing_points,
            'reverse_trailing_points': reverse_trailing_points,
            'ce_options_with_serial': ce_options_sorted,
            'pe_options_with_serial': pe_options_sorted,
            # 'max_serial_number': max_serial_number,
            'atm_index': atm_index,
            'expiry_response': first_expiry_date,
            'positions_data': positions_data,
            'order_limit': order_limit,
            'exp_brokerage_limit': exp_brokerage_limit,
            'day_exp_profit': exp_brokerage_limit * reward_ratio,
            'exp_loss': exp_loss,
            'day_max_loss': day_max_loss,
            'day_max_loss_end': -(exp_brokerage_limit * reward_ratio),
            'exp_profit': exp_profit,
            'super_trader_threshold': super_trader_threshold,
            'total_order_status': total_order_status,
            'day_exp_brokerage': exp_brokerage,
            'actual_profit': actual_profit,
            'options_data': response
        })
        return render(request, template, context)

def calculate_tax(cost):
    a = 0.000732
    b = 3.962
    tax = a * cost + b
    return tax

def update_latest_data(request):
    data_instance = get_data_instance(request)

    positions = data_instance.positions()
    TradingData.objects.update_or_create(
        category='POSITIONS',
        defaults={'data': positions, 'last_updated': timezone.now()}
    )

    orders = data_instance.orderbook()
    TradingData.objects.update_or_create(
        category='ORDERS',
        defaults={'data': orders, 'last_updated': timezone.now()}
    )

    funds = data_instance.funds()
    TradingData.objects.update_or_create(
        category='FUNDS',
        defaults={'data': funds, 'last_updated': timezone.now()}
    )

    return HttpResponse('Data saved')

   
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import FormView
from .forms import TradingConfigurationsForm
from .models import TradingConfigurations

from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import TradingConfigurationsForm
from .models import TradingConfigurations
from django.utils import timezone

from django.utils import timezone
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .forms import TradingConfigurationsForm
from .models import TradingConfigurations

class ConfigureTradingView(LoginRequiredMixin, FormView):
    login_url = '/login'
    template_name = 'trading_tool/html/configure_trading.html'
    form_class = TradingConfigurationsForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        six_hours_ago = timezone.now() - timezone.timedelta(seconds=1)
        trading_config_exists = TradingConfigurations.objects.filter(last_updated__gte=six_hours_ago)
        if trading_config_exists.exists():
            kwargs['instance'] = trading_config_exists.first()
        else:
            kwargs['instance'] = TradingConfigurations()

        return kwargs

    def form_valid(self, form):
        six_hours_ago = timezone.now() - timezone.timedelta(seconds=1)
        trading_config_exists = TradingConfigurations.objects.filter(last_updated__gte=six_hours_ago)
        if trading_config_exists.exists():
            return JsonResponse({'error': True})
        else:
            trading_config = form.save(commit=False)
            # Calculate scalping_amount_limit
            trading_config.scalping_amount_limit =  trading_config.capital_limit_per_order / trading_config.scalping_ratio
            trading_config.scalping_stoploss = trading_config.scalping_ratio * trading_config.default_stoploss
            form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_configurations'] = TradingConfigurations.objects.all().order_by('-last_updated')[:1]  # Modify the query as needed
        return context


def get_default_lotsize(index):
    if index == 'MIDCPNIFTY':
        return 75
    elif index == 'FINNIFTY':
        return 40
    elif index == 'BANKNIFTY':
        return 15
    elif index == 'NIFTY':
        return 25
    elif index == 'SENSEX':
        return 10
    else:
        return False


from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
from .models import TradingConfigurations, OpenOrderTempData

def instantBuyOrderWithSL(request):
    if request.method == 'POST':
        data_instance = get_data_instance(request)
        der_symbol = request.POST.get('der_symbol')
        ex_symbol = request.POST.get('ex_symbol')
        ltp = Decimal(request.POST.get('ltp'))
        get_lot_count = get_default_lotsize(ex_symbol)
        trade_config_data = TradingConfigurations.objects.order_by('-last_updated').first()
        scalping_mode = trade_config_data.scalping_mode
        allOrderData = data_instance.orderbook()
        total_order_count = sum(1 for order in allOrderData.get("orderBook", []) if order["status"] == 2)
        max_order_count_limit = trade_config_data.max_trade_count
        if int(total_order_count) >= int(max_order_count_limit):
            message = "Max Order count limit Reached"
            return JsonResponse({'response': message})
        
        tempDatainstance = OpenOrderTempData.objects.order_by('-last_updated').first()
        if tempDatainstance and tempDatainstance.symbol != der_symbol:
            message = "Unable to place another Symbol Order Now."
            return JsonResponse({'response': message})

        if trade_config_data.order_quantity_mode == "MANUAL":
            order_qty = trade_config_data.default_order_qty * get_lot_count

        elif trade_config_data.order_quantity_mode == "AUTOMATIC":
            limit_amount = trade_config_data.scalping_amount_limit if scalping_mode else trade_config_data.capital_limit_per_order
            per_lot_expense = ltp * get_lot_count
            lotqty = Decimal(limit_amount) // per_lot_expense
            order_qty = int(lotqty * get_lot_count)
            if order_qty == 0:
                message = "Amount Usage Limit Reached"
                return JsonResponse({'response': message})

        data = {
            "symbol": der_symbol,
            "qty": order_qty,
            "type": 2,  # Market Order
            "side": 1,  # Buy
            "productType": "INTRADAY",
            "validity": "DAY",
            "offlineOrder": False
        }

        response = data_instance.place_order(data=data)
        
        if response["code"] == 1101:
            
            order_with_status_6 = next((order for order in allOrderData["orderBook"] if order['status'] == 6 and order["symbol"] == der_symbol), None)
            if tempDatainstance and order_with_status_6:
                exst_qty = tempDatainstance.quantity
                new_qty = order_qty + exst_qty
                total_order_expense = order_qty * ltp
                ext_total_order_expense = Decimal(tempDatainstance.order_total) + total_order_expense
                average_price = ext_total_order_expense / new_qty
                sl_price = tempDatainstance.sl_price
                exp_loss = (Decimal(average_price) - Decimal(sl_price)) * Decimal(new_qty)
                is_averaged = tempDatainstance.is_averaged + 1

                tempDatainstance.update(
                    order_total=ext_total_order_expense, 
                    premium_price=ltp, 
                    quantity=new_qty, 
                    average_price=average_price, 
                    exp_loss=exp_loss, 
                    is_averaged=is_averaged
                )

                modify_data = {"id": order_with_status_6["id"], "type": 4, "qty": new_qty}
                modify_response = data_instance.modify_order(data=modify_data)
                return JsonResponse({'response': modify_response["message"]})
            
            else:
                buy_order_id = response["id"]
                buy_order_data = {"id": buy_order_id}
                order_details = data_instance.orderbook(data=buy_order_data)["orderBook"][0]
                traded_price = Decimal(order_details["tradedPrice"])

                stoplossConf = trade_config_data.scalping_stoploss if scalping_mode else trade_config_data.default_stoploss
                default_stoploss = Decimal(stoplossConf)
                stoploss_limit_slippage = Decimal(trade_config_data.stoploss_limit_slippage)

                stoploss_price = traded_price - (traded_price * default_stoploss / 100)
                stoploss_price = round(stoploss_price / Decimal(0.05)) * Decimal(0.05)
                stoploss_price = round(stoploss_price, 2)
                stoploss_limit = stoploss_price - stoploss_limit_slippage
                stoploss_limit = round(stoploss_limit / Decimal(0.05)) * Decimal(0.05)
                stoploss_limit = round(stoploss_limit, 2)

                sl_data = {
                    "symbol": der_symbol,
                    "qty": order_qty,
                    "type": 4,  # SL-L Order
                    "side": -1,  # Sell
                    "productType": "INTRADAY",
                    "limitPrice": stoploss_limit,
                    "stopPrice": stoploss_price,
                    "validity": "DAY",
                    "offlineOrder": False,
                }

                stoploss_order_response = data_instance.place_order(data=sl_data)
                total_purchase_value = traded_price * order_qty
                sl_price = stoploss_price
                exp_loss = (traded_price - sl_price) * order_qty

                OpenOrderTempData.objects.create(
                    symbol=der_symbol, 
                    order_total=total_purchase_value, 
                    premium_price=traded_price, 
                    average_price=traded_price, 
                    quantity=order_qty, 
                    sl_price=sl_price, 
                    exp_loss=exp_loss, 
                    is_averaged=0
                )

                if stoploss_order_response["code"] == 1101:
                    message = "BUY/SL-L Placed Successfully"
                    return JsonResponse({'response': message, 'symbol': der_symbol, 'qty': order_qty, 'traded_price': traded_price})
                elif stoploss_order_response["code"] == -99:
                    message = "SL-L not Placed, Insufficient Fund"
                    return JsonResponse({'response': message})
                else:
                    return JsonResponse({'response': stoploss_order_response["message"]})
        elif response["code"] == -99:
            return JsonResponse({'response': response['message'], 'symbol': der_symbol, 'code': response["code"]})
        else:
            return JsonResponse({'response': response["message"]})
    else:
        message = "Some Error Occurred Before Execution"
        return JsonResponse({'response': message})


def StopLossCalculator(purchase_price: float, loss_percentage: float) -> int:
    stop_loss_price = purchase_price * (1 - loss_percentage / 100)
    return int(round(stop_loss_price))


def trailingwithlimit(request):
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')
    
    if access_token:
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
        order_data = fyers.orderbook()

        if 'orderBook' not in order_data:
            message = "Error fetching order book data."
            messages.error(request, message)
            return JsonResponse({'message': message})
        
        existing_stop_price = None
        existing_limit_price = None
        symbol = None

        for order in order_data.get("orderBook", []):
            if order.get("status") == 6:
                existing_stop_price = order.get("stopPrice", existing_stop_price)
                existing_limit_price = order.get("limitPrice", existing_limit_price)
                symbol = order.get("symbol", symbol)
        
        if existing_stop_price is not None and existing_limit_price is not None:
            trade_config_data = TradingConfigurations.objects.order_by('-last_updated').first()
            if not trade_config_data:
                message = "No trading configuration data found."
                messages.error(request, message)
                return JsonResponse({'message': message})

            forwrd_trail_limit = Decimal(trade_config_data.forward_trailing_points)

            new_stop_price = Decimal(existing_stop_price) + forwrd_trail_limit
            new_limit_price = Decimal(existing_limit_price) + forwrd_trail_limit

            if symbol:
                data = {"id": order["id"], "type": order["type"], "limitPrice": float(new_limit_price), "stopPrice": float(new_stop_price)}
                trailing_order_update = fyers.modify_order(data=data)

                if 'message' in trailing_order_update:
                    openTempDatainstance = OpenOrderTempData.objects.filter(symbol=symbol).first()
                    if openTempDatainstance:
                        exp_loss = (Decimal(openTempDatainstance.open_traded_price) - new_stop_price) * Decimal(openTempDatainstance.order_qty)
                        openTempDatainstance.sl_price = new_stop_price
                        openTempDatainstance.exp_loss = exp_loss
                        openTempDatainstance.save()
                    
                    message = trailing_order_update['message']
                    messages.success(request, message)
                    return JsonResponse({'message': message})
                else:
                    message = "Error updating trailing order."
                    messages.error(request, message)
                    return JsonResponse({'message': message})
            else:
                message = "No valid orders to modify."
                messages.error(request, message)
                return JsonResponse({'message': message})
        
        message = "No SL/Pending Orders"
        messages.error(request, message)
        return JsonResponse({'message': message})
    
    return redirect('dashboard')



def trailingtodown(request):
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')
    
    if access_token:
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
        order_data = fyers.orderbook()

        if 'orderBook' not in order_data:
            message = "Error fetching order book data."
            messages.error(request, message)
            return JsonResponse({'message': message})
        
        existing_stop_price = None
        existing_limit_price = None
        symbol = None

        for order in order_data.get("orderBook", []):
            if order.get("status") == 6:
                existing_stop_price = order.get("stopPrice", existing_stop_price)
                existing_limit_price = order.get("limitPrice", existing_limit_price)
                symbol = order.get("symbol", symbol)
        
        if existing_stop_price is not None and existing_limit_price is not None:
            trade_config_data = TradingConfigurations.objects.order_by('-last_updated').first()
            if not trade_config_data:
                message = "No trading configuration data found."
                messages.error(request, message)
                return JsonResponse({'message': message})

            reverse_trail_limit = Decimal(trade_config_data.reverse_trailing_points)

            new_stop_price = Decimal(existing_stop_price) - reverse_trail_limit
            new_limit_price = Decimal(existing_limit_price) - reverse_trail_limit

            if symbol:
                data = {"id": order["id"], "type": order["type"], "limitPrice": float(new_limit_price), "stopPrice": float(new_stop_price)}
                trailing_order_update = fyers.modify_order(data=data)

                if 'message' in trailing_order_update:
                    openTempDatainstance = OpenOrderTempData.objects.filter(symbol=symbol).first()
                    if openTempDatainstance:
                        exp_loss = (Decimal(openTempDatainstance.open_traded_price) - new_stop_price) * Decimal(openTempDatainstance.order_qty)
                        openTempDatainstance.sl_price = new_stop_price
                        openTempDatainstance.exp_loss = exp_loss
                        openTempDatainstance.save()
                    
                    message = trailing_order_update['message']
                    messages.success(request, message)
                    return JsonResponse({'message': message})
                else:
                    message = "Error updating trailing order."
                    messages.error(request, message)
                    return JsonResponse({'message': message})
            else:
                message = "No valid orders to modify."
                messages.error(request, message)
                return JsonResponse({'message': message})
        
        message = "No SL/Pending Orders"
        messages.error(request, message)
        return JsonResponse({'message': message})
    
    return redirect('dashboard')


def trailingtotop(request):
    client_id = settings.FYERS_APP_ID
    access_token = request.session.get('access_token')
    symbol = None

    if access_token:
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
        order_data = fyers.orderbook()

        if 'orderBook' not in order_data:
            message = "Error fetching order book data."
            messages.error(request, message)
            return JsonResponse({'message': message})

        for order in order_data.get("orderBook", []):
            if order.get("status") == 6:
                symbol = order.get("symbol", symbol)

        if symbol is not None:
            response = fyers.positions()

            if 'netPositions' not in response:
                message = "Error fetching positions data."
                messages.error(request, message)
                return JsonResponse({'message': message})

            filtered_positions = [position for position in response["netPositions"] if position["symbol"] == symbol]

            if not filtered_positions:
                message = "No matching positions found."
                messages.error(request, message)
                return JsonResponse({'message': message})

            ltp = Decimal(filtered_positions[0]["ltp"])

            trade_config_data = TradingConfigurations.objects.order_by('-last_updated').first()
            if not trade_config_data:
                message = "No trading configuration data found."
                messages.error(request, message)
                return JsonResponse({'message': message})

            trailing_to_top_points = Decimal(trade_config_data.trailing_to_top_points)
            stoploss_limit_slippage = Decimal(trade_config_data.stoploss_limit_slippage)

            new_stop_price = ltp - trailing_to_top_points
            new_limit_price = new_stop_price - stoploss_limit_slippage

            if symbol:
                data = {"id": order["id"], "limitPrice": float(new_limit_price), "stopPrice": float(new_stop_price)}
                trailing_order_update = fyers.modify_order(data=data)

                if 'message' in trailing_order_update:
                    openTempDatainstance = OpenOrderTempData.objects.filter(symbol=symbol).first()
                    if openTempDatainstance:
                        exp_loss = (Decimal(openTempDatainstance.open_traded_price) - new_stop_price) * Decimal(openTempDatainstance.order_qty)
                        openTempDatainstance.sl_price = new_stop_price
                        openTempDatainstance.exp_loss = exp_loss
                        openTempDatainstance.save()

                    message = trailing_order_update['message']
                    messages.success(request, message)
                    return JsonResponse({'message': message})

            else:
                message = "No valid orders to modify."
                messages.error(request, message)
                return JsonResponse({'message': message})

        message = "No SL/Pending Orders"
        messages.error(request, message)
        return JsonResponse({'message': message})

    return redirect('dashboard')




def fyer_websocket_view(request):
    template_name = 'trading_tool/html/fyerwebsocket.html'
    access_token = request.session.get('access_token')
    return render(request, template_name)




from django.http import JsonResponse
def store_current_value_in_session(request):
    if request.method == 'POST':
        #print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
        # Retrieve data from POST request
        open_symbol = request.POST.get('open_symbol')
        open_qty = request.POST.get('open_qty')
        open_traded_price = request.POST.get('open_traded_price')
        
        # Store data in session
        request.session['open_symbol'] = open_symbol
        request.session['open_qty'] = open_qty
        request.session['open_traded_price'] = open_traded_price
        
        return JsonResponse({'message': 'Current values stored in session successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    

def get_open_temp_data(request):
    if request.method == 'GET':
        # Retrieve session data
        # open_symbol = request.session.get('open_symbol')
        # open_qty = request.session.get('open_qty')
        # open_traded_price = request.session.get('open_traded_price')
        # exp_stoploss_amount = request.session.get('exp_stoploss_amount')
        openTempDatainstance = OpenOrderTempData.objects.order_by('-last_updated')
        confData = TradingConfigurations.objects.order_by('-last_updated').first()
        print("ENtry111111111111111111111111111111111")
        scalping_mode = confData.scalping_mode
        print("ENtry111111111111111111111111111111111", scalping_mode)
        

        # Check if session data exists
        # if open_symbol is not None and open_qty is not None and open_traded_price is not None:
        if openTempDatainstance.exists():
            print("entry22222222222222222222222222222222222")
            openTempData = openTempDatainstance.first()
            open_symbol = openTempData.symbol
            open_qty = openTempData.quantity
            open_traded_price = openTempData.average_price
            total_order_amount = openTempData.order_total
            exp_loss = openTempData.exp_loss
            exp_stoploss_amount = request.session.get('exp_stoploss_amount')
            sl_price = openTempData.sl_price
    
            return JsonResponse({
                'open_symbol': open_symbol,
                'open_qty': open_qty,
                'open_traded_price': open_traded_price,
                'exp_stoploss_amount': exp_stoploss_amount,
                'total_order_amount': total_order_amount,
                'exp_loss': exp_loss,
                'sl_price': sl_price,
                'scalping_mode': scalping_mode

                
            })
        else:
            return JsonResponse({'error': 'No Open Position for now'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    

def remove_session_data(request):
    if request.method == 'POST':
        # Remove session data
        request.session.pop('open_symbol', None)
        request.session.pop('open_qty', None)
        request.session.pop('open_traded_price', None)
        return JsonResponse({'message': 'Session data removed successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    

def switch_scalp_mode(request):
    if request.method == 'GET':
        # Fetch the latest TradingConfigurations entry
        confData = TradingConfigurations.objects.order_by('-last_updated').first()
        if not confData.scalping_mode:
            capital_limit_per_lot  = confData.scalping_amount_limit
        else:
            capital_limit_per_lot  = confData.capital_limit_per_order
        if confData:
            print("Entry - Toggling scalping_mode")
            # Toggle the scalping_mode value
            confData.scalping_mode = not confData.scalping_mode
            confData.save()
            # Return the updated value as a JsonResponse
            return JsonResponse({'scalping_mode': confData.scalping_mode, 'capital': capital_limit_per_lot })
        else:
            print("No TradingConfigurations entry found.")
            # Return an error if no entry is found
            return JsonResponse({'error': 'No configuration found.'}, status=404)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def get_scalp_mode_state(request):
    if request.method == 'GET':
        # Fetch the latest TradingConfigurations entry
        confData = TradingConfigurations.objects.order_by('-last_updated').first()
        if confData.scalping_mode:
            capital_limit_per_lot  = confData.scalping_amount_limit
        else:
            capital_limit_per_lot  = confData.capital_limit_per_order

        
        if confData:
            # Return the updated value as a JsonResponse
            return JsonResponse({'scalping_mode': confData.scalping_mode, 'capital': capital_limit_per_lot })
        else:
            print("No TradingConfigurations entry found.")
            # Return an error if no entry is found
            return JsonResponse({'error': 'No configuration found.'}, status=404)



