---
date: 2026-09-18
topic: "Services and APIs"
description: "Architects aim for a Ubiquitous Language, yet call services all sorts of things. Four categories as a shared language."
---

# Which type of service do we actually mean?

Within a domain we aim for a Ubiquitous Language: the idea from Domain-Driven Design that everyone uses the same words for the same concepts. We do not always apply that discipline to our own professional vocabulary. Do architects speak the same language when they talk about services?

In architecture diagrams I come across names such as data service, business service, API service, process service, integration service and technical service. A name like that usually says something about the technology or about the position in the landscape, and little about the responsibility. On top of that, different concepts get mixed up. An API is the contract through which you call a service, not a kind of service. Two architects can agree on the same diagram and still have something different in mind.

A limited, explicit classification of service types moves that conversation forward. The SOA literature offers one that has been around for twenty years: the service models described by Thomas Erl. Not a formal standard and not part of DDD, but a useful starting point, because the categories are about functional responsibility rather than technology.

Start with the **Entity Service**. It follows directly from the domain model: it is organised around a recognisable business entity such as Case, Document or Person, and it manages and exposes the data of that entity. Such a service certainly contains logic, but that logic stays within the functional context of the entity. Register case, for example, runs through a sequence of steps. This is what makes the service business process-agnostic, and why the same Entity Service can be reused by the social assistance process, the permit process and the objection process.

Not all logic fits into such a context. As soon as a piece of processing spans multiple entity domains, it no longer belongs to any one of those entities. Calculate entitlement to social assistance combines data about Person, Income and Case, performs calculations and validates the result, which makes it a parent task. For that we create a **Task Service**: its functional boundary is defined by the task rather than by an entity. Such a service has less reuse potential than an Entity Service, and it typically acts as the controller of a composition of more process-agnostic services.

A particular variant of this is the **Orchestrated Task Service**. That is a Task Service whose underlying process is hosted as a process definition in an orchestration platform, for example Handle social assistance application. Functionally it is the same idea: a task that directs other services. The design characteristics differ because of that technology, which is why it gets a label of its own. You will also encounter it as a process service or an orchestration service, which shows how quickly the confusion of terms arises.

Outside the domain, finally, sits the **Utility Service**: functionality that does not derive from the business domain, such as sending notifications, logging or converting to PDF. Reusable across the entire landscape, but you will not find that logic in a business model or a case type.

There is room to play with the names, and the literature does exactly that. The same four models each carry a handful of alternative labels:

| Service type | Also known as |
|---|---|
| Entity Service | entity-centric business service, business entity service |
| Task Service | task-centric business service, business process service |
| Orchestrated Task Service | process service, business process service, orchestration service |
| Utility Service | application service, infrastructure service, technology service |

Look at business process service: that term appears in two rows at once. Anyone using it without saying what they mean leaves it open whether this is a task or a process hosted in an orchestration platform. That is precisely where the confusion this article is about begins. Which label you pick matters less than picking one and recording what you mean by it.

These four do not all sit at the same level, and that is not sloppiness. Entity and Task are two ways of setting the functional boundary of a service: around an entity or around a task. Orchestrated Task is an implementation variant of Task. Utility stands apart because the logic originates outside the domain. Name that, and the borderline cases stay a conversation about the design. Is Schedule appointment a task or an entity? That question is then about the responsibility of the service, not about the classification.

Does a classification from the SOA era remain useful? For the purpose I describe here, it does. The underlying question, which responsibility belongs to this service, has not changed since we started talking about microservices and APIs. What an organisation adopts from it is its own choice: four categories, three, or a classification of its own that fits the domain better.

More important than which limited classification we choose is that we explicitly agree what our service types mean, and record that where architects can find it. Better naming does not start with inventing yet another service type, but with jointly establishing what we mean by the ones we already have.

Sources: [Concept: The Concept of Service Layers](https://docs.jboss.org/savara/methodology/1.0-M1/jboss_soa_plugin/guidances/concepts/concept_service_layers_742015EF.html) (SAVARA/JBoss) and [Service Models](https://patterns.arcitura.com/soa-patterns/basics/soamethodology/entity_services) (Arcitura Patterns), both based on Thomas Erl.
