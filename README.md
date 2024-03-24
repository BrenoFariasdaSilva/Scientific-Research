<div align="center">
   
# [Scientific Research](https://github.com/BrenoFariasdaSilva/Scientific-Research) <img src="https://github.com/BrenoFariasdaSilva/Scientific-Research/blob/main/.assets/Icons/Bash.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Welcome to my Scientific Research Repository!

This repository contains code and data related to my Scientific Research project. This project is massive and complex, containing multiple tools and exploring different goals and research questions. With that in mind, each of the directories in this repository has its own `README.md` file explaining it's purpose and how it contributes to the overall research project. 

The main tool is the Worked Example Miner, which is a comprehensive tool for Java repository analysis. This tool integrates CK, PyDriller, and RefactoringMiner to analyze Java repositories and generate data and metadata about the software evolution. This tool has really grown and evolved over time, and it's now a powerful tool for analyzing Java repositories, so it is now a submodule of this repository. With that in mind, you can find the Worked Example Miner repository by just opening the `Worked-Example-Miner` directory in this repository or [here](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner). A Github Workflow is also available to update the submodule automatically every hour, so you don't need to worry about updating it manually, just be aware that, in order to clone this repository with the submodule, you need to use the `--recurse-submodules` flag, as explained in the [Clone with Submodule](#clone-with-submodule) or [Clone Submodule](#clone-submodule) sections.
The Word2Vec tool is also used to perform similarity analysis between various texts, such as code snippets and questions. This analysis aids in identifying patterns and relationships that may not be immediately evident.

---

</div>

<div align="center">

![GitHub Build/WorkFlow](https://img.shields.io/github/actions/workflow/status/BrenoFariasDaSilva/Scientific-Research/update-submodule.yml)
![GitHub Code Size in Bytes](https://img.shields.io/github/languages/code-size/BrenoFariasdaSilva/Scientific-Research)
![GitHub Commits](https://img.shields.io/github/commit-activity/t/BrenoFariasDaSilva/Scientific-Research/main)
![GitHub Last Commit](https://img.shields.io/github/last-commit/BrenoFariasdaSilva/Scientific-Research)
![GitHub Forks](https://img.shields.io/github/forks/BrenoFariasDaSilva/Scientific-Research)
![GitHub Language Count](https://img.shields.io/github/languages/count/BrenoFariasDaSilva/Scientific-Research)
![GitHub License](https://img.shields.io/github/license/BrenoFariasdaSilva/Scientific-Research)
![GitHub Stars](https://img.shields.io/github/stars/BrenoFariasdaSilva/Scientific-Research)
![wakatime](https://wakatime.com/badge/github/BrenoFariasdaSilva/Scientific-Research.svg)

</div>

<div align="center">
   
![Repobeats Statistics](https://repobeats.axiom.co/api/embed/cc926b338fcd1c49112ae0c1707e41cbfc07f606.svg "Repobeats analytics image")

</div>

## Table of Contents
- [Scientific Research ](#scientific-research-)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Setup](#setup)
    - [Clone without Submodule](#clone-without-submodule)
    - [Clone with Submodule](#clone-with-submodule)
    - [Clone Submodule](#clone-submodule)
  - [Goals](#goals)
  - [Skills](#skills)
  - [Directories](#directories)
  - [Tools](#tools)
    - [Word2Vec](#word2vec)
    - [Worked Example Miner](#worked-example-miner)
  - [Repositories](#repositories)
    - [Apache Commons-lang](#apache-commons-lang)
    - [JabRef](#jabref)
  - [Methodology](#methodology)
    - [Data Collection](#data-collection)
    - [Code Analysis](#code-analysis)
  - [Research Questions](#research-questions)
  - [Proposed Approach](#proposed-approach)
    - [Software Metrics](#software-metrics)
    - [Tools Utilized](#tools-utilized)
  - [Conclusion](#conclusion)
  - [Contributing](#contributing)
  - [Collaborators](#collaborators)
  - [License](#license)

## Introduction

This repository stands as the cornerstone for the extensive code, data, and insights generated through our focused research into the similarity of texts in order to suggest similar solved issues to unsolved issues on platforms like [Github](http://github.com) or [Stack Overflow](http://stackoverflow.com/). As our project has advanced, i've developed interest in understanding the nuances of software development and code evolution, particularly within the realm of Distributed Systems, which is now the main goal of my research and the tool related to it, the [Worked Example Miner](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner), which is a submodule of this repository.

## Setup
### Clone without Submodule

In order to clone this repository without the submodule (Worked-Example-Miner), you can use the following command:

```bash
git clone https://github.com/BrenoFariasdaSilva/Scientific-Research
```

### Clone with Submodule

In order to clone this repository with the submodule (Worked-Example-Miner), you can use the following command:

```bash
git clone --recurse-submodules https://github.com/BrenoFariasdaSilva/Scientific-Research.git
```

### Clone Submodule

In case you have already cloned the repository and forgot to clone the submodule, you can use the following command to clone the submodule:

```bash
git submodule init
git submodule update
```

## Goals

1. **Similarity Analysis:**
   - Explore different similarity algorithms, including Word2Vector, Yake, Sentence Bert, and TF-IDF, to evaluate the similarity between texts.
   - Create datasets for storing solved and unsolved questions and recommend changes based on the similarity of these questions.

2. **Enhancing the given data:**
   - Analyze the results of the usage of the similarity algorithms to suggest similar solved issues to unsolved issues using different aspects, like a code snippet, a question, or a title or a mix of them.

3. **Enhancing Code Solutions:**
   - Investigate the use of tools like ChatGPT and GitHub Copilot to improve students' code solutions when they are stuck.
   - Utilize CK to generate Code Metrics for repositories like Apache Commons-lang and Jabref.
   - Employ PyDriller to traverse the commit tree in the repository and run CK for every commit hash.

4. **Providing Data to AI Tools:**
   - Gather valuable data to provide to tools like ChatGPT and GitHub Copilot, showcasing what constitutes good code and why.
   - Explore how contextual information, such as code samples, can assist these tools in suggesting better code improvements for students.

## Skills

Our research project involves expertise in the following areas:

- Python Language.
- Similarity Measures (Word2Vec, Yake, Sentence Bert, TF-IDF).
- Apache Commons-lang (Java Library).
- Jabref (Bibliography Reference Manager).
- GitHub Repositories.
- Data Collection and Analysis.

Other skills are required but are related to the [Worked Example Miner](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner) and are well explained in its repository.

Feel free to explore the code and data in this repository. If you have any questions or suggestions, please don't hesitate to reach out to me.

## Directories

Each directory in this repository has its own README.md file explaining its purpose. Please refer to individual README files for more details.

## Tools

### Word2Vec 

As a technique rooted in natural language processing, Word2Vec is applied to perform similarity analysis between various texts, such as code snippets and questions. This analysis aids in identifying patterns and relationships that may not be immediately evident.

### Worked Example Miner

As mentioned earlier, the Worked Example Miner is a comprehensive tool for Java repository analysis. This tool integrates CK, PyDriller, and RefactoringMiner to analyze Java repositories and generate data and metadata about the software evolution. This tool has really grown and evolved over time, and it's now a powerful tool for analyzing Java repositories, so it is now a submodule of this repository. With that in mind, you can find the Worked Example Miner directory documentation  [here](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner?tab=readme-ov-file#directories)


## Repositories

Our research encompasses a diverse set of open-source projects available on GitHub, chosen for their relevance and the rich insights they provide into various aspects of software development and maintenance. Below is a brief overview of each repository and its role in our study:

### [Apache Commons-lang](https://github.com/apache/commons-lang)

- **Purpose:** Apache Commons Lang is a library with helper utilities for the java.lang API, notably String manipulation methods, basic numerical methods, object reflection, and concurrency, among others.
- **Usage in Research:** We leverage this repository to study code evolution and gather code metrics using CK. It serves as a prime example of library development practices and evolution in the Java ecosystem.

### [JabRef](https://github.com/JabRef/jabref)

- **Purpose:** JabRef is an open-source bibliography reference manager. It uses BibTeX as its native format, facilitating the organization of references for researchers and academicians.
- **Usage in Research:** This repository is utilized to analyze code solutions, extract code metrics using CK, and understand the code evolution of a real-world application, offering insights into application development and maintenance practices.

The [Worked Example Miner](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner) tool analyzes different repositories, which are the Apache Kafka and Apache ZooKeeper repositories. They are used to represent the state of the art in Distributed Systems (DS) and are expected to provide valuable insights into code evolution and quality. In order to read more about the Worked Example Miner repositories, read [here](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner?tab=readme-ov-file#repositories).

## Methodology

This research adopts a systematic approach to explore the evolution of Distributed Systems (DS) through code metric analysis. Our methodology encompasses data collection, code analysis, and the integration of several tools and metrics to examine how code evolves in terms of complexity, quality, efficiency and in many other aspects.

### Data Collection

- **Repositories Selection:** We select relevant repositories that align with our research goals, focusing on projects like Apache Kafka and ZooKeeper.
- **CK Integration:** CK tool is integrated for conducting code metric analysis on chosen commits, classes, or methods within the repositories.
- **Mining Software Repositories:** PyDriller is utilized to navigate through the commit history, extracting essential data regarding code metrics and their evolution.
- **Metric Evaluation:** We evaluate code metrics that generates the values of each selected metric for each state (commit) of the code. This allows us to identify trends, patterns, and changes in the code over time.
- **Metric Visualization:** We employ Matplotlib for generating visual representations that illustrate the progression of code metrics over time.
- **RefactoringMiner Integration:** RefactoringMiner is used to detect refactorings in the codebase that signal improvements or changes contributing to code evolution.

### Code Analysis

We analyze instances where code initially demonstrated suboptimal metrics but evolved positively over time. Identifying exemplary modifications sheds light on effective practices for code improvement, focusing on alterations that enhance metric scores.

## Research Questions

Our investigation is guided by four principal questions:

1. How to identify relevant code quality metrics for analyzing DS evolution?
2. What patterns and trends signify clear code improvement in DS?
3. How do code improvements reflect on selected metrics and their correlation with non-functional characteristics?
4. Which metrics and characteristics are crucial for selecting appropriate code examples for educational purposes in Software Engineering (SE)?

## Proposed Approach

The project aims to develop a heuristic for identifying code examples that represent quality improvements in DS. This heuristic will aid in selecting code segments for educational examples, illustrating the adaptation and evolution of DS code over time. The heuristic will focus on improvements detectable through selected metrics, using specific tools on carefully chosen open-source repositories.

### Software Metrics

Our analysis leverages a suite of metrics for object-oriented design as outlined in the seminal work by Chidamber and Kemerer. The study, titled "A Metrics Suite for Object Oriented Design," was published in the IEEE Transactions on Software Engineering (vol. 20, no. 6, pp. 476–493, 1994). It introduces key metrics that have become foundational in assessing and improving the design quality of object-oriented software systems. These metrics include:

- **Coupling Between Object classes (CBO):** Reflects the degree of coupling by measuring the number of classes directly associated with a given class through method calls. A higher CBO value suggests higher complexity and lower flexibility, potentially leading to increased maintenance challenges. Reducing CBO over time can indicate improvements in code quality, aiming for a more modular software design that minimizes the impact of changes across the system.

- **Response for a Class (RFC):** Represents the set of methods that can be executed in response to a message received by an instance of the class. A lower RFC value denotes fewer behaviors and potentially lower complexity, making the class more cohesive and easier to maintain and test.

- **Weighted Methods per Class (WMC):** Calculates the sum of complexity measures of the class's methods. High WMC values may indicate complex classes with multiple responsibilities, affecting development and maintenance costs. Lower WMC values suggest a more focused and cohesive class, facilitating understanding and extension.

Additionally, the CK tool offers insights into other metrics that help understand code evolution:

- **Depth of Inheritance Tree (DIT):** Measures the number of ancestor classes, indicating the complexity level and the potential for side effects from changes in superclasses. A higher DIT value can imply more complex inheritance structures that may affect maintainability.

- **Lack of Cohesion in Methods (LCOM):** Indicates the degree of method cohesion within a class, ranging from 0 (high cohesion) to 1 (low cohesion). Preferred low values suggest that methods within a class are closely related to each other, enhancing the class's cohesiveness.

- **Number of Children (NOC):** Counts the direct subclasses of a class, with higher values hinting at greater reusability and significance within the codebase, as it implies a foundational role due to other classes' dependency on it.

Collectively, these metrics provide a comprehensive view of the codebase's complexity, quality, and maintainability. They serve as essential tools for developers to refine software design and architecture effectively. It's important to note that these metrics are derived from static code analysis, which involves evaluating the source code without executing the program. This approach allows for an in-depth understanding of the code's structural and qualitative aspects, facilitating targeted improvements and ensuring a more robust, maintainable, and efficient software system.

Dynamic code analysis complements our understanding by examining the code's behavior during execution. It sheds light on runtime characteristics, class communication, performance, and resource utilization, offering a holistic view of the software's operational efficiency. Despite the value of dynamic analysis, our research emphasizes static code analysis. This focus allows us to delve into the software quality's evolution within the domain of Distributed Systems (DS), providing insights into the code design changes and their impact on maintainability and reliability over time.


### Tools Utilized

- **CK Tool:** For static code analysis in Java projects, assessing metrics related to complexity, coupling, and cohesion.
- **RefactoringMiner:** Specializes in identifying and analyzing source code refactorings.
- **PyDriller:** A Python library for mining software repositories, facilitating the extraction of changes, contributions, and evolution of code.

## Conclusion

This research methodology, underpinned by detailed code metric analysis and tool integration, aims to offer significant insights into the evolution of software quality in DS. By identifying and analyzing patterns of improvement, this work contributes to the broader field of Software Engineering, particularly in educational contexts where real-world examples of code evolution are invaluable.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. If you have suggestions for improving the code, your insights will be highly welcome.
In order to contribute to this project, please follow the guidelines below or read the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details on how to contribute to this project, as it contains information about the commit standards and the entire pull request process.
Please follow these guidelines to make your contributions smooth and effective:

1. **Set Up Your Environment**: Ensure you've followed the setup instructions in the [Setup](#setup) section to prepare your development environment.

2. **Make Your Changes**:
   - **Create a Branch**: `git checkout -b feature/YourFeatureName`
   - **Implement Your Changes**: Make sure to test your changes thoroughly.
   - **Commit Your Changes**: Use clear commit messages, for example:
     - For new features: `git commit -m "FEAT: Add some AmazingFeature"`
     - For bug fixes: `git commit -m "FIX: Resolve Issue #123"`
     - For documentation: `git commit -m "DOCS: Update README with new instructions"`
     - For refactors: `git commit -m "REFACTOR: Enhance component for better aspect"`
     - For snapshots: `git commit -m "SNAPSHOT: Temporary commit to save the current state for later reference"`
   - See more about crafting commit messages in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

3. **Submit Your Contribution**:
   - **Push Your Changes**: `git push origin feature/YourFeatureName`
   - **Open a Pull Request (PR)**: Navigate to the repository on GitHub and open a PR with a detailed description of your changes.

4. **Stay Engaged**: Respond to any feedback from the project maintainers and make necessary adjustments to your PR.

5. **Celebrate**: Once your PR is merged, celebrate your contribution to the project!

## Collaborators

We thank the following people who contributed to this project:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/BrenoFariasdaSilva" title="Breno Farias da Silva">
        <img src="https://github.com/BrenoFariasdaSilva/Scientific-Research/blob/main/.assets/Images/BrenoFarias.jpg" width="100px;" alt="My Profile Picture"/><br>
        <sub>
          <b><a href="https://github.com/BrenoFariasdaSilva">Breno Farias da Silva</a></b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## License

This project is licensed under the [Apache License 2.0](LICENSE). This license permits use, modification, distribution, and sublicense of the code for both private and commercial purposes, provided that the original copyright notice and a disclaimer of warranty are included in all copies or substantial portions of the software. It also requires a clear attribution back to the original author(s) of the repository. For more details, see the [LICENSE](LICENSE) file in this repository.
