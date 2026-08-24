from pathlib import Path

p = Path('frente-build/app/src/main/java/com/nacho/frente/MainActivity.java')
s = p.read_text()

# Persistent round duration + round history.
s = s.replace('    private static final String KEY_SAVED_MIXES = "saved_mixes";\n',
'''    private static final String KEY_SAVED_MIXES = "saved_mixes";\n    private static final String KEY_ROUND_SECONDS = "round_seconds";\n''')

s = s.replace('    private List<String> replayWords = new ArrayList<>();\n',
'''    private List<String> replayWords = new ArrayList<>();\n    private final List<String> correctWords = new ArrayList<>();\n    private final List<String> passedWords = new ArrayList<>();\n    private int roundSeconds = 60;\n''')

s = s.replace('''        prefs = getSharedPreferences(PREFS, MODE_PRIVATE);\n        initWords();\n        loadCustomData();''',
'''        prefs = getSharedPreferences(PREFS, MODE_PRIVATE);\n        roundSeconds = Math.max(10, Math.min(600, prefs.getInt(KEY_ROUND_SECONDS, 60)));\n        initWords();\n        expandBuiltInWords();\n        loadCustomData();''')

expansion = r'''    private void addExtraWords(String name, String encoded) {
        List<String> base = builtInCategories.get(name);
        if (base == null) return;
        List<String> out = new ArrayList<>(base);
        for (String word : encoded.split("\\|")) {
            if (out.size() >= 100) break;
            String clean = word.trim();
            if (!clean.isEmpty()) out.add(clean);
        }
        builtInCategories.put(name, out);
    }

    private void expandBuiltInWords() {
        addExtraWords("Películas y series", "The Mandalorian|House of the Dragon|Better Call Saul|Lost|Dark|Narcos|Succession|The Last of Us|Euphoria|The Crown|Vikings|Cobra Kai|How I Met Your Mother|Modern Family|Brooklyn Nine-Nine|Rick y Morty|South Park|One Piece|Dragon Ball|Naruto|The Witcher|Arcane|Fallout|Dune|Oppenheimer|Barbie|Inception|El club de la lucha|Seven|El resplandor|Tiburón|Alien|Terminator 2|Blade Runner|Kill Bill|Django desencadenado|Mad Max|La La Land|Whiplash|Parasite|El silencio de los corderos|Cadena perpetua|El gran Lebowski|El lobo de Wall Street|Top Gun|Dirty Dancing|Grease|Pretty Woman|Eduardo Manostijeras|Beetlejuice");
        addExtraWords("Animales", "Gato|Perro|León|Tigre|Oso|Conejo|Vaca|Cerdo|Caballo|Gallina|Gallo|Pato|Oveja|Ciervo|Mono|Chimpancé|Guepardo|Hiena|Jaguar|Puma|Bisonte|Alce|Reno|Ardilla|Castor|Comadreja|Tejón|Chacal|Iguana|Lagarto|Rana|Sapo|Salamandra|Tritón|Pez payaso|Pez espada|Atún|Salmón|Calamar|Langosta|Gamba|Mejillón|Ostra|Estrella de mar|Abeja|Avispa|Libélula|Saltamontes|Ciempiés|Luciérnaga");
        addExtraWords("Objetos", "Teléfono|Bolígrafo|Lápiz|Cuaderno|Libro|Botella|Vaso|Taza|Plato|Tenedor|Cuchillo|Cuchara|Tabla de cortar|Rollo de papel|Caja|Sobre|Carpeta|Regla|Compás|Pegamento|Cinta adhesiva|Metrónomo|Parlante|Micrófono|Proyector|Pantalla|Impresora|Escáner|Memoria USB|Disco externo|Ratón de ordenador|Teclado|Despertador|Cronómetro|Monedero|Cartera|Gafas|Gorra|Cinturón|Zapato|Guante|Bufanda|Pulsera|Collar|Anillo|Paraguas plegable|Mosquetón|Cuerda|Escalera|Caja de herramientas");
        addExtraWords("Personajes famosos", "Kylian Mbappé|Erling Haaland|Lamine Yamal|Vinícius Jr.|Pau Gasol|Marc Márquez|Jorge Martín|Carlos Sainz|Lewis Hamilton|Max Verstappen|Novak Djokovic|Serena Williams|Simone Biles|Usain Bolt|Michael Jordan|Stephen Curry|Shaquille O'Neal|Neymar|Ronaldinho|Zinedine Zidane|George Clooney|Matt Damon|Ben Affleck|Chris Hemsworth|Chris Evans|Scarlett Johansson|Anne Hathaway|Emma Stone|Emma Watson|Timothée Chalamet|Jenna Ortega|Pedro Almodóvar|Javier Bardem|Úrsula Corberó|Mario Casas|Amaia Salamanca|Enrique Iglesias|Alejandro Sanz|C. Tangana|Lola Índigo|Rauw Alejandro|Ozuna|Daddy Yankee|Bruno Mars|The Weeknd|Justin Bieber|Selena Gomez|Katy Perry|Adele|Måneskin");
        addExtraWords("Videojuegos", "Terraria|Hollow Knight|Celeste|Cuphead|Undertale|Deltarune|Sekiro|Bloodborne|Darkest Dungeon|Dead Cells|Baldur's Gate 3|Diablo|Path of Exile|Mass Effect|Dragon Age|BioShock|Dishonored|Death Stranding|Ghost of Tsushima|Helldivers|Destiny|Warframe|Apex Legends|PUBG|Rainbow Six Siege|Battlefield|Team Fortress 2|Dota 2|Hearthstone|StarCraft|Warcraft III|XCOM|Total War|Cities: Skylines|SimCity|Euro Truck Simulator|Gran Turismo|Forza Horizon|Need for Speed|Trackmania|Tekken|Soulcalibur|Kingdom Hearts|Final Fantasy|Persona|Monster Hunter|Genshin Impact|Pokémon GO|Sea of Thieves|No Man's Sky");
        addExtraWords("Comida y bebida", "Salmorejo|Fabada|Cocido|Lentejas|Garbanzos|Arroz a banda|Fideuá|Pulpo a la gallega|Calamares|Boquerones|Patatas bravas|Huevos fritos|Tortitas|Magdalena|Bizcocho|Tiramisú|Crema catalana|Natillas|Arroz con leche|Mousse|Croissant|Baguette|Pan de ajo|Sándwich mixto|Hot dog|Burrito|Quesadilla|Ceviche|Poke|Tempura|Gyoza|Pad thai|Noodles|Katsu curry|Hummus|Cuscús|Shawarma|Moussaka|Fondue|Raclette|Mango|Kiwi|Melocotón|Pera|Manzana|Cereza|Uva|Melón|Granada|Mandarina");
        addExtraWords("Países y lugares", "Alemania|Reino Unido|Irlanda|Noruega|Suecia|Finlandia|Islandia|Grecia|Turquía|Marruecos|Sudáfrica|India|Tailandia|Vietnam|Corea del Sur|Indonesia|Nueva Zelanda|Chile|Perú|Colombia|Cuba|Estados Unidos|Suiza|Austria|Bélgica|Praga|Berlín|Viena|Dublín|Estocolmo|Copenhague|Atenas|Estambul|Marrakech|Dubái|Singapur|Bangkok|Seúl|Tokio|Sídney|Río de Janeiro|Buenos Aires|Ciudad de México|San Francisco|Miami|Alaska|Patagonia|Islas Maldivas|Gran Cañón|Niágara");
        addExtraWords("Profesiones", "Ingeniero|Ingeniero informático|Desarrollador de videojuegos|Artista 3D|Animador|Diseñador gráfico|Diseñador de interiores|Contable|Economista|Banquero|Notario|Procurador|Fiscal|Cirujano|Pediatra|Fisioterapeuta|Nutricionista|Óptico|Técnico de laboratorio|Paramédico|Conductor de autobús|Maquinista|Marinero|Azafato|Controlador aéreo|Mensajero|Cartero|Dependiente|Cajero|Comercial|Community manager|Editor|Escritor|Guionista|Productor|Ilustrador|Escultor|Músico|Bailarín|Coreógrafo|Entrenador personal|Árbitro|Geólogo|Biólogo|Químico|Meteorólogo|Ingeniero agrónomo|Cerrajero|Soldador|Relojero");
        addExtraWords("Acciones", "Caminar|Gatear|Arrastrarse|Agacharse|Levantarse|Sentarse|Tumbarse|Girar|Dar una voltereta|Hacer una pirueta|Lanzar|Atrapar|Empujar|Tirar|Levantar peso|Golpear|Patear|Chutar un balón|Botar una pelota|Encestar|Brindar|Comer|Beber|Masticar|Tragar|Oler|Probar comida|Cortar|Pelar|Mezclar|Fregar platos|Tender la ropa|Doblar ropa|Pasar la aspiradora|Hacer la cama|Regar plantas|Ducharse|Lavarse el pelo|Peinarse|Vestirse|Desvestirse|Coser|Tejer|Hacer crochet|Pintar|Tocar el piano|Hacer una llamada|Mandar un mensaje|Comprar|Pagar");
        addExtraWords("Deportes", "Fútbol sala|Fútbol americano|Baloncesto 3x3|Tenis de mesa|Squash|Frontón|Pelota vasca|Lacrosse|Polo|Hockey sobre hielo|Hockey hierba|Patinaje de velocidad|Patinaje en línea|Curling|Bobsleigh|Skeleton|Biathlon|Esquí de fondo|Salto de esquí|Windsurf|Vela|Rafting|Wakeboard|Esquí acuático|Paddle surf|Snorkel|Apnea|Orientación|Trail running|Carrera de obstáculos|Decatlón|Lanzamiento de jabalina|Lanzamiento de disco|Salto de altura|Salto de longitud|Salto con pértiga|Marcha atlética|Powerlifting|Strongman|Muay Thai|Kickboxing|Jiu-jitsu|MMA|Sumo|Capoeira|Bolos|Petanca|Disc golf|Ultimate frisbee|Carrera de karts");
        addExtraWords("Música", "Clarinete|Oboe|Fagot|Violonchelo|Contrabajo|Trombón|Tuba|Mandolina|Banjo|Castañuelas|Pandereta|Cajón flamenco|Gaita|Sintetizador|Caja de ritmos|Mesa de mezclas|Amplificador|Pedal de efectos|Afinador|Partitura|Acorde|Escala musical|Melodía|Armonía|Tempo|Compás|Improvisación|Remix|Mashup|Sample|Indie|Blues|Soul|Funk|Disco music|House|Trance|Drum and bass|Punk|Grunge|Country|Bachata|Salsa|Merengue|Rumba|Trap|Lo-fi|Banda sonora|Musical|Ensayo");
        addExtraWords("Tecnología", "Portátil|Smart TV|Ebook|Consola portátil|Gafas VR|Sensor|Microchip|Placa base|Fuente de alimentación|Ventilador de PC|SSD|Tarjeta SD|Cable HDMI|Ethernet|NFC|5G|Antena|Punto de acceso|Código de barras|Escáner biométrico|Domótica|Bombilla inteligente|Termostato inteligente|Cámara de seguridad|Impresión láser|CNC|Brazo robótico|Coche autónomo|Coche eléctrico|Panel solar|Batería de litio|Criptografía|Blockchain|Base de datos|API|Algoritmo|Compilador|Sistema operativo|Linux|Windows|Android|iOS|GitHub|Control de versiones|Terminal|Firewall|VPN|Centro de datos|Superordenador|Computación cuántica");
        addExtraWords("Personajes ficticios", "Luke Skywalker|Leia Organa|Han Solo|Obi-Wan Kenobi|Anakin Skywalker|Chewbacca|Thanos|Capitán América|Viuda Negra|Doctor Strange|Black Panther|Loki|Aquaman|Harley Quinn|Flash|Green Lantern|Robin|Catwoman|Lex Luthor|Magneto|Profesor X|Dumbledore|Voldemort|Hagrid|Ron Weasley|Gollum|Aragorn|Legolas|Sauron|Daenerys Targaryen|Jon Snow|Tyrion Lannister|Walter White|Jesse Pinkman|Saul Goodman|Eleven|Dustin Henderson|Rick Sanchez|Morty Smith|Peter Griffin|Stewie Griffin|Bugs Bunny|Tom y Jerry|Popeye|Doraemon|Ash Ketchum|Link|Master Chief|Nathan Drake|Joel Miller");
        addExtraWords("Marcas", "Puma|Reebok|New Balance|Converse|Vans|Under Armour|Asics|Uniqlo|H&M|Mango|Primark|Shein|Temu|AliExpress|eBay|Wallapop|Vinted|Uber|Cabify|Booking|Expedia|Ryanair|Iberia|Vueling|Renfe|Seat|Cupra|Audi|Porsche|Lamborghini|Ford|Honda|Hyundai|Kia|Volvo|Jeep|GoPro|DJI|Xiaomi|Huawei|Lenovo|HP|Dell|Logitech|Razer|Corsair|AMD|Meta|Adobe|PayPal");
        addExtraWords("Historia y cultura", "Alejandro Magno|Sócrates|Platón|Aristóteles|Marco Aurelio|Nerón|Espartaco|Juana de Arco|Isabel la Católica|Fernando el Católico|William Shakespeare|Galileo Galilei|Isaac Newton|Mozart|Beethoven|Van Gogh|Goya|Dalí|Frida Kahlo|Andy Warhol|Tutankamón|Ramsés II|Pompeya|Troya|Acrópolis|Partenón|Alhambra|Mezquita de Córdoba|Camino de Santiago|Revolución industrial|Guerra Civil Española|Guerra Fría|Muro de Berlín|Desembarco de Normandía|Ruta de la Seda|Imperio bizantino|Imperio otomano|Mayas|Aztecas|Incas|Caballero medieval|Gladiador|Faraón|Momia|Jeroglífico|Pergamino|Imprenta|Máquina de vapor|Telescopio|Pintura rupestre");
        addExtraWords("Casa y vida diaria", "Microondas|Tostadora|Cafetera|Hervidor|Batidora|Licuadora|Freidora de aire|Campana extractora|Fregadero|Grifo|Escurridor|Mantel|Servilleta|Vajilla|Cubiertos|Tupper|Fiambrera|Estantería|Escritorio|Cómoda|Mesita de noche|Cabecero|Colchón|Almohada|Edredón|Perchero|Zapatero|Espejo|Secador|Plancha de pelo|Maquinilla de afeitar|Desodorante|Perfume|Crema hidratante|Botiquín|Termómetro|Mopa|Cubo de basura|Tendedero|Pinza de ropa|Tabla de planchar|Cesta de ropa|Trastero|Pasillo|Patio|Jardín|Valla|Buzón|Videoportero|Aire acondicionado");
        addExtraWords("Internet y redes", "Short|Story|Thread|Hilo|Retuit|Compartir|Guardar publicación|Etiqueta|Mención|DM|Servidor de Discord|Canal de voz|Chat en directo|Emote|Suscriptor|Donación|Bits|Raid|Clip|VOD|Newsletter|Blog|Foro|Wiki|Buscador|Enlace|Hipervínculo|URL|Dominio|Página de inicio|Banner|Anuncio|Adblock|Ventana emergente|Código promocional|Sorteo|Unboxing|Review|Tutorial|Gameplay|Challenge|Trend|Dueto|Stitch de TikTok|Verificado|Cuenta privada|Cuenta bloqueada|Silenciar|Reportar|Deslizar");
    }

'''
s = s.replace('    private void loadCustomData() {', expansion + '    private void loadCustomData() {', 1)

