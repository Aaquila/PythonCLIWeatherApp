# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 12:23:27 2023

@author: Aaqui
"""

'''To use in command line use: python3 WeatherCommandLineApp.py'''
import requests


class WeatherApp():
    '''Class to create the command line App to check current weather in a city and maintain 3 favorites.
    '''
    def __init__(self):
        '''Constructor with default parameters necessary.
        '''
        self.__url = "http://api.openweathermap.org/data/2.5/weather?"
        self.__favs = {}
        self.__apiKey = "68cd03d22e5b9c5f9fc8a4d29b977869"
        self.__terms = {'temp': {'disp':'Temperature','unit':'K'},
                        'feels_like':{'disp':' Feels like','unit':'K'},
                        'temp_min': {'disp':'   Min temp','unit':'K'},
                        'temp_max': {'disp':'   Max temp','unit':'K'},
                        'pressure': {'disp':'   Pressure','unit':'hPa'},
                        'humidity': {'disp':'   Humidity','unit':'%'},
                        'description': {'disp':'Description','unit':''}}
        self.options = {0:'Check current weather in a city',
                        1: 'Display Favorites',
                        2: 'Add a city to Favorites',
                        3: 'Update (remove and add) Favorites',
                        4: 'Display Menu',
                        5: 'Close App'}
        
        self.__displayInitial()
        self.displayOptions()        
                    
    def __displayInitial(self):
        '''Message to display when starting the App.'''
        print('-----------------------------------------------------')
        print('\t\tWelcome to Weather App!!')
        print('-----------------------------------------------------')
        
    def displayOptions(self):
        '''Displays options Menu stored in self.options.'''
        print('\n############  Menu  ###############')
        for i in self.options:
            print('    ',i,' : ',self.options[i])
        print('###################################')
    
    def enterOption(self):
        '''Prompts user to enter Menu option number.       
        Returns
        -------
        option : int
            Input given by user.
        '''
        option = int(input('\nEnter option number:'))
        if option not in self.options:
            print('Invalid option entered. Try again.')
        return option
        
    def setAPIKey(self,api_key):
        '''To set a new api key to use with OpenWeather API.       
        Parameters
        ----------
        api_key : str
        '''
        self.__apiKey = api_key
    
    def checkWeather(self):
        '''Prompts input city and displays weather details.
        '''
        city = input("\nEnter City Name: ")
        print('-------------------------------')
        data = self.__getWeatherDetails(city)
        if data:
            self.__displayWeather(data, city)
        print('-------------------------------\n')
           
        
    def __getWeatherDetails(self,city):
        '''Gets the weather details from OpenWeather API       
        Parameters
        ----------
        city : str 
            Input city name to get weather details.           
        Returns
        -------
        data : dict
            Obtained dictionary of weather details with necessary keys: temp, feels_like, temp_min, temp_max,
            pressure, humidity, description.
        '''
        new_url = self.__url + "appid=" + self.__apiKey + "&q=" + city
        response = requests.get(new_url)
        out = response.json()
        
        if out["cod"] == "404":
            print("Unknown City! Try another City!!")
        else:
            data = {}
            for key in self.__terms:
                if key !='description':
                    data[key] = out['main'][key]
            data['description'] = out['weather'][0]['description'] 
            return data
        
    def __displayWeather(self, data, city):
        '''Prints weather in specific format.
        Parameters
        ----------
        data : dict
            Dictionary with weather details obtained from getWeatherDetails
        city : str
        '''
        print("  Current weather in ",city)
        for key in data:
            print('\t',self.__terms[key]['disp'],' : ', data[key],self.__terms[key]['unit'])
    
    def addToFavorites(self,city=None):
        '''Add a city to favorites.
        Parameters
        ----------
        city : str, optional
            If not given, prompts from user. The default is None.
        '''
        if city is None:
            city = input('Enter city to add to Favorites: ')
        if city in self.__favs:
            print(city, ' is already in Favorites')
        elif len(self.__favs) == 3:
            print('Favorites already has 3 cities.')
        else:
            data = self.__getWeatherDetails(city)
            if data:
                self.__favs[city] = data
                print(city, ' added to Favorites')
        
    def displayFavorites(self):
        '''Prints current favorite cities and its weather details.
        '''
        print('\n###########  Favorites  ###########')
        if not self.__favs:
            print('  Favorites empty')
        for city in self.__favs:
            self.__displayWeather(self.__favs[city], city)
            print('----------------------------')
        print('###################################\n')
            
    def updateFavorites(self,cityToAdd=None,cityToRemove=None):
        '''Method to update favorites by removing a current city and adding a new one.        
        Parameters
        ----------
        cityToAdd : str, optional
            City to add to favorites. If not given, user can enter the input. The default is None.
        cityToRemove : str, optional
            City to remove from favorites. If not given, user can enter the input. The default is None.
        '''
        if not self.__favs:
            print('  Favorites empty, cannot delete')
        if cityToRemove is None:
            cityToRemove = input('Enter city to remove from Favorites: ')
        if cityToRemove not in self.__favs:
            print(cityToRemove,' not in Favorites')
        else:
            del self.__favs[cityToRemove]
            print(cityToRemove, ' removed from Favorites')
        self.addToFavorites(cityToAdd)
    
    def __delete__(self):
        '''Destructor for the class, displays exit message.        
        '''
        print('\n-----------------------------------------------------')
        print('\t\tClosing Weather App!!')
        print('-----------------------------------------------------\n')
    
    

if __name__ == '__main__':   
    app = WeatherApp()
    
    '''Run the command line app in loop till closed.'''
    while 1:
        option = app.enterOption()
        if option == 0:
            app.checkWeather()
        elif option == 1:
            app.displayFavorites()
        elif option == 2:
            app.addToFavorites()
        elif option == 3:
            app.updateFavorites()
        elif option == 4:
            app.displayOptions()
        elif option == 5:
            app.__delete__()
            break
    
                
 

        
        