from django import forms
from .models import *
from django.forms import ModelForm

class CalorieCal(forms.Form):

   CASES = [
      ('1','운동강도 하'),
      ('2','운동강도 중'),
      ('3','운동강도 상')
   ]
   gender = [
      ('Male','남자'),
      ('Female','여자')
   ]
   
   Age=forms.IntegerField(label='AGE:',widget=forms.TextInput(attrs={'placeholder': '나이'}))
   Weight=forms.IntegerField(label='Weight:',widget=forms.TextInput(attrs={'placeholder': '몸무게'}))
   WeightChoice=forms.CharField(widget=forms.RadioSelect(choices=[('LB','LB'),('KG','KG')]))
   #Height for US
   Height=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '키','class':'US'}),required=False)
   #Height for metric
   #Feet
   Height_1st=forms.IntegerField(label='Height (Feet)',widget=forms.TextInput(attrs={'placeholder': '키','class':'metric',}),required=False)
   Height_2nd=forms.IntegerField(label='Height (Inches)',widget=forms.TextInput(attrs={'placeholder': '키','class':'metric'}),required=False)
   HeightChoice=forms.CharField(widget=forms.RadioSelect(choices=[('CM','CM'),('Feet','Feet')],attrs={'class':'heightChoice CM','onchange':'myFunction(this.value)'}))

   Gender=forms.CharField(widget=forms.RadioSelect(choices=gender))
   CalType=forms.CharField(widget=forms.Select(choices=[('Losing Weight','다이어트'),('Gaining Muscle','근육증가')]))
   Activity=forms.CharField(max_length=50,widget=forms.Select(choices=CASES))


