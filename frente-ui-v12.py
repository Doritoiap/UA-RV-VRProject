from pathlib import Path

p = Path('frente-build/app/src/main/java/com/nacho/frente/MainActivity.java')
s = p.read_text()

if 'import android.graphics.drawable.GradientDrawable;' not in s:
    s = s.replace('import android.graphics.Typeface;\n', 'import android.graphics.Typeface;\nimport android.graphics.drawable.GradientDrawable;\n')

def replace_block(text, start_marker, end_marker, replacement):
    a = text.index(start_marker)
    b = text.index(end_marker, a)
    return text[:a] + replacement + text[b:]

helpers = r'''    private static final int BG_DARK = Color.rgb(15, 18, 31);
    private static final int SURFACE = Color.rgb(31, 35, 54);
    private static final int SURFACE_2 = Color.rgb(43, 48, 70);
    private static final int TEXT_LIGHT = Color.rgb(248, 250, 252);
    private static final int TEXT_MUTED = Color.rgb(174, 181, 204);
    private static final int ACCENT = Color.rgb(112, 92, 255);
    private static final int ACCENT_2 = Color.rgb(59, 130, 246);

    private GradientDrawable roundedBg(int color, int radiusDp) {
        GradientDrawable d = new GradientDrawable();
        d.setColor(color);
        d.setCornerRadius(dp(radiusDp));
        return d;
    }

    private GradientDrawable gradientBg(int start, int end, int radiusDp) {
        GradientDrawable d = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                new int[]{start, end});
        d.setCornerRadius(dp(radiusDp));
        return d;
    }

    private TextView text(String value, int sizeSp, boolean bold) {
        TextView v = new TextView(this);
        v.setText(value);
        v.setTextColor(Color.rgb(24, 24, 24));
        v.setTextSize(sizeSp);
        v.setGravity(Gravity.CENTER);
        v.setPadding(dp(14), dp(10), dp(14), dp(10));
        v.setTypeface(Typeface.create("sans-serif", bold ? Typeface.BOLD : Typeface.NORMAL));
        return v;
    }

    private void styleButton(Button b, int background, int textColor) {
        b.setBackground(roundedBg(background, 17));
        b.setTextColor(textColor);
        b.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        b.setPadding(dp(14), dp(8), dp(14), dp(8));
        b.setElevation(dp(2));
    }

    private Button button(String label) {
        Button b = new Button(this);
        b.setText(label);
        b.setTextSize(17);
        b.setAllCaps(false);
        b.setMinHeight(dp(54));
        styleButton(b, SURFACE, TEXT_LIGHT);
        return b;
    }

    private TextView sectionLabel(String label) {
        TextView v = text(label, 13, true);
        v.setGravity(Gravity.START | Gravity.CENTER_VERTICAL);
        v.setTextColor(TEXT_MUTED);
        v.setLetterSpacing(0.08f);
        v.setPadding(dp(4), dp(22), dp(4), dp(6));
        return v;
    }

    private String categoryIcon(String name) {
        switch (name) {
            case "Películas y series": return "🎬";
            case "Animales": return "🐾";
            case "Objetos": return "🎒";
            case "Personajes famosos": return "⭐";
            case "Videojuegos": return "🎮";
            case "Comida y bebida": return "🍕";
            case "Países y lugares": return "🌍";
            case "Profesiones": return "🧑‍🚒";
            case "Acciones": return "🕺";
            case "Deportes": return "🏆";
            case "Música": return "🎵";
            case "Tecnología": return "💻";
            case "Personajes ficticios": return "🦸";
            case "Marcas": return "🛍️";
            case "Historia y cultura": return "🏛️";
            case "Casa y vida diaria": return "🏠";
            case "Internet y redes": return "📱";
            default: return "✨";
        }
    }

'''
s = replace_block(s, '    private TextView text(', '    private void showMenu()', helpers)