# Reset per-round word histories.
s = s.replace('''        score = 0;\n        skipped = 0;\n        showCountdown();''',
'''        score = 0;\n        skipped = 0;\n        correctWords.clear();\n        passedWords.clear();\n        showCountdown();''')

# Menu: dynamic word count/time + duration control.
s = s.replace('TextView meta = text("850 palabras · 17 categorías · 60 segundos", 13, false);',
              'TextView meta = text("1700 palabras · 17 categorías · " + roundSeconds + " s", 13, false);')

menu_anchor = '''        root.addView(creatorRow, new LinearLayout.LayoutParams(-1, -2));\n\n        Button mixAll = button("🎲  Mezcla de todo");'''
menu_replacement = '''        root.addView(creatorRow, new LinearLayout.LayoutParams(-1, -2));\n\n        Button roundTime = button("⏱  Duración de ronda: " + roundSeconds + " s");\n        styleButton(roundTime, Color.rgb(42, 48, 76), TEXT_LIGHT);\n        roundTime.setOnClickListener(v -> showRoundTimeDialog());\n        root.addView(roundTime, menuButtonParams());\n\n        Button mixAll = button("🎲  Mezcla de todo");'''
s = s.replace(menu_anchor, menu_replacement, 1)

time_dialog = r'''    private void saveRoundSeconds(int seconds) {
        roundSeconds = Math.max(10, Math.min(600, seconds));
        prefs.edit().putInt(KEY_ROUND_SECONDS, roundSeconds).apply();
        showMenu();
    }

    private void showRoundTimeDialog() {
        final String[] labels = {"30 segundos", "45 segundos", "60 segundos", "90 segundos", "2 minutos", "3 minutos", "Personalizado…"};
        final int[] values = {30, 45, 60, 90, 120, 180};
        new AlertDialog.Builder(this)
                .setTitle("Duración de la ronda")
                .setItems(labels, (dialog, which) -> {
                    if (which < values.length) {
                        saveRoundSeconds(values[which]);
                        return;
                    }
                    EditText input = editField("Segundos (10 - 600)", false);
                    input.setInputType(InputType.TYPE_CLASS_NUMBER);
                    input.setText(String.valueOf(roundSeconds));
                    input.setSelectAllOnFocus(true);
                    int pad = dp(24);
                    FrameLayout holder = new FrameLayout(this);
                    holder.setPadding(pad, dp(8), pad, 0);
                    holder.addView(input, new FrameLayout.LayoutParams(-1, -2));
                    new AlertDialog.Builder(this)
                            .setTitle("Tiempo personalizado")
                            .setView(holder)
                            .setPositiveButton("Guardar", (d, w) -> {
                                try {
                                    int seconds = Integer.parseInt(input.getText().toString().trim());
                                    saveRoundSeconds(seconds);
                                } catch (NumberFormatException ex) {
                                    Toast.makeText(this, "Introduce un número entre 10 y 600", Toast.LENGTH_SHORT).show();
                                }
                            })
                            .setNegativeButton("Cancelar", null)
                            .show();
                })
                .setNegativeButton("Cancelar", null)
                .show();
    }

'''
s = s.replace('    private LinearLayout.LayoutParams menuButtonParams() {',
              time_dialog + '    private LinearLayout.LayoutParams menuButtonParams() {', 1)

