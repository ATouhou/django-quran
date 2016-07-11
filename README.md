
# Features:
1. Verified arabic text
1. Translations
1. Word meanings
1. Morphological information of words
1. Distinct words
1. All ayas that contains a given word
1. Helper javascript functions
1. Sura, aya, word, page views
1. Management commands, unit tests
1. Transliteration at multiple levels


# Installation:
1. Download and install django-quran (install in the developer mode if you will contribute to the package: `pip install -e /path/to/project`
1. Add `'quran'` to INSTALLED_APPS
1. Add quran urls to your urls.py: `url(r'^quran/', include('quran.urls')),`
1. Migrate: `.\manage.py migrate`
1. Load data `.\manage.py load_all`


# Resources
- Fully verified Quranic text from [Tanzil](http://tanzil.info/wiki/Main_Page)
- Morphological data (including words, roots) from [The Quranic Arabic Corpus](http://quran.uk.net/)
- Translations from [Zekr](http://zekr.org/resources.html)