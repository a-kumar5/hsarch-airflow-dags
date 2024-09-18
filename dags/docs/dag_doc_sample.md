# DAG Name: {{ DAG_NAME }}

## Overview
Provide a brief description of what the DAG is designed to do. Mention the system or process it integrates with, and any important context.

- **Owner**: [Team or Person responsible]
- **Schedule**: How frequently the DAG runs (e.g., `@daily`, `0 6 * * *`)
- **Start Date**: Date when the DAG starts execution
- **Catchup**: Whether catchup is enabled or disabled
- **Tags**: List of any tags associated with the DAG

## Purpose
Explain the overall business or technical goal the DAG is addressing.

## Process Overview
Describe, at a high level, the sequence of tasks and how they contribute to the overall goal of the DAG.

### Key Points
- **Dependencies**: Mention any external dependencies (e.g., databases, cloud services, or APIs).
- **Failure Handling**: Describe how failures are handled (e.g., retries, alerting mechanisms).
- **Expected Runtime**: Mention the average runtime or expected duration of the DAG.
- **Logs**: Where to find logs or error details (e.g., S3, CloudWatch, Airflow UI).

## Contact Information
For issues related to this DAG, contact: [Contact Info]

## Sample Logs
If applicable, provide an example of the kind of logs generated for debugging or monitoring.

---

### Task-Level Documentation (for `doc_md` in individual tasks)
```markdown
## Task Name: {{ TASK_NAME }}

### Overview
Provide a short explanation of what this task does. Explain the task's purpose and how it contributes to the overall DAG.

- **Operator**: [Operator used in the task, e.g., BashOperator, PythonOperator]
- **Execution Time**: Approximate time this task takes to execute.
- **Retries**: How many retries are configured, if applicable.

### Inputs
List any inputs, such as files, database queries, or parameters this task relies on.

### Outputs
List the outputs or results produced by this task (e.g., files, database updates, API responses).

### Success Criteria
Mention what determines the success of this task (e.g., a file is generated, or an API call returns a 200 response).

### Failure Handling
Explain what happens if the task fails. Is it retried, skipped, or does it notify someone?

## Task Dependencies
- Preceding Task(s): [List of tasks that must complete before this task]
- Following Task(s): [List of tasks triggered after this task]