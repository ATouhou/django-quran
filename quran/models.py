from django.db import models
from django.utils.safestring import mark_safe
from quran.buckwalter import *


class QuranicToken(models.Model):
    class Meta:
        abstract = True

    def id_str(self): # to be overridden below
        return ""

    def __str__(self):
        return self.id_str() + ' ' + get_buckwalter(self.text)

    def __unicode__(self):
        return self.id_str() + ' ' + self.text


SURA_TYPES = (
    ('Meccan', 'Meccan'),
    ('Medinan', 'Medinan'),
)


class Sura(QuranicToken):
    """Sura (chapter) of the Quran"""
    number = models.IntegerField(primary_key=True, verbose_name='Sura Number')
    name = models.CharField(max_length=50, verbose_name='Sura Name')
    name_english = models.CharField(max_length=50, verbose_name='English Name')
    order = models.IntegerField(verbose_name='Revelation Order')
    type = models.CharField(max_length=7, choices=SURA_TYPES, verbose_name='')
    rukus = models.IntegerField(verbose_name='Number of Rukus')
    bismillah = models.CharField(max_length=50, blank=True, verbose_name='Bismillah')
    aya_count = models.IntegerField()

    class Meta:
        ordering = ['number']

    @models.permalink
    def get_absolute_url(self):
        return 'quran_sura', [str(self.number)]

    @property # allows extending QuranicToken
    def text(self):
        return self.name

    def id_str(self):
        return str(self.number)



class Aya(QuranicToken):
    """Aya (verse) of the Quran"""

    number = models.IntegerField(verbose_name='Aya Number')
    sura = models.ForeignKey(Sura, related_name='ayas', db_index=True)
    text = models.TextField(blank=False) # unicode arabic

    class Meta:
        unique_together = ('number', 'sura')
        ordering = ['sura', 'number']

    def end_marker(self):
        return mark_safe('&#64831;&#1633;&#64830;')

    @models.permalink
    def get_absolute_url(self):
        return 'quran_aya', [str(self.sura_id), str(self.number)]

    def id_str(self):
        return self.sura.id_str() + '.' + str(self.number)


class Translation(models.Model):
    """Metadata relating to a translation of the Quran"""
    name = models.CharField(blank=False, max_length=50)
    translator = models.CharField(blank=False, max_length=50)
    source_name = models.CharField(blank=False, max_length=50)
    source_url = models.URLField(blank=False)

    def __unicode__(self):
        return self.name


class AyaTranslation(models.Model):
    """Translation of an aya"""
    sura = models.ForeignKey(Sura, related_name='translations', db_index=True)
    aya = models.ForeignKey(Aya, related_name='translations', db_index=True)
    translation = models.ForeignKey(Translation, db_index=True)
    text = models.TextField(blank=False)

    class Meta:
        unique_together = ('aya', 'translation')
        ordering = ['aya']

    def __str__(self):
        return self.text


class Word(QuranicToken):
    """Arabic word in the Quran"""

    sura = models.ForeignKey(Sura, related_name='words', db_index=True)
    aya = models.ForeignKey(Aya, related_name='words', db_index=True)
    number = models.IntegerField()
    text = models.CharField(max_length=50, db_index=True)

    class Meta:
        unique_together = ('aya', 'number')
        ordering = ['number']

    @models.permalink
    def get_absolute_url(self):
        return 'quran_word', [str(self.sura_id), str(self.aya.number), str(self.number)]

    def id_str(self):
        return self.aya.id_str() + '.' + str(self.number)


class WordSegment(models.Model):
    """ for the ManyToMany relationship btw Words and Segments """
    word = models.ForeignKey(Word)
    segment = models.ForeignKey('Segment')
    number = models.IntegerField()
    type = models.CharField(max_length=10) # prefix, stem, suffix


class QuranicSubToken(models.Model):
    """ for segment, lemma, and root: have text in ascii instead of unicode """
    class Meta:
        abstract = True

    def __str__(self):
        return self.text

    def __unicode__(self):
        return get_unicode(self.text)


class Segment(QuranicSubToken):
    """
    Morphological Segment(s) of a Word
    Segments are unique, so there are multiple segments in a word as well as multiple words that a segment go into
    """
    text = models.CharField(max_length=50) # cant be pk because there could be same text with different attributes
    words = models.ManyToManyField(Word, through=WordSegment)
    lemma = models.ForeignKey('Lemma', db_index=True, null=True, blank=True)
    pos = models.ForeignKey('Pos', db_index=True, null=True, blank=True)
    mood = models.ForeignKey('Mood', db_index=True, null=True, blank=True)
    gender = models.ForeignKey('Gender', db_index=True, null=True, blank=True)
    form = models.ForeignKey('Form', db_index=True, null=True, blank=True)
    special = models.ForeignKey('Special', db_index=True, null=True, blank=True)
    case = models.ForeignKey('Case', db_index=True, null=True, blank=True)
    definite = models.ForeignKey('Definite', db_index=True, null=True, blank=True)
    tense = models.ForeignKey('Tense', db_index=True, null=True, blank=True)
    participle = models.ForeignKey('Participle', db_index=True, null=True, blank=True)
    other = models.ForeignKey('Other', db_index=True, null=True, blank=True) # mostly for prefix and suffixes

    class Meta:
        ordering = ['text']

    @models.permalink
    def get_absolute_url(self):
        return 'quran_segment', [str(self.pk)] # todo


class Lemma(QuranicSubToken):
    """ Distinct Arabic word (lemma) in the Quran """
    text = models.CharField(max_length=50, primary_key=True) # unicode arabic
    root = models.ForeignKey('Root', null=True, related_name='lemmas', db_index=True)

    class Meta:
        ordering = ['text']

    @models.permalink
    def get_absolute_url(self):
        return 'quran_lemma', [str(self.pk)]


class Root(QuranicSubToken):
    """ Root word """
    text = models.CharField(max_length=10, primary_key=True) # to my knowledge, there is no root with more than 7 letters -idris

    @models.permalink
    def get_absolute_url(self):
        return 'quran_root', [str(self.pk)]


class SegmentFeature(QuranicToken):
    """ abstract class to derive generic tables """
    short_name = models.CharField(max_length=10, primary_key=True)
    long_name = models.CharField(max_length=50)

    def __str__(self):
        return self.long_name + '(' + self.short_name + ')'

    def __unicode__(self):
        return self.__str__()

    class Meta:
        abstract=True


class Pos(SegmentFeature):
    pass

class Mood(SegmentFeature):
    pass

class Gender(SegmentFeature):
    pass

class Form(SegmentFeature):
    pass

class Special(SegmentFeature):
    pass

class Case(SegmentFeature):
    pass

class Definite(SegmentFeature):
    pass

class Tense(SegmentFeature):
    pass

class Participle(SegmentFeature):
    pass

class Other(SegmentFeature):
    category = models.CharField(max_length=50, null=True, blank=True)
    pass

