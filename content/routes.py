from flask import (Flask, Blueprint, render_template, current_app,
                    redirect, request, url_for, flash, session)
                    

content = Blueprint('content', __name__)


@content.route('/howitworks')
def howitworks():
    return render_template('howitworks.html')

@content.route('/contact')
def contact():
    return render_template('contact.html')
