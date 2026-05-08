# Laten we alsjeblieft deployen!

**Datum:** 2024-09-05 16:00

**Laten we alsjeblieft deployen naar productie**

Ik kom er maar niet door heen. Het team heeft nieuwe functionaliteit gerealiseerd. Het gaat om een eenvoudig scherm dat gegevens toont. De gegevens worden opgehaald door het aanroepen van een nieuw gerealiseerde REST-service. Dit is een eerste stap. Het is onvoldoende om het een MVP te noemen; het zal niet worden gebruikt door de business. Toch stel ik voor het naar de productie-omgeving te deployen. Over twee maanden zal de REST-service beschikbaar worden gesteld aan een andere klant; deze oplossing is voor deze klant wel *viable.* Het beeld is hardnekkig, ‘Net na een deployment zijn we het meest kwetsbaar, dus het aantal deployments moeten we beperken. We gaan niet deployen’.

**Betere prestaties dankzij onderzoek**

DevOps Research Assessment (DORA) is een groot en langlopend onderzoeksprogramma, dat onder andere probeert te begrijpen hoe softwarelevering het beste kan worden georganiseerd. DORA helpt teams dit toe te passen. Dit moet leiden tot betere prestaties [1]. DORA is ooit gestart door een klein groepje vooraanstaande personen in de wereld van DevOps en inmiddels overgenomen door Google.

DORA definieert vier metrieken die de volwassenheid aangeven van de IT-organisatie in termen van DevOps. Als eerste wordt genoemd ‘frequentie van deployments’. Wanneer wordt toegelicht waarom dit van belang is, wordt dit verklaard vanuit het risico-perspectief. Kleinere deployments zijn makkelijker te beheersen. Eventuele incidenten die ontstaan na de deployment, zijn sneller op te lossen.

**Het concept Lead Time**

DORA hanteert het concept *Lead Time*. *Lead Time* is de tijd tussen het moment dat een ontwikkelaar commitment afgeeft op het maken van een stuk software tot het moment dat het bruikbaar draait in de productie-omgeving. *Lead Time* gaat over snel kunnen leveren*.* Snel leveren is een belangrijk concept in de wereld van Project Management. Hoe vaak hoor je een Project Manager wel niet het woord *deadline* uitspreken? Maar Lead Time is niet het enige waar het om draait in het managen van een organisatie. Goldratt [2] modelleert de omgeving van de manager met een model waarin twee werelden in spanning met elkaar leven; de *wereld van kosten* en de *wereld van leveren*.



**Voorraadkosten**



Stel voor dat in bovenstaande figuur wordt weergegeven een keten van stappen waarin staal wordt bewerkt. Als gevolg van varianties in doorlooptijden, kan niet worden ontkomen aan voorraden. Stel dat in stap vier, Murphy is verschenen, dan loopt voorraad C op. Voorraden leiden tot kosten, die beheerst moeten worden. Zie hier de spanning tussen snel leveren en kosten beheersen.

**Voorraadkosten voor software?**

Nu zal de lezer opmerken dat dit voorbeeld gaat over de productie van staal. Dat is anders dan de productie van software waar de opslag van extra versies in het versiebeheersysteem nihil zijn te noemen; er is geen sprake van fysieke voorraden. Stel voor dat de keten voorstelt de productie van software. In stap 4 wordt de acceptatietest uitgevoerd. Wanneer in stap 4 het uitvoeren van de acceptatietest een fout wordt ontdekt, in een stuk software dat ergens in stap 3 wordt bewerkt, dan rest de ontwikkelaar niks anders dan te branchen en later te mergen. Wanneer de fout is te herleiden tot het functioneel ontwerp, kan ook de ontwerper aan de slag met branchen en mergen. Wat is het probleem met 'branchen en mergen'?

* Het kost tijd; het legt beslag op schaarse resources.
* Het vermindert de focus; het leidt af van wat de ontwikkelaar het liefst doet, features realiseren (naast nieuwe dingen onderzoeken, en de code oppoetsen).
* Het is foutgevoelig; iedereen heeft het wel eens meegemaakt, ‘hé die fout die we vorige maand hebben opgelost, is weer terug (maar nu in productie)’.
* Het leidt tot extra complexiteit in het beheer van de omgevingen.
* Het is vervelend werk.

**Beperk de voorraden, deploy!**

Stel je moet besluiten om wel of niet te deployen en de situatie is de volgende

* werkende software ligt op de plank,
* die niet nu, maar later gereleased kan worden
* die geen negatieve impact heeft op de huidige productie-omgeving en
* Google concludeert dat *deployment-frequentie* een belangrijke prestatiefactor is

dan heb je eigenlijk geen argumenten meer nodig om te overtuigen de software te deployen.

**En hoe is het nu met die deployment afgelopen?**

Relevant voor het verhaal is dat het de eerste keer was dat we iets gingen hosten op het containerplatform. Een procesinrichter heeft uiteindelijk het management overtuigd te deployen omdat hij wilde zien of de autorisaties zouden werken op dit nieuwe platform. En….het bleek niet te werken. Na analyse is het na twee dagen opgelost. Deze fout leidde niet tot een verstoring in de productie-omgeving omdat het ‘*green-on-black-scherm*’ nog draaide. De volgende deployments op dit platform verliepen probleemloos, mede dankzij de geleerde lessen.

bronnen:

1 <https://www.atlassian.com/devops/frameworks/dora-metrics>

2 Critical Chain, Eliyahu Goldratt, 1997.