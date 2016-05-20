from django.db import models
from django.utils.safestring import mark_safe
from quran.buckwalter import *


class QuranicToken(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return buckwalter(self.letters)

    def __unicode__(self):
        return ' '.join(str(self.letters))


class Sura(models.Model):
    """Sura (chapter) of the Quran"""

    SURA_TYPES = (
        ('Meccan', 'Meccan'),
        ('Medinan', 'Medinan'),
    )

    number = models.IntegerField(primary_key=True, verbose_name='Sura Number')
    name = models.CharField(max_length=50, verbose_name='Sura Name')
    tname = models.CharField(max_length=50, verbose_name='English Transliterated Name')
    ename = models.CharField(max_length=50, verbose_name='English Name')
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

    def __str__(self):
        return self.tname

    def __unicode__(self):
        return self.name


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


class WordSegment(models.Model):
    """ for the ManyToMany relationship btw Words and Segments """
    word = models.ForeignKey(Word)
    number = models.IntegerField()
    segment = models.ForeignKey('Segment')


class Segment(QuranicToken):
    """
    Morphological Segment(s) of a Word
    Segments are unique, so there are multiple segments in a word as well as multiple words that a segment go into
    """
    words = models.ManyToManyField(Word, through=WordSegment)
    text = models.CharField(max_length=50, db_index=True)
    lemma = models.ForeignKey('Lemma', db_index=True)
    pos = models.ForeignKey('Pos', db_index=True)
    mood = models.ForeignKey('Mood', db_index=True)
    gender = models.ForeignKey('Gender', db_index=True)
    form = models.ForeignKey('Form', db_index=True)
    special = models.ForeignKey('Special', db_index=True)
    case = models.ForeignKey('Case', db_index=True)
    definite = models.ForeignKey('Definite', db_index=True)
    tense = models.ForeignKey('Tense', db_index=True)
    participle = models.ForeignKey('Participle', db_index=True)

    class Meta:
        ordering = ['text']

    @models.permalink
    def get_absolute_url(self):
        return 'quran_segment', [str(self.id)] # todo


class Lemma(QuranicToken):
    """ Distinct Arabic word (lemma) in the Quran """
    text = models.CharField(max_length=50, unique=True, db_index=True) # unicode arabic
    root = models.ForeignKey('Root', null=True, related_name='lemmas', db_index=True)

    class Meta:
        ordering = ['text']

    @models.permalink
    def get_absolute_url(self):
        return 'quran_lemma', [str(self.id)]


class Root(QuranicToken):
    """ Root word """
    text = models.CharField(max_length=10, unique=True, db_index=True) # to my knowledge, there is no root with more than 7 letters -idris

    @models.permalink
    def get_absolute_url(self):
        return 'quran_root', [str(self.id)]


class SegmentPart(QuranicToken):
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=50)

    def __str__(self):
        return self.long_name + '(' + self.short_name + ')'

    class Meta:
        abstract=True


class Pos(SegmentPart):
    pass

class Mood(SegmentPart):
    pass

class Gender(SegmentPart):
    pass

class Form(SegmentPart):
    pass

class Special(SegmentPart):
    pass

class Case(SegmentPart):
    pass

class Definite(SegmentPart):
    pass

class Tense(SegmentPart):
    pass

class Participle(SegmentPart):
    pass




