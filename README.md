# Sprint_7

Тесты API Яндекс Самоката. Проверяю регистрацию и вход курьера, создание заказа и список заказов.

### Запуск

```bash
pip install -r requirements.txt
pytest --alluredir=target/allure-results --clean-alluredir
allure serve target/allure-results
```

Один тест падает, потому что курьер создаётся даже без `firstName`. [Отчёт Allure](allure-report/index.html)
