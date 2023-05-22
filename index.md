---
title: Semantic bSDD
subtitle: Improving the GraphQL, JSON and RDF Representations of buildingSmart Data Dictionary
keywords:
- Linked building data
- LBD
- buildingSMART Data Dictionary
- bSDD
- FAIR data
- data quality
author: Vladimir Alexiev, Mihail Radkov, Nataliya Keberle
mainfont: Georgia, serif
fontsize: 14pt
linestretch: 1
maxwidth: 100%
header-includes: |
  <link rel="icon" type="image/x-icon" href="img/favicon.ico">
  <style>
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
    .subtitle {font-weight: bold}
    .author {font-style: italic}
  </style>
include-before: <div><img src='./img/SemBSDD-Logo-400px.png'/></div>
---

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
|<https://github.com/Accord-Project/bsdd><br/>Technical work (open source): scripts to get and refactor data, obtain GraphQL schema, generate and refactor SOML|![](img/github-contributions.png)|
|[README.html](https://bsdd.ontotext.com/README.html)<br/>Detailed description of the work we did, 40 pages|![](img/readme-TOC-cropped.png){style="clip-path: ellipse(100% 95% at 50% 0)"} |
|[paper.pdf](https://bsdd.ontotext.com/paper/paper.pdf)<br/>Accepted at 11th [Linked Data in Architecture and Construction Workshop (LDAC 2023)](https://linkedbuildingdata.net/ldac2023/), 15-16 June 2023 |![](img/paper-footer.png) |
|[presentation.html](https://bsdd.ontotext.com/paper/presentation.html)|Presentation at LDAC 2023 |
| webinars: video, transcript (if important, ask us to edit it), brief notes<br/>[24 Mar 2023 to ACCORD](https://drive.google.com/open?id=1Mhts8JwbdJFUmQHGULCqduijZ0NpEoxX), [26 Apr 2023 to bSI](https://drive.google.com/open?id=1iW05O6VcR4fhs2Q_vxM18s14tvHFejzY), 22 May 2023 to LBD|![](img/video-folder.png) |
|[discussion](https://forums.buildingsmart.org/t/semantic-bsdd/4669/5)<br/>At bSI forum: please contribute!|![](img/bSI-forum.png)|
|**Refactored Endpoints**| |
|[Voyager Refactored](https://rawgit2.com/Accord-Project/bsdd/main/bsdd-graphql-voyager-refact.html)<br/>Refactored GraphQL schema visualization with Voyager |![](img/bsdd-graphql-voyager-refact-overview.png)|
|PlantUML Overview Diagram: [png](img/bsdd-graphql-soml-diagram-overview.png) or [svg](http://www.plantuml.com/plantuml/svg/fLCzRy8m4DtpAquPAn4Lf2weOe6nGuNKJfKYOryI2yUEBeuG_xvsFWWE40OodS_ltRjtlXHI861PsJEKM1wGwgZmAIw9AumKPXQi0P9vOK58GcwbqL5zbBfYn4hGHc2D5NoyHn5NhAuX_bnRaapdZMAKKgEGrXluqTB6mEes6978o1OfAv4aPxN3RKsZBPrRQ1-Fw5oP0wOdwIYU8PoAvtnvCPPZIneE8-jWpD73zfWXeUQuCxmfKNVzt6H7ec87L8wuCoMJkaLtuGWvUMhXCDzaAYJRDJuSHbmc5QQPKQ8TnjQdPUOi-sbsNeFKLGzI7syOUrIFcCFLJOMXfu0xJOwiWfLkn2dJ8hru39K2n_UlmZUuQkANgGQ33jfCr8qNxdtnCacMCIp4OWFnUvAynHFH0Bq67bp-QH3TqysG-h9EeekNJoJS7-3sPJiLueLKOlAUSwgh95avLNfaR7YSNfNwerDgGnIprP-DRNY0ksCRBhshq510WsU6fdiMZF6EeRdg5qFmcg5gMD8PiVwxdbwmi33P2AQKEQ7ebdcchLVg_WC0) |![](img/bsdd-graphql-soml-diagram-overview.png){width=800} |
|PlantUML Full Diagram: [png](img/bsdd-graphql-soml-diagram.png) or [svg](http://www.plantuml.com/plantuml/svg/xLbBR-Cs4BxxLmZkhMY2E6qlHX1WuQH0q6oIPkFsie11YIEB3KMg99LOMFU_ToZ9NibwqN6xcosYWo5HCvptp4ShOXGyY1EJUJ74FYWzYknIm5J0OSGXD9wHdcBBo7YKAGWCasAa7vb8Y2An9oG53Odtyybe572YjJS-c_fIFkhfkNSF8IWG0Lp888r1cB57T7FL-pGw-yue8ZJkYSy_L1_ErsVJW70GbAZf-PeI0slF_Zwm6EycnyUJzGXfTC8KuGiX3II48gKWzhqsYebb7vrXXZS8_wvOi-JIXyKpCz4Y1iKeGztGk6iYbYbPGcxJvc7Gb8PufcM0FdJHjCsYggBumgh1YLgeb0EwoviBLZZTtkolt26QjT7fBFOb_qnvqh01Y48_4-leW5WtpsGgZCfo8yhxBsj7LJjEVE2er8MC2HEvJiNjIrHAihoiRgHX0Upwf8s5bqasQxUcKYMehvadjahet0HkzS9H2w7T52b8vugxKCTImPK8fIDvHovLh5F0WMYus6a5tLjgGqogNOG_OGV41jUN0o7Zi0Wbftc1pUmo2p5PRMCiihIsj4zp8zXTdt8kQrjNv6ntjGbK4_EG9KWpQrdhDjQrAeAYx6x3MqnO9bpyk6MPxsJKzntq2eYHwhermqzQSe32kpvdTMj68MJO2sj1xgDESERbKYvN2HOWSUOiXzjssXsG-mqwjTcqmr4j3DmsWwimk1GuyBARcg3kk2X0emEWj_wVEFeRqdgvaAYNhLRHJqmFH79o-kDF5TARrCALjSU4sQVqUsPJwbDMxEsSjZeJKcIn2sdAQ7z6bwt7mGKbPRi7E1EsEw0XAU7tDdqrPc6UjdF5aDh-DEVkiqsd21lQdP89A5CCtCt3lz_43cX6Gc1E0TtevfgKhwQBDLi5CQJerTzsnmCTA9OuawFQGhSJbuc-9NaNsqZSXXzI7miwRwRrhDzbkEIO8mWXPwcoAJf4VWrYQQ91gZHcGgRwIXYxOB8XXlTON4Cq3n6eMD8CMpyB7l0e1WexbXgqi8ZwGFTxqH0gTRcpvpimeAg5fbtA05OaJdYRB9zmBit2bwlYF1L443pcXw2BGkZQGtI3w4vKMW1ObBpGYNm4ka1WYqS3RPbYihfS1JpLxCdYG0XOJ7X5M0_VbUZXQm9OC96aj-5xH9qOcJXFg8PjdUAOU9cQJEodfYjuI8X18KurcaIPHZ39Vqj93XlQGbgWqQHCajy9J-5N9d3OtJMN-W3ABj3GBqGQ-fk26jfvk1XOcL-aYebnYLmxt6YIuM3ezzVNXIK5spQLxYsCtPopTXVtFuEhahC-V2TTMjHFLpLTsb_zTnf598v1BOYWYorog-jGmt7jhruLgdi3Ps_Wx0sS7GJElW8swsQwXxzIfe1Mk1n4_Q6O8RxLhydrXWDVCmviyc3mRNC3cWD0DvOYcJ-0-P98y-qlhS5FDAw0TF9_1wH54jOpheP6yvNzWP-lAPq-rGl55LQzTEgNRj9IcHOVeTNbjwssQsoL6tj7zEZS6zimZNU_UrIlgLV_Ml5HU3JVUzJ3D2XYYsFRH6nUegZwYrwHXHWKMTnF1gmg0ZhRjIs86ASpTwcdnyUdA5KTUUs6RiyJXTJD8G4bbV_hZsgky3fstxgnSNAgshJdxjiWUOS5QTFM-uILLpKZwcMt4nuBCvxB-JFgKUkGVVy1) |![](img/bsdd-graphql-soml-diagram-cropped.png){style="clip-path: ellipse(100% 50% at 50% 50%)"} |
|[bsdd-graphql-soml.patch](https://github.com/Accord-Project/bsdd/blob/main/bsdd-graphql-soml.patch)<br/>Differences betwen original and refactored schema (as SOML)|![](img/bsdd-graphql-soml-diff.png)|
|<https://bsdd.ontotext.com/platform><br/>Semantic Objects workbench: administrative interface for the Ontotext Platform implementing GraphQL (protected)|![](img/graphql-workbench.png){width=1000}|
|<https://bsdd.ontotext.com/graphql><br/>Refactored GraphQL endpoint|(protected) |
|<https://bsdd.ontotext.com/graphiql><br/>Refactored GraphQL query editor|![](img/graphiql-refact.png)|
|<https://bsdd.ontotext.com/graphdb><br/>GraphDB Workbench: administrative interface for our semantic database|(protected) |
|<https://bsdd.ontotext.com/graphdb/repositories/bsdd><br/>GraphDB SPARQL endpoint| |
|<https://bsdd.ontotext.com/graphdb/sparql><br/>GraphDB SPARQL editor|![](img/graphdb-sparql.png)|
|<https://bsdd.ontotext.com/graphdb/graphs-visualizations><br/>Visual Graph visualizations|![](img/viz-ClassDOMAIN-cropped.png){style="clip-path: ellipse(100% 95% at 50% 0)"} |
|**Original Endpoints**| |
|[Voyager Original](https://rawgit2.com/Accord-Project/bsdd/main/bsdd-graphql-voyager-orig.html)<br/>Original GraphQL schema visualization with Voyager |![](img/bsdd-graphql-voyager-overview.png)|
|[Analysis Sheet](https://docs.google.com/spreadsheets/d/1z_NRMlExlVuqWhBbSErQ9iiDBY4O_fKMd3avV3-NCmo/edit)<br/>Analysis of differences between GraphQL, JSON and RDF representations|![](img/bsdd-data-analysis-sheet-cropped.png){style="clip-path: ellipse(100% 95% at 50% 0)"}|
|<https://test.bsdd.buildingsmart.org/graphql><br/>Original GraphQL endpoint|(protected)|
|<https://test.bsdd.buildingsmart.org/graphiql><br/>Original GraphQL query editor|![](img/graphiql-orig.png){style="clip-path: ellipse(100% 95% at 50% 0)"} |

<div class="ack">
|**Acknowledge** | | |
|---|----|-----------------------|
|Developed by|![](img/ontotext.png){width=200}          |[Ontotext (Sirma AI)](https://ontotext.com/)|
|Funded by   |![](img/accord.png){width=200}            |Horizon Europe [Project ACCORD](https://accordproject.eu/) (101056973)|
|Powered by  |![](img/graphdb.png){width=200}           |[Ontotext GraphDB](https://graphdb.ontotext.com/)|
|Powered by  |![](img/ontotext-platform.png){width=200} |[Ontotext Platform Semantic Objects](https://platform.ontotext.com/semantic-objects/)|
|Data from   |![](img/bsdd.png){width=200}              |[buildingSMART Data Dictionary](https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/) |
</div>
