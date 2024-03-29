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

![GitHub Build/WorkFlow](https://img.shields.io/github/actions/workflow/status/BrenoFariasDaSilva/Scientific-Research/update-worked-example-miner-submodule.yml)
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
    - [Tools Utilized](#tools-utilized)
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

### Tools Utilized

- **Setence Bert:** Sentence-BERT is an adaptation of the BERT (Bidirectional Encoder Representations from Transformers) model, specifically optimized for sentence-level embeddings. Unlike traditional BERT that requires comparing all possible sentence pairs to find the most similar sentences, SBERT generates embeddings that are directly comparable in vector space. This means it can efficiently perform similarity analysis between sentences, making it highly effective for tasks such as semantic search, sentiment analysis, and duplicate question detection. Its ability to understand the nuanced meanings of sentences makes it a powerful tool for any application requiring deep semantic understanding.
- **TF-IDF (Term Frequency-Inverse Document Frequency):** TF-IDF is a statistical measure used to evaluate the importance of a word within a document in relation to a collection of documents, known as a corpus. This technique is grounded in the idea that the significance of a word increases proportionally to the number of times it appears in the document but is offset by its frequency in the corpus. TF-IDF is instrumental in performing similarity analysis between texts by identifying which words are most distinguishing between them. It's widely used in document classification, search engine optimization (SEO), and information retrieval systems to rank the relevance of documents and texts.
- **Yake (Yet Another Keyword Extractor):** YAKE is an unsupervised, lightweight, and efficient algorithm designed for automatic keyword extraction from individual documents. Unlike other keyword extraction methods that rely on large corpora or deep linguistic knowledge, YAKE focuses on statistical features from the text itself, such as word frequency, position, and co-occurrence information. This makes YAKE particularly useful for extracting relevant and meaningful keywords from texts, aiding in summarization, indexing, and categorization tasks without the need for extensive computational resources.
- **Word2Vec:** Word2Vec is a groundbreaking neural network-based technique developed to convert text into numerical form, allowing machines to understand human language. It maps words into a high-dimensional vector space, where semantically similar words are positioned closely together. Word2Vec is versatile in performing similarity analysis not only between words but also between larger text structures like sentences, paragraphs, and documents by averaging the word vectors. Its application extends beyond similarity analysis to include language modeling, translation, and even exploring syntactic and semantic word relationships. Word2Vec's ability to capture the context of words within documents makes it invaluable for a wide range of natural language processing (NLP) applications.

In order to read about the tools utilized in the Worked Example Miner, read [here](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner?tab=readme-ov-file#tools-utilized).

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
     - For refactorings: `git commit -m "REFACTOR: Enhance component for better aspect"`
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
