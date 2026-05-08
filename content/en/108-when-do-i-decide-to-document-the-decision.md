# When do I decide to document the decision?

**Date:** 2024-07-04 09:05

My favorite book on architecture is 'Software Architect Elevator' by Gregor Hohpe. His special view on architectural issues, combined with a healthy dose of German humor, made me buy and read the book. While I often quickly work my way through the foreword, this was not the case for the foreword in this book, written by an experienced Chief Architect of the Boston Consulting Group. *I believe that architects make two things that are of vital importance and in short supply: they make sense and they make* *decisions**. Whenever architects help their organizations understand a world that is increasingly difficult to grasp, figure out what* *decisions* *need to be taken, and help take those decisions in a rational way at the right time, then they have had a good day at the office.*

That is very often the word *decisions.* The fact that Hohpe shares his image is evident from his website consisting of one page with Gregor's law displayed on it: '*Excessive complexity is nature's punishment for organizations that are unable to make decisions.*'

Armed with this knowledge that I can well substantiate, I propose to my team to enrich our architecture repository with a decision log. In this logbook we would neatly record the decisions with costs and benefits. "But Hans, isn't that very bureaucratic?" And they have a point, after all, an architect continuously records his decisions by writing documents with strategies, including entities in a conceptual data model (or not), and establishing a standard. When do we opt for an Architectural Decision Record (ADR), and do we explicitly record the decision?

Then continue looking for more evidence. A Google search for 'ADR decision' will yield an endless array of good content on this subject. When is it important to make a record?



1. it is a significant decision ('the quotation system is hosted in the Cloud');
2. has an impact on multiple stakeholders ('if I have to explain it again in a year, I will be able to find it quickly')

But when is a decision significant and how many stakeholders is enough to call it several? I suggest, if in doubt, do it, because then

1. History is recorded (if the decision does not turn out well, we can judge whether the decision was not good or whether we were unlucky);
2. it is easier to convince auditors (they are very fond of documented decision-making processes);
3. and that also applies to managers;
4. do your fellow architects, developers and designers a favor because they usually don't like reading; a summary of the decisions makes it a lot easier for them.

Finally, my last example based on an experience. A lead developer suggested using a certain framework. This would then be applied by all teams. I was convinced and promised to record the ADR. It turned out to be difficult to express the benefits properly, so I asked him to describe the benefits. A day later I received an email from him, 'Hi Hans, I don't think we should do it after all.' He was also unable to specifically list the benefits.

An ADR helps to increase the quality of the decision!

So, record your decisions with an ADR. The costs are often lower than the benefits.

Sources:

* Software Architect Elevator, Gregor Hohpe, 2020.
* https://www.bcg.com/about/people/experts/david-knott
* https://architectelevator.com/gregors-law/
* <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
* <https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-michael-nygard/index.md>