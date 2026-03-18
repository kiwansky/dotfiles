## Clean Code Principles

- **Meaningful Names**: Every variable, function, class, and module must have a name that clearly communicates its purpose and intent. No abbreviations unless universally understood. No single-letter variables except in trivial loop counters. If a name requires a comment to explain, rename it.
- **Short Functions**: Each function should do exactly one thing and do it well. Target 5-15 lines per function. If a function needs a comment explaining what it does or sectioning its body, break it into smaller functions with descriptive names.
- **Don't Repeat Yourself (DRY)**: Extract shared logic into reusable functions, modules, or abstractions. If you write similar code twice, refactor it into a shared component. Suggest abstractions only when the duplication is real, not coincidental.
- **Keep It Simple, Stupid (KISS)**: Choose the simplest solution that correctly solves the problem. Complexity must be justified. Avoid premature optimization, over-engineering, and unnecessary abstractions.
- **Composition over Inheritance**: Prefer composing behavior from smaller, focused objects over building deep inheritance hierarchies. Inheritance should model a genuine "is-a" relationship; everything else is composition.

## SOLID Principles

- **Single Responsibility Principle (SRP)**: Every class and module should have one and only one reason to change. If a class does more than one thing, split it.
- **Open/Closed Principle (OCP)**: Design entities that are open for extension but closed for modification. Use abstractions, interfaces, and polymorphism to allow new behavior without changing existing code. Watch for switch statements or if-chains that will grow with new requirements.
- **Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types without altering the correctness of the program. Honor contracts defined by parent classes and interfaces.
- **Interface Segregation Principle (ISP)**: No client should be forced to depend on methods it does not use. Prefer many small, specific interfaces over one large general-purpose interface.
- **Dependency Inversion Principle (DIP)**: Depend on abstractions, not concretions. High-level modules should not depend on low-level modules; both should depend on abstractions. Avoid direct instantiation of dependencies where injection is appropriate.

## Code Quality Priorities

When writing or evaluating code, apply these priorities in order — a higher priority always outweighs a lower one:

1. **Correctness** — The code must work and fulfill its requirements.
2. **Clarity** — The code must be immediately understandable by another developer.
3. **Simplicity** — The simplest correct solution wins. No unnecessary abstractions.
4. **Maintainability** — Future developers must be able to modify it confidently.
5. **Performance** — Optimize only when there is a demonstrated, measured need.
