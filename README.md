
# Installation:
1. Download and install django-quran (install in the developer mode if you will contribute to the package: `python install.py develop`
2. Add `'quran'` to INSTALLED_APPS
3. Add quran urls to your urls.py: `url(r'^quran/', include('quran.urls')),`
3. Make migrations: `.\manage.py makemigrations quran` 
4. Migrate: `.\manage.py migrate`
4. Load data `.\manage.py quran_loaddata`


# Resources
- Fully verified Quranic text from [Tanzil](http://tanzil.info/wiki/Main_Page)
- Morphological data (including words, roots) from [The Quranic Arabic Corpus](http://quran.uk.net/)
- Translations from [Zekr](http://zekr.org/resources.html)