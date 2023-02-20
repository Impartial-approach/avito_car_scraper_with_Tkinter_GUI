from setuptools import setup

setup(
    name='avito_car_scraper',
    version='0.1',
    packages=['avito_car_scraper'],
    install_requires=[
        'numpy',
        'pandas',
        'tkinter',
        'requests',
        'pyfiglet'
    ],
    entry_points={
        'console_scripts': [
            'avito_car_scraper=avito_car_scraper.__main__:main'
        ]
    }
)