# Timer uses chosen duration.
s = s.replace('timerView = text("⏱  60", 23, true);',
              'timerView = text("⏱  " + roundSeconds, 23, true);')
s = s.replace('roundTimer = new CountDownTimer(60000, 1000) {',
              'roundTimer = new CountDownTimer(roundSeconds * 1000L, 1000) {')

# Record the actual word before moving to the next one.
s = s.replace('''        candidateDirection = 0;\n        candidateSince = 0L;\n\n        if (correct) {''',
'''        candidateDirection = 0;\n        candidateSince = 0L;\n\n        String answeredWord = wordView == null ? "" : wordView.getText().toString().trim();\n        if (correct) {\n            if (!answeredWord.isEmpty()) correctWords.add(answeredWord);''', 1)
s = s.replace('''        } else {\n            skipped++;\n            vibrate(35);''',
'''        } else {\n            if (!answeredWord.isEmpty()) passedWords.add(answeredWord);\n            skipped++;\n            vibrate(35);''', 1)

# Detailed results screen: show every correct and passed/failed word.
def replace_block(text, start_marker, end_marker, replacement):
    a = text.index(start_marker)
    b = text.index(end_marker, a)
    return text[:a] + replacement + text[b:]

results = r'''    private void finishRound() {
        if (!playing) return;
        playing = false;
        unregisterSensors();
        stopRound();

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackground(gradientBg(BG_DARK, Color.rgb(35, 29, 77), 0));

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER_HORIZONTAL);
        root.setPadding(dp(28), dp(18), dp(28), dp(28));
        scroll.addView(root, new ScrollView.LayoutParams(-1, -2));

        TextView over = text("RONDA TERMINADA", 17, true);
        over.setTextColor(TEXT_MUTED);
        over.setLetterSpacing(0.12f);
        root.addView(over, new LinearLayout.LayoutParams(-1, -2));

        TextView result = text(String.valueOf(score), 80, true);
        result.setTextColor(Color.rgb(83, 214, 139));
        result.setPadding(dp(8), 0, dp(8), 0);
        root.addView(result, new LinearLayout.LayoutParams(-1, -2));

        TextView label = text("✓ " + score + " acertadas   ·   ↗ " + skipped + " falladas", 18, true);
        label.setTextColor(TEXT_LIGHT);
        root.addView(label, new LinearLayout.LayoutParams(-1, -2));

        TextView cat = text(selectedCategory + "   ·   " + roundSeconds + " s", 14, true);
        cat.setTextColor(TEXT_MUTED);
        cat.setBackground(roundedBg(SURFACE, 14));
        LinearLayout.LayoutParams catp = new LinearLayout.LayoutParams(-2, -2);
        catp.setMargins(0, dp(6), 0, dp(10));
        root.addView(cat, catp);

        TextView goodTitle = sectionLabel("✓  ACERTADAS  (" + correctWords.size() + ")");
        goodTitle.setTextColor(Color.rgb(112, 225, 158));
        root.addView(goodTitle, new LinearLayout.LayoutParams(-1, -2));
        if (correctWords.isEmpty()) {
            TextView empty = text("Ninguna palabra acertada", 15, false);
            empty.setTextColor(TEXT_MUTED);
            root.addView(empty, new LinearLayout.LayoutParams(-1, -2));
        } else {
            for (String word : correctWords) {
                TextView row = text("✓   " + word, 17, true);
                row.setGravity(Gravity.START | Gravity.CENTER_VERTICAL);
                row.setTextColor(TEXT_LIGHT);
                row.setBackground(roundedBg(Color.rgb(31, 71, 58), 14));
                LinearLayout.LayoutParams rp = new LinearLayout.LayoutParams(-1, dp(48));
                rp.setMargins(0, dp(3), 0, dp(3));
                root.addView(row, rp);
            }
        }

        TextView badTitle = sectionLabel("↗  FALLADAS / PASADAS  (" + passedWords.size() + ")");
        badTitle.setTextColor(Color.rgb(242, 142, 142));
        root.addView(badTitle, new LinearLayout.LayoutParams(-1, -2));
        if (passedWords.isEmpty()) {
            TextView empty = text("Ninguna palabra fallada", 15, false);
            empty.setTextColor(TEXT_MUTED);
            root.addView(empty, new LinearLayout.LayoutParams(-1, -2));
        } else {
            for (String word : passedWords) {
                TextView row = text("↗   " + word, 17, true);
                row.setGravity(Gravity.START | Gravity.CENTER_VERTICAL);
                row.setTextColor(TEXT_LIGHT);
                row.setBackground(roundedBg(Color.rgb(83, 43, 53), 14));
                LinearLayout.LayoutParams rp = new LinearLayout.LayoutParams(-1, dp(48));
                rp.setMargins(0, dp(3), 0, dp(3));
                root.addView(row, rp);
            }
        }

        LinearLayout buttons = new LinearLayout(this);
        buttons.setOrientation(LinearLayout.HORIZONTAL);
        buttons.setGravity(Gravity.CENTER);
        Button again = button("↻  Otra ronda");
        styleButton(again, ACCENT, Color.WHITE);
        again.setOnClickListener(v -> startCategory(selectedCategory, replayWords));
        Button menu = button("☰  Categorías");
        styleButton(menu, SURFACE_2, TEXT_LIGHT);
        menu.setOnClickListener(v -> showMenu());
        LinearLayout.LayoutParams bp = new LinearLayout.LayoutParams(0, dp(60), 1);
        bp.setMargins(dp(6), dp(20), dp(6), 0);
        buttons.addView(again, bp);
        buttons.addView(menu, bp);
        root.addView(buttons, new LinearLayout.LayoutParams(-1, -2));

        setContentView(scroll);
    }

'''
s = replace_block(s, '    private void finishRound()', '    private void resetGestureState()', results)

p.write_text(s)
print('Frente v1.3 applied')
