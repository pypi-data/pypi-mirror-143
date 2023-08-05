# Cores_ft

Monitora a temperatura e frequências dos cores.

Para obter a frequencia dos cores foi usado o arquivo **/proc/cpuinfo**.

Para obter as temperatura do cores foi utilizado o utilitáqrio **sensors** do pacote **lm_sensors**


## Como usar

Criando o ambiente virtual e instalando pelo pip

```console
python -m venv .venv_test --upgrade-deps
pip install cores_ft
```

Para rodar basta fazer:

```console
python -m cores_ft
```
