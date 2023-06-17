

# send email function
def send_reset_email(user):
    """This functions sends a reset password link to user email
    parameter:
         user: user object
    """
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}

IF you did not make this request then simply ignore it and no changes will be made
'''
    mail.send(msg)