menu = r'''    private void showMenu() {
        stopRound();
        playing = false;
        unregisterSensors();
        hideSystemUi();

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackground(gradientBg(BG_DARK, Color.rgb(27, 24, 62), 0));

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER_HORIZONTAL);
        root.setPadding(dp(28), dp(18), dp(28), dp(28));
        scroll.addView(root, new ScrollView.LayoutParams(-1, -2));

        LinearLayout hero = new LinearLayout(this);
        hero.setOrientation(LinearLayout.VERTICAL);
        hero.setGravity(Gravity.CENTER);
        hero.setPadding(dp(24), dp(14), dp(24), dp(14));
        hero.setBackground(gradientBg(ACCENT, ACCENT_2, 24));
        hero.setElevation(dp(5));

        TextView title = text("FRENTE", 40, true);
        title.setTextColor(Color.WHITE);
        title.setLetterSpacing(0.06f);
        hero.addView(title, new LinearLayout.LayoutParams(-1, -2));

        TextView sub = text("Adivina · inclina · ríete", 17, true);
        sub.setTextColor(Color.rgb(236, 240, 255));
        sub.setPadding(dp(8), 0, dp(8), 2);
        hero.addView(sub, new LinearLayout.LayoutParams(-1, -2));

        TextView meta = text("850 palabras · 17 categorías · 60 segundos", 13, false);
        meta.setTextColor(Color.rgb(218, 225, 255));
        meta.setPadding(dp(8), 2, dp(8), dp(4));
        hero.addView(meta, new LinearLayout.LayoutParams(-1, -2));

        LinearLayout.LayoutParams heroParams = new LinearLayout.LayoutParams(-1, -2);
        heroParams.setMargins(0, 0, 0, dp(12));
        root.addView(hero, heroParams);

        LinearLayout creatorRow = new LinearLayout(this);
        creatorRow.setOrientation(LinearLayout.HORIZONTAL);
        Button newCategory = button("＋  Nueva categoría");
        styleButton(newCategory, SURFACE_2, TEXT_LIGHT);
        newCategory.setOnClickListener(v -> showCategoryEditor(null, null));
        Button newMix = button("🎛  Crear mix");
        styleButton(newMix, Color.rgb(52, 66, 104), TEXT_LIGHT);
        newMix.setOnClickListener(v -> showMixEditor(null, null));
        LinearLayout.LayoutParams half = new LinearLayout.LayoutParams(0, dp(58), 1);
        half.setMargins(dp(4), dp(5), dp(4), 0);
        creatorRow.addView(newCategory, half);
        creatorRow.addView(newMix, half);
        root.addView(creatorRow, new LinearLayout.LayoutParams(-1, -2));

        Button mixAll = button("🎲  Mezcla de todo");
        styleButton(mixAll, ACCENT, Color.WHITE);
        mixAll.setOnClickListener(v -> startCategory("Mezcla de todo", allWords()));
        root.addView(mixAll, menuButtonParams());

        if (!savedMixes.isEmpty()) {
            root.addView(sectionLabel("MIS MIXES"), new LinearLayout.LayoutParams(-1, -2));
            for (Map.Entry<String, List<String>> e : new ArrayList<>(savedMixes.entrySet())) {
                String mixName = e.getKey();
                List<String> selections = new ArrayList<>(e.getValue());
                Button b = button("🎛  " + mixName);
                styleButton(b, Color.rgb(47, 54, 79), TEXT_LIGHT);
                b.setOnClickListener(v -> startCategory(mixName, resolveMix(selections)));
                b.setOnLongClickListener(v -> { showMixEditor(mixName, selections); return true; });
                root.addView(b, menuButtonParams());
            }
        }

        if (!customCategories.isEmpty()) {
            root.addView(sectionLabel("MIS CATEGORÍAS"), new LinearLayout.LayoutParams(-1, -2));
            for (Map.Entry<String, List<String>> e : new ArrayList<>(customCategories.entrySet())) {
                String name = e.getKey();
                List<String> words = new ArrayList<>(e.getValue());
                Button b = button("✨  " + name + "   ·   " + words.size());
                styleButton(b, Color.rgb(49, 55, 80), TEXT_LIGHT);
                b.setOnClickListener(v -> startCategory(name, words));
                b.setOnLongClickListener(v -> { showCategoryEditor(name, words); return true; });
                root.addView(b, menuButtonParams());
            }
        }

        root.addView(sectionLabel("CATEGORÍAS"), new LinearLayout.LayoutParams(-1, -2));
        LinearLayout categoryRow = null;
        int categoryIndex = 0;
        for (Map.Entry<String, List<String>> e : builtInCategories.entrySet()) {
            if (categoryIndex % 2 == 0) {
                categoryRow = new LinearLayout(this);
                categoryRow.setOrientation(LinearLayout.HORIZONTAL);
                root.addView(categoryRow, new LinearLayout.LayoutParams(-1, -2));
            }
            String name = e.getKey();
            List<String> words = e.getValue();
            Button b = button(categoryIcon(name) + "  " + name + "\n" + words.size() + " palabras");
            b.setTextSize(15);
            styleButton(b, SURFACE, TEXT_LIGHT);
            b.setGravity(Gravity.CENTER);
            b.setOnClickListener(v -> startCategory(name, words));
            LinearLayout.LayoutParams cp = new LinearLayout.LayoutParams(0, dp(72), 1);
            cp.setMargins(dp(4), dp(4), dp(4), dp(4));
            categoryRow.addView(b, cp);
            categoryIndex++;
        }
        if (categoryIndex % 2 != 0 && categoryRow != null) {
            View spacer = new View(this);
            LinearLayout.LayoutParams sp = new LinearLayout.LayoutParams(0, dp(72), 1);
            sp.setMargins(dp(4), dp(4), dp(4), dp(4));
            categoryRow.addView(spacer, sp);
        }

        TextView instructions = text(
                "↓  Hacia el suelo = ACERTADA      ↑  Hacia el techo = PASAR\n\nMantén el móvil quieto al empezar para calibrarlo.\nMantén pulsadas tus categorías o mixes para editarlos.",
                14, false);
        instructions.setTextColor(TEXT_MUTED);
        instructions.setGravity(Gravity.CENTER);
        instructions.setBackground(roundedBg(Color.rgb(27, 31, 48), 20));
        instructions.setPadding(dp(20), dp(16), dp(20), dp(16));
        LinearLayout.LayoutParams ip = new LinearLayout.LayoutParams(-1, -2);
        ip.setMargins(0, dp(16), 0, 0);
        root.addView(instructions, ip);
        setContentView(scroll);
    }

'''
s = replace_block(s, '    private void showMenu()', '    private LinearLayout.LayoutParams menuButtonParams()', menu)

