# Development of an Intelligent Tutoring System for Geometry Learning Using Ontology and Python

## Overview
The development of an Intelligent Tutoring System (ITS) to help secondary school students learn how to find the area of basic geometries (square, triangle, rectangle) has been done in this repository. The geometric concepts are represented by ontologies and the system provides an interactive learning for the students.

## Features
- **Interactive Learning:** The system provides students with problem-solving exercises related to geometric shapes.
- **Ontology-based:** Geometric shapes and their properties are modeled using Protégé ontology, which serves as the foundation of the knowledge representation.
- **Assessment:** The ITS evaluates students' answers, provides feedback, and guides them through the learning process.

## Technologies Used
- **Python:** For coding the logic and problem-solving functionality of the ITS.
- **Protégé:** For ontology development and semantic knowledge representation.
- **OWL (Web Ontology Language):** To define and structure the ontology.

## Installation
1. Python Version: 3.13.1
2. Clone the repository:
```ruby
git clone https://github.com/LonLeo/GeoShape.git
cd GeoShape
```
3. Install required dependencies:
```ruby
pip install -r requirements.txt
```
4. Open the ontology file in Protégé to explore the knowledge representation.
5. Run the system (Python code) as needed to start interacting with the ITS.

## Usage
1. The system asks questions about finding the area of geometric shapes (Square, Triangle, Rectangle).
2. Students provide their answers, and the system checks the correctness.
3. Based on the correctness of the answer, the ITS provides feedback and further hints if required.
4. The ITS can be extended to include more shapes and further features.

## File Structure
- ontology/: Contains the Protégé ontology files representing geometric shapes.
- /: Python code implementing the ITS logic.
- requirements.txt: Python dependencies for the system.