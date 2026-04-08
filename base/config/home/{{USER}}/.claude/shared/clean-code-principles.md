# Clean Code Principles

## Clean Code

- **Meaningful Names**: Use intention-revealing, pronounceable, searchable names for variables, functions, and classes. Avoid abbreviations, noise words, and mental mapping.
- **Functions**: Keep functions small (ideally under 20 lines), do one thing, operate at a single level of abstraction, and have no side effects unless explicitly necessary.
- **Comments**: Write self-documenting code. Use comments only to explain *why*, never *what*. Remove dead code and commented-out code.
- **Formatting**: Enforce consistent formatting, proper indentation, and logical grouping of related code.
- **Error Handling**: Use exceptions rather than error codes, provide context in error messages, and never swallow exceptions silently.
- **No Magic Numbers/Strings**: Extract literals into named constants.
- **DRY (Don't Repeat Yourself)**: Eliminate duplication ruthlessly.

## SOLID Principles

- **Single Responsibility Principle (SRP)**: Every class or module should have one, and only one, reason to change. If a class has multiple responsibilities, decompose it.
- **Open/Closed Principle (OCP)**: Code should be open for extension but closed for modification. Prefer abstractions and polymorphism over conditional branching.
- **Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types without altering program correctness. Avoid overriding in ways that break parent contracts.
- **Interface Segregation Principle (ISP)**: Prefer many small, specific interfaces over large, general-purpose ones. Clients should not depend on methods they don't use.
- **Dependency Inversion Principle (DIP)**: Depend on abstractions, not concretions. High-level modules should not depend on low-level modules.

## KISS (Keep It Simple, Stupid)

- Favor the simplest solution that solves the problem correctly.
- Avoid over-engineering, premature abstraction, and unnecessary complexity.
- If two solutions work equally well, always choose the simpler one.
- Question every layer of indirection — it must earn its place.
- Don't design for hypothetical future requirements unless there's strong evidence they're coming.

## Quality Checklist

- [ ] Are all names intention-revealing and free of ambiguity?
- [ ] Does every function/method do exactly one thing?
- [ ] Is there any duplicated logic that should be extracted?
- [ ] Does every class have a single responsibility?
- [ ] Are dependencies pointing toward abstractions, not concretions?
- [ ] Is the solution as simple as it can be while still being correct?
- [ ] Are there any magic numbers or strings that should be named constants?
- [ ] Is error handling explicit and informative?
- [ ] Would a new engineer understand this code without needing to ask questions?

## Red Flags

- Abstractions with only one implementation
- Layers that only pass data through without transformation
- Generic/configurable systems built before the second use case exists
- Deep inheritance hierarchies
- "Enterprise patterns" applied to simple CRUD operations
- Functions or classes with multiple unrelated responsibilities
- Long parameter lists
- Feature envy, data clumps, primitive obsession
