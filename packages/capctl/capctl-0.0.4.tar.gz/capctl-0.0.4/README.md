# CAPCTL

CAP 유저 관리를 위한 CLI 툴

## Prerequisite
Python >= 3.6 설치   
## Install
```
pip install -r requirements.txt
pip install -e ./
```

## Quick Start 
### **user**  
1. **add (Create user)**
    ```
    > capctl user add \
    --email shhong3@dudaji.com \
    --password shhong3 \
    --username shhong3
    ```
1. **delete (Delete user (also leave in all projects))**
    ```
    # ex) Delete "shhong3@dudaji.com"
    > capctl user delete --email shhong3@dudaji.com
    ```
1. **password (Change password)**
    ```
    > capctl user password admin@kubeflow.org 'asdf!!'
    ```