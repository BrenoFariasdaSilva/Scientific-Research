<div align="center">
   
# [Scientific Research](https://github.com/BrenoFariasdaSilva/Scientific-Research) <img src="https://github.com/BrenoFariasdaSilva/Scientific-Research/blob/main/.assets/Bash.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Welcome to my Scientific Research Repository! This repository contains code and data related to my ongoing scientific research project. Our team is focused on various goals, as described below.
  
---

</div>

<div align="center">

![GitHub Code Size in Bytes](https://img.shields.io/github/languages/code-size/BrenoFariasdaSilva/Scientific-Research)
![GitHub Last Commit](https://img.shields.io/github/last-commit/BrenoFariasdaSilva/Scientific-Research)
![GitHub](https://img.shields.io/github/license/BrenoFariasdaSilva/Scientific-Research)
![wakatime](https://wakatime.com/badge/github/BrenoFariasdaSilva/Scientific-Research.svg)

</div>

<div align="center">
   
![Repobeats Statistics](https://repobeats.axiom.co/api/embed/cc926b338fcd1c49112ae0c1707e41cbfc07f606.svg "Repobeats analytics image")

</div>

## Table of Contents
- [Scientific Research ](#scientific-research-)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Goals](#goals)
  - [Skills](#skills)
  - [Directories](#directories)
  - [Tools](#tools)
    - [Worked Example Miner: A Comprehensive Tool for Java Repository Analysis](#worked-example-miner-a-comprehensive-tool-for-java-repository-analysis)
    - [Word2Vec](#word2vec)
  - [Repositories](#repositories)
    - [Apache Commons-lang](#apache-commons-lang)
    - [JabRef](#jabref)
  - [Methodology](#methodology)
    - [Data Collection](#data-collection)
    - [Code Analysis](#code-analysis)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

Welcome to the documentation of my scientific research project! This repository serves as a central hub for the code, data, and findings related to our ongoing research endeavors. We aim to explore various aspects of software development, code evolution, and the application of artificial intelligence tools to enhance code solutions.

## Goals

1. **Similarity Analysis:**
   - Explore different similarity algorithms, including Word2Vector, Yake, Sentence Bert, and TF-IDF, to evaluate the similarity between texts.
   - Create datasets for storing solved and unsolved questions and recommend changes based on the similarity of these questions.

2. **Enhancing Code Solutions:**
   - Investigate the use of tools like ChatGPT and GitHub Copilot to improve students' code solutions when they are stuck.
   - Utilize CK to generate Code Metrics for repositories like Apache Commons-lang and Jabref.
   - Employ PyDriller to traverse the commit tree in the repository and run CK for every commit hash.

3. **Analyzing Code Evolution:**
   - Analyze code that started with "bad" metrics and evolved over time.
   - Identify good code examples that indicate what makes code better and what changes are typically made to improve it.

4. **Providing Data to AI Tools:**
   - Gather valuable data to provide to tools like ChatGPT and GitHub Copilot, showcasing what constitutes good code and why.
   - Explore how contextual information, such as code samples, can assist these tools in suggesting better code improvements for students.

## Skills

Our research project involves expertise in the following areas:

- CK
- PyDriller
- RefactoringMiner
- Word2Vector
- Pandas
- NumPy
- Matplotlib
- Scikit-Learn
- Statistical Data Analysis
- Similarity measures
- Apache Commons-lang
- Jabref
- Code metrics
- Python (Programming Language)

Feel free to explore the code and data in this repository. If you have any questions or suggestions, please don't hesitate to reach out to me.

## Directories

Each directory in this repository has its own README.md file explaining its purpose. Please refer to individual README files for more details.

## Tools

### Worked Example Miner: A Comprehensive Tool for Java Repository Analysis

This project introduces the "Worked Example Miner", an innovative tool designed to streamline and enhance the analysis of Java repositories. By aggregating the capabilities of several established tools, it provides a robust framework for generating detailed data and metadata pivotal for examining repository evolution, identifying trends, and selecting prime candidates for creating worked examples. Here's how Worked Example Miner integrates these tools to offer a multifaceted analysis approach:

- **CK (Chidamber & Kemerer):** Utilized for its adeptness in collecting and analyzing code metrics, CK plays a crucial role in our tool by generating essential code metrics for repositories such as Apache Commons-lang and Jabref.

- **PyDriller:** This Python framework excels in mining software repositories. Within Worked Example Miner, PyDriller is harnessed to navigate through the commit tree of a repository, facilitating the execution of CK at every commit, thereby ensuring a comprehensive analysis across the development timeline.

- **RefactoringMiner:** Renowned for its ability to detect refactorings within Git repositories, RefactoringMiner is incorporated to pinpoint code modifications that signify evolution. This insight is invaluable in understanding the adaptive measures taken throughout a project's lifecycle.

By leveraging the combined strengths of these tools, Worked Example Miner emerges as a powerhouse for Java repository analysis. It not only facilitates the generation of differential analyses for each commit but also meticulously tracks the historical progression of selected CK metrics at each stage of code development. Furthermore, the tool is equipped to conduct linear regression analyses, detect substantial changes, and identify refactoring types cataloged by RefactoringMiner.

The integration of these capabilities allows Worked Example Miner to produce an array of outputs, from detailed commit diffs to analyses of repository evolution and potential trends. Such comprehensive data is instrumental in pinpointing exemplary candidates for the creation of worked examples, thus enriching educational resources and facilitating a deeper understanding of Java repository dynamics.

In essence, Worked Example Miner stands as a testament to the synergy of combining specialized tools to achieve a greater understanding of software development practices by the code metrics evolution. Through its detailed analyses, educators, researchers, and developers are better equipped to study Java repositories, enabling the cultivation of rich, informative worked examples that highlight best practices and evolutionary insights in software development.

### Word2Vec 
As a technique rooted in natural language processing, Word2Vec is applied to perform similarity analysis between various texts, such as code snippets and questions. This analysis aids in identifying patterns and relationships that may not be immediately evident.

## Repositories

### [Apache Commons-lang](https://github.com/apache/commons-lang)

- **Purpose:** Apache Commons Lang is a library with helper utilities for the java.lang API, notably String manipulation methods, basic numerical methods, object reflection, and more.
- **Usage in Research:** We leverage this repository to study code evolution and gather code metrics using CK.

### [JabRef](https://github.com/JabRef/jabref)

- **Purpose:** JabRef is an open-source bibliography reference manager that uses BibTeX as its native format.
- **Usage in Research:** We utilize JabRef to analyze code solutions, extract code metrics using CK, and understand the code evolution of a real-world application.

Feel free to explore these repositories to gain insights into our research and methodologies.

## Methodology

Our research follows a systematic methodology to achieve its goals. This includes:

### Data Collection

- **Repositories Selection:** Identify and select repositories relevant to the research goals, such as Apache Commons-lang and JabRef.
  
- **CK Integration:** Integrate CK to perform code metric analysis on specific commits, classes, or methods within the repository.

- **Mining Software Repositories:** Utilize PyDriller to traverse the commit tree in the repository and extract information relevant to code metrics and evolution.

- **Metric Visualization:** Utilize Matplotlib to create visualizations depicting the evolution of code metrics over time.

- **RefactoringMiner Integration:** Integrate RefactoringMiner to identify changes in the code that contribute to code evolution.

### Code Analysis

- **Code Analysis:** Analyze code that started with "bad" metrics and evolved over time. Identify good code examples that indicate what makes code better and what changes are typically made to improve it.

## Contributing

Contributions are very welcome! If you have ideas, improvements, or findings related to our research goals, feel free to submit a pull request or open an issue.

## License

This project is licensed under the [Creative Commons Zero v1.0 Universal](LICENSE), which means you are free to use, modify, and distribute the code, as long as you mention include the license and attribute you as the original author for the repository. See the [LICENSE](LICENSE) file for more details.
