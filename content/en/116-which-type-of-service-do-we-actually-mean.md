# Which type of service do we actually mean?

**Date:** 2026-09-18

Within a domain we aim for a Ubiquitous Language: the idea from Domain-Driven Design that everyone uses the same words for the same concepts. We do not always apply that discipline to our own professional vocabulary. Do architects speak the same language when they talk about services?

In architecture diagrams I come across names such as data service, business service, API service, process service, integration service and technical service. A name like that usually says something about the technology or about the position in the landscape, and little about the responsibility. On top of that, different concepts get mixed up. An API is the contract through which you call a service, not a kind of service. Two architects can agree on the same diagram and still have something different in mind.

A limited, explicit classification of service types moves that conversation forward. The SOA literature offers one that has been around for twenty years: the service layers described by Thomas Erl. Not as a formal standard, and it is not part of DDD either. But it is a useful starting point, because the four categories are about responsibility rather than technology.

An **Orchestration Service** adds a parent level of abstraction. It determines the sequence in which other services are called and holds the scenario-specific logic of the process, so that the underlying services do not need to know about it. Think of Handle social assistance application.

An **Entity Service** is organised around a recognisable business entity: Case, Document or Person. It manages and exposes the data of that entity and is business process-agnostic. That is precisely why the same Entity Service can be reused by the social assistance process, the permit process and the objection process.

A **Task Service** contains the business logic of one specific task, for example Calculate entitlement to social assistance or Calculate fees. That is something other than orchestration: a Task Service performs that one task, whereas an Orchestration Service directs multiple steps and services in concert. Whoever confuses the two ends up building process sequence into a task without noticing.

A **Utility Service** offers functionality that does not derive from the business domain: sending notifications, logging, converting to PDF. Reusable across the entire landscape, but you will not find that logic in a business model or a case type.

One nuance applies when you use this classification. The four are presented as layers in which every service has exactly one place, but the criteria behind them differ. Orchestration is about composition and sits above the rest. Entity and Task are two ways of delimiting the responsibility of business logic: around an entity or around a task. Utility stands apart because the logic originates outside the domain. That is not a problem, as long as you name it. If you do not, the first borderline cases — is Schedule appointment a task or an entity? — will be about the classification instead of about the design.

Does a classification from the SOA era remain useful? For the purpose I describe here, it does. The underlying question, which responsibility belongs to this service, has not changed since we started talking about microservices and APIs. What an organisation adopts from it is its own choice: four categories, three, or a classification of its own that fits the domain better.

More important than which limited classification we choose is that we explicitly agree what our service types mean, and record that where architects can find it. Better naming does not start with inventing yet another service type, but with jointly establishing what we mean by the ones we already have.

Source: [Concept: The Concept of Service Layers](https://docs.jboss.org/savara/methodology/1.0-M1/jboss_soa_plugin/guidances/concepts/concept_service_layers_742015EF.html) (SAVARA/JBoss), based on Thomas Erl.
