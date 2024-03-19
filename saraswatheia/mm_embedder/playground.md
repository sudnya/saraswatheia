# React app

Call a Multimodal Model from this web app.

First, get `<YOUR-SARASWATHEIA-API-KEY>` at [https://TODO-SUDNYA/account](https://TODO-SUDNYA/account).

Add the key to a config file ~/.mm_embedder/mm_embedder.yaml

```yaml
key: <YOUR-SARASWATHEIA-API-KEY>
url: https://BLAH
```

# Start the app

Start the app.

```bash
cd saraswatheia/mm_embedder
./mm_embedder-up
```

Navigate to the app [http://localhost:5001](http://localhost:5001).

# Edit the prompt

Edit the prompt in the [python backend](backend/fastapi/main.py.py#L59C1-L60C1)

