---
header-includes: |
  <link rel="icon" type="image/x-icon" href="img/favicon.ico">
  <style>
  html {line-height: 1}
  body {max-width: 100%}
  body::before {
    content: "";
    z-index: -1;
    position: absolute;
    top: 0px;
    right: 0px;
    bottom: -5000px;
    left: 0px;
    background-image: url("img/background-bridge.avif");
    transform: scaleX(-1);
    background-size: 100%;
    background-repeat: repeat-y;
    opacity: 0.13;
  }
  header {margin-bottom: 0px; text-align: left}
  h1, h2 {margin-top: 0px}
  table {border-collapse: unset}
  tr {vertical-align: top}
  .ack tr {vertical-align: middle}
  td, th {text-align: left}
  </style>
title: Semantic bSDD
---

## Improving the GraphQL, JSON and RDF Representations of buildingSmart Data Dictionary

The buildingSmart Data Dictionary (bSDD) is an important shared resource in the Architecture, Engineering, Construction, and Operations (AECO) domain.
It is a collection of datasets ("domains") that define various classifications (objects representing building components, products, and materials),
their properties, allowed values, etc.
bSDD defines a GraphQL API, as well as REST APIs that return JSON and RDF representations.
This improves the interoperability of bSDD and its easier deployment in architectural Computer Aided Design (CAD) and other AECO software.

However, bSDD data is not structured as well as possible, and data retrieved via different APIs is not identical in content and structure.
This lowers bSDD data quality, usability and trust.

We conduct a thorough comparison and analysis of bSDD data related to fulfillment of FAIR (findable, accessible, interoperable, and reusable) principles.
Based on this analysis, we suggest enhancements to make bSDD data better structured and more FAIR.

We implement many of the suggestions by refactoring the original data to make it better structured/interconnected, and more "semantic".
We provide a SPARQL endpoint using [Ontotext GraphDB](https://graphdb.ontotext.com/), and GraphQL endpoint using [Ontotext Platform Semantic Objects](https://platform.ontotext.com/semantic-objects/).

|**Links**| |
|---------|---------------------------------------------------------------------------|
|<https://bsdd.ontotext.com><br/>This home page: schemas, data, sample queries| |
|<https://github.com/Accord-Project/bsdd><br/>Technical work (open source)|![](img/github-contributions.png)|
|[README.html](https://bsdd.ontotext.com/README.html)<br/>Detailed description of the work we did, 40 pages|![](img/readme-TOC-cropped.png){style="clip-path: ellipse(100% 95% at 50% 0)"} |
|[paper.pdf](https://bsdd.ontotext.com/paper/paper.pdf)<br/>Paper submitted to LDAC 2023 | Submitted on 28 February 2023, awaiting peer review |
|[presentation.pdf](https://bsdd.ontotext.com/paper/presentation.pdf)<br/>Presentation at LDAC 2023|TODO |
|**Original Endpoints**| |
|<https://test.bsdd.buildingsmart.org/graphql><br/>Original GraphQL endpoint|(protected)|
|<https://test.bsdd.buildingsmart.org/graphiql><br/>Original GraphQL query editor|![](img/graphiql-orig.png){style="clip-path: ellipse(100% 95% at 50% 0)"} |
|[bsdd-graphql-voyager-orig.html](https://rawgit2.com/Accord-Project/bsdd/main/bsdd-graphql-voyager-orig.html)<br/>Original GraphQL schema visualization with Voyager|![](img/bsdd-graphql-voyager-overview.png)|
|[Analysis Sheet](https://docs.google.com/spreadsheets/d/1z_NRMlExlVuqWhBbSErQ9iiDBY4O_fKMd3avV3-NCmo/edit)<br/>Analysis of differences between GraphQL, JSON and RDF representations|![](img/bsdd-data-analysis-sheet-cropped.png){style="clip-path: ellipse(100% 95% at 50% 0)"}|
|**Refactored Endpoints**| |
|<https://bsdd.ontotext.com/platform><br/>Semantic Objects workbench: administrative interface for the Ontotext Platform implementing GraphQL (protected)|![](img/graphql-workbench.png)|
|<https://bsdd.ontotext.com/graphql><br/>Refactored GraphQL endpoint|(protected) |
|<https://bsdd.ontotext.com/graphiql><br/>Refactored GraphQL query editor|![](img/graphiql-refact.png)|
|[bsdd-graphql-voyager-refact.html](https://rawgit2.com/Accord-Project/bsdd/main/bsdd-graphql-voyager-refact.html)<br/>Refactored GraphQL schema visualization with Voyager|![](img/bsdd-graphql-voyager-refact-overview.png)|
|[bsdd-graphql-soml.patch](https://github.com/Accord-Project/bsdd/blob/main/bsdd-graphql-soml.patch)<br/>Differences betwen original and refactored schema (as SOML)|![](img/bsdd-graphql-soml-diff.png)|
|<https://bsdd.ontotext.com/graphdb><br/>GraphDB Workbench: administrative interface for our semantic database|(protected) |
|<https://bsdd.ontotext.com/graphdb/repositories/bsdd><br/>GraphDB SPARQL endpoint| |
|<https://bsdd.ontotext.com/graphdb/sparql><br/>GraphDB SPARQL editor|![](img/graphdb-sparql.png)|
|<https://bsdd.ontotext.com/graphdb/graphs-visualizations><br/>Visual Graph visualizations|![](img/viz-ClassDOMAIN-cropped.png){style="clip-path: ellipse(100% 95% at 50% 0)"} |

<div class="ack">
|**Acknowledge** | | |
|---|----|-----------------------|
|Developed by|![](img/ontotext.png){width=200}          |[Ontotext (Sirma AI)](https://ontotext.com/)|
|Funded by   |![](img/accord.png){width=200}            |Horizon Europe [Project ACCORD](https://accordproject.eu/) (101056973)|
|Powered by  |![](img/graphdb.png){width=200}           |[Ontotext GraphDB](https://graphdb.ontotext.com/)|
|Powered by  |![](img/ontotext-platform.png){width=200} |[Ontotext Platform Semantic Objects](https://platform.ontotext.com/semantic-objects/)|
|Data from   |![](img/bsdd.png){width=200}              |[buildingSMART Data Dictionary](https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/) |
</div>
