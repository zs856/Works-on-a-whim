import dash
import dash_core_components as dcc
import dash_html_components as html


import dash_bootstrap_components as dbc
from datetime import date
import plotly.graph_objects as go

#import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import json
import dash_table
from datetime import date, timedelta


###-----------------  LOADING DATA -------------------------###

today = date.today() - timedelta(days=2)
previous_day = date.today() - timedelta(days=3)

# Month abbreviation, day and year  
today_formatted = today.strftime("%m-%d-%Y")
previous_day_formatted = previous_day.strftime("%m-%d-%Y")

today_formatted_text = today.strftime("%d %b %Y")

# DAILY CASES
df_daily_report = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" + str(today_formatted) + ".csv")
df_daily_report_previous = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" + str(previous_day_formatted) + ".csv")

# COMPUTING CONFIRMED, RECOVERED, ACTIVE, DEATHS CASES AND PERCENTAGE INCREASE/DECREASE
confirmed_world = df_daily_report['Confirmed'].sum()
confimred_world_previous = df_daily_report_previous['Confirmed'].sum()
confirmed_world_today = confirmed_world - confimred_world_previous

recovered_world = df_daily_report['Recovered'].sum()
recovered_world_previous = df_daily_report_previous['Recovered'].sum()
active_world = df_daily_report['Active'].sum()
active_world_previous = df_daily_report_previous['Active'].sum()
active_world_today = round((active_world - active_world_previous),0)

deaths_world = df_daily_report['Deaths'].sum()
deaths_world_previous = df_daily_report_previous['Deaths'].sum()

confirmed_outcome_world = recovered_world + deaths_world
percentage_recovered = round((recovered_world / confirmed_outcome_world)*100,1)
percentage_deaths = round((deaths_world / confirmed_outcome_world)*100,1)


## VACCINATION DATA
df_vacc = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv')
df_vacc_max = df_vacc.groupby(["location"], as_index=False).max()
total_vaccinations_world = df_vacc_max['total_vaccinations']
countries_vacc = df_vacc['location'].unique()


#LOADING COUNTRY CODES
with open('cc3_cn_r.json') as json_file:
    cc3_cn_r = json.load(json_file)



#### GROUPING BY COUNTRIES 


#REARRANGING COLUMNS



# LIST OF COUNTRIES



# TIME SERIES DATA FOR CONFIRMED CASES
df_time_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')


# TIME SERIES DATA FOR RECOVERED CASES
df_time_recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')



## LOADING NEWS ARTICLES

news_articles_list = open("covid_news_articles.csv", "r",encoding='utf-8').readlines()


BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
app = dash.Dash(external_stylesheets=[BS])


############----------------------------------------- INDICATOR -------------------------###############
fig_indicator = go.Figure()
fig_indicator.add_trace(go.Indicator(
    mode='number+delta',
    value=recovered_world,
    title={'text':'Recovered cases'},
    domain={'x':[1,0.5], 'y':[0.8,0.9]},
    title_font_size=25,
    number_font_size = 40,
    delta={'reference':recovered_world_previous}
    ))

fig_indicator.add_trace(go.Indicator(
    mode='number+delta',
    value=confirmed_world,
    title={'text':'confirmed cases'},
    domain={'x':[1,0.5], 'y':[0.4,0.5]},
    delta_increasing_color = '#FF4136',
    title_font_size=25,
    number_font_size = 40,
    delta={'reference':confimred_world_previous}
    ))

fig_indicator.add_trace(go.Indicator(
    mode='number+delta',
    value=deaths_world,
    title={'text':'Total Deaths'},
    domain={'x':[1,0.5], 'y':[0,0.1]},
    delta_increasing_color = '#FF4136',
    title_font_size=25,
    number_font_size = 40,
    delta={'reference':deaths_world_previous}
    ))

#---------------------- CARDS ACTIVE AND OUTCOME CASES----------------------------#



#------------------------------ DROPDOWN COUNTRIES SELECTION ------------------------------------#


#---------------------------- CONFIRMED AND RECOVERED GRAPHS ---------------------------------#


#----------------------- RADIO BUTTON WORLD MAP -------------------------------------------------------#