countdown = r'''    private void showCountdown() {
        unregisterSensors();
        stopRound();
        playing = false;
        FrameLayout root = new FrameLayout(this);
        root.setBackground(gradientBg(Color.rgb(76, 58, 190), BG_DARK, 0));
        TextView counter = text("3", 112, true);
        counter.setTextColor(Color.WHITE);
        counter.setShadowLayer(dp(10), 0, dp(3), Color.argb(90, 0, 0, 0));
        root.addView(counter, new FrameLayout.LayoutParams(-1, -1));
        TextView hint = text("🤳  Ponte el móvil en la frente y déjalo recto", 19, true);
        hint.setTextColor(Color.rgb(225, 229, 245));
        hint.setBackground(roundedBg(Color.argb(85, 255, 255, 255), 18));
        FrameLayout.LayoutParams hp = new FrameLayout.LayoutParams(-1, dp(62), Gravity.BOTTOM);
        hp.setMargins(dp(36), 0, dp(36), dp(24));
        root.addView(hint, hp);
        setContentView(root);
        new CountDownTimer(2400, 800) {
            int n = 3;
            @Override public void onTick(long ms) { counter.setText(String.valueOf(n--)); }
            @Override public void onFinish() { showGame(); }
        }.start();
    }

'''
s = replace_block(s, '    private void showCountdown()', '    private void showGame()', countdown)

