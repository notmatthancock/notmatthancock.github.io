---
layout: post
title: Wavelet Tour Notes
tags: math 
mathjax: true
published: false
---

A picked up Stephane Mallat's **A Wavelet Tour of Signal Processing** a while ago and have been spending my few off-hours working through it. I bought the 2nd edition because the price was substantially cheaper and the only substantial differences between the 2nd and 3rd editions seemed to be the later topics. Since the errata for this second edition is not available, I intend to use this post to catalog some of the notes I've made reading the text, as well as list some (what I believe to be) small errors.

* [Review](#review)
* [Errors](#errors)
* [Notes](#notes)

### Review

I've only read up to the first 7 chapters, which are the meat of the text. So don't expect any comment on the later chapters.

First, let's talk about the prerequisites. Make no mistake &mdash; this is a math text. This should not be your first introduction to mathematical signal processing. You should be very comfortable with linear algebra and Fourier series and transforms. On the other hand, the text is definitely written from an applied perspective. Essentially, you have the theorem-proof style with many signal processing examples peppered throughout to keep the reader interested / motivated. This is nice because things often do get quite technical.

Chapters 1-3 provide a whirlwind review of Fourier theory moving from continuous to discrete &mdash; from the uncertainty principle to Shannon's sampling theorem and problems of aliasing. These chapters are a delight to read and make the text an excellent reference for these topics alone. 

The rest of the text introduces wavelets in a similar manner to the first three chapters, moving from the continuous to the discrete. Chapter 4 begins with windowed Fourier transforms before introducing the continuous wavelet transform. This chapter builds some of the intuition that's useful for later chapters, hinting at the wavelet as a band-pass filter and introducing the scaling function as a complementary low-pass filter. One gets sense in this chapter (and later ones) that the wavelet literature is vast and perhaps overwhelming. I also began in this chapter to feel as though the text was trying to cover *too* much, and that a "less is more" approach may have proved more effective.

Chapter 5 is an introduction to frame theory and wavelet frames. I would skip this chapter and perhaps return to it later in life if you're interested in an introduction to frame theory from a signal processing perspective. It seemed to me that the only reason this chapter was placed here was that it fit the theme of moving from continuous to discrete, with the overcomplete representations of this chapter lying somewhere on the road form continuous transforms to complete orthonormal expansions.

Chapter 6 is has results on regularity. One nice result relates vanishing moments and derivatives of the scaling function to the continuous wavelet transform. Unfortunately, the latter sections of both chapters 5 and 6 really require you to read chapter 7 first. I would skip directly from chapter 4 to 7, before optionally returning to the preceding two chapters.

Chapter 7 is the ride you bought the ticket for. This chapter introduces orthonormal wavelet bases through the framework of the multiresolution analysis &mdash; topics that the author himself was a main contributor. Unfortunately, this chapter is very slow-going, but I get the impression that it doesn't necessarily need to be depending on if the reader wants to trudge through the many tediously technical proofs or not. I chose to trudge. That the proofs to many theorems are technical and somewhat long seems to be the nature of the topic &mdash; I do not mean to give the impression that the author has some preference for long-winded pedantry. One should keep in mind the end-game, which is building up orthonormal wavelet bases of $L^2(\mathbb{R})$, with many of the results providing the necessary results to lead up to this.

If you're patient, you're finally rewarded with conditions that lead to orthormal wavelet bases. In doing so, one gains insight into the close connection between the scaling function and its associated discrete filter. This, in turn, lays the ground-work for fast transform algorithms where one sees how the convolution with these discrete filters together with the a downsampling decimation operation allow one to quickly compute the coefficients in the wavelet expansion of a signal (with similar operations for fast reconstruction). The rest of the chapter provides variants on all sorts of related methods and applications.

### Errors

### Notes
