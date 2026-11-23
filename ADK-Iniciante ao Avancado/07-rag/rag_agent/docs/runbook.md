# Runbook: API de pagamentos lenta
1. Verifique o p95 de latência no dashboard.
2. Se o pool de conexões do banco estiver esgotado, aumente `max_connections` ou reinicie o serviço.
3. Escale o deployment se a CPU passar de 80%.
