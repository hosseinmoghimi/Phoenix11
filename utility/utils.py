from .models import LinkHelper,ImageHelper,DateTimeHelper,DateHelper
def str_to_html(value):
    html=""
    lines=value.splitlines()
    for line in lines:
        html=html+line+"<br>"
    return html
def fixed_length(lenn,vall):
    if len(vall)<lenn:
        vall=(lenn-len(vall))*'0'+str(vall)
    return vall