# Please let's deploy!

**Date:** 2024-09-05 16:00

**Please let's deploy to production**

I just can't get through it. The team has implemented new functionality. It is a simple screen that shows data. The data is retrieved by calling a newly instantiated REST service. This is a first step. It's not enough to call it an MVP; it will not be used by the business. Still, I suggest deploying it to the production environment. In two months, the REST service will be made available to another customer; this solution is *viable for this customer.* The image is persistent, 'We are most vulnerable just after a deployment, so we must limit the number of deployments. We are not going to deploy'.

**Better performance thanks to research**

DevOps Research Assessment (DORA) is a large and long-term research program that, among other things, tries to understand how software delivery can best be organized. DORA helps teams apply this. This should lead to better performance [1]. DORA was once started by a small group of leading people in the world of DevOps and has now been acquired by Google.

DORA defines four metrics that indicate the maturity of the IT organization in terms of DevOps. The first one mentioned is 'frequency of deployments'. When explaining why this is important, this is explained from the risk perspective. Smaller deployments are easier to manage. Any incidents that arise after deployment can be resolved more quickly.

**The Lead Time concept**

DORA uses the concept *Lead Time*. *Lead Time* is the time between the moment a developer commits to creating a piece of software until the moment it is usable in the production environment. *Lead Time* is about being able to deliver quickly*.* Delivering quickly is an important concept in the world of Project Management. How often do you hear a Project Manager say the word *deadline*? But Lead Time is not the only thing that matters in managing an organization. Goldratt [2] models the manager's environment with a model in which two worlds live in tension with each other; the *world of costs* and the *world of delivery*.



**Inventory costs**



Suppose the figure above shows a chain of steps in which steel is processed. Due to variances in lead times, inventory cannot be avoided. Suppose that in step four, Murphy has appeared, then stock C will increase. Inventories lead to costs that must be controlled. See here the tension between fast delivery and cost control.

**Inventory costs for software?**

Now the reader will note that this example concerns the production of steel. This is different from the production of software where the storage of extra versions in the version management system is nil; there are no physical stocks. Suppose the chain represents the production of software. In step 4 the acceptance test is performed. If an error is discovered in step 4 of performing the acceptance test, in a piece of software that is edited somewhere in step 3, the developer has no choice but to branch and merge later. If the error can be traced back to the functional design, the designer can also start branching and merging. What's the problem with 'branch and merge'?

* It takes time; it takes up scarce resources.
* It reduces focus; it distracts from what the developer prefers to do, realizing features (in addition to researching new things and polishing the code).
* It is error-prone; Everyone has experienced it, 'hey, that error we fixed last month is back (but now in production)'.
* It leads to additional complexity in the management of the environments.
* It's tedious work.

**Limit supplies, deploy!**

Suppose you have to decide whether or not to deploy and the situation is as follows

* working software is on the shelf,
* which cannot be released now, but later
* that has no negative impact on the current production environment and
* Google concludes that *deployment frequency* is an important performance factor

then you actually no longer need arguments to convince you to deploy the software.

**And how has that deployment ended?**

Relevant to the story is that it was the first time we hosted something on the container platform. A process designer ultimately convinced management to deploy because he wanted to see whether the authorizations would work on this new platform. And…it turned out not to work. After analysis, it was resolved after two days. This error did not cause any disruption in the production environment because the '*green-on-black-screen*' was still running. Subsequent deployments on this platform went smoothly, partly thanks to the lessons learned.

sources:

1 <https://www.atlassian.com/devops/frameworks/dora-metrics>

2 Critical Chain, Eliyahu Goldratt, 1997.