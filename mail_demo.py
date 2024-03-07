@auth_bp.route('/send_mail_to_a_user', methods=['GET', 'POST'])
def reset_password_request():
    form = PasswordResetForm()

    if form.validate_on_submit():
        msg = Message("Hey", sender='noreply@apogen.com', recipients=[form.email.data])
        msg.body = "Hey how are you doing today. This is Apogen Software Solutions"

        mail.send(msg)
        return "Message sent successfully"

    return render_template('auth/reset_password_request.html', form=form, hide_navbar=True, hide_sidebar=True, hide_footer=True)
