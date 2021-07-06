---
title: "DICOM for Data Scientists With a Life"
date: 2021-03-07T12:57:21+01:00
draft: true
---

Most definitions I found on DICOM where not actionable. Many focus on individual analyses of radiologists. Who owns a CD-ROM Drive? Others where at absurd technical detail. Analyzing pixel input streams anybody?

This quick overview assumes you want to batch analyse DICOM images with either Python or R. Maybe you want to create a model across different images. With the current tools it's easy to do. However, it could be a lot easier to get your head around the different attributes (and especially groups of attributes) of the resulting objects.

## The history of DICOM

DICOM (more specifically it's predecessor ACR-NEMA) where defined in 1985. This is when desktop computers where the latest shit. The original DICOM standard is from 1993 and an update in 2007. 

## DICOM Datasets

What you will find when you download a dataset from e.g. [The Cancer Imaging Archive](cancerimagingarchive.net) is a large collection of Files in a directory structure. Usually you will find data from one or multiple studies in one of these downloads. This is important, because the same patient can paticipate in multiple studies and have scans done in each of them.

There are also publicly accessible [REST Apis](https://wiki.cancerimagingarchive.net/display/Public/TCIA+Programmatic+Interface+REST+API+Guides)  available. For larger analyses or machine learning applications these are a good option.

## DICOM File

A DICOM file looks a little like assembler on first sight. So, it is by all means not directly accessible for developers used to more modern data structures. However, the complexity handled within a fairly limited space is not to underestimate. Like with most attempts focussing too much on efficiency, accessibility is what you trade off with.

## DICOM Groups

This is where it actually becomes interesting. DICOM groups are helpful for analyzing data cross series, patient, or study.The vast array of options in the file is still overwhelming though. For this tutorial we are focussing on timestamps only. So, when was an image shot. We will aggregate that to the level of each patient to derive a duration of a one scan. 

The level of the scan is an interesting unit of analysis, because from there we could chunk up towards one treatment and from there to a series of consecutive treatments. However, if something goes wrong we can either see this in the length of one treatment (too short, too long) or in the repetition of the treatment.
