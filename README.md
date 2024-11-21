# FAIR vocabularies registry

This repository contains code and documentation of the CLARIAH (1) (continued by SHHOCK.nl (2)) FAIR vocabulary registry project. Here we include all the documentation and references to the different components (sub-projects).

# 1. About the FAIR vocabularies project

## Introduction
The FAIR vocabularies project pursues the goal of gathering vocabularies that are relevant to researchers, developers, or curators in the humanities and social sciences who are connected to both the CLARIN (3), CLARIAH (2) and SSHOC.nl (2) communities. The results of this project convey in a "vocabulary registry", which is a one-stop reference service for vocabularies useful to these communities or created during any of their projects.

The project aligns to other international initiatives that aim to increase the FAIR-ness (Findability, Accessibility, Reproducibility and Interoperability) of research data or cultural heritage metadata, in this case with a focus on semantic artefacts (controlled vocabularies or any other knowledge organization system, such as authority lists, taxonomies, thesauri, classification schemes, or schemas and abstract models such as ontologies (see for example Zeng, 2008).

What distinguishes this FAIR vocabulary registry from similar international initiatives is that it aims to:
- do semi-automatic curation work, which include automatic processes in the selection and processing, but also involves the community of experts in the selection and curation of the vocabularies,
- serve a clear user group, which gives advantages when selecting vocabularies to include and datasets to link to; also to have a closer relation with users during the development and evaluation of the registry;
- formalize the characteristics that make a vocabulary FAIR,
- widen the scope to make room for vocabularies that are not only RDF-based;
- it will find relations between the vocabularies and the dataset registries used by these communities to see which vocabularies were used in those datasets (to get statistics about vocabulary use), it will collect user reviews, and provide recommendations to encourage vocabulary reuse.

## Development roadmap
The project started during the CLARIAH Plus project. It continues during SSHOC.nl (2).
Previous CLARIAH development roadmap: https://github.com/orgs/CLARIAH/projects/3 (to be updated)
Current development roadmap: (forthcoming)

# 2. How-to guides
## Using the prototype:

### Searching/browsing
If you want to use the registry for searching and browsing you can make use of the vocabulary registry right away in the resulting web portal for the registry, here: https://registry.vocabs.dev.clariah.nl/ (this is a development version). This registry is a search and browsing interface for the selected vocabularies. You can use the search query to find vocabularies relevant to your search per keywords in the title or descriptions. You can use the different facets to filter the results per type of vocabulary, and other characteristics.

### Rating a vocabulary
(forthcoming)

### Getting recommendations
(forthcoming)

## Publishing a vocabulary
- If your vocabulary is already available on the Web, you can suggest it using the button "Register a new vocabulary". This form will be received by the curators of the project, and you will be notified when the vocabulary is made available or, if not, why.
- If your vocabulary doesn't exist on the Web (e.g., you or your institution has created a vocabulary and you don't know how to publish it): you can get advise: (forthcoming)

## Installing and contributing to the registry's code base
- If you are interested in installing it and/or understanding the code, see the section below ("Development set Up")

# 3. Development set up

## 1. Intro
The vocabulary registry has different components:

![FAIR vocabulary registry architecture](https://github.com/CLARIAH/vocab-registry/blob/6-update-readme-file/documentation/cac.png?raw=true)
(Source: Meijer & Windhower, 2024)

A complete description of the architecture can be found in the paper by Meijer & Windower (2024). This is a summary of the different components:

- The Editor: it's built based on a CMDI (Clarin metadata infrastructure) profile, it serves the purpose to add descriptive metadata to the vocabularies
   - See the code at this Github repository: (forthcoming)
   - The CMDI profile can also be accessed as a FAIR vocabulary via the registry: (forthcoming; temporarily you can see the data model here: https://github.com/CLARIAH/vocab-registry/blob/ec430d55d5c76345e4f25b5726ea84600c96d522/documentation/model.plantuml)
      - The editing process is done semi-automatically.

- The Workers: see the code at this Github repository: https://github.com/CLARIAH/vocab-workers). These are python-based applications that perform each of the tasks that build the registry, i.e.,: downloading/caching the vocabulary, summarizing, storing in a SPARQL store, converting to RDF, uploading to SKOSMOS (if it is a SKOS vocabulary), documenting, or finding if the vocabulary is also registered in other vocabulary registries.

- The interface (see the code at this Github repository: https://github.com/CLARIAH/vocab-registry). There are two components:
   - a) A python layer for the API
   - b) A public interface built in ReactJs' Java Script library

- A vocabulary recommender (see the code at this Github repository: (currently in private repo))

- The data (vocabulary records, cache) is temporarily stored in a private Gitlab repository: https://code.huc.knaw.nl/tsd/clariah/vocab-registry-data during the development phase. In the initial phase, vocabularies were uploaded automatically from two sources: YALC and Awsome humanities (more details forthcoming).

- The mappings for customizing the indexes in Elastic Search are available in this repository: (forthcoming)

## 2. Set up the vocabulary workers
(forthcoming)

## 3. Set up the vocabulary registry's API and public interfaces
(forthcoming)


# REFERENCES
- Meijer, K. and Windhouer, M. (2024). The CLARIAH FAIR Vocabulary Registry. CLARIN Annual Conference 2024 (forthcoming proceedings).
- Zeng, M.L. (2008). Knowledge Organization Systems (KOS). Knowledge Organization, 35, 160-182. https://doi.org/10.5771/0943-7444-2008-2-3-160

# FOOTNOTES
- (1) CLARIAH: Common Lab Research Infrastructure for the Arts and Humanities (https://www.clariah.nl/)
- (2) CLARIN: Common Language Resources and Technology Infrastructure (https://www.clarin.eu/)
- (3) SSHOC.nl: Digital Infrastructure for Social Sciences and Humanities (https://sshoc.nl/)

# CREDITS
- Ideation and project management: Menzo Windhouwer (lead software engineer at the KNAW Humanities Cluster)
- Ideation and development: Kerim Meijer (senior software engineer at the KNAW Humanities Cluster)
- Associate developer: Meindert Kroese (KNAW Humanities Cluster)
- Associate developer trainee and user researcher: Liliana Melgar (KNAW Humanities Cluster)
- Other project members: (forthcoming)
- This project is part of the CLARIAH infrastructure, it's funded by CLARIAH Plus and SSHOC.nl and gets collaboration from DANS (forthcoming)