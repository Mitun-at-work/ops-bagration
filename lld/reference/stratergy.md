# Stratergy

1. Instead of writing multiple algorithms inside one class using if-else statements, you create separate classes for each algorithm and allow the main class to use whichever algorithm it needs.

Whenever The Open/Closed Principle states: Software entities should be open for extension but closed for modification

Testing one algorithm means working with the same class that contains all the other algorithms.


| Component | Responsibility |
|---|---|
| Strategy | Defines a common interface for algorithms. |
| Concrete Strategy | Implements a specific algorithm. |
| Context | Uses a strategy without knowing its internal implementation. |

Fact 1: Strategies can be functions instead of classes
Python treats functions as first-class objects, you can pass functions as strategies.

Fact 2: Strategy Pattern is closely related to Dependency Injection

Fact 3: Strategies can maintain their own state
Many people assume strategies must be stateless.
One important consideration: if a strategy is shared across multiple contexts or threads, you must consider state isolation and thread safety.


Fact 4: Strategy Pattern and State Pattern look similar but solve different problems


| Strategy Pattern | State Pattern |
|---|---|
| Changes an algorithm. | Changes behavior based on internal state. |
| Usually selected by the client. | Often changes through internal transitions. |
| Focuses on interchangeable algorithms. | Focuses on state-dependent behavior. |
| Example: Different route calculation methods. | Example: An order being pending, shipped, or delivered. |


Fact 5: Strategy Pattern can eliminate conditional complexity, but it doesn't eliminate all conditionals
The goal isn't to eliminate every if-else statement.
The goal is to isolate algorithms that vary.


4. You want to switch behavior at runtime

Common responsibilities should not be unnecessarily duplicated.