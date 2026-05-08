# Post-deterministische IT

**Datum:** 2026-01-04 09:27

## Dertig Jaar IT: Kennis en Onwetendheid

Ik werk inmiddels dertig jaar in de IT. Ik heb zo ongeveer alle gangbare opleidingen en stromingen voorbij zien komen: van ITIL tot SAFe for Architects, van SQL tot systeemarchitectuur. Maar een berg aan kennis gaat inmiddels vergezeld met een zee aan onwetendheid. Voor mijn ogen verschuift een paradigma. Ik merk dat ik me ineens in een andere wereld bevind, waarvoor nog nauwelijks boeken of artikelen bestaan die houvast bieden. Waar ik tegenwoordig mijn vrije uurtjes aan besteed? Het bouwen van een agent-ecosysteem.

## "De Computer Heeft Altijd Gelijk"

Tijdens mijn eerste lessen informatica zei een docent: "De computer heeft altijd gelijk." Die uitspraak is me altijd bijgebleven. Ze hielp bij het analyseren en oplossen van talloze problemen. Toch lijkt de computer soms een eigen wil te hebben en we spreken van *hij* om dat aan te duiden. We kennen allemaal dit soort uitspraken:

- Hij is traag vandaag *-* Ik heb hem opnieuw opgestart, maar hij blijft kuren vertonen
- Gisteren werkte hij nog prima

Dat soort gedrag blijkt vrijwel altijd terug te voeren op slordigheid: verkeerde initialisatie, incomplete foutafhandeling, impliciete aannames. Ik noem dat **onbedoeld non-determinisme**, in gewoon Nederlands: een bug.

## De Paradigmawisseling

Sinds ik met agents werk, zie ik een paradigmawisseling ontstaan. Niet primair omdat we sneller werken, al maak ik tegenwoordig een conceptueel datamodel in een halve dag waar we eerder maanden voor nodig hadden en dan ook met een beter resultaat op veel punten (niet alle).

De echte verschuiving zit ergens anders. We bouwen steeds vaker systemen die **interpreteren** in plaats van **uitvoeren**. Systemen die betekenis afleiden, intenties wegen en context meenemen.

Dat zal niet snel gebeuren in applicaties voor internetbankieren of het berekenen van energiefacturen. Daar blijft determinisme essentieel.

Maar wél in software die:

- Klantvragen beantwoordt
- Dossiers analyseert
- Hypotheekaanvragen beoordeelt

## Het Fundament Verschuift

Jarenlang was ons uitgangspunt helder:

*code + regels + data = voorspelbaar gedrag*

Dat fundament schuift.
Niet omdat developers slordiger zijn geworden.
Niet omdat testen tekortschieten.
Maar omdat **interpretatie** een expliciet onderdeel van onze systemen wordt.

## Nieuwe Architectuurvragen

De tegenhanger van deterministische software is probabilistische software. Architectuur zal steeds minder gaan over alles vastleggen en steeds meer over waar onzekerheid mag bestaan, en waar niet.

Mijn overtuiging: de komende jaren wordt het **bewust plaatsen van probabiliteit** een belangrijke vaardigheid voor architecten.
Niet alles wat kan probabiliseren, mag dat ook.
Maar doen alsof alles deterministisch blijft, is geen optie meer.

## Taal Geven aan Verandering

Wat hier op architecten afkomt, is nieuw. Ik heb dit niet uit een boek, artikel of gezien in een webinar. Ik zie het voor mijn ogen gebeuren. Deze post is een eerste, voorzichtige poging om taal te geven aan die verandering, zodat we erover kunnen spreken met de stakeholders met wie we strategische keuzes maken.

https://www.linkedin.com/pulse/post-deterministic-why-architects-need-embrace-systems-hans-blok-ii4ae
