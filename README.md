# Full-stack homework

## Overview

This is a homework assignment for a full-stack engineer position at Aiven.

The homework assignment is the most important part of our assessment when selecting candidates to interview. Please pay attention that your solution demonstrates your skills and experience in developing production-quality code.

Use **React** with **TypeScript** on the front end and **Python** on the back end for the assignment. Other than this, you have the freedom to select tools and libraries.

Provide instructions on how to run the project. The project should not need root permissions to run.

Your code will only be used for candidate assessment, and will not be shared or used outside of the review process.

## The assignment

An Aiven customer can launch a service in any of the clouds supported by Aiven's data platform.

Your task is to create a web application for cloud selection. The implementation details are up to you, but the user should be able to:

* Filter clouds by the cloud provider (e.g. Amazon Web Services or Google Cloud Platform).
* Sort clouds by their distance from the user. The distance comparison should be based on geolocation.

Any further actions beyond selecting a cloud are outside the scope of the assignment (e.g. calling the API to launch a database).

The application should include a frontend and a backend implementation. The backend should act as an intermediate cache and a transformation layer on top of Aiven's API.

The available clouds can be listed using [Aiven's API](https://api.aiven.io/doc/#operation/ListClouds).

## Criteria for evaluation

* The main design goal is maintainability:
    - Code formatting and clarity
    - Simple and understandable solution
* The solution:
    - Must work (we need to be able to run the solution)
    - Must be tested and have tests
    - Must handle errors
    - Should be of production quality, with the exception of graphic design
*  Attribution:
    - If you take code from Google results, examples, etc., add attributions. We all know new things are often written based on search results.
* Continuous Integration is not evaluated

If you run out of time, show us a bit of every aspect of your ideal solution, rather than completing one aspect perfectly while leaving out others completely (e.g. testing), and describe how you would continue given more time.

## The homework template

In this GitHub repository, we have provided a bare bones starter application for the assignment:
* a [backend](./backend) written in [Python](https://www.python.org/) and [FastAPI](https://fastapi.tiangolo.com/)
* a [frontend](./frontend) written in [TypeScript](https://www.typescriptlang.org/) and [React](https://react.dev/)

You are free to:
* replace or edit the starter code. Or not use it at all, if you feel like it.
* use any other templates for your assignment. Please apply those in a separate commit, and add your code as commits on top.

## Candidate notes

Add your notes here - or replace this `README.md`.
