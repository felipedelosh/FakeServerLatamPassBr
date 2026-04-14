<h1 align="center"> LATAM PASS BR Fake Server </h1>
<br>
<h4>Mock server built with Python + Flask for LATAM PASS BR integrations</h4>

![Banner](Docs/banner.png)
<br>
:construction: Active Development  
This repository simulates the **LATAM PASS BR APIs** used in the integration layer, allowing local development and testing before connecting to real external services. :construction:
<br><br>

The objective of this project is to provide a local fake server capable of handling **different protocols in the same application**:

- **SOAP/XML**
- **REST/JSON**

This is necessary because the LATAM PASS BR integration is not homogeneous. Some operations are exposed through **SOAP/XML**, while others follow a **REST/JSON** approach.


The server follows a **clean layered architecture**, using:
> `Controller → UseCase → Service → Repository`

---

## Objective

Build a Flask-based fake server that can receive and respond to the same type of calls expected by the real LATAM PASS BR integrations.

This server is intended for:

- local development
- contract understanding
- request/response validation
- integration testing without real credentials
- progressive implementation while real access is pending

---

## Install requirements.txt


```
C:\Users\docto\AppData\Local\Programs\Python\Python313\python.exe -m pip install -r requirements.txt
```
```
pip install -r requirements.txt
```

## :play_or_pause_button:How to execute a project

```
C:\Users\docto\AppData\Local\Programs\Python\Python313\python.exe run.py
```
```
python run.py
```

## Supported protocols

### SOAP/XML
These operations must be handled as SOAP endpoints, not as regular REST resources:

- submit accumulation
- accumulation status query

### REST/JSON
These operations must be handled as REST endpoints:

- login
- oauth token
- user info
- redeem
- accumulation token
- create accumulation
- status accumulation

---

## Important architectural note

This project is **not only a REST mock**.

It must support a **mixed integration model**, where:

- some endpoints receive **SOAP envelopes in XML**
- others receive and return **JSON**
- authentication-related endpoints may use special formats such as:
  - query params
  - form-urlencoded
  - bearer tokens
  - basic auth

Because of that, the implementation must clearly separate protocol handling and business intent.

---

## Autor

| [<img src="https://avatars.githubusercontent.com/u/38327255?v=4" width=115><br><sub>Andrés Felipe Hernánez</sub>](https://github.com/felipedelosh)|
| :---: |
