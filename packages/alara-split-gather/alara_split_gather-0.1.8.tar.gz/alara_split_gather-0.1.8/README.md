## alara\_split\_gather
This package is used to:
- split a large ALARA input file to smaller sub-tasks,
- check the status of sub-tasks,
- gather all phtn_src file

## Installation

```bash
pip install alara-split-gather
```

## Basic usage
### Help info
```bash
alara_split_task -h
```

### Split task
```
alara_split_task -i [alara_inp] -n [num_tasks]
```

### Check status
```
alara_tasks_status
```

### Gather outputs of sub-tasks
```
alara_gather_tasks -p phtn_src
```

## Notes
Refer to '-h' or source code for detalied usage.
