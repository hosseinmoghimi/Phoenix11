from django import forms

class AddMealItemForm(forms.Form):
    food_item_id=forms.IntegerField(required=True)
    meal_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=True)
    unit_price=forms.IntegerField(required=True)
    unit_name=forms.CharField(max_length=50,required=True)