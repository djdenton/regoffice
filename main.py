#!/usr/bin/env python
#
# Daniel Denton 2014

import os
import webapp2
import duedil
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Companies(webapp2.RequestHandler):
    def get(self):
        companies = duedil.get_slides(duedil.get_companies('EC4M 8AB','London'))
        template_values = {'slides': companies}
        template = JINJA_ENVIRONMENT.get_template('templates/slides.html')
        self.response.write(template.render(template_values))
		
app = webapp2.WSGIApplication([
	('/Companies', Companies)
], debug=True)
