# <a name="main"></a>C++ Core Guidelines

Jun 14, 2026

Editors:

* [Bjarne Stroustrup](https://www.stroustrup.com)
* [Herb Sutter](https://herbsutter.com/)

This is a living document under continuous improvement.
Had it been an open-source (code) project, this would have been release 0.8.
Copying, use, modification, and creation of derivative works from this project is licensed under an MIT-style license.
Contributing to this project requires agreeing to a Contributor License. See the accompanying [LICENSE](https://github.com/isocpp/CppCoreGuidelines/blob/master/LICENSE) file for details.
We make this project available to "friendly users" to use, copy, modify, and derive from, hoping for constructive input.

Comments and suggestions for improvements are most welcome.
We plan to modify and extend this document as our understanding improves and the language and the set of available libraries improve.
When commenting, please note [the introduction](#s-introduction) that outlines our aims and general approach.
The list of contributors is [here](#ss-ack).

Problems:

* The sets of rules have not been completely checked for completeness, consistency, or enforceability.
* Triple question marks (???) mark known missing information.
* Update reference sections; many pre-C++11 sources are too old.
* For a more-or-less up-to-date to-do list see: [To-do: Unclassified proto-rules](#s-unclassified).

You can [read an explanation of the scope and structure of this Guide](#s-abstract) or just jump straight in:

* [In: Introduction](#s-introduction)
* [P: Philosophy](#s-philosophy)
* [I: Interfaces](#s-interfaces)
* [F: Functions](#s-functions)
* [C: Classes and class hierarchies](#s-class)
* [Enum: Enumerations](#s-enum)
* [R: Resource management](#s-resource)
* [ES: Expressions and statements](#s-expr)
* [Per: Performance](#s-performance)
* [CP: Concurrency and parallelism](#s-concurrency)
* [E: Error handling](#s-errors)
* [Con: Constants and immutability](#s-const)
* [T: Templates and generic programming](#s-templates)
* [CPL: C-style programming](#s-cpl)
* [SF: Source files](#s-source)
* [SL: The Standard Library](#sl-the-standard-library)

Supporting sections:

* [A: Architectural ideas](#s-a)
* [NR: Non-Rules and myths](#s-not)
* [RF: References](#s-references)
* [Pro: Profiles](#s-profile)
* [GSL: Guidelines support library](#s-gsl)
* [NL: Naming and layout suggestions](#s-naming)
* [FAQ: Answers to frequently asked questions](#s-faq)
* [Appendix A: Libraries](#s-libraries)
* [Appendix B: Modernizing code](#s-modernizing)
* [Appendix C: Discussion](#s-discussion)
* [Appendix D: Supporting tools](#s-tools)
* [Glossary](#s-glossary)
* [To-do: Unclassified proto-rules](#s-unclassified)

You can sample rules for specific language features:

* assignment:
[regular types](#rc-regular) --
[prefer initialization](#rc-initialize) --
[copy](#rc-copy-semantic) --
[move](#rc-move-semantic) --
[other operations](#rc-matched) --
[default](#rc-eqdefault)
* `class`:
[data](#rc-org) --
[invariant](#rc-struct) --
[members](#rc-member) --
[helpers](#rc-helper) --
[concrete types](#ss-concrete) --
[ctors, =, and dtors](#s-ctor) --
[hierarchy](#ss-hier) --
[operators](#ss-overload)
* `concept`:
[rules](#ss-concepts) --
[in generic programming](#rt-raise) --
[template arguments](#rt-concepts) --
[semantics](#rt-low)
* constructor:
[invariant](#rc-struct) --
[establish invariant](#rc-ctor) --
[`throw`](#rc-throw) --
[default](#rc-default0) --
[not needed](#rc-default) --
[`explicit`](#rc-explicit) --
[delegating](#rc-delegating) --
[`virtual`](#rc-ctor-virtual)
* derived `class`:
[when to use](#rh-domain) --
[as interface](#rh-abstract) --
[destructors](#rh-dtor) --
[copy](#rh-copy) --
[getters and setters](#rh-get) --
[multiple inheritance](#rh-mi-interface) --
[overloading](#rh-using) --
[slicing](#rc-copy-virtual) --
[`dynamic_cast`](#rh-dynamic_cast)
* destructor:
[and constructors](#rc-matched) --
[when needed?](#rc-dtor) --
[must not fail](#rc-dtor-fail)
* exception:
[errors](#s-errors) --
[`throw`](#re-throw) --
[for errors only](#re-errors) --
[`noexcept`](#re-noexcept) --
[minimize `try`](#re-catch) --
[what if no exceptions?](#re-no-throw-codes)
* `for`:
[range-for and for](#res-for-range) --
[for and while](#res-for-while) --
[for-initializer](#res-for-init) --
[empty body](#res-empty) --
[loop variable](#res-loop-counter) --
[loop variable type ???](#res-???)
* function:
[naming](#rf-package) --
[single operation](#rf-logical) --
[no throw](#rf-noexcept) --
[arguments](#rf-smart) --
[argument passing](#rf-conventional) --
[multiple return values](#rf-out-multi) --
[pointers](#rf-return-ptr) --
[lambdas](#rf-capture-vs-overload)
* `inline`:
[small functions](#rf-inline) --
[in headers](#rs-inline)
* initialization:
[always](#res-always) --
[prefer `{}`](#res-list) --
[lambdas](#res-lambda-init) --
[default member initializers](#rc-in-class-initializer) --
[class members](#rc-initialize) --
[factory functions](#rc-factory)
* lambda expression:
[when to use](#ss-lambdas)
* operator:
[conventional](#ro-conventional) --
[avoid conversion operators](#ro-conversion) --
[and lambdas](#ro-lambda)
* `public`, `private`, and `protected`:
[information hiding](#rc-private) --
[consistency](#rh-public) --
[`protected`](#rh-protected)
* `static_assert`:
[compile-time checking](#rp-compile-time) --
[and concepts](#rt-check-class)
* `struct`:
[for organizing data](#rc-org) --
[use if no invariant](#rc-struct) --
[no private members](#rc-class)
* `template`:
[abstraction](#rt-raise) --
[containers](#rt-cont) --
[concepts](#rt-concepts)
* `unsigned`:
[and signed](#res-mix) --
[bit manipulation](#res-unsigned)
* `virtual`:
[interfaces](#ri-abstract) --
[not `virtual`](#rc-concrete) --
[destructor](#rc-dtor-virtual) --
[never fail](#rc-dtor-fail)

You can look at design concepts used to express the rules:

* assertion: ???
* error: ???
* exception: exception guarantee (???)
* failure: ???
* invariant: ???
* leak: ???
* library: ???
* precondition: ???
* postcondition: ???
* resource: ???
