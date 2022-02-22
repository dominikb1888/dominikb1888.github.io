---
title: "Refactoring Exercise (1/3) - Step-by-step improving python code"
date: 2022-02-01T08:14:53+02:00
draft: false
---

# Stage 1 - Understand the objectives and making it DRY 

Looking for a good exercise on python code refactoring that is suitable for beginners, I came across this repository: https://github.com/lamchau/refactoring-exercise. Thank you to Lam Chau for making this publicly available!

So, let's get started with reworking this very "elaborate" piece of software craftsmanship ;-)

After cleaning the direct and obvious formal flaws from the code (Indenting according to PEP8 with 4 Spaces and an unused variable: https://www.python.org/dev/peps/pep-0008/), it is about understanding the business objectives of the code and understanding what is a repetition and what is potentially business logic, i.e. unclean, but still intended.

## Business Logic

Just by looking at the code it is hard to understand what it does. We can guess it has something to do with Venture Capital and Financing Rounds. The two main functions are called "where" and "find_by". So, we can assume it is some kind of database that is searchable. But the what, why and how is really obfuscated in many repetitive lines of code. 

## DRYing up on block level 
The code is Class with @staticmethod decorators, this means that we do not need to create an object to access the class methods. 

The first things that spring even to a relatively untrained eye are repeated code blocks:

### Doubled CSV Import

The Import of the CSV is doubled in both the where and find_by functions. This may make sense in combination with the staticmethod class, but overall is weird. We neither bind data to functionality nor functionality to data. Rather we are hiding plain functions in a class, with relatively little reason as they don't share any underlying data structure. The data is imported twice and could come from two completely different sources. Actually this is a misleading use of a class, we could argue.

### Multiple mappings to dictionaries

In both functions we find many mappings of code blocks that can cleaned by extracting them into a separate function and the string literals into lists. Here the first real question arises. What is this code actually trying to achieve? 

We are seeing three steps:
1. Data import
2. Data checking (all columns present?)
3. Data filtering (Prepare Result by add matches to new dictionary)


Here's the intermediate codebase:
{{< gist 5abfff10e1776d7bf2efe1c4ba1fca15 >}}

## Analysis

We went through this code very roughly, without even trying to get any closer to what it intends to do. So these were mainly semantic and structural edits. However, we may even go further. Many areas in the code are still doubled across the two functions or they are very imperative and could be replace by built-ins (Python Built-Ins: https://docs.python.org/3/library/functions.html).

We will go about these things in our next post!
