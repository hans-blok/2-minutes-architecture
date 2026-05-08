# Wanneer besluit ik het besluit te documenteren?

**Datum:** 2024-07-04 09:05

Mijn favoriete boek over architectuur is 'Software Architect Elevator' van Gregor Hohpe. Zijn bijzondere kijk op architectuurvraagstukken, gecombineerd met een gezonde dosis Duitse humor, deed mij het boek kopen en lezen. Waar ik me vaak snel door het voorwoord heen werk, gold dit niet voor het voorwoord in dit boek, geschreven door een ervaren Chief Architect van de Boston Consulting Group. *I believe that architects make two thing that are of vital importance and in short supply: they make sense and they make* *decisions**. Whenever architects help their organizations understand a world that is increasingly difficult to grasp, figure out what* *decisions* *need to be taken, and help take those decisions in a rational way at the right time, then they have had a good day at the office.*

Dat is dus heel vaak het woord *decisions.* Dat Hohpe zijn beeld deelt, blijkt uit zijn website bestaande uit één pagina met daarop weergegeven Gregor’s law: '*Excessive complexity is nature’s punishment for organizations that are unable to make decisions.*'

Gewapend met deze kennis die ik goed kan onderbouwen, stel ik mijn team voor om onze architectuur repository te verrijken met een besluiten-logboek. In dit logboek zouden we netjes de besluiten vastleggen met kosten en baten. ‘Maar Hans, is dat niet heel erg bureaucratisch?' En ze hebben een punt, een architect legt immers continue zijn besluiten vast door documenten te schrijven met strategieën, entiteiten op te nemen in een conceptueel datamodel (of juist niet), een standaard vast te leggen. Wanneer kiezen we voor een Architectural Decision Record (ADR), en leggen we het besluit expliciet vast?

Dan maar weer verder zoeken naar meer onderbouwing. Een zoekopdracht in Google met 'ADR decision' levert een eindeloze reeks van goede content over dit onderwerp. Wanneer is het belangrijk om een record vast te leggen?



1. het gaat om een significant besluit ('het offertesysteem wordt gehost in de Cloud');
2. heeft impact op meerdere stakeholders ('wanneer ik het over een jaar nog eens moet uitleggen, dan kan ik het snel vinden' )

Maar wanneer is een besluit significant en hoeveel stakeholders is voldoende om te spreken van meerdere? Ik stel voor, bij twijfel doen, want dan

1. wordt de geschiedenis vastgelegd (wanneer het besluit niet goed uitpakt, kunnen we beoordelen of het besluit niet goed was, of dat we pech hebben gehad);
2. overtuig je makkelijker auditers (zij zijn erg gecharmeerd van gedocumenteerde besluitvormingsprocessen);
3. en dat geldt ook voor managers;
4. doe je je collega-architecten, developers en ontwerpers een plezier omdat ze meestal niet houden van lezen; een samenvatting van de besluiten maakt het een stuk makkelijker voor hen.

Tenslotte mijn laatste voorbeeld aan de hand van een ervaring. Een lead developer stelde voor een bepaald framework in te zetten. Dit zou dan door alle teams worden toegepast. Ik was overtuigd en beloofde het ADR vast te leggen. Het bleek lastig om de baten goed te verwoorden en dus vroeg ik hem de baten te beschrijven. Een dag later ontving ik een mail van hem, ' Hoi Hans, Ik denk dat we het toch maar niet moeten doen.' Het lukte hem ook niet om concreet de baten op te sommen.

Een ADR helpt om de kwaliteit van het besluit te verhogen!

Dus, leg je besluiten vast met een ADR. De kosten zijn vaak lager dan de baten.

Bronnen:

* Software Architect Elevator, Gregor Hohpe, 2020.
* https://www.bcg.com/about/people/experts/david-knott
* https://architectelevator.com/gregors-law/
* <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
* <https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-michael-nygard/index.md>