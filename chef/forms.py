from accounting.forms import AddProductForm,forms

class AddMealItemForm(forms.Form):
    food_item_id=forms.IntegerField(required=True)
    meal_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=True)
    unit_price=forms.IntegerField(required=True)
    coef=forms.IntegerField(required=True)
    discount_percentage=forms.IntegerField(required=True)
    unit_name=forms.CharField(max_length=50,required=True)
    save=forms.BooleanField(required=False)
    default=forms.BooleanField(required=False)

class AddMealForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    event_datetime=forms.CharField(max_length=50,required=False)
    bestankar_id=forms.IntegerField(required=True)
    bedehkar_id=forms.IntegerField(required=True)

class AddFoodItemForm(AddProductForm):
    pass