# Requirement
Compares block numbers between two Ethereum providers (Ankr and Infura)
   - if Ankr blocknumber - Infura blocknumber < 5 => success
   - else => fail

# Run local 
```shell
pip install flask requests python-dotenv
pỵthon app.py
```

# Run with docker compose
```shell
docker-compose up --build
```

# Test
```shell
curl http://localhost:5000/block_diff_status
```