game = r'''    private void showGame() {
        hideSystemUi();
        gameRoot = new FrameLayout(this);
        gameRoot.setBackground(gradientBg(BG_DARK, Color.rgb(28, 31, 52), 0));
        LinearLayout top = new LinearLayout(this);
        top.setOrientation(LinearLayout.HORIZONTAL);
        top.setGravity(Gravity.CENTER_VERTICAL);
        top.setPadding(dp(24), dp(10), dp(24), dp(6));
        timerView = text("⏱  60", 23, true);
        timerView.setGravity(Gravity.CENTER);
        timerView.setTextColor(Color.WHITE);
        timerView.setBackground(roundedBg(Color.rgb(49, 54, 78), 18));
        scoreView = text("✓ 0", 22, true);
        scoreView.setGravity(Gravity.CENTER);
        scoreView.setTextColor(Color.WHITE);
        scoreView.setBackground(roundedBg(Color.rgb(35, 100, 72), 18));
        LinearLayout.LayoutParams stat = new LinearLayout.LayoutParams(0, dp(50), 1);
        stat.setMargins(dp(4), 0, dp(4), 0);
        top.addView(timerView, stat);
        top.addView(scoreView, stat);
        gameRoot.addView(top, new FrameLayout.LayoutParams(-1, dp(68), Gravity.TOP));
        wordView = text("", 58, true);
        wordView.setTextColor(Color.rgb(20, 22, 30));
        wordView.setPadding(dp(40), dp(34), dp(40), dp(34));
        wordView.setBackground(gradientBg(Color.WHITE, Color.rgb(242, 244, 255), 28));
        wordView.setElevation(dp(7));
        FrameLayout.LayoutParams wp = new FrameLayout.LayoutParams(-1, -1);
        wp.setMargins(dp(28), dp(76), dp(28), dp(72));
        gameRoot.addView(wordView, wp);
        gestureHint = text("CALIBRANDO… mantén el móvil quieto", 15, true);
        gestureHint.setTextColor(TEXT_MUTED);
        gestureHint.setBackground(roundedBg(Color.rgb(31, 35, 54), 18));
        FrameLayout.LayoutParams gp = new FrameLayout.LayoutParams(-1, dp(54), Gravity.BOTTOM);
        gp.setMargins(dp(28), 0, dp(28), dp(10));
        gameRoot.addView(gestureHint, gp);
        feedbackView = text("", 46, true);
        feedbackView.setTextColor(Color.WHITE);
        feedbackView.setVisibility(View.GONE);
        gameRoot.addView(feedbackView, new FrameLayout.LayoutParams(-1, -1));
        gameRoot.setOnTouchListener((v, e) -> {
            if (!playing || e.getAction() != MotionEvent.ACTION_DOWN) return true;
            if (e.getX() < gameRoot.getWidth() / 2f) registerAnswer(false); else registerAnswer(true);
            return true;
        });
        setContentView(gameRoot);
        nextWord();
        resetGestureState();
        playing = true;
        roundStartedAt = System.currentTimeMillis();
        calibrationUntil = roundStartedAt + CALIBRATION_MS;
        registerSensors();
        roundTimer = new CountDownTimer(60000, 1000) {
            @Override public void onTick(long ms) {
                long secs = (ms + 999) / 1000;
                timerView.setText("⏱  " + secs);
                if (secs <= 10) timerView.setBackground(roundedBg(Color.rgb(116, 55, 61), 18));
            }
            @Override public void onFinish() { timerView.setText("0"); finishRound(); }
        }.start();
    }

'''
s = replace_block(s, '    private void showGame()', '    private void nextWord()', game)

results = r'''    private void finishRound() {
        if (!playing) return;
        playing = false;
        unregisterSensors();
        stopRound();
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER);
        root.setPadding(dp(34), dp(20), dp(34), dp(20));
        root.setBackground(gradientBg(BG_DARK, Color.rgb(35, 29, 77), 0));
        TextView over = text("RONDA TERMINADA", 18, true);
        over.setTextColor(TEXT_MUTED);
        over.setLetterSpacing(0.12f);
        root.addView(over, new LinearLayout.LayoutParams(-1, -2));
        TextView result = text(String.valueOf(score), 94, true);
        result.setTextColor(Color.rgb(83, 214, 139));
        result.setPadding(dp(8), 0, dp(8), 0);
        root.addView(result, new LinearLayout.LayoutParams(-1, -2));
        TextView label = text("acertadas   ·   " + skipped + " pasadas", 19, true);
        label.setTextColor(TEXT_LIGHT);
        root.addView(label, new LinearLayout.LayoutParams(-1, -2));
        TextView cat = text(selectedCategory, 15, true);
        cat.setTextColor(TEXT_MUTED);
        cat.setBackground(roundedBg(SURFACE, 14));
        LinearLayout.LayoutParams catp = new LinearLayout.LayoutParams(-2, -2);
        catp.setMargins(0, dp(8), 0, dp(2));
        root.addView(cat, catp);
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
        setContentView(root);
    }

'''
s = replace_block(s, '    private void finishRound()', '    private void resetGestureState()', results)

p.write_text(s)
print('Frente v1.2 UI applied')
