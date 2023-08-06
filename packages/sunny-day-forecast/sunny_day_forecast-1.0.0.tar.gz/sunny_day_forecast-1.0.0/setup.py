from setuptools import setup
 
setup(  
    name='sunny_day_forecast',        #Your package will have this name
    packages = ['sunny_day_forecast'], #Name the package again
    version="1.0.0",         #To be increased anytime you change your library
    license = 'MIT',
    description= 'Weather forecast data',
    author="Okodi Ataime",  
    author_email="ataimeokodi@gmail.com",
    keywords= ['weather', 'forecast', 'openweather', 'sunny_day'],
    install_requires = ['requests',] ,
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    )