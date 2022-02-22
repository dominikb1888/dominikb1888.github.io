---
title: "Refactoring Exercise (3/3) - Abstraction an Types are fun!"
date: 2022-02-01T08:15:53+02:00
draft: false
---


# From chaos to code - Embeding Type Checking, Exensibility, and Security

In our previous posts we went through a horrible piece of code and cleaned it (DRY principle) and create a stronger OOP logic. In itself the code is good and clean. Still it has substantial flaws, if we look at it from the outside. What happens, if we would like to employ a different search strategy but a union search on all options? What if the CSV contains malicious code that may infect our system? How can we make sure we sanitize and track user input? How will this behave with large datasets? What about Error Handling? Lot's of questions...

One thing changes now. For each change we will also need to change the test suite we operate on. We include new logic that is not within the existing frame of reference.

## Type Checking - May you be safe

Currently our functions do not employ any type of type checking. Python offers in the Standard library since 3.5. So we may as well add the typing module to our file and annotate our functions. This is good practice as it enhances comprehensibility of our code and increases unintended side effects. Let's look at the new code and the tests:


{{< gist dominikb1888 4db7ccdaa01c8aea0954c29a07dcadcd >}}
