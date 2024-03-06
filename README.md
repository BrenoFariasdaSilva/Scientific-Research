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

Our research leverages various tools to accomplish the stated goals:

- **CK (Chidamber & Kemerer):** A tool used to collect and analyze code metrics from repositories. In this project, CK is employed to generate code metrics for repositories like Apache Commons-lang and Jabref.

- **PyDriller:** A Python framework used for mining software repositories. It is utilized to traverse the commit tree in the repository and run CK for every commit hash it is in.

- **RefactoringMiner:** A tool used for mining refactorings in Git repositories. It helps identify changes in the code that contribute to code evolution.

- **Word2Vector:** A technique used for natural language processing and understanding. In this project, Word2Vector is employed for similarity analysis between texts, such as code snippets and questions.

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
