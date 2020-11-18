
import uuid
import vobject

from datetime import datetime, timedelta 

from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from email.mime.text import MIMEText

# -----------------------------------------------------------------------------
# Append invitation links 
# -----------------------------------------------------------------------------
def invitation_links(invite):
    links = ''
    invitation = invite['invitation'] + '<hr>'
    for link in invite['course_invites']:
        links = links + '<br><br>' + link
    invite['invitation'] = invitation + links
    return invite

# -----------------------------------------------------------------------------
# Sends email webinar registration (HTML)
# -----------------------------------------------------------------------------
def send_registration_email(invite):
    print('DEBUG>>> send_registration_email(): sending email')

    # Site domain setting
    domain = 'https://' + str(Site.objects.get_current())
    context= { 'domain' : domain, 'invite' : invite, 'course_invites' : invite['course_invites'] }
 
    # Set email parameters
    subject    = 'Link to Singapore Polytechnic Open House Info Session'
#    from_email = 'sp-webinar@onedash22.com.au'
    from_email = 'sp-webinar@spoh21registration.com'
    to_email   = [ invite['email'] ]

    text_content = invite['invitation']
    html_content = render_to_string('email_invite.html', context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email )
    msg.attach_alternative(html_content, "text/html")

    # Prepare ICS attachment
    icalstream = create_ics_reminder(invite)
    part = MIMEText(icalstream,'calendar')
    part.add_header('Filename','sp-event-reminder.ics') 
    part.add_header('Content-Disposition','attachment; filename=sp-event-reminder.ics') 

    msg.attach(part)
    msg.send()

# -----------------------------------------------------------------------------
# Sends email webinar registration (PLAIN)
# -----------------------------------------------------------------------------
def send_registration_email_plain(invite):
    print('DEBUG>>> send_registration_email(): sending email')

    # Site domain setting
    domain = 'https://' + str(Site.objects.get_current())
    context= { 'domain' : domain, 'invite' : invite, 'course_invites' : invite['course_invites'] }
 
    # Set email parameters
    subject    = 'Singapore Polytechnic Open House 2021 – Info Session'
    #subject    = 'Singapore Polytechnic Open House 2021 – Info Session (Parents’ Forum)'
#    from_email = 'sp-webinar@onedash22.com.au'
    from_email = 'sp-webinar@spoh21registration.com'
    to_email   = [ invite['email'] ]

    text_content = invite['invitation']
    html_content = render_to_string('email_invite_plain.html', context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email )
    msg.attach_alternative(html_content, "text/html")

    # Prepare ICS attachment
    icalstream = create_ics_reminder(invite)
    part = MIMEText(icalstream,'calendar')
    part.add_header('Filename','sp-event-reminder.ics') 
    part.add_header('Content-Disposition','attachment; filename=sp-event-reminder.ics') 

    msg.attach(part)
    msg.send()

# -----------------------------------------------------------------------------
# Create ics calendar reminder
# -----------------------------------------------------------------------------
def create_ics_reminder(invite):
    print('DEBUG>>> create_ics_reminder(): creating ICS reminder')
    cal = vobject.iCalendar()
    cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this

    vevent = cal.add('vevent')
    vevent.add('dtstart').value     = invite['calendar']['start']
    vevent.add('dtend').value       = invite['calendar']['end']
    vevent.add('summary').value     = invite['tagline']
    vevent.add('organizer').value   = 'info-session@sp.edu.sg'
    vevent.add('description').value = invite['details']
    vevent.add('uid').value         = str(uuid.uuid4())
    vevent.add('dtstamp').value     = datetime.now()

    return cal.serialize()

