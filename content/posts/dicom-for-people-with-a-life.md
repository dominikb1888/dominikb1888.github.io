---
title: "DICOM for Data Scientists With a Life"
date: 2021-03-07T12:57:21+01:00
draft: true
---

Most definitions I found on DICOM where not actionable. Many focus on individual analyses of radiologists. Who owns a CD ROM Drive? Others where at absurd technical detail. Analyzing pixel input streams anybody?

This quick overview assumes you  want to batch analye DICOM images with either Python or R. Maybe you want to create a model across different images. With the current tools it's easy to do. However it could be a lot easier to get your head around the different attributes (and especially groups of attributes) of the resulting objects.

## The history of DICOM

DICOM (more specfically it's predecessor ACR-NEMA) where defined in 1985. This is when desktop computers where the latest shit. The original DICOM standard is from 1993 and an update in 2007. 

## DICOM Datasets

What you will find when you download a dataset from e.g. [The Cancer Imaging Archive](cancerimagingarchive.net) is a large collection of Files in a directory structure. Usually you will find data from one or multiple studies in one of these downloads. This is important, because the same patient can paticipate in multiple studies and have scans done in each of them.

There are also publicly accessible [REST Apis available](https://wiki.cancerimagingarchive.net/display/Public/TCIA+Programmatic+Interface+REST+API+Guides). For larger analyses or machine learning applications these are a good option.

## DICOM File

A DICOM file looks a little bit like assembler on first sight. An it is by all means not directly accessible for developers used to more modern data structures. However, the complexity handled within a fairly limited space is not to underestimate. 




## DICOM Groups

This is where it actually becomes interesting. DICOM groups are helpful for analyzing data cross series, patient, or study.