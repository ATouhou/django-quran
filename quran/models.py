from django.core.urlresolvers import reverse
from django.db import models
from django.utils.safestring import mark_safe
from quran.buckwalter import *


class QuranicToken(models.Model):
    # text fields will hold sura name in Sura and quran text in Word, Segment, Lemma and Root
    ttext = models.TextField(blank=True, null=True, db_index=True)  # transliterated/ascii text
    utext = models.TextField(blank=True, null=True, db_index=True)  # unicode

    class Meta:
        abstract = True

    @property  # to access from templates
    def key(self):  # to be overridden below
        return ""  # will be 1.1.1.1 for sura:1 aya:1 word:1 segment:1

    @property
    def str(self):
        if self.ttext:
            return self.ttext
        else:
            return get_buckwalter(self.utext)

    @property
    def unicode(self):
        if self.utext:
            return self.utext
        else:
            return get_unicode(self.ttext)

    @property
    def text(self):  # quranic tokens want to be displayed in arabic
        return self.unicode

    def __str__(self):
        return self.str

    def __unicode__(self):
        return self.unicode


SURA_TYPES = (
    ('Meccan', 'Meccan'),
    ('Medinan', 'Medinan'),
)


class Sura(QuranicToken):
    """Sura (chapter) of the Quran"""
    etext = models.TextField(blank=True, null=True, db_index=True)  # english name
    number = models.IntegerField(primary_key=True, verbose_name='Sura Number')
    order = models.IntegerField(verbose_name='Revelation Order')
    type = models.CharField(max_length=7, choices=SURA_TYPES, verbose_name='')
    rukus = models.IntegerField(verbose_name='Number of Rukus')
    aya_count = models.IntegerField()

    class Meta:
        ordering = ['number']

    def get_absolute_url(self):
        return reverse('quran_sura', args=[str(self.number)])

    @property  # for backward compatibility - may be removed when not needed
    def name(self):
        return self.utext

    @property
    def key(self):
        return str(self.number)


class Aya(QuranicToken):
    """Aya (verse) of the Quran"""

    number = models.IntegerField(verbose_name='Aya Number')
    sura = models.ForeignKey(Sura, related_name='ayas', db_index=True)
    bismillah = models.CharField(max_length=50, blank=True, verbose_name='Bismillah')

    class Meta:
        unique_together = ('number', 'sura')
        ordering = ['sura', 'number']

    @staticmethod
    def end_marker():
        return mark_safe('&#64831;&#1633;&#64830;')

    def get_absolute_url(self):
        return reverse('quran_aya', args=[str(self.sura_id), str(self.number)])

    @property
    def key(self):
        return self.sura.key + '.' + str(self.number)


class TranslationModel(models.Model):
    """ parent class of below Translation and AyaTranslation"""
    class Meta:
        abstract=True

    @property
    def text(self):
        return self.ttext

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.text


class Translation(TranslationModel):
    """Metadata relating to a translation of the Quran"""
    ttext = models.CharField(blank=False, max_length=50)
    translator = models.CharField(blank=False, max_length=50)
    source_name = models.CharField(blank=False, max_length=50)
    source_url = models.URLField(blank=False)


class AyaTranslation(TranslationModel):
    """Translation of an aya"""
    sura = models.ForeignKey(Sura, related_name='translations', db_index=True)
    aya = models.ForeignKey(Aya, related_name='translations', db_index=True)
    translation = models.ForeignKey(Translation, db_index=True)
    ttext = models.TextField(blank=False)

    class Meta:
        unique_together = ('aya', 'translation')
        ordering = ['aya']


class Word(QuranicToken):
    """Arabic word in the Quran"""
    sura = models.ForeignKey(Sura, related_name='words', db_index=True)
    aya = models.ForeignKey(Aya, related_name='words', db_index=True)
    number = models.IntegerField()
    lemma = models.ForeignKey('Lemma', related_name='words', null=True, blank=True)

    class Meta:
        unique_together = ('aya', 'number')
        ordering = ['number']

    def get_absolute_url(self):
        return reverse('quran_word', args=[str(self.sura_id), str(self.aya.number), str(self.number)])

    @property
    def key(self):
        return self.aya.key + '.' + str(self.number)


class WordSegment(models.Model):
    """ for the ManyToMany relationship btw Words and Segments """
    word = models.ForeignKey(Word, related_name='word_segments')
    segment = models.ForeignKey('Segment', related_name='word_segments')
    number = models.IntegerField()
    type = models.CharField(max_length=10)  # prefix, stem, suffix


class Segment(QuranicToken):
    """
    Morphological Segment(s) of a Word
    Segments are unique, so there are multiple segments in a word as well as multiple words that a segment go into
    """
    words = models.ManyToManyField(Word, related_name='segments', through=WordSegment)
    lemma = models.ForeignKey('Lemma', related_name='segments', db_index=True, null=True, blank=True)
    pos = models.ForeignKey('Pos', db_index=True, null=True, blank=True)
    mood = models.ForeignKey('Mood', db_index=True, null=True, blank=True)
    gender = models.ForeignKey('Gender', db_index=True, null=True, blank=True)
    form = models.ForeignKey('Form', db_index=True, null=True, blank=True)
    special = models.ForeignKey('Special', db_index=True, null=True, blank=True)
    case = models.ForeignKey('Case', db_index=True, null=True, blank=True)
    definite = models.ForeignKey('Definite', db_index=True, null=True, blank=True)
    tense = models.ForeignKey('Tense', db_index=True, null=True, blank=True)
    participle = models.ForeignKey('Participle', db_index=True, null=True, blank=True)
    other = models.ForeignKey('Other', db_index=True, null=True, blank=True)  # mostly for prefix and suffixes

    class Meta:
        ordering = ['ttext']


class Lemma(QuranicToken):
    """
    Distinct Arabic word (lemma) in the Quran
    homonyms: same spelling but different meanings, e.g., EaSaA عصا could mean both 'wand' and 'to rebel'.
    it  seems like to work around some uniqueness constraint they just put a 2 to the end of second such item
    in such cases we put a 2 in meaning field below, otherwise None; actual meanings maybe put here later on
    """
    root = models.ForeignKey('Root', null=True, related_name='lemmas', db_index=True)
    meaning = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['ttext']

    def get_absolute_url(self):
        return reverse('quran_lemma', args=[self.id])


class Root(QuranicToken):
    """ Root word """

    def get_absolute_url(self):
        return reverse('quran_root', args=[self.id])


class SegmentFeature(models.Model):
    """ abstract class to derive generic tables """
    ttext = models.CharField(max_length=10, primary_key=True)
    long_name = models.CharField(max_length=50)

    @property  # to access from templates
    def str(self):
        return self.ttext

    @property  # to access from templates
    def unicode(self):
        return self.long_name + '(' + self.ttext + ')'

    @property
    def text(self):  # morphological features shown in latin
        return self.str

    def __str__(self):
        return self.str

    def __unicode__(self):
        return self.unicode

    class Meta:
        abstract = True


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
