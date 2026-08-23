package com.nacho.frente;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.Typeface;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Build;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.view.Gravity;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class MainActivity extends Activity implements SensorEventListener {
    private final Map<String, List<String>> categories = new LinkedHashMap<>();
    private final List<String> mixed = new ArrayList<>();
    private SensorManager sensorManager;
    private Sensor accelerometer;
    private Vibrator vibrator;
    private FrameLayout gameRoot;
    private TextView wordView, timerView, scoreView, gestureHint, feedbackView;
    private List<String> deck = new ArrayList<>();
    private int deckIndex = 0, score = 0, skipped = 0;
    private String selectedCategory = "Mezcla de todo";
    private CountDownTimer roundTimer;
    private boolean playing = false;
    private float filteredZ = 0f;
    private boolean filterReady = false, gestureArmed = false;
    private long neutralSince = 0L, lastGestureAt = 0L, roundStartedAt = 0L;
    private static final float NEUTRAL_Z = 2.6f;
    private static final float TILT_Z = 5.3f;
    private static final long NEUTRAL_ARM_MS = 220L;
    private static final long GESTURE_COOLDOWN_MS = 550L;

    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        hideSystemUi();
        initWords();
        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        vibrator = (Vibrator) getSystemService(VIBRATOR_SERVICE);
        showMenu();
    }

    private void hideSystemUi() {
        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
                View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
                View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_STABLE);
    }

    private void initWords() {
        categories.put("Películas y series", Arrays.asList(
                "Titanic","Shrek","Harry Potter","Breaking Bad","Toy Story","Star Wars","Los Simpson","Stranger Things",
                "Jurassic Park","Avatar","Gladiator","Frozen","El Rey León","Batman","Spider-Man","Los Vengadores",
                "Regreso al futuro","The Office","Friends","La Casa de Papel","Matrix","Piratas del Caribe","Juego de Tronos",
                "The Walking Dead","Rocky","Indiana Jones","Buscando a Nemo","Monstruos S.A.","Deadpool","Miércoles","Black Mirror","Los Soprano"));
        categories.put("Animales", Arrays.asList(
                "Elefante","Pingüino","Jirafa","Canguro","Tiburón","Pulpo","Panda","Cocodrilo","Camaleón","Flamenco","Gorila","Koala",
                "Delfín","Murciélago","Avestruz","Rinoceronte","Medusa","Lobo","Mapache","Caballito de mar","Ornitorrinco","Pavo real",
                "Serpiente","Águila","Hipopótamo","Foca","Erizo","Perezoso","Leopardo","Lémur","Cangrejo","Tortuga"));
        categories.put("Objetos", Arrays.asList(
                "Paraguas","Microondas","Cepillo de dientes","Semáforo","Mochila","Martillo","Tostadora","Sacacorchos","Almohada","Extintor",
                "Ventilador","Calculadora","Tijeras","Escoba","Linterna","Ascensor","Auriculares","Nevera","Cremallera","Prismáticos","Taladro",
                "Reloj","Cafetera","Grapadora","Mando a distancia","Colador","Destornillador","Plancha","Cargador","Candado","Maleta","Sartén"));
        categories.put("Personajes famosos", Arrays.asList(
                "Messi","Cristiano Ronaldo","Taylor Swift","Elon Musk","Shakira","Leonardo DiCaprio","MrBeast","Lady Gaga","Tom Cruise","Bad Bunny",
                "Dwayne Johnson","Aitana","Will Smith","Rihanna","Ibai Llanos","Rosalía","Pedro Pascal","Beyoncé","Keanu Reeves","Ariana Grande",
                "Brad Pitt","Jennifer Aniston","Michael Jackson","Freddie Mercury","David Beckham","Miley Cyrus","Robert Downey Jr.","Snoop Dogg","Karol G","Fernando Alonso"));
        categories.put("Videojuegos", Arrays.asList(
                "Minecraft","Fortnite","GTA","The Sims","Mario Kart","Pokémon","Call of Duty","Skyrim","Dark Souls","EA Sports FC","Among Us","Tetris",
                "The Last of Us","Resident Evil","Red Dead Redemption","Fall Guys","Zelda","Roblox","Cyberpunk 2077","God of War","Super Mario",
                "League of Legends","Valorant","Counter-Strike","Animal Crossing","Clash Royale","Elden Ring","Portal","Half-Life","Overwatch","Fallout","Assassin's Creed"));
        for (List<String> list : categories.values()) mixed.addAll(list);
    }

    private TextView text(String value, int sizeSp, boolean bold) {
        TextView v = new TextView(this);
        v.setText(value); v.setTextColor(Color.rgb(24,24,24)); v.setTextSize(sizeSp); v.setGravity(Gravity.CENTER);
        v.setPadding(dp(14),dp(10),dp(14),dp(10));
        if (bold) v.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        return v;
    }

    private Button button(String label) {
        Button b = new Button(this); b.setText(label); b.setTextSize(18); b.setAllCaps(false); b.setMinHeight(dp(54)); return b;
    }

    private void showMenu() {
        stopRound(); playing = false; unregisterSensors(); hideSystemUi();
        ScrollView scroll = new ScrollView(this); scroll.setBackgroundColor(Color.rgb(246,242,234));
        LinearLayout root = new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL); root.setGravity(Gravity.CENTER_HORIZONTAL);
        root.setPadding(dp(28),dp(20),dp(28),dp(24)); scroll.addView(root,new ScrollView.LayoutParams(-1,-2));
        root.addView(text("FRENTE",48,true),new LinearLayout.LayoutParams(-1,-2));
        TextView sub=text("Elige categoría · 60 segundos",17,false); sub.setTextColor(Color.DKGRAY); root.addView(sub,new LinearLayout.LayoutParams(-1,-2));
        Button mix=button("🎲  Mezcla de todo"); mix.setOnClickListener(v->startCategory("Mezcla de todo",mixed)); root.addView(mix,menuButtonParams());
        for(Map.Entry<String,List<String>> e:categories.entrySet()){
            Button b=button(e.getKey()); String name=e.getKey(); List<String> words=e.getValue();
            b.setOnClickListener(v->startCategory(name,words)); root.addView(b,menuButtonParams());
        }
        TextView instructions=text("EN LA FRENTE\n\n↓ Hacia el suelo = ACERTADA\n↑ Hacia el techo = PASAR\n\nVuelve al centro después de cada gesto.",15,false);
        instructions.setTextColor(Color.rgb(75,75,75)); root.addView(instructions,new LinearLayout.LayoutParams(-1,-2));
        setContentView(scroll);
    }

    private LinearLayout.LayoutParams menuButtonParams(){LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-1,dp(58));p.setMargins(0,dp(8),0,0);return p;}

    private void startCategory(String name,List<String> words){selectedCategory=name;deck=new ArrayList<>(words);Collections.shuffle(deck);deckIndex=0;score=0;skipped=0;showCountdown();}

    private void showCountdown(){
        unregisterSensors();stopRound();playing=false;
        FrameLayout root=new FrameLayout(this);root.setBackgroundColor(Color.rgb(21,23,25));
        TextView counter=text("3",100,true);counter.setTextColor(Color.WHITE);root.addView(counter,new FrameLayout.LayoutParams(-1,-1));
        TextView hint=text("Ponte el móvil en la frente",20,true);hint.setTextColor(Color.LTGRAY);
        FrameLayout.LayoutParams hp=new FrameLayout.LayoutParams(-1,dp(70),Gravity.BOTTOM);hp.setMargins(dp(20),0,dp(20),dp(20));root.addView(hint,hp);setContentView(root);
        new CountDownTimer(2400,800){int n=3;@Override public void onTick(long ms){counter.setText(String.valueOf(n--));}@Override public void onFinish(){showGame();}}.start();
    }

    private void showGame(){
        hideSystemUi();gameRoot=new FrameLayout(this);gameRoot.setBackgroundColor(Color.rgb(250,248,243));
        LinearLayout top=new LinearLayout(this);top.setOrientation(LinearLayout.HORIZONTAL);top.setGravity(Gravity.CENTER_VERTICAL);top.setPadding(dp(24),dp(10),dp(24),dp(6));
        timerView=text("60",28,true);timerView.setGravity(Gravity.START|Gravity.CENTER_VERTICAL);scoreView=text("✓ 0",22,true);scoreView.setGravity(Gravity.END|Gravity.CENTER_VERTICAL);
        top.addView(timerView,new LinearLayout.LayoutParams(0,dp(56),1));top.addView(scoreView,new LinearLayout.LayoutParams(0,dp(56),1));gameRoot.addView(top,new FrameLayout.LayoutParams(-1,dp(70),Gravity.TOP));
        wordView=text("",56,true);wordView.setTextColor(Color.rgb(15,15,15));wordView.setPadding(dp(38),dp(34),dp(38),dp(34));
        FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);wp.setMargins(dp(20),dp(68),dp(20),dp(70));gameRoot.addView(wordView,wp);
        gestureHint=text("↓ ACERTADA        vuelve al centro        PASAR ↑",16,true);gestureHint.setTextColor(Color.rgb(88,88,88));
        FrameLayout.LayoutParams gp=new FrameLayout.LayoutParams(-1,dp(64),Gravity.BOTTOM);gp.setMargins(dp(16),0,dp(16),dp(3));gameRoot.addView(gestureHint,gp);
        feedbackView=text("",44,true);feedbackView.setTextColor(Color.WHITE);feedbackView.setVisibility(View.GONE);gameRoot.addView(feedbackView,new FrameLayout.LayoutParams(-1,-1));
        gameRoot.setOnTouchListener((v,e)->{if(!playing||e.getAction()!=android.view.MotionEvent.ACTION_DOWN)return true;if(e.getX()<gameRoot.getWidth()/2f)registerAnswer(false);else registerAnswer(true);return true;});
        setContentView(gameRoot);nextWord();resetGestureState();playing=true;roundStartedAt=System.currentTimeMillis();registerSensors();
        roundTimer=new CountDownTimer(60000,1000){@Override public void onTick(long ms){timerView.setText(String.valueOf((ms+999)/1000));}@Override public void onFinish(){timerView.setText("0");finishRound();}}.start();
    }

    private void nextWord(){if(deck.isEmpty())return;if(deckIndex>=deck.size()){Collections.shuffle(deck);deckIndex=0;}wordView.setText(deck.get(deckIndex++));}

    private void registerAnswer(boolean correct){
        long now=System.currentTimeMillis();if(!playing||now-lastGestureAt<GESTURE_COOLDOWN_MS)return;lastGestureAt=now;gestureArmed=false;neutralSince=0L;
        if(correct){score++;scoreView.setText("✓ "+score);vibrate(75);flashFeedback("¡ACERTADA!",Color.rgb(44,168,94));}
        else{skipped++;vibrate(35);flashFeedback("PASAR",Color.rgb(211,75,75));}nextWord();
    }

    private void flashFeedback(String label,int color){feedbackView.setText(label);feedbackView.setBackgroundColor(color);feedbackView.setVisibility(View.VISIBLE);feedbackView.animate().cancel();feedbackView.setAlpha(1f);feedbackView.animate().alpha(0f).setDuration(320).withEndAction(()->feedbackView.setVisibility(View.GONE)).start();}

    private void vibrate(long ms){if(vibrator==null||!vibrator.hasVibrator())return;if(Build.VERSION.SDK_INT>=26)vibrator.vibrate(VibrationEffect.createOneShot(ms,VibrationEffect.DEFAULT_AMPLITUDE));else vibrator.vibrate(ms);}

    private void finishRound(){
        if(!playing)return;playing=false;unregisterSensors();stopRound();
        LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setGravity(Gravity.CENTER);root.setPadding(dp(28),dp(20),dp(28),dp(20));root.setBackgroundColor(Color.rgb(246,242,234));
        root.addView(text("FIN DE LA RONDA",22,true),new LinearLayout.LayoutParams(-1,-2));root.addView(text(String.valueOf(score),92,true),new LinearLayout.LayoutParams(-1,-2));
        TextView label=text("acertadas  ·  "+skipped+" pasadas",20,false);label.setTextColor(Color.DKGRAY);root.addView(label,new LinearLayout.LayoutParams(-1,-2));
        TextView cat=text(selectedCategory,16,true);cat.setTextColor(Color.GRAY);root.addView(cat,new LinearLayout.LayoutParams(-1,-2));
        LinearLayout buttons=new LinearLayout(this);buttons.setOrientation(LinearLayout.HORIZONTAL);buttons.setGravity(Gravity.CENTER);
        Button again=button("Otra ronda");again.setOnClickListener(v->startCategory(selectedCategory,selectedCategory.equals("Mezcla de todo")?mixed:categories.get(selectedCategory)));
        Button menu=button("Categorías");menu.setOnClickListener(v->showMenu());LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(0,dp(60),1);bp.setMargins(dp(6),dp(18),dp(6),0);buttons.addView(again,bp);buttons.addView(menu,bp);root.addView(buttons,new LinearLayout.LayoutParams(-1,-2));setContentView(root);
    }

    private void resetGestureState(){filteredZ=0f;filterReady=false;gestureArmed=false;neutralSince=0L;lastGestureAt=0L;}

    @Override public void onSensorChanged(SensorEvent event){
        if(!playing||event.sensor.getType()!=Sensor.TYPE_ACCELEROMETER)return;if(System.currentTimeMillis()-roundStartedAt<700)return;
        float z=event.values[2];if(!filterReady){filteredZ=z;filterReady=true;}else filteredZ=filteredZ*0.82f+z*0.18f;
        long now=System.currentTimeMillis();if(Math.abs(filteredZ)<=NEUTRAL_Z){if(neutralSince==0L)neutralSince=now;if(now-neutralSince>=NEUTRAL_ARM_MS)gestureArmed=true;gestureHint.setText("LISTO · ↓ ACERTADA          PASAR ↑");return;}
        neutralSince=0L;if(!gestureArmed||now-lastGestureAt<GESTURE_COOLDOWN_MS)return;if(filteredZ<=-TILT_Z)registerAnswer(true);else if(filteredZ>=TILT_Z)registerAnswer(false);
    }

    @Override public void onAccuracyChanged(Sensor sensor,int accuracy){}
    private void registerSensors(){if(accelerometer!=null)sensorManager.registerListener(this,accelerometer,SensorManager.SENSOR_DELAY_GAME);}
    private void unregisterSensors(){if(sensorManager!=null)sensorManager.unregisterListener(this);}
    private void stopRound(){if(roundTimer!=null){roundTimer.cancel();roundTimer=null;}}
    @Override protected void onResume(){super.onResume();hideSystemUi();if(playing)registerSensors();}
    @Override protected void onPause(){unregisterSensors();super.onPause();}
    @Override protected void onDestroy(){stopRound();unregisterSensors();super.onDestroy();}
    private int dp(int n){return Math.round(n*getResources().getDisplayMetrics().density);}
}
