# Jugador Autónomo para HEX

## Explicación de la Estrategia 

`MinimaxPlayer`: Jugador autónomo que hereda de la clase `Player` y consiste en un algoritmo minimax con poda alfa-beta para obtener la mejor jugada. Pero al tener el juego Hex un inmenso árbol de estados, se tomó un parámetro `depth` para detener el algoritmo cuando este llegue a cero, retornando la mejor jugada entre todas las candidatas. Para poder evaluar si una jugada es mejor que otra se utiliza una heurística para determinar cuál de todos los jugadores controla el centro del tablero. 

`MCTSPlayer`: Otro jugador autónomo que hereda de la clase `Player`. Este es una mejor alternativa ante la estrategia implementada en `MinimaxPlayer`. Este jugador obtiene una buena jugada basándose en Monte Carlo Tree Search

## Monte Carlo Tree Search

**Monte Carlo Tree Search** es un algoritmo de *búsqueda heurística* utilizado para procesos de toma de decisiones en entornos complejos, por ejemplo: juegos con enormes espacios de estado, como el juego Hex. MCTS se basa en la búsqueda inteligente en árbol que equilibra la exploración y la explotación. El enfoque de MCTS se centra en el análisis de los movimientos más prometedores, expandiendo el árbol de búsqueda basado en el muestreo aleatorio del espacio de búsqueda.