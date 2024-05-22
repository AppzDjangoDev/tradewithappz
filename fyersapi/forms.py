from django import forms
from django.conf import settings
from .models import TradingConfigurations
from .models import SOD_EOD_Data

class TradingConfigurationsForm(forms.ModelForm):
    class Meta:
        model = TradingConfigurations
        fields = '__all__'  # To include all fields from the model
        # Alternatively, you can specify the fields explicitly:
        # fields = ['default_stoploss', 'default_order_qty', 'max_loss', 'max_trade_count', 'capital_usage_limit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add classes to form fields for Bootstrap styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class SOD_DataForm(forms.ModelForm):
    class Meta:
        model = SOD_EOD_Data
        fields = ['opening_balance', 'withdrwal_amount', 'deposit_amount', 'week_no','prev_day_slippage', 'trading_date']


    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add classes to form fields for Bootstrap styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['opening_balance'].disabled = True
        self.fields['week_no'].disabled = True
        self.fields['trading_date'].disabled = True
        

        

class EOD_DataForm(forms.ModelForm):
    class Meta:
        model = SOD_EOD_Data
        fields = ['closing_balance', 'withdrwal_amount', 'deposit_amount','day_p_and_l','day_exp_brokerage','day_order_count','notes']


    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add classes to form fields for Bootstrap styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['closing_balance'].disabled = True
        self.fields['day_p_and_l'].disabled = True
        self.fields['day_order_count'].disabled = True
        self.fields['day_exp_brokerage'].disabled = True


