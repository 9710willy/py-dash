# Flask imports
from flask import Blueprint, render_template, url_for, current_app
# Import db model from models file
from .models import Data
# Import db instance of our app
from .. import db
import json
import requests
import urllib.request as request

# Dash Blueprint Creation
dash_bp = Blueprint('dash_bp', __name__,
    template_folder='templates',
    static_folder='static/dash')

country_codes = {
"Afghanistan" 	:"AF",
"Albania"	:"AL", 
"Algeria"	:"DZ", 
"American Samoa" 	:"AS", 
"Andorra" 	:"AD", 
"Angola" 	:"AO", 
"Anguilla" 	:"AI", 
"Antarctica" 	:"AQ", 
"Antigua and Barbuda"	:"AG", 
"Argentina"	:"AR", 
"Armenia" 	:"AM", 
"Aruba" 	:"AW", 
"Australia" 	:"AU", 
"Austria"	:"AT", 
"Azerbaijan" 	:"AZ", 
"Bahamas" 	:"BS", 
"Bahrain" 	:"BH", 
"Bangladesh":"BD", 
"Barbados" 	:"BB", 
"Belarus" 	:"BY", 
"Belgium" 	:"BE", 
"Belize" 	:"BZ", 
"Benin" 	:"BJ", 
"Bermuda" 	:"BM", 
"Bhutan" 	:"BT", 
"Bolivia": 	"BO", 
"Bonaire Sint Eustatius and Saba": 	"BQ", 
"Bosnia and Herzegovina": 	"BA", 
"Botswana": 	"BW", 
"Bouvet Island": 	"BV", 
"Brazil": 	"BR", 
"British Indian Ocean Territory (the)": 	"IO", 
"Brunei Darussalam": 	"BN", 
"Bulgaria": 	"BG", 
"Burkina Faso": 	"BF", 
"Burundi": 	"BI", 
"Cabo Verde": 	"CV", 
"Cambodia": 	"KH", 
"Cameroon": 	"CM", 
"Canada": 	"CA", 
"Cayman Islands (the)": 	"KY", 
"Central African Republic (the)": 	"CF", 
"Chad": 	"TD", 
"Chile": 	"CL", 
"China": 	"CN", 
"Christmas Island": 	"CX", 
"Cocos (Keeling) Islands (the)": 	"CC", 
"Colombia": 	"CO", 
"Comoros (the)": 	"KM", 
"Congo (the Democratic Republic of the)": 	"CD",
"Congo (the)": 	"CG",
"Cook Islands (the)": 	"CK",
"Costa Rica": 	"CR",
"Croatia": 	"HR",
"Cuba": 	"CU",
"Curaçao": 	"CW",
"Cyprus": 	"CY",
"Czechia": 	"CZ",
"Côte d'Ivoire": 	"CI",
"Denmark": 	"DK",
"Djibouti": 	"DJ",
"Dominica": 	"DM",
"Dominican Republic (the)": 	"DO",
"Ecuador": 	"EC",
"Egypt": 	"EG",
"El Salvador": 	"SV",
"Equatorial Guinea": 	"GQ",
"Eritrea": 	"ER",
"Estonia": 	"EE",
"Eswatini": 	"SZ",
"Ethiopia": 	"ET",
"Falkland": 	"FK",
"Faroe": "FO",
"Fiji": 	"FJ",
"Finland": 	"FI",
"France": 	"FR", 
"French Guiana": 	"GF", 
"French Polynesia": 	"PF", 
"French": 	"TF", 
"Gabon" :	"GA", 
"Gambia (the)" :	"GM", 
"Georgia" :	"GE", 
"Germany" :	"DE", 
"Ghana" :	"GH", 
"Gibraltar" :	"GI", 
"Greece" :	"GR", 
"Greenland" :	"GL", 
"Grenada" :	"GD", 
"Guadeloupe" :	"GP", 
"Guam" :	"GU",
"Guatemala" :	"GT",
"Guernsey" :	"GG", 
"Guinea" :	"GN", 
"Guinea-Bissau" :	"GW", 
"Guyana" :	"GY", 
"Haiti" :	"HT", 
"Heard Island and McDonald Islands" :	"HM", 
"Holy See (the)" :	"VA", 
"Honduras" :	"HN", 
"Hong Kong" :	"HK", 
"Hungary" :	"HU", 
"Iceland" :	"IS", 
"India" :	"IN", 	
"Indonesia" :	"ID", 
"Iran (Islamic Republic of)" :	"IR", 
"Iraq" :	"IQ", 
"Ireland" :	"IE", 
"Isle of Man" :	"IM", 
"Israel" :	"IL", 
"Italy" :	"IT", 
"Jamaica" :	"JM", 
"Japan" :	"JP", 
"Jersey" :	"JE", 
"Jordan" :	"JO", 
"Kazakhstan" :	"KZ", 
"Kenya" :	"KE", 
"Kiribati" :	"KI", 
"Korea (the Democratic People's Republic of)" :	"KP", 
"Korea (the Republic of)" :	"KR", 
"Kuwait" :	"KW", 
"Kyrgyzstan" :	"KG", 
"Lao People's Democratic Republic (the)" :	"LA", 
"Latvia" :	"LV", 
"Lebanon" :	"LB", 
"Lesotho" :	"LS", 
"Liberia" :	"LR", 
"Libya" :	"LY", 
"Liechtenstein" :	"LI",
"Lithuania" :	"LT", 
"Luxembourg" :	"LU", 
"Macao" :	"MO", 
"Malaysia" :	"MY", 
"Maldives" :	"MV", 
"Mali" :	"ML", 
"Malta" :	"MT", 
"Marshall Islands (the)" :	"MH", 
"Martinique" :	"MQ", 
"Mauritania" :	"MR", 
"Mauritius" :	"MU", 
"Mayotte" :	"YT", 
"Mexico" :	"MX", 
"Micronesia (Federated States of)" :	"FM", 
"Moldova (the Republic of)" :	"MD", 
"Monaco" :	"MC", 
"Mongolia" :	"MN", 
"Montenegro" :	"ME", 
"Montserrat" :	"MS", 
"Morocco" :	"MA", 
"Mozambique" :	"MZ", 
"Myanmar" :	"MM", 
"Namibia" :	"NA", 
"Nauru" :	"NR", 
"Nepal" :	"NP", 
"Netherlands" :	"NL", 
"New Caledonia" :	"NC", 
"New Zealand" :	"NZ", 
"Nicaragua" :	"NI", 
"Niger (the)" :	"NE", 
"Nigeria" :	"NG", 
"Niue" :	"NU", 
"Norfolk Island" :	"NF", 
"Northern Mariana Islands" :	"MP",
"Norway" :	"NO", 
"Oman" :	"OM", 
"Pakistan" :	"PK", 
"Palau" :	"PW",
"Palestine" :	"PS", 
"Panama" :	"PA", 
"Papua New Guinea" :	"PG", 
"Paraguay" :	"PY", 
"Peru" :	"PE", 
"Philippines" :	"PH", 
"Pitcairn" :	"PN", 
"Poland" :	"PL", 
"Portugal" :	"PT", 
"Puerto Rico "	:"PR", 
"Qatar" :	"QA", 
"Republic of North Macedonia" :	"MK", 	
"Romania" :	"RO", 
"Russian Federation (the)" :	"RU", 
"Rwanda" :	"RW", 
"Réunion" :	"RE", 
"Saint Barthélemy" :	"BL", 
"Saint Helena, Ascension and Tristan da Cunha" :	"SH", 
"Saint Kitts and Nevis" :	"KN", 
"Saint Lucia" :	"LC", 
"Saint Martin" :	"MF", 
"Saint Pierre and Miquelon" :	"PM", 
"Saint Vincent and the Grenadines" :	"VC", 
"Samoa" :	"WS", 
"San Marino" :	"SM", 	
"Sao Tome and Principe" :	"ST", 	
"Saudi Arabia" :	"SA", 
"Senegal" :	"SN", 
"Serbia" :	"RS", 
"Seychelles" :	"SC", 
"Sierra Leone" :	"SL", 
"Singapore" :	"SG", 
"Sint Maarten (Dutch part)" :	"SX", 
"Slovakia" :	"SK", 	
"Slovenia" :	"SI", 	
"Solomon Islands" :	"SB", 	
"Somalia" :	"SO", 	
"South Africa" :	"ZA", 	
"South Georgia and the South Sandwich Islands" :	"GS", 	
"South Sudan" :	"SS", 	
"Spain" :	"ES", 	
"Sri Lanka" :	"LK", 	
"Sudan (the)" :	"SD", 	
"Suriname" :	"SR", 	
"Svalbard and Jan Mayen" :	"SJ", 	
"Sweden" :	"SE", 	
"Switzerland" :	"CH", 	
"Syrian Arab Republic" :	"SY", 	
"Taiwan" :	"TW", 	
"Tajikistan" :	"TJ", 	
"Tanzania" :	"TZ", 	
"Thailand" :	"TH", 	
"Timor-Leste" :	"TL", 	
"Togo" :	"TG", 	
"Tokelau" :	"TK", 	
"Tonga" :	"TO", 	
"Trinidad and Tobago" :	"TT", 	
"Tunisia" :	"TN", 	
"Turkey" :	"TR", 	
"Turkmenistan" :	"TM", 	
"Turks and Caicos Islands (the)" :	"TC", 	
"Tuvalu" :	"TV", 	
"Uganda" :	"UG", 	
"Ukraine" :	"UA", 	
"United Arab Emirates (the)" :	"AE", 	
"United Kingdom of Great Britain and Northern Ireland" :	"GB", 	
"United States Minor Outlying Islands" :	"UM", 	
"United States of America" :	"US", 	
"Uruguay" :	"UY", 	
"Uzbekistan" :	"UZ", 	
"Vanuatu" :	"VU", 	
"Venezuela" :	"VE", 	
"Viet Nam" :	"VN", 	
"Virgin Islands (British)" :	"VG", 	
"Virgin Islands (U.S.)" :	"VI", 	
"Wallis and Futuna" :	"WF", 	
"Western Sahara" :	"EH", 	
"Yemen" :	"YE", 	
"Zambia" :	"ZM", 	
"Zimbabwe" :	"ZW", 	
"Åland Islands" :	"AX"
}

# Dash Blueprint Routes
@dash_bp.route('/')
def index():
    # Covid all/summary Urls
    getUrlAll = "https://api.covid19api.com/all"
    getUrlSum = "https://api.covid19api.com/summary"

    # response_all = requests.get(getUrlAll)
    response_sum = requests.get(getUrlSum)
   
    # all_data = json.loads(response_all.text)
    sum_data = json.loads(response_sum.text)

    # return html template to browser with covid summary data
    return render_template('dash/dash.html', data = sum_data, cc = country_codes)