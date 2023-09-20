from googletrans import Translator


def translate_to_english(text):
    text_to_str = str(text)
    translator = Translator()
    result = translator.translate(text_to_str, dest='en')
    print(f'Translated text: {result.text} and original text: {text}')
    return result.text


def translate_text_to_text(lang_from, lang_to, text_to_translate):
    translator = Translator()
    result = translator.translate(
        text_to_translate, src=lang_from, dest=lang_to)
    return result.text


languages_list = '''

af : afrikaans
sq : albanian
am : amharic
ar : arabic
hy : armenian
az : azerbaijani
eu : basque
be : belarusian
bn : bengali
bs : bosnian
bg : bulgarian
ca : catalan
ceb : cebuano
ny : chichewa
zh-cn : chinese (simplified)
zh-tw : chinese (traditional)
co : corsican
hr : croatian
cs : czech
da : danish
nl : dutch
en : english
eo : esperanto
et : estonian
tl : filipino
fi : finnish
fr : french
fy : frisian
gl : galician
ka : georgian
de : german
el : greek
gu : gujarati
ht : haitian creole
ha : hausa
haw : hawaiian
iw : hebrew
hi : hindi
hmn : hmong
hu : hungarian
is : icelandic
ig : igbo
id : indonesian
ga : irish
it : italian
ja : japanese
jw : javanese
kn : kannada
kk : kazakh
km : khmer
ko : korean
ku : kurdish (kurmanji)
ky : kyrgyz
lo : lao
la : latin
lv : latvian
lt : lithuanian
lb : luxembourgish
mk : macedonian
mg : malagasy
ms : malay
ml : malayalam
mt : maltese
mi : maori
mr : marathi
mn : mongolian
my : myanmar (burmese)
ne : nepali
no : norwegian
ps : pashto
fa : persian
pl : polish
pt : portuguese
pa : punjabi
ro : romanian
ru : russian
sm : samoan
gd : scots gaelic
sr : serbian
st : sesotho
sn : shona
sd : sindhi
si : sinhala
sk : slovak
sl : slovenian
so : somali
es : spanish
su : sundanese
sw : swahili
sv : swedish
tg : tajik
ta : tamil
te : telugu
th : thai
tr : turkish
uk : ukrainian
ur : urdu
uz : uzbek
vi : vietnamese
cy : welsh
xh : xhosa
yi : yiddish
yo : yoruba
zu : zulu
fil : Filipino
he : Hebrew

код : название
Можно использовать код либо целиком название языка.
    '''
