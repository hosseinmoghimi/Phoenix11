from django import forms
class AddMealItemForm(forms.Form):
    food_item_id=forms.IntegerField(required=True)
    meal_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=True)
    price=forms.IntegerField(required=True)