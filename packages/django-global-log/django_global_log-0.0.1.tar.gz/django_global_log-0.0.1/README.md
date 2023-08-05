## Django Global Log

### 注册到 `installed_apps` 中

```python
INSTALLED_APPS = [
    "corsheaders",
    "django_global_log",
    ···
]
```

### 添加 `middleware`

```python
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django_global_log.middlewares.DjangoGlobalLogMiddleware",
    ···
]
```
