"""# Strategy Pattern Challenge: Smart Data Export Engine

You're building a data export engine for an analytics application. The application allows users to export large datasets in different formats, and each format has its own processing requirements.

Your task is to design and implement this system using **ONLY the Strategy Pattern**.

You can use normal Python features such as inheritance, composition, dictionaries, lists, and functions.

---

## 1. Problem Statement

Your application receives a dataset containing thousands of records.

Users should be able to export this dataset using three different strategies:

1. CSV Export
2. JSON Export
3. XML Export

Each export strategy behaves differently.

### CSV Export Strategy

- Convert records into comma-separated values.
- Include column headers.
- Allow users to specify which columns they want.
- Ignore records where all selected fields are empty or `None`.

Example:

```python
data = [
    {"name": "John", "age": 25, "city": "Chennai"},
    {"name": "Alice", "age": 30, "city": "Coimbatore"},
    {"name": None, "age": None, "city": None}
]
```

Expected output:

```text
name,age,city
John,25,Chennai
Alice,30,Coimbatore
```

### JSON Export Strategy

- Convert records into valid JSON.
- Allow users to specify selected columns.
- Ignore records where all selected fields are empty or `None`.
- Support pretty printing.
- Allow users to exclude fields containing `None`.

Example:

```json
[
    {
        "name": "John",
        "age": 25,
        "city": "Chennai"
    },
    {
        "name": "Alice",
        "age": 30,
        "city": "Coimbatore"
    }
]
```

### XML Export Strategy

- Convert records into valid XML.
- Allow users to specify selected columns.
- Ignore records where all selected fields are empty or `None`.
- Every record should be represented by a `<record>` element.
- Each field should become a child element.

Example:

```xml
<records>
    <record>
        <name>John</name>
        <age>25</age>
        <city>Chennai</city>
    </record>
    <record>
        <name>Alice</name>
        <age>30</age>
        <city>Coimbatore</city>
    </record>
</records>
```

---

# 2. Business Requirements

Your implementation must satisfy the following requirements.

### Requirement 1: Common Interface

All export strategies must implement:

```python
export(data, options)
```

The method should return the exported content as a string.

### Requirement 2: Runtime Strategy Switching

The user should be able to change the export format without creating a new exporter.

Example:

```python
exporter.set_strategy(CSVExportStrategy())
exporter.export(data, options)

exporter.set_strategy(JSONExportStrategy())
exporter.export(data, options)
```

### Requirement 3: Column Selection

Users should be able to specify which columns to export.

Example:

```python
options = {
    "columns": ["name", "city"]
}
```

Expected CSV:

```text
name,city
John,Chennai
Alice,Coimbatore
```

### Requirement 4: Handle Missing Columns

Suppose the user requests:

```python
options = {
    "columns": ["name", "salary", "city"]
}
```

But the dataset doesn't contain `salary`.

Your implementation must handle this gracefully.

For this challenge, represent missing values as empty fields.

### Requirement 5: Export Validation

Your implementation must handle:

- Empty datasets.
- Invalid export options.
- Missing columns.
- Invalid strategy implementations.
- Records containing `None` values.

You decide how to handle these situations, but document your decisions.

### Requirement 6: Export Statistics

Every export operation must also provide the following information:

```python
{
    "total_records": 1000,
    "exported_records": 850,
    "skipped_records": 150,
    "export_format": "CSV"
}
```

The actual export method should return the exported content, and you should decide how your context makes the statistics available.

---

# 3. Architecture Constraints

These constraints are important.

Your solution must follow these rules:

1. There must be one common Strategy interface.
2. CSV, JSON, and XML must be separate concrete strategies.
3. The Context must not contain CSV, JSON, or XML conversion logic.
4. The Context must not use `if-elif-else` to determine the export format.
5. Adding a new export strategy must not require modifying the Context.
6. Strategies must be interchangeable at runtime.
7. Common responsibilities should not be unnecessarily duplicated.

**Important:** You are allowed to use conditionals inside individual strategies. The restriction applies to the Context selecting or implementing export algorithms.

---

# 4. Test Dataset

Use this dataset to test your implementation:

```python
data = [
    {
        "id": 1,
        "name": "John",
        "age": 25,
        "city": "Chennai",
        "salary": 50000
    },
    {
        "id": 2,
        "name": "Alice",
        "age": 30,
        "city": "Coimbatore",
        "salary": 60000
    },
    {
        "id": 3,
        "name": None,
        "age": None,
        "city": None,
        "salary": None
    },
    {
        "id": 4,
        "name": "Bob",
        "age": 28,
        "city": "Bangalore",
        "salary": None
    },
    {
        "id": 5,
        "name": "Sarah",
        "age": 27,
        "city": "Mumbai",
        "salary": 75000
    }
]
```

---

# 5. Expected Usage

Ultimately, your implementation should support something similar to this:

```python
exporter = DataExporter(CSVExportStrategy())

result = exporter.export(data, {
    "columns": ["name", "age", "city"]
})

print(result)

# Change strategy

exporter.set_strategy(JSONExportStrategy())

result = exporter.export(data, {
    "columns": ["name", "age", "city"],
    "pretty": True,
    "exclude_none": True
})

print(result)

# Change strategy again

exporter.set_strategy(XMLExportStrategy())

result = exporter.export(data, {
    "columns": ["name", "city"]
})

print(result)
```

This is the expected interface, not the implementation.

---

# 6. Bonus Challenges (For Extra Difficulty)

Once you finish the basic requirements, try these:

**Bonus 1: Custom Export Strategy**

Create a Markdown export strategy without modifying the existing Context.

**Bonus 2: Compression Option**

Allow users to compress the exported content using a compression algorithm of their choice. Keep the compression implementation separate from the export strategies; don't introduce another design pattern.

**Bonus 3: Strategy Validation**

Prevent objects that don't implement the required strategy interface from being assigned to the Context.

**Bonus 4: Performance**

Your application should handle 100,000 records without unnecessarily creating multiple copies of the entire dataset.

---

## 7. What I'll Evaluate When You Submit

| Evaluation criteria | Weight |
|---|---:|
| Correct Strategy Pattern implementation | 25% |
| Proper separation of responsibilities | 20% |
| Runtime strategy switching | 15% |
| Handling edge cases | 15% |
| Code quality and Python practices | 15% |
| Extensibility | 10% |

### One important rule

I want to see whether you understand **why Strategy Pattern is useful**, not whether you can write the most complicated Python code.

**Your mission:** Implement the complete challenge and send me your code.

I'll review it like a senior developer conducting a code review. I'll point out:
- Architectural mistakes.
- Violations of the Strategy Pattern.
- Unnecessary abstractions.
- SOLID principle violations.
- Edge cases you missed.
- How your implementation could be improved.

I won't give you the solution upfront."""

from abc import abstractmethod, ABC
from typing import Any


class ExportInterface(ABC):

    @abstractmethod
    def export(
        self,
        data: dict[str, list], 
        options: dict[str, Any]
    ) -> str:
        pass


class CSVExporter(ExportInterface):

    def export(
        self,
        data: dict[str, Any], 
        options: dict[str, Any]
    ):
        pass

class JSONExporter(ExportInterface):

    def export(
        self,
        data: dict[str, Any], 
        options: dict[str, Any]
    ):
        pass

class XMLExporter(ExportInterface):

    def export(
        self,
        data: dict[str, Any], 
        options: dict[str, Any]
    ):
        pass

class DataExporter:

    def __init__(self, stratergy: ExportInterface):
        self._export_stratergy = stratergy

    @property
    def export_stratergy(self):
        return self.export_stratergy

    @export_stratergy.setter
    def export_stratergy(self, new_startergy: ExportInterface) -> Any:
        if (not isinstance(new_startergy, ExportInterface) 
                or new_startergy == self.export_stratergy):
            return TypeError
        self._export_stratergy = new_startergy

    def export(self, data, options):
        self._export_stratergy.export(data, options)