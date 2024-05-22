from django.shortcuts import redirect, render
from account.forms import UserLoginForm, UserprofileUpdate
from django.contrib import auth
from django.views import View  
from django.contrib.auth import logout
from django.contrib import messages
from account.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from datetime import datetime
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView
from fyersapi.models import TradingConfigurations, TradingData
from fyersapi.views import brokerconnect, get_accese_token_store_session, get_data_instance
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from urllib.parse import urlparse, parse_qs
from django.contrib.auth.decorators import login_required
import time
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from urllib.parse import urlparse, parse_qs
from django.contrib import messages
import time
from django.contrib.auth.mixins import LoginRequiredMixin


def homePage(request):
    return render(request,'accounts/index.html')

class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = "trading_tool/html/index.html"
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            current_url = request.build_absolute_uri()
            parsed_url = urlparse(current_url)
            query_params = parse_qs(parsed_url.query)
            auth_code = query_params.get('auth_code', [''])[0]
            if auth_code:
                request.session['auth_code'] = auth_code
                messages.success(request, 'Auth code stored successfully.')
            else:
                messages.error(request, 'Failed to extract auth code from the URL.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}. No broker connected.')

        # Delay the execution of get_access_token function by 1 second
        time.sleep(1)
        get_accese_token_store_session(request)
        access_token = request.session.get('access_token')
        data_instance = get_data_instance(request)
        try:
            self.positions_data = data_instance.positions()
        except AttributeError as e:
            self.positions_data = {'code': -1, 'message': f'Error occurred: {str(e)}', 's': 'error'}
            #print("Error occurred while fetching positions data:", e)

        try:
            self.order_data = data_instance.orderbook()
        except AttributeError as e:
            self.order_data = {'code': -1, 'message': f'Error occurred: {str(e)}', 's': 'error'}
            #print("Error occurred while fetching order data:", e)

        try:
            self.fund_data = data_instance.funds()
        except AttributeError as e:
            self.fund_data = {'code': -1, 'message': f'Error occurred: {str(e)}', 's': 'error'}
            #print("Error occurred while fetching fund data:", e)

        self.total_order_status = 0
        self.pending_orders_status_6 = 0
        self.expected_brokerage = 0 
        average_brokerage = 30
        self.recent_order_data = []
        trading_config = TradingConfigurations.objects.first()
        # #print("self.order_limitself.order_limit", self.order_limit) 
        #  trading_config.max_trade_count
        self.order_limit =  trading_config.max_trade_count
        self.progress_percentage= 0
        if self.order_data and "orderBook" in self.order_data:
            # Filter orders with status 6
            filled_orders = [order for order in self.order_data["orderBook"] if order["status"] == 2]
            # Sort pending orders by orderDateTime in descending order
            filled_orders_sorted = sorted(filled_orders, key=lambda x: x["orderDateTime"], reverse=True)
            # Iterate over the first 10 items in the sorted data
            for order in filled_orders_sorted[:10]:
                self.recent_order_data.append(order)
            # Update pending order count
            self.pending_orders_status_6 = sum(1 for order in self.order_data["orderBook"] if order["status"] == 6)
            # Update total order count for status 2
            self.total_order_status = sum(1 for order in self.order_data["orderBook"] if order["status"] == 2)
            

            self.progress_percentage = (self.total_order_status / self.order_limit) * 100
            self.progress_percentage = round(self.progress_percentage, 1)
        self.expected_brokerage = self.total_order_status * average_brokerage
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_limit'] = self.order_limit
        context['order_data'] = self.order_data
        context['fund_data'] = self.fund_data
        context['total_order_status'] = self.total_order_status
        context['progress_percentage'] = self.progress_percentage
        context['pending_orders_status'] = self.pending_orders_status_6
        context['expected_brokerage'] = self.expected_brokerage
        context['recent_order_data'] = self.recent_order_data
        context['positions_data'] = self.positions_data
        return context

class UserloginView(View):
    def get(self, request):
        template = "trading_tool/html/authentication-login.html"
        context = {}
        context['form'] = UserLoginForm()
        #print("context", context)
        logged_user = request.user

        if logged_user.is_authenticated:
            #print(logged_user)
            #print("dashboard__form")
            return redirect('brokerconnect')  
        else:
            #print(logged_user)
            #print("login__form")
            return render(request, template, context)
        
    def logoutUser(self, request):  # Make sure to include `self` as the first parameter for methods in a class
        #print("logout_processing")
        logout(request)
        messages.success(request, "Logout Successful !")
        return redirect('login')

    def post(self, request):
        context={}
        form = UserLoginForm(request.POST)
        context['form']= form
        template = "trading_tool/html/authentication-login.html"
        if request.method == "POST":
            if form.is_valid():
                login_username = request.POST["username"]
                login_password = request.POST["password"]
                #print(login_username)
                #print(login_password)
                user = auth.authenticate(username=login_username, password=login_password)
                if user :
                # if user is not None and  user.is_superuser==False and user.is_active==True:
                    auth.login(request, user)
                    #print("login success")
                    messages.success(request, "Login Successful !")
                    # return render(request, "user/dashboard.html")
                    return redirect('brokerconnect')  
                else:
                    #print("user not Exists")
                    # messages.info(request, "user not Exists")
                    messages.error(request, 'Username or Password incorrect !')
                    return render(request, template, context)
            else:
                #print("user not created")
                return render(request, template, context)


class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "trading_tool/html/authentication-register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Authenticate and log in the user
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        messages.success(self.request, 'Registration completed successfully')
        user = authenticate(username=username, password=password)
        messages.success(self.request, 'redirected to Dashboard')
        login(self.request, user)
        return response

class MemberListView(View):
    def get(self, request , **kwargs):
        template = "user/accountmanage.html"
        breadcrumb = {"1":"Member Management", "2":"Manage member" }
        label = { 'title' : "Manage member" }
        header = { "one": 'First Name',"two" : 'Last Name', "three" : "User Name",}
        Data =  User.objects.all()
        context = {'header':header , 'label':label, "breadcrumb":breadcrumb ,"Data": Data}
        return render(request, template, context)

class SuccessView(View):
    def get(self, request):
        template = "success_page.html"
        context={}
        #print("context", context)
        return render(request, template, context)
        
