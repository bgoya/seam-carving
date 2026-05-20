# Seam Carving Image Resizing

![Demo](assets/drawing.png)

Academic project focused on content-aware image resizing using Seam Carving algorithms implemented in C++ and Python.

The project explores brute force, backtracking and dynamic programming approaches to efficiently identify and remove low-energy seams from images.

## Overview

Seam carving is a content-aware image resizing technique that removes low-energy paths of pixels from an image while preserving its most relevant visual content.

This project focuses on reducing PNG images by iteratively identifying and removing seams using different algorithmic strategies.

## Algorithmic Approaches

The project compares multiple strategies for solving the seam selection problem:

- Brute Force
- Backtracking
- Dynamic Programming

This comparison allowed us to analyze trade-offs between correctness, efficiency and scalability across increasingly optimized approaches.

## How It Works

1. Compute the image energy map
2. Identify the minimum-energy seam
3. Remove the seam from the image
4. Repeat the process iteratively until reaching the desired width

## Technologies

- C++
- Python
- PNG image processing
- Dynamic Programming
- Backtracking
- Brute Force algorithms

## What I Learned

Through this project I gained experience in:

- Dynamic programming optimization techniques
- Algorithmic complexity analysis
- Recursive problem solving
- Image processing workflows
- Translating theoretical algorithms into practical systems

## Academic Context

Academic project developed for an Algorithms Design course at Universidad Torcuato Di Tella.

## Technical Report

A detailed report describing the implementation process, algorithmic decisions and complexity analysis can be found in:

[`docs/report.pdf`](docs/report.pdf)
