# School of Computing &mdash; Year 4 Project Proposal Form

> Edit (then commit and push) this document to complete your proposal form.
> Make use of figures / diagrams where appropriate.
>
> Do not rename this file.

## SECTION A

|                     |                   |
|---------------------|-------------------|
|Project Title:       | Noted             |
|Student 1 Name:      | Mike Purcell      |
|Student 1 ID:        | 15446908          |
|Project Supervisor:  | Jennifer Foster   |

> Ensure that the Supervisor formally agrees to supervise your project; this is only recognised once the
> Supervisor assigns herself/himself via the project Dashboard.
>
> Project proposals without an assigned
> Supervisor will not be accepted for presentation to the Approval Panel.

## SECTION B

> Guidance: This document is expected to be approximately 3 pages in length, but it can exceed this page limit.
> It is also permissible to carry forward content from this proposal to your later documents (e.g. functional
> specification) as appropriate.
>
> Your proposal must include *at least* the following sections.


### Introduction

> Describe the general area covered by the project.

My idea is a Note taking rest api with a web app front end.Notes will be stored on a containerised 
database with my rest framework.
### Outline

> Outline the proposed project.

The goal is to have a unique note taking interface to allow past notes to become present dynamically during your writing.
This is done through Tags(#) and SubTags(!). Once a Tag is defined using a # all future occurrences will automatically
be selected and stored. As you begin to type and use a stored tag, the app will begin displaying past notes under the same topic.
Another core concept of the app is spaced repetition as a learning method. If selected, a note will be saved to then be 
displayed over intervals of days/weeks to avail of the spaced repetition.

### Background

> Where did the ideas come from?

With interests all over the place, I found myself making small note after note with no real logic to them as they came to my head. 
This has led to the same thing either being rewritten again or forgotten about completely. This is what led to the idea, and from
there I decided what would be most needed for something like this, hence the Categorisation and spaced repetition
as well as labelling notes as unfinished.

### Achievements

> What functions will the project provide? Who will the users be?

The app will provide a space for any user to learn and evolve ideas over time with continued participation. This change range from any academic topic
to any hobby, especially ones given custom templates.(e.g. fitness)

### Justification

> Why/when/where/how will it be useful?

two use cases  
A. Using it as a gym tracker, as there will be custom templates such as (5 5 50) would create a table to track workouts that would allow
you to mark your progress as you go. This will allow creating and tracking workouts to be done in the same setting as everything else.
  
B. Future projects, due to the nature of the app, it’s perfect for the progression of a future project, allowing for tech stacks needed
to be looked into/concepts being put into spaced repetition and kept at the forefront of your mind. The tag system will allow for notes
on things like databases, languages etc will automatically be sorted for ease of reading as you continue to write. 

### Programming language(s)

> List the proposed language(s) to be used.

Backend language is python  
Frontend Language is Javascript  

### Programming tools / Tech stack

> Describe the compiler, database, web server, etc., and any other software tools you plan to use.

Backend - Flask Framework  
Front end - React js  
Metric program DataDog  
Mysql /postgresql  
sqlalchemy (ORM)  
Flake 8 to create and adhere to rules  
Electron For desktop application framework  
Stored in markdown  

### Hardware

> Describe any non-standard hardware components which will be required.

No additional Tech

### Learning Challenges

> List the main new things (technologies, languages, tools, etc) that you will have to learn.

API/Flask framework  
react/ using javascript  
Containerize my database/flask framework  
Use of flake8/data dog etc..  
Electron framework for desktop app  

## Example of project UI

<p align="center">
  <img src="./res/mockUp.png" width="300px">
</p>