#-------------------------- WORLD MAP -----------------------------------------#


#------------------------ WORLD MAP 2 ----------------------------------------#



#---------------------------------- TABLE COVID ----------------------------------#



#------------------------------------- VACCINE COUNTRIES DROPDOWN ------------------------------------#


#----------------------------- VACCINE DATA SELECTION -------------------------------------#


#------------------------ NEWS CARDS ----------------------------------------------#




PLOTLY_LOGO = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOIAAADfCAMAAADcKv+WAAABjFBMVEX///8QOFYAntsAjdCAw0LJJSw0nknyZTHOi06ZP5gAmdkAnNoAmtoAKUwAJEkAL1AAH0YALk8AHUUAJkoAM1IAGUMZP1zFzNIAldgAiM719/gAhM3Q1drFAAAAKU3i5umTLZLs7/HLgz61vcWirLaXo67d4eV5wDRoeot2hpUrSmQAFkLw+f3R6vfxWxyGlKFSZ3t1vyvd7/lWteOv2vEnmj+NmqY+WG+ps7zxWRjD4/RhdIbK0NYYlzbHERuQI49IX3U1UWnpzrnftpSd0u5JsOElpt6KyerA4Ke93MLy6PLKgDdPpdl2tuD059zt1sTjwKTZ7Mp4wuj5wbLzelH1+vD3p5Ci0nqy2ZL+7+rN5rr708iUzGJgr27Wam7P5dPosLKSxpvH4cvNO0DYvdjizuLTs9Oxc7DSlmHXonXaqYEACj384dn2mn74sZ70h2WMyFbzbTyd0HL2k3Xuw8TfjZCgzKfLLTTafYB9vIjTXWFKplveiozQT1OhUaDjn6GqZanDl8PJoci5g7l3vd9xAAAdQ0lEQVR4nO1dC3faRhYG7DiNhF4gQJYd2xhsA4ZAAGMCtosTHm3qJA1p2ni7fTdJH2m33W27abtNm+aP72hmJCTNjBAg7DSn3zk9dYQQ8+neua95hUKBIp1pd7IzPSFTzq4H1Jg5QG9WxLiqiu0ZnlGRFUEuNLYDa1SQSLUTa2rYQGJ6MRwkjAeoSuy4qQfYtiCwXlZFxA8glp76OZk4foYqrOVWA2zgrMh0EkrYgtCZ/knphPWiwlKskH05RKlnk6KtXaKYm6VdKUmUrIepglCeXiOCQrosCjZ+Uj4164s/yKs2lkosf74GVi+LyuiVi+1UMI9N5YS4pRiKnDs/knpjRFAK1gbqmU7M9uz8OalrVrFUVI0Hb/7Wy5Klr4rYCPrxPpBJmvYdMDyej+Vrj8yYoDbn8hNsrHfk0c+H1c58fiU/MjvhsHh8piFPw04QQJ6Ll07L+A3i/8Xy8/gVKg6SZieUlCT8fbUyj98pQ4OjJgtml1CUgEz2OORj5mvdzaVDWIxzUCJ9DSloOtS0DJucC/53CKwr2JircsXglYW/rs6SXTDQgE9WoHY2zGhAUecfuR5jEQphrDToXc+QXbCAHryLXGK6HTNVZ+6BQAyL0HJUW/BlS4FrkPu5qTBSH6Uc9C+5Ae2LuD96lTrqJ6Lny9XXVzNN+x2ZbGZ129Obqu5OrudjI82dJ1K7iiA6ahcNxeOX9fXUVn5/LSGL8fjXGetqUhTiopxY289lD+jBWRaaUcnRx1Mq+Kmv598Zt8tbzkbpyH0liKbqqUZHlUVBMp2obIqtYWW+kiCKhVyWbDYuIDgttZ5fO/MoBwL5L2cf0Q8a+wlRYUQIbXvYYvCUxXbWwaYZn5+/nQJpEdlYq2ulm23BTQ9aR/OOLZH4THVWpVBIMZ+oaRqgWFJARlbPVBICQU9VJWV3y/rGcUxQJPdNqhIrbCGblIHvYF6x7xRYR55EBH9u523ZLG74miiqhU6+bBdJKtvIV5KCHHcKG8hy3zBKBXg1dnBOhCjIQTEq+cx+THKwi8fUSrm5yspo9e1Mo6LG4naBqnGpUUYh0/6ZkvDGNjKqkl1BpXj8uJzxk66vZ/IF0S57HCOKZxR0+0PFrZyykstMkievN9trouR8yPHcmjsNMoKtbYqcLE9jClM5QbSrwdwjtUmQStq6kpif2tRDa2w9Sii/HJVigO2ObBFEBnEGpLfCligVYbZRrsBQNlPksJSoBGHmM8dW3UQ8fgmcf0ayqhxyLqjc/8CqfqmJ/Dlrq14xdVTdDbQyv7ovW7n3uQoyE5fMPlgJunqTMgu1auIcTWvOFGE8OQ8vvWWGSkLhnEY1tpO4UCWtbY2/exqk22YlNTajnZ4OTbOzyO35DaqYBZvwGZaJLeRxRUyS5vuCzd8R9s/Ysur7ginCef9yCg9QqeqZjmmsh/HPyn4rKae371y/PfpnsTuol4r+vqpXRPxjZ5h5rOKkSfFl6W5f/+qL1zYB3rpuXqouA6wsL5wMWn54bmFljZ1ZPJdK4OhqfJX/9ttfAm6vYbxlXj5ZXkBYXlnhbtXH0jzA7zR2Rh4yY77TcSO3t2+8NqJnYNNUVW3BBkDzpDuGZbqAs+QzMayZXczQ25Ia/F5zYdP88NbyghPLyyd175+tCGfGEctQFTwjx+tfbLoIGp3RsjdFbmV52U1yYeApyrx4RhwzqB+qYQ9Do7/t0s/NzS9vvH3ntv2eVvfWiQZ42okur9wqefx0A9f55twfV5GWqkl2QKPfsBPc3Pzixp1Txq3FUvdkYWXZTvKkyv5xbFjlOYWLGKiaKBXY/t4uwc3Nr5j0LJS6vI0lIMlW1ywKWePTtd0nIEWVzfC6Q0Xv+HxqsavZJTlk3liG+ZU414lGqa+BDJMshre/cNqY24z7CFSdXmShxbrRsKvSnIuPTSnRYb3EG2+5nMRbPjlWV1w+hK2tlYScnHvyyBQh6Qdfe83fI7UFN5aXWW5y+/zKHG+7RQjtzdt+vlp3CxEK8ta8WzwpvqSIEOALP989cUYB+F/LnM9M5Gxw2xLbV19OrqlOPdVumUJdZlqd+cAr871uinDzeuiGU1P9PNqpoSehlhnzrAwCarwfpI+/VpjZ79uY4eaXp6N/TCBFzqGmJ+B1nqyM65DpfCfgEY8kcPm7DFv2lckQ2pY7Dopf+Xm4I+9Y7hqXuibHE1aDBFUoTEGECThqy5i2ZDI0Hb2doT/HWLJb1BVkZKrcsiVUCuBcACHAgHwbphcCNfzFDDe/MNXmzsh7bPoSokOMK13zIlZWOkc03SERXMEKTe2jhobY0tjJWB5y80u/P2D2PUfnw5Z1mdYfdTSjIzBVbcLniVRzg3zE5g37tTswztn05/cRhssIDhM6QBxXaPkVblNA9So09ZUxB+YGyRDgzo2vblwfm0bZUQQp8q26y0Yio7NC/UIHaVYwVjUPK0MxevB7CrKntyYQ12Sog0yS4TjQxHFlkjmielvdpw7xonlDAqvcdnrjhu+caXK0Tvgu4yM06ThGtzh6iiKRpBJWv6ZJCs43UZNTt3JugNPk6BMBMzFxlyhjpWSGW1iFCiEHMjZT7HYHg2633qoGEWFnUMsoAYn+teFR3MMDUFY05w679YxTtVpDrG31vhaNRjmO0/hetzSrqYC+jGYGUyJFvmi+JeWNrMKeGJshD23VeK1vSW3ARyB4PsrxtfGlfi8gBaO0bTtG8eNornmYfEyFpfB3H/zDRyuKA57j+ciISS0aGYHntJrPhOn0CeVihSVGOBHS1e1o1wyg+XsJ8kU9uLpz9d/j2lUcRqNAalGbUSz2Ig4ACY+p9EO8f+3alfeJq0jFKMtg4OIRZ+yDJCuTBhUVFUkh3r26uLh49a53uwYa0koOk+gCqgsc6Iq8gyQXGUvy9NrFixevkYKEhkIihwBQv3M4FDi7m2JT0jFGF100sOOpqq0IZ5LohUpGZFYc9KvD4aAVGvJuSXrUwA3cuwIoXnyHuJ5CRpW0Wx1CK+EsPcqEM+heKcr+xs7iGCkWa9qIBzfo8aFQr1fDA6Y9O0Ue9kl2edjA+4YUL167R3xwzOhgzTWXpuIeR2YSkDo58/U+ZLj4HrtNpciIBbCdWn9Q43qhen3BkGaLszHs9zmuPxhEeE9BvnMRgrgO9wGgxCXphKvnQXtK0dOUSLez7yEh3me2qGsTId/v1kPFKlKmgVYLde0M+X61BclVB1629QkU45V3iQ/WGD1pX3XqpfvfJtp0Nbh/FfbEN5gNGmo2DjV4qTQohYqR/iDK1zXkF3ngTgwV1Xz5xm9gb7xGXIdWhLJgC9lUy04SUsXQaR4U4D2opovM5tQcYjJ7WbdWqmpat1XlDIK9Ws9w/MViaTSkOPCwOqdX6GJcRwaHuB/1vZhpiJBCkxk0uk54DCxEpjl1MAReETUcmJ9+qFvUQzrHg25Jotjjohp7CPVbxJG4DjUwTobQMEiPm2YEriShxKcV+rdRT/yO1ZahkyFyi8Ve1HAeNYNtqTYkdXPYByFdr8WxOSKK37ovN6FGknNHYJZrkUIug6hbIP8pui9jIbIcxsDNMBIdAAvDIy9fo3wBCpnTjF4LeDJ1lSFG1JvWCNeIqONxunU8XbDtWn+G9JR4P8gnsnpiXXMzhG4D+b8IR1rN0gIUXLXej/ZDQ3APM/9AFAnfSNO1dKqMJuTH9RHfMNwkQ+w0DqyfgMEbqaeLXua0SsjQZBnp8xrILVwcS1qtjktSw2g11GpVeVo/hXiXHuLANXK2IG67mQvL5s4Y2KfbNwhQFVHcx2tk4lQNuAuFuMNoRp9nMKyVWkBSXbcUi61WxIjDqzCtqoEwAIRCjGefohDHHami/rRm/KmnGhVJFmx8FFSPKbhWoBkrncL5DFxcSgZv0GPsPKC3YhhlMIwCdwE+L5E9rdTrV+sRDYQ4kRoPX5DGigH+RfcbMIhTGpl8MkasKET+QE+EKZAEKGoyHoDG5upH1DaUaB3RsDJ8txXR+GIR/Ed8qdbnoTHieStbZlB8/wo1isMLfQVisSC8bNyxigrLgkS5gczF/uHlMfo0giDthQYFajwlkikS7yXKismvUDV1lVzvCXUR/g/ug4Ws6342p7oXExrX3b+C9PSN+3fvkhFqnWZruLpXfF3sV0tRIEWOt3dijfKV0ydPQu/SNdVN0Vi4q7Qb8G/o/KGPhH+tZ8r7omhfoEe6DOQxdq7u7FxddMc3vDbSNT6CPSHTQEKUQCfk+VatHukiYXKQbt99373vrwGgdON794f2ZXeGISnkM4byQQWGPQ1GQFaAqq9utSXRXDNJdEVkTzF2XPoKjCbKBLneoA9cOR+JRmreQTa4n4N6PKiXoOOs1/tGPctlcd7B7CCuuUcSGuaWGIIY32+kzJg6Y3kT+Oma4zvGmkk0ZODOUh7YKS7u/NPdZJgKwkJGFSghTeFc9/M4TC/VWnUuyg1D1dZAi7ic4/cX7SC8fwqtHldB7GJ3cTASN1LEtPmHE8jbxN1e8btFB8gIAIiFN6O0ojaOYagIUqwqikv7Xb5bg4WsIR9xxOMokRrhP9S2Ku5no9AujO0RmXDBqI5Ip+/vLLo4ur/XjUasULro3Q8NMhqQmKb1I0AxW6Fatd7rR0Biwo1eU8h0+Xa4HwOpEME0rlnoSMpk2puiMoeFNzuI8g2wquNlZ8L0FzwS2jDUMqwPDB9sifI9lxDJzgjtjUzktRVsZWB6TEai8LLiZv4GIUW3VS0Ci2gkT6ArDr1nCQMTYxV4+B6uMxZLdRQD2mqv77opEhVVmPqLxLgaDLLB5bJE/RgGrnF3Yeq9sRSBweG0QT0CzH61tew1STjUt9VTDRuKOqJZnhv5DZKiO2mEK5nJbBB5jUwo7/AZFmAhkij7uKwNNW2s1ocaF4V/1vseHGuueLYX1WrGiBW+PNJUQlEJe3Ng9CqFGAGFlUbg96DCrhF6DJ1GzG1Q3UJkVOGGWhSvShjWWJXuLiWe5TkuYiovZ33xCWFu3AkVtI2kyUxh5gXD7EjuT3WJFr7dd1sbVsZRiuLar15iDT5Ro70IP6jxODwa2dR33BSJQhxM3jvuq8hZlPEOYO5PYaWf2DvgLiFFevMNGY0rHdaomSUgpsH/DbiIdSvhNQiTargHsr6GHF8Oxm8KEYqiyMBdfENpxoP3sDB3FpnF4uIC1DM2T7LEg7ugDi1qdNi3vaT3TY7XvvkP/J872YBBqOTuVmk8krqaEASFsDb0gAD6DGBE734HwvAdlpZClKL9QXHQbxEBNQY17zK6YGkA7U3UYapO/3XtypUr176/h4pUhNdAHpCo+hgGJQ4c3/rWFjmYAQMCYjspGKFCI3r3H29QsiknBhrXq3F9unek66lRWS5C+fKRniPAPX3/23uG7KB5JaJU6AHJLZK3JTnRYTUPRumEGYZucYee8ZMAsZyRU3FUQbLqWHwkhD/hqLYYZv6EY4RenLaj4AF7BB/myUQq9W+2nyBRNM0/36fJccgSYwhpqjvbwIAehMiKoZMn0iJvZKkU/zkBxWLU4sBHKBFAlaNzjBZD8N3wdCnSKcKhtTOnaJcSkeIaaPHG7BSCKGfk1caQJD1mgA7kyje05pJRqCe2qFEfoujvCY5iDFmpgKjWS9WeK44Dt/a0fpeVTCMf6Y7gEMXJlhrPTNFZV+MjzBur7lgViNGjWECn2Jya4gyKWnRYzGjdY1KGe3JDrdXqMof+g5Pi7H3RWfrnhi1m0tFzdUcQjGuUESyEJx4UJ+uLdKfx3gQUXWG2MfGEHs7pZMrhUZl84mFuJrOodNf/YBLX7x7B4bUoVZBkNdxrhgpy/VS/OOFmwijVYgdwPkDGL4zBCrdJpTtEjHv06Eah5vWeoFenzDDcH7okxwiNpNPccN7F5W89YtTJJn96JFMek1FcIAcbOZoKOigyPL6Fd9mZBjkY7gmUErsLyLDG6J9iyy1G+shh3aapvPdEMVw2JvJFOMQ44dxutHCB+NJ3O4s7rAFiEkUXxSh9Jrs9r6JMBnDCyI6vEAM3YVqNYhyS1PJU6ME/H/hMNEKEwWFFcXaLGh2rbPe+v/aOu64BS/sT74iLioyzrUlyu0a6EnbtFpVVJPAGnEE98U7UMMmccffOkpMiYwx/YE9JmFGNJ6AXn3hzQ7in9e5sUrSZG4+gzN4VNda6E2/AdXDixOsswoKUmHFTkpGi8v1SlZU+9G3vYcqFtbqghtUJfYbxtXJ+1uUnNooebbeicDw5rDjFIuntpFg4lzPULEPCezl0qy8in9LiuWl+65z2pjRr99GIl2BwNQpVP4qRcdPEzwJvfvKpzzsRw97QO+rE6szDpQxVjRrjWXjyg99mzoAPDvcOf/Z3q+bh8G2AoSyuYA2jnrd/ePnoaO4kPzpcWlo69JcyGoXiaG8sRaOmGEV1yKrmOcnj48sXLlw48tfQ6fHmHqC494mvewc83x/v6EBKrFneoufp+38DDC9cpq2eChJQikt7vu4dUqZBUVAM+drSD3TEy5Cir3t9Yj2XJCeMGwyXDn1ZnD4f9bPkyzd+PDL09EPi+mpz2rWHaVGhnGv6E9TUD/w8oMcz0qcpcQEKkTA35d347pT7NMBaKrEQ/D7U1EM/KVVVmzYio+JjQ4gX/uu+vG3s28ba/2MM8go1fv8AitGX3+izi+BT4DOD4dHv7suw+rY23R4GMH4nZ8chg3PoJ2KqBqmnPyBjQx0KDsvTbcmuwzmQ5Hq4X5f8+40AgYT41H0ZrS4lpgb7BCzdkdPj3nT0xvs//fyz75COhnor1KMPBpz+/vSXD3/EbhALkdjVAk4Om/rsKaSpZNVnySbGnw/3AA6XpiTZ6ve0fqhPdS6/Hx0dXTg6uoy8BBIi6THgnJop9TTEXBw4EuP9pb0lhMOfpvmBGpoNwNPGWD+EYjN4/RYyzSkpRNYSS7/IMxYHIjEC3/irydB33OpAdzRGTGSUv5sMoez0I3pPREVi5gYg44H2BkgQRgyL8VP0fxOTPn3I2WvEC674e8TQCEufIoqEENfhZqYTjmY4wFqN/OsSCbcYW0PPqZrOdSvEWA1STCeOfiQeAvVspjPF8KnkxPWPDkmKe+7eWNdQbFMEQTYcW3QF26MhD14jsuanNIpEO9CpgbPVQuEj4uSWTD/vkRRJTznstYqtnqGPIJmv1l39zahB8lyE46JDMkn8hWRIRqd4Uf5sG9Uwn0GhSLGp1eGCsTYczaPhXIXgohbl+Dpe9OYGKUWKw0DrbKYM3kzglahkufFTQlX33qQ9oDiIjMxmtFezm67SkB3gkX2RtDV48xNhxuob6s+UzcgIVT1kPaJVA7qIaPLRSNfbCJk4vexiSFFTFGHO4DEQ0C4btA3SxnfFEUqDHq8BnsZifo20LTT86BQjxSWiPQYD2EQM7R9GCXOdVnXv1zHPKVbr3WGt1+v3ej1fldJfHBw/I29Abz+AXQtRb6Rpw08jjr7rjpPg6eURSUpHxBt8z9oTDaBjQGm7FY66489TRG/j8eR/n7E7It7Ph75R5IRAnVqiRRA4RJ0mPPUHbFcvE6l+CKfCAW3eho7PpR1Jcn+PHrsFhY8vM01NaAu1KqCDdfCScYrSWxxnyYmZwMkGzefj/RYCOyz1gH2qs2lWD6l+fzY8xQx/o324jw5LDWxQMaewVHXEMfBaDnYadIZITWf2+iPo+Iggmn22OAbrNk4/82KIa1JBbhTZlJlW1eK4txSg0fkBu8SjX6gf4zN9p6sP6ylq8lWBblakOiErzPHRIR89fvbs8edjb/sfjlAv02yp2XGmjGtWRVE+puijjnJjyrZ+IVuR6vAD73GAhxsblwA2Lj30vO3Jf7EMqf7QPDmEvlFxKj/ucC9DAwSa6cRH1kr0gyY+wBz36BkVxqPXL2G87iXIp1bpjT4gjAx8OE6zpuWEInr3UCQs2l7VeFMc1h7Pn1jKyi423rQYAo43mbf9ZnbDz+ibHadh6RNIgqJR8OidMXs0Jxm7oTbMwyTJdYAIVjGOmTaG/rhkw2PWXT+Y3ZDm8A1Ye9dQIpsCa5dXG9DOse70UK/gMzsN/WA84L4ZsLIif7sQgRhZt5lh6ceMzyuK1RTieLQs2m1yTLUKRQ3OXRm2w/aNYphnIEFlZQ+uPtywU9xgWRyY7h/9xtqRO2c/xjpecbQz7S+oQ07VsVd1xjwuE+8twjyQ8KOlw8M9pk393EmRaXB+OLrMFGGojIMQs0WOc26QZxs/wxTvEj4StnmMZVjO41eYYNrlT0fhuP788XOHpLyk+PD5C9u/2VMyyvigqdyxuSWYrUOiTubDW6L0MKxgFbCOy4QnrrbRP/ycgwi8H/CCNpbMvvjwObhzw9OPYGCjZxyJZh2ma3VI7Lr9jDSilyEhy2keJgl6I1SJjuKT4yMkM9D0P/58iOg8Ji2qfvPR440NLN6xLTNlCP121lQus0NiNfVVGcf3Nh3P6eC3XkCWJzaunvBopJaAw7MXf35+03bp0sajm5//+eKZRc8PRXx0n4AjZevtK7BDImsqjT/10kAaSXx3PdQmtCGkmxzHqLxTLSHPDa9/X9p4MaZZubiDIWjKqEOm0LwN/8WqDGZmHq2s7tqcrMlRHHNAwMNnLg6e2HidGQtg4CMmBXu2Y3VIMYf2J/R/QnN75F5hN3SYYR2f2Tn2oOCbz5+97ovlxsYfj9gBHUQav+64UxGz1iHsSGX9n8ug2/dKEzouKvq+QqNOZfnoD7dCEvp76cXnY/iB/AHv3kaozqp9W7eJUuTV0Q5/tJOrcTzn7+Tuh4+gWSH6HjC2l/54Pp4ewBY+flWm7BC+Pwp3JjvqpmEGpfTjXvIy8zfpuPnw8z+fv/jjGeb37PGL548e+mEHoHdwYxJUM56zmjrhIFwHGRWBISfzMGRh/hPrrQO0WTXTMvqclQMxoaOAlJmYmIGrKs/5xGfruHVmz8+pE3dEBLRlc5jJwEo/xM4cj3xMhXFXEyss+40ODw2LU6gTPp6XmX2Zp5MDQc7riFk9ZyY57EgD+w3iDBRfwIkL7WQVhK0YbkA8OZejLZsC9s+SxJwAlpntIF+cO7ETsO2CGUIFeDSZhS3Tc8lMJTW9G7Wi5gv7aJMtid3Zyrt4C8456Cp2TBIzBQcMUalK6Uz9IzoqBankxk2jHynE50VxF4uQfQoxmsA2+RJbO9Io+PM8EXwrJqkKuSHi7DDyb4XlmA3gHXxV2rCgf6RRlUSl1mXNe3LHuXn4Db2trOU9Wn9gnsg+4+tdFzBHn2+qHC7kZzCv2+Xj3OiXdK8fPcBayijQT4B1FOZQ5sHRADJzVZLVxlQGdn0rGVNUwWfPQu3ysoX+fxg+yydFbOcVuVCeUJarjWNZmGDoF4+Eq4F0kbSqhKW4P3WwquaqIsYqzr2DmdBXs21RtjI/n6PbaBvegMxcui1UfL4sMwNBNAVZOM43Vz2aoa8288eKbN/IW/F5+mdzV5AL57G+NquKjm3kVUkQY2v7uUYztbqeThsGRNfT6e2DTLORq6gJcc2xHbsqxNp+m72eDWhGysRI5cS4e7N8VVIEUZQRH1VZk2UxLijuTfeB1AvZOTjYOUDP5NaIMxHGQYrHOlvnsnB9WqTKBZE8EoBFT5DVXOavIT8H0pnycUyknwEx0mBBTIRzzb+U+JwA/iB/HBZhz5NGZI2+KYC+Gd7PZw/+gtIjkV4F9jOfa+Oal5qs5PJbwMS+EuRcQPM+pl2J95cAWsT1Eh4AHBz+pvgq4G+KrwL+pvgq4G+KrwL+pvgq4G+KrwJeSYqpjD3lPSAobqem3lXp5UA6LMfF2Fqy0wYpcCa1io5dVZqpTDPbyFWOw7Icj+/OuLvl+QKtGQmrqioJQjxulljBn4JRY8SFjsTU+5y8BHCfJEvHxJu3vkzIKeMJjp+S/1JjXYgrqqckVVWJzbILyPlDz5YrBckwKkaVUbUgKYoQh1XGduO8RiaChJ7eTmWyjXK+Xal0Op1KpZ3Ll40i4/qZDCz9Hw3Wq80kEMU6AAAAAElFTkSuQmCC"

