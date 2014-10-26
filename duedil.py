# Daniel Denton 2014

import urllib
import urllib2 # Use requests library outside of AppEngine
import json
import math


#DueDil API URL for searching companies in the sandbox.
DUEDIL_API_URL = "http://duedil.io/v3/sandbox/companies?"
DUEDIL_API_KEY = "kskwdhqw7dcb26tn8hytd87f"


def get_names(companies):
    """Extracts company names from json and returns them in a list."""
    try:
        return [company['name'] for company in companies]   
    except:
        return []


def get_companies(postcode,location):
    """Given a postcode and location returns a list of companies at that address sorted asc.
    
    The DueDil sandbox does not allow filtering by location or postcode so this
    section of the code is commented out.
    """
    try:
        # Build filters
        filters = {}
        # filters['location'] = location
        # filters['postcode'] = postcode
        filters['locale'] = 'uk'
        filters = json.dumps(filters)

        # Build parameters
        parameters = {'fields': 'name', 'limit':'100'}
        parameters['filters'] = filters
        encoded_parameters = urllib.urlencode(parameters)
        
        # Build URL
        url = DUEDIL_API_URL + encoded_parameters

        companies = []
        
        
        while url:
            # Add API key to url. (This is not included in the next_url returned by Due Dil.)
            url = url + '&api_key=' + DUEDIL_API_KEY
            
            # Make request
            request = urllib2.Request(url) #package request
            response = urllib2.urlopen(request) #send request
            data = json.loads(response.read())
            
            # Build list of companies
            companies += get_names(data['response']['data'])

            # Get the URL of the next page of results.
            url = data.get('response',{}).get('pagination',{}).get('next_url','')

            # Caps results returned at 500. Remove in production.
            if len(companies) > 199: url = ''

        return sorted(companies)
    
    except:
        return ['There has been an error returning the list of companies from DueDil']  


def count_lines(company):
    """Returns an estimate of how many lines on screen a company will take up."""
    return int(math.ceil(float(len(company)) / 36))



def get_slides(companies):
    """Splits the list of companies into slides [[Slide1],[Slide2],...] """
    slide = []
    slides = []
    slide_line_count = 1
    breakpoints = [15,29,39]

    try:
        for company in companies:
            
            line_count =  count_lines(company)
            
            # Prevent a long company name being spread across two columns / slides on screen.
            if line_count > 1:              
                for point in breakpoints:
                    if slide_line_count < point and (slide_line_count + line_count) >= point:
                        slide.extend(['']*(point - slide_line_count))
                        slide_line_count = point


            # Starts a new slide every 41 lines.

            if slide_line_count > 38:
                slides.append(slide)
                slide_line_count = 1
                slide = []

            #Add company
            slide.append(company)
            slide_line_count += line_count

        return slides
    except:
        return [[]]

