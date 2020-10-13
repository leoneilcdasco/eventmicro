
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

# -----------------------------------------------------------------------------
# Sends email webinar registration 
# -----------------------------------------------------------------------------
def send_registration_email(invite):

    #Site domain setting
    domain = 'https://' + str(Site.objects.get_current())
    context= { 'domain' : domain, 'invite' : invite }
 
    #Set email parameters
    subject    = '[Singapore Polytechnic] Thank you for registering to our Webinar!'
    from_email = 'sp-webinar@onedash22.com.au'
    to_email   = [ invite['email'] ]

    text_content = invite['invitation']
    html_content = render_to_string('email_invite.html', context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
