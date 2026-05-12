# Design Document for Subsystem A
1. Considerations
1.1 Assumptions
    * Program runs on Ubuntu 22.04 LTS
    * Python 3.10+ is used to compile the program.
    * Scheduler works via simulated time instead of real time
    * Subsystem interacts with the scheduler through the API instead of utilizing access via internal structures.
    
1.2 Constraints
* No printing inside core functions, error codes instead of exceptions, and stable function signatures
* FCFS and RR scheduling must work
* Able to run through CLI and makefiles
* Must be modular for integration

1.3 System Environment
* Ubuntu 22.04 LTS
* Python 3.10+

2. Architecture
2.1 Overview
This program implements subsystem A in a modular, API-driven fashion to create a mini OS.


4.2 References
https://github.com/imayobrown/DesignDocumentTemplates/blob/master/DesignDocument.md for Design Document Template
