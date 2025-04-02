Proceso para la consulta de la API a Binance:

1. Obtener todos los pares de criptomonedas
2. Filtrar para tener solo pares contra USDT
3. Ordenar por volumen y quedarse con el top 50
4. Para cada par en el top 50:
   a. Obtener los datos de precio actual
   b. Calcular cambio de 1h usando velas OHLC
   c. Tomar el cambio de 24h directamente de los datos
   d. Calcular cambio de 7d usando velas OHLC
   e. Si es posible, consultar capitalización y suministro de una API secundaria
5. Mapear los tickers a nombres completos
6. Construir la estructura de datos final ordenada