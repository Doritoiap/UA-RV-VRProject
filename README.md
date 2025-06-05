# Proyecto VR Meta Quest 3 – Aim Master VR

## Descripción de la experiencia

El jugador se encuentra en un entorno virtual donde su primera tarea es localizar y recoger tanto un arma como un escudo, necesarios para sobrevivir. Una vez equipado, el objetivo principal consiste en explorar el escenario, localizar a los enemigos repartidos por el mapa y eliminarlos utilizando las herramientas recogidas.

---

## Cómo jugar / Controles

VR:
![T_Quest2_controller](https://github.com/user-attachments/assets/59cbbd95-cbe7-4837-b7cd-ca78cd63be71)

PC:
- **Moverse:** WASD
- **Interactuar:** E
- **Acceder al menú de pausa:** ESC
- **Disparar:** Click Izquierdo

---

## Licencias

Todos los assets, sonidos y recursos usados en este proyecto provienen de fuentes con licencias libres para uso en videojuegos y han sido correctamente referenciados:

Audio:
- Crate-break-1-93926 – Content/Audio/S_crate-break-1-93926 – CC0 – https://pixabay.com/sound-effects/crate-break-1-93926/
- Large Metal Lift Door Opening – Content/Audio/S_DoorOpen – CC0 – https://pixabay.com/sound-effects/large-metal-lift-door-openingwav-14459/
- Explosion 9 – Content/Audio/S_explosion-9-340460 – CC0 – https://pixabay.com/sound-effects/explosion-9-340460/
- Laser – Content/Audio/S_laser_sound – CC0 – https://pixabay.com/sound-effects/laser-14792/
- 005479_Tense creepy atmosphere – Content/Audio/S_005479_tense-creepy-atmosphere-51160 – CC0 – https://pixabay.com/sound-effects/005479-tense-creepy-atmosphere-51160/
- [Ejemplo: "Wind Ambience.wav" – Content/Sounds/WindAmbience – Pixabay Audio License – https://pixabay.com/es/music/"]

Modelos:
- Meta Quest Pro Left Controller – Content/Models/Controllers/MetaQuestTouchPro_Left – CC Attribution-NoDerivs – https://sketchfab.com/3d-models/meta-quest-pro-left-controller-b65700705dec4df9a12dd9e31933fb62
- Meta Quest Pro Right Controller – Content/Models/Controllers/MetaQuestTouchPro_Right – CC Attribution-NoDerivs – https://sketchfab.com/3d-models/meta-quest-pro-right-controller-76a1fbb0530842eea882019bcfe51b79

Imágenes:
- Meta Quest Hardware Art – Content/Textures/T_Quest2_controller – Meta License – https://developers.meta.com/horizon/downloads/package/oculus-controller-art/?locale=en_GB

Se han usado algunas texturas de ambientcg y opengameart con licencia Creative Commons CC0 las cuales posteriormente han sido altamente modificadas con Photoshop y convertido en nuevas imágenes.
Enlaces:
- https://ambientcg.com/
- https://opengameart.org/
  
Texturas que usan esto:
- Content/Textures/T_Baldosa_difusse
- Content/Textures/T_Scifi_Panel6_difusse
- Content/Textures/T_Scifi_Panel6_difusse_AZUL
- Content/Textures/T_SueloBig_Diffuse
- Content/Textures/T_Vault_Diffuse
- Content/Textures/T_vault_hight_Diffuse

---

## Entrevista / Proceso de creación

### Dificultades encontradas y soluciones
- #### ¿Qué dificultades has encontrado durante el desarrollo? ¿Cómo las has resuelto?
  El primer desafío al que tuve que enfrentarme fue desarrollar una versión para Meta Quest 3 sin disponer físicamente del dispositivo. Para poder probar las funcionalidades básicas, fue necesario crear una versión para PC que integrase, de la manera más fiel posible, las mecánicas principales del juego. Sin embargo, no siempre era posible replicar exactamente las mismas interacciones, ya que ciertos elementos, como el manejo de objetos con los mandos o el uso de widgets, funcionan de manera diferente en PC y en realidad virtual. Más adelante, utilicé Meta XR Simulator, lo que me permitió simular de forma mucho más precisa las características y funciones específicas de Meta Quest 3, facilitando así el desarrollo y la adaptación al entorno VR.

  Otra de las dificultades encontradas fue el desarrollo del sistema de disparo, especialmente en el caso de los enemigos. El reto no residía tanto en la complejidad técnica, sino en la falta de experiencia inicial con Blueprints y en la lógica de las colisiones. Aunque la implementación básica del Raycast fue relativamente sencilla, pronto surgieron nuevos retos: había que considerar, por ejemplo, si el enemigo realmente veía al jugador dentro de su radio de acción. Si tenía línea de visión, debía disparar el láser, si no, debía permanecer inactivo. Además, el sistema debía detectar si el disparo impactaba en el escudo o directamente en el jugador y actuar en consecuencia. Inicialmente, fue complicado gestionar la referencia y comunicación entre actores, pero una vez superado este obstáculo, se facilitó mucho la comprensión y el desarrollo del resto de sistemas del proyecto.

  Por último, uno de los retos más complejos a los que me enfrenté fue la implementación del teletransporte. Inicialmente, intenté desarrollar mi propio sistema basándome únicamente en la lógica que creía conveniente, sin utilizar una trayectoria parabólica y mostrando solo un marcador en el suelo. Mi objetivo era no recurrir a la plantilla de Unreal Engine para VR, que no se ha utilizado en el proyecto. Ante la falta de resultados, comencé a investigar más a fondo y descubrí que muchos desarrolladores empleaban un sistema basado en NavMesh, el cual desconocía por completo hasta ese momento. Gracias a varios tutoriales y vídeos en YouTube, conseguí implementar un sistema de teletransporte funcional, incluyendo la visualización de la parábola para indicar el destino del movimiento. Aunque el sistema aún no es perfecto, incluido a nivel visual, cumple su función correctamente.


### Siguientes pasos

Si tuviera más tiempo, me gustaría:
- Mejorar el juego a nivel visual:
Reemplazaría los elementos provisionales por modelos, materiales y texturas definitivos, creando assets personalizados para el entorno y los objetos.

- Diseñar un nivel más elaborado:
Planificaría cuidadosamente la distribución de enemigos, objetos y rutas, pensando en el ritmo y el flujo de la experiencia para el jugador.

- Optimizar y balancear el sistema de disparos:
Revisaría y ajustaría la lógica de disparo tanto para el jugador como para los enemigos, realizando pruebas para equilibrar las distancias de detección y disparo, asegurando una jugabilidad más justa y divertida.

- Mejorar el feedback visual y sonoro en el combate:
Implementaría nuevos efectos visuales y sonidos que aporten feedback e inmersión a las acciones durante el combate.

- Aplicar técnicas de optimización:
Mejoraría el rendimiento utilizando reducción de polígonos, optimización de texturas, LODs entre otras cosas para garantizar una experiencia fluida en Meta Quest 3.

- Ampliar la variedad de enemigos y su comportamiento:
Desarrollaría nuevos tipos de enemigos y crearía distintos patrones de comportamiento para ofrecer mayores desafíos y variedad al jugador.

