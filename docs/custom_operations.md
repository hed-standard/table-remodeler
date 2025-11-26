# Custom operations

This guide provides comprehensive documentation for developers who want to create custom remodeling operations for Table Remodeler. It covers the architecture, requirements, and best practices for extending the remodeling framework.

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Operation class structure](#operation-class-structure)
3. [PARAMS dictionary specification](#params-dictionary-specification)
4. [Implementing BaseOp](#implementing-baseop)
5. [Implementing summarization operations](#implementing-summarization-operations)
6. [Validator integration](#validator-integration)
7. [Testing custom operations](#testing-custom-operations)
8. [Best practices](#best-practices)

## Architecture overview

Operations are defined as classes that extend `BaseOp` regardless of whether they are transformations or summaries. However, summaries must also implement an additional supporting class that extends `BaseSummary` to hold the summary information.

In order to be executed by the remodeling functions, an operation must appear in the `valid_operations` dictionary located in `remodel/operations/valid_operations.py`.

### Key components

- **BaseOp**: Abstract base class for all operations
- **BaseSummary**: Abstract base class for summary support classes
- **Dispatcher**: Orchestrates operation execution on datasets
- **RemodelerValidator**: Validates operation specifications against JSON schemas
- **valid_operations**: Registry dictionary mapping operation names to classes

## Operation class structure

Each operation class must have:

1. **NAME**: Class variable (string) specifying the operation name
2. **PARAMS**: Class variable containing a JSON schema dictionary of parameters
3. **Constructor**: Calls `super().__init__(parameters)` and sets up operation-specific properties
4. **do_op()**: Main method that performs the operation
5. **validate_input_data()**: Static method for additional validation beyond JSON schema

### Basic operation template

```python
from remodel.operations.base_op import BaseOp

class MyCustomOp(BaseOp):
    """Brief description of what this operation does."""
    
    NAME = "my_custom_operation"
    
    PARAMS = {
        "type": "object",
        "properties": {
            "my_parameter": {
                "type": "string",
                "description": "Description of parameter"
            },
            "optional_param": {
                "type": "integer", 
                "description": "Optional parameter"
            }
        },
        "required": ["my_parameter"],
        "additionalProperties": False
    }
    
    def __init__(self, parameters):
        """Initialize the operation with validated parameters."""
        super().__init__(parameters)
        self.my_parameter = parameters['my_parameter']
        self.optional_param = parameters.get('optional_param', default_value)
    
    def do_op(self, dispatcher, df, name, sidecar=None):
        """
        Execute the operation on a DataFrame.
        
        Parameters:
            dispatcher (Dispatcher): The dispatcher managing operations
            df (pd.DataFrame): The tabular data to transform
            name (str): Identifier for the file (for error messages)
            sidecar (dict): Optional JSON sidecar for HED operations
            
        Returns:
            pd.DataFrame: The transformed DataFrame
        """
        # Your transformation logic here
        # For transformations, return modified DataFrame
        # For summaries, update dispatcher.summary_dict and return original df
        return df
    
    @staticmethod
    def validate_input_data(parameters):
        """
        Perform additional validation beyond JSON schema.
        
        Parameters:
            parameters (dict): The operation parameters
            
        Returns:
            list: List of error message strings (empty if no errors)
        """
        errors = []
        # Add custom validation logic here
        return errors
```

## PARAMS dictionary specification

The `PARAMS` dictionary uses [JSON Schema](https://json-schema.org/) (draft-2020-12) to specify operation parameters.

### Basic structure

```python
PARAMS = {
    "type": "object",  # Always "object" at top level
    "properties": {
        # Define each parameter here
    },
    "required": [
        # List required parameter names
    ],
    "additionalProperties": False  # Recommended: disallow unexpected parameters
}
```

### Parameter types

#### String parameter

```python
"column_name": {
    "type": "string",
    "description": "The name of the column to process"
}
```

#### Integer/number parameter

```python
"max_count": {
    "type": "integer",
    "minimum": 1,
    "description": "Maximum number of items"
}
```

#### Boolean parameter

```python
"ignore_missing": {
    "type": "boolean",
    "description": "If true, ignore missing columns"
}
```

#### Array (list) parameter

```python
"column_names": {
    "type": "array",
    "items": {
        "type": "string"
    },
    "minItems": 1,
    "description": "List of column names"
}
```

#### Object (dictionary) parameter

```python
"column_mapping": {
    "type": "object",
    "patternProperties": {
        ".*": {
            "type": "string"
        }
    },
    "minProperties": 1,
    "description": "Mapping of old names to new names"
}
```

### Example: rename_columns PARAMS

```python
PARAMS = {
    "type": "object",
    "properties": {
        "column_mapping": {
            "type": "object",
            "patternProperties": {
                ".*": {
                    "type": "string"
                }
            },
            "minProperties": 1,
            "description": "Dictionary mapping old column names to new names"
        },
        "ignore_missing": {
            "type": "boolean",
            "description": "If false, raise error for missing columns"
        }
    },
    "required": [
        "column_mapping",
        "ignore_missing"
    ],
    "additionalProperties": False
}
```

### Parameter dependencies

Use `dependentRequired` for conditional requirements:

```python
"dependentRequired": {
    "factor_names": ["factor_values"]  # factor_names requires factor_values
}
```

## Implementing BaseOp

### Constructor requirements

Always call the superclass constructor first:

```python
def __init__(self, parameters):
    super().__init__(parameters)
    # Then initialize operation-specific attributes
    self.column_names = parameters['column_names']
```

### The do_op method

**Signature:**
```python
def do_op(self, dispatcher, df, name, sidecar=None):
```

**Parameters:**
- `dispatcher`: Instance of `Dispatcher` managing the remodeling process
- `df`: Pandas DataFrame representing the tabular file
- `name`: Identifier for the file (usually filename or relative path)
- `sidecar`: Optional JSON sidecar containing HED annotations (for HED operations)

**Returns:**
- Modified DataFrame (for transformations)
- Original DataFrame (for summaries - they modify dispatcher.summary_dict instead)

**Important Notes:**

1. **n/a Handling**: The `do_op` method assumes that `n/a` values have been replaced with `numpy.NaN` in the incoming DataFrame. The `Dispatcher` handles this conversion automatically using `prep_data()` before operations and `post_proc_data()` after.

2. **Don't Modify in Place**: Return a new DataFrame rather than modifying the input DataFrame in place.

3. **Error Handling**: Raise appropriate exceptions with clear messages for error conditions.

### Example implementation

```python
def do_op(self, dispatcher, df, name, sidecar=None):
    """Remove specified columns from the DataFrame."""
    return df.drop(self.column_names, axis=1, errors=self.error_handling)
```

### The validate_input_data method

Use this static method for validation that cannot be expressed in JSON schema.

```python
@staticmethod
def validate_input_data(parameters):
    """
    Validate parameters beyond JSON schema constraints.
    
    Common use cases:
    - Checking list lengths match
    - Validating value ranges based on other parameters
    - Checking for logical inconsistencies
    
    Returns:
        list: User-friendly error messages (empty if valid)
    """
    errors = []
    
    # Example: Check that two lists have the same length
    if parameters.get("query_names"):
        if len(parameters["query_names"]) != len(parameters["queries"]):
            errors.append(
                "The query_names list must have the same length as queries list."
            )
    
    return errors
```

## Implementing summarization operations

Summarization operations require both an operation class (extending `BaseOp`) and a summary class (extending `BaseSummary`).

### Summarization operation class

```python
from remodel.operations.base_summary import BaseSummary

class MySummarySummary(BaseSummary):
    """Holds summary information for my_summary operation."""
    
    def __init__(self, sum_op):
        """Initialize with operation parameters."""
        super().__init__(sum_op)
        self.summary_data = {}  # Store your summary data
    
    def update_summary(self, summary_dict):
        """
        Update summary with information from one file.
        
        Parameters:
            summary_dict (dict): File-specific information
                Example: {"name": "file.tsv", "column_names": [...]}
        """
        # Extract and store information
        name = summary_dict['name']
        # ... accumulate your summary data
    
    def get_summary_details(self, verbose=True):
        """
        Return the summary information as a dictionary.
        
        Parameters:
            verbose (bool): If True, include detailed information
            
        Returns:
            dict: Summary data formatted for output
        """
        return {
            'summary_type': 'my_summary',
            'data': self.summary_data
            # ... your summary structure
        }

class MySummaryOp(BaseOp):
    """Summarize some aspect of the data."""
    
    NAME = "my_summary"
    
    PARAMS = {
        "type": "object",
        "properties": {
            "summary_name": {
                "type": "string",
                "description": "Unique identifier for this summary"
            },
            "summary_filename": {
                "type": "string",
                "description": "Base filename for saving summary"
            }
        },
        "required": ["summary_name", "summary_filename"],
        "additionalProperties": False
    }
    
    def __init__(self, parameters):
        super().__init__(parameters)
        self.summary_name = parameters['summary_name']
        self.summary_filename = parameters['summary_filename']
    
    def do_op(self, dispatcher, df, name, sidecar=None):
        """Update summary without modifying DataFrame."""
        # Get or create summary object
        summary = dispatcher.summary_dict.get(self.summary_name)
        if not summary:
            summary = MySummarySummary(self)
            dispatcher.summary_dict[self.summary_name] = summary
        
        # Update with file-specific information
        summary.update_summary({
            "name": name,
            "data": self._extract_data(df)
        })
        
        # Return original DataFrame unchanged
        return df
    
    def _extract_data(self, df):
        """Helper method to extract relevant data."""
        # Your data extraction logic
        return extracted_data
    
    @staticmethod
    def validate_input_data(parameters):
        return []  # No additional validation needed
```

### BaseSummary required methods

#### update_summary(summary_dict)

Called by the operation's `do_op` method for each file processed. Accumulates information across all files.

```python
def update_summary(self, summary_dict):
    file_name = summary_dict['name']
    file_data = summary_dict['data']
    
    # Store file-specific information
    self.file_summaries[file_name] = file_data
    
    # Update overall statistics
    self.total_files += 1
    # ... accumulate other data
```

#### get_summary_details(verbose=True)

Returns the accumulated summary data as a dictionary. This is called when saving summaries to JSON or text format.

```python
def get_summary_details(self, verbose=True):
    details = {
        'overall': {
            'total_files': self.total_files,
            # ... overall statistics
        }
    }
    
    if verbose:
        details['individual_files'] = self.file_summaries
    
    return details
```

## Validator integration

### Registering your operation

Add your operation to `remodel/operations/valid_operations.py`:

```python
from remodel.operations.my_custom_op import MyCustomOp

valid_operations = {
    # ... existing operations ...
    "my_custom_operation": MyCustomOp,
}
```

### Validation stages

The validator processes operations in stages:

1. **Stage 0**: Top-level structure (must be array of operations)
2. **Stage 1**: Operation dictionary format (must have operation, description, parameters keys)
3. **Stage 2**: Operation dictionary values (validate types and check valid operation names)
4. **Later Stages**: Nested parameter validation using JSON schema
5. **Final Stage**: Call `validate_input_data()` for each operation

### Error messages

The validator provides user-friendly error messages indicating:
- Operation index in the remodeling file
- Operation name
- Path to the invalid value
- What constraint was violated

## Testing custom operations

### Unit testing structure

Create test files in `tests/operations/` following the pattern:

```python
import unittest
import pandas as pd
from remodel.operations.my_custom_op import MyCustomOp
from remodel import Dispatcher

class TestMyCustomOp(unittest.TestCase):
    """Test cases for MyCustomOp."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
    
    def test_basic_functionality(self):
        """Test basic operation behavior."""
        params = {
            'my_parameter': 'value'
        }
        op = MyCustomOp(params)
        
        # Create a simple dispatcher for testing
        dispatcher = Dispatcher([], data_root=".")
        
        result = op.do_op(dispatcher, self.sample_df, "test_file.tsv")
        
        # Assert expected transformations
        self.assertIsInstance(result, pd.DataFrame)
        # ... more assertions
    
    def test_parameter_validation(self):
        """Test parameter validation."""
        # Test invalid parameters
        errors = MyCustomOp.validate_input_data({
            'my_parameter': 'value',
            'invalid_list': [1, 2]  # Wrong length
        })
        self.assertTrue(len(errors) > 0)
        
        # Test valid parameters
        errors = MyCustomOp.validate_input_data({
            'my_parameter': 'value',
            'valid_list': [1, 2, 3]
        })
        self.assertEqual(len(errors), 0)
    
    def test_error_handling(self):
        """Test error conditions."""
        params = {'my_parameter': 'value'}
        op = MyCustomOp(params)
        dispatcher = Dispatcher([], data_root=".")
        
        # Test with problematic data
        bad_df = pd.DataFrame({'wrong_col': [1, 2, 3]})
        
        with self.assertRaises(KeyError):
            op.do_op(dispatcher, bad_df, "test.tsv")

if __name__ == '__main__':
    unittest.main()
```

### Integration testing

Test with complete remodeling workflows:

```python
def test_full_remodeling_workflow(self):
    """Test operation in a complete remodeling pipeline."""
    operations = [
        {
            "operation": "my_custom_operation",
            "description": "Test my operation",
            "parameters": {
                "my_parameter": "test_value"
            }
        }
    ]
    
    dispatcher = Dispatcher(operations, data_root="path/to/test/data")
    dispatcher.run_operations()
    
    # Assert expected results
```

## Best practices

### Design principles

1. **Single Responsibility**: Each operation should do one thing well
2. **Immutability**: Don't modify input DataFrames in place
3. **Clear Errors**: Provide helpful error messages with context
4. **Documentation**: Include docstrings for class and methods
5. **Type Hints**: Use type hints for better IDE support

### Parameter design

1. **Required vs Optional**: Make commonly-used parameters required
2. **Sensible Defaults**: Provide defaults for optional parameters
3. **Clear Names**: Use descriptive parameter names
4. **Consistent**: Follow naming conventions from existing operations

### Error handling

```python
def do_op(self, dispatcher, df, name, sidecar=None):
    # Check preconditions
    if self.column_name not in df.columns:
        raise ValueError(
            f"Column '{self.column_name}' not found in {name}. "
            f"Available columns: {list(df.columns)}"
        )
    
    # Perform operation with try/except for specific errors
    try:
        result = df.copy()
        # ... transformation logic
        return result
    except Exception as e:
        raise RuntimeError(
            f"Error processing {name} with {self.NAME}: {str(e)}"
        )
```

### Performance considerations

1. **Vectorize Operations**: Use pandas vectorized operations instead of loops
2. **Avoid Copies**: Only copy DataFrames when necessary
3. **Lazy Evaluation**: Compute expensive operations only when needed
4. **Memory Efficiency**: For large datasets, consider memory usage

### Documentation

Include comprehensive docstrings:

```python
class MyCustomOp(BaseOp):
    """
    Transform data by applying custom logic.
    
    This operation processes tabular data by...
    
    Common use cases:
    - Use case 1
    - Use case 2
    
    Example JSON:
        {
            "operation": "my_custom_operation",
            "description": "Process the data",
            "parameters": {
                "my_parameter": "value"
            }
        }
    
    See Also:
        - related_operation: For alternative approach
        - another_operation: For complementary functionality
    """
```

### Testing checklist

- [ ] Unit tests for basic functionality
- [ ] Tests for edge cases
- [ ] Tests for error conditions
- [ ] Parameter validation tests
- [ ] Integration tests with Dispatcher
- [ ] Tests with various DataFrame structures
- [ ] Tests with n/a values
- [ ] Performance tests for large datasets (if applicable)

## Example: complete custom operation

Here's a complete example of a custom operation that converts column values to uppercase:

```python
from remodel.operations.base_op import BaseOp
import pandas as pd

class UppercaseColumnsOp(BaseOp):
    """
    Convert specified columns to uppercase.
    
    Example JSON:
        {
            "operation": "uppercase_columns",
            "description": "Convert trial_type to uppercase",
            "parameters": {
                "column_names": ["trial_type", "condition"],
                "ignore_missing": true
            }
        }
    """
    
    NAME = "uppercase_columns"
    
    PARAMS = {
        "type": "object",
        "properties": {
            "column_names": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "description": "List of column names to convert to uppercase"
            },
            "ignore_missing": {
                "type": "boolean",
                "description": "If true, ignore columns not in DataFrame"
            }
        },
        "required": ["column_names", "ignore_missing"],
        "additionalProperties": False
    }
    
    def __init__(self, parameters):
        super().__init__(parameters)
        self.column_names = parameters['column_names']
        self.ignore_missing = parameters['ignore_missing']
    
    def do_op(self, dispatcher, df, name, sidecar=None):
        """Convert specified columns to uppercase."""
        result = df.copy()
        
        for col in self.column_names:
            if col not in result.columns:
                if not self.ignore_missing:
                    raise KeyError(
                        f"Column '{col}' not found in {name}. "
                        f"Available: {list(result.columns)}"
                    )
                continue
            
            # Convert to uppercase, preserving NaN values
            result[col] = result[col].str.upper()
        
        return result
    
    @staticmethod
    def validate_input_data(parameters):
        """No additional validation needed beyond JSON schema."""
        return []
```

Register it:

```python
# In remodel/operations/valid_operations.py
from remodel.operations.uppercase_columns_op import UppercaseColumnsOp

valid_operations = {
    # ... existing operations ...
    "uppercase_columns": UppercaseColumnsOp,
}
```

## Resources

- **JSON Schema Documentation**: https://json-schema.org/
- **Pandas DataFrame API**: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
- **Python unittest**: https://docs.python.org/3/library/unittest.html
- **Table Remodeler Repository**: https://github.com/hed-standard/table-remodeler
- **Operations Reference**: [operations_reference.md](operations_reference.md)

## Getting help

- Review existing operations in `remodel/operations/` for examples
- Check the test suite in `tests/operations/` for testing patterns
- Open an issue on GitHub for questions or feature requests
- See the [User Guide](user_guide.md) for operation usage examples