####################---------------- NAVIGATION BAR --------------------------##
navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("CoronaMeter - COVID-19 CORONAVIRUS PANDEMIC", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="success",
    dark=True,
)


# -------------------------------------- APP LAYOUT ---------------------------------------------------#
app.layout = html.Div(children=[navbar,

    dbc.Row([dbc.Col(html.P('Last updated on: ' + str(today_formatted_text), \
        style={"fontSize":14, 'color':'grey'}),width=10)],justify='center'),
    #INDICATOR
    dbc.Row([dbc.Col(dcc.Graph(figure=fig_indicator),width=10)],justify='center'),
    #ACTIVE & CLOSED CASES CARDS

    html.Br(),
    html.Br(),

    dbc.Row([dbc.Col(html.H5('Case Status by Countries'),width=10)],justify='center'),
    html.Br(),

    #DROPDOWN COUNTRIES

    #RECOVERED AND CONFIRMED CASES GRAPHS

    html.Br(),
    html.Br(),

    dbc.Row([dbc.Col(html.H5('Coronavirus Tracker: Find latest updates!'),\
        width=10)],justify='center'),
    dbc.Row([dbc.Col(html.P("The coronavirus COVID-19 is affecting 219 countries \
        and territories. The day is reset after midnight GMT+0."),width=10)],justify='center'),
    dbc.Row([dbc.Col(html.P("The list of countries and their regional \
        classification is based on the United Nations Geoscheme."),width=10)],justify='center'),
    
    #TABLE

    html.Br(),
    dbc.Row([dbc.Col(html.H5('World Map with Confirmed COVID-19 Cases'),width=10)],justify='center'),
    html.Br(),

    # RADIO BUTTONS
    html.Br(),
    # WORLD GRAPH


   
    html.Br(),
    dbc.Row([dbc.Col(html.H5('Vaccination timeline '),\
                        width=10)],justify='center'),
    dbc.Row([dbc.Col(html.P("Vaccination has started all over the world with countries providing vaccine to their citizens.")\
                        ,width=10)],justify='center'),
    dbc.Row([dbc.Col(html.P("The rollout was done on phase wise basis based on the age and health condition of the people.")\
                        ,width=10)],justify='center'),
    #DROPDOWN VACCINE TIMELINE 
    
    #VACCINE TIMELINE GRAPH
    dbc.Row([dbc.Col(html.H5('Current Vaccination Status for Different Countries'),\
        width=10)],justify='center'),
    
    #RADTIO BUTTON VACCINE
    
    #BAR GRAPH VACCINES
    html.Br(),
    dbc.Row([dbc.Col(html.H5('Find latest updates related to the COVID-19 Pandemic'),\
        width=10)],justify='center'),
    html.Br(),
    #NEWS CARDS

    ]
    )




#------------------------- DEFINING CALL BACKS ------------------------------#


# LINE CHART CONFIRMED 

# LINE CHART RECOVERED

# WORLD GRAPH

# VACCINE TIMELINE

# VACCINATION STATUS



#------------------------------ RUNNING THE SERVER --------------------------------#
app.run_server(debug=True)


