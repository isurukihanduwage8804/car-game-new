import streamlit as st
import streamlit.components.v1 as components

# පේජ් එකේ සැකසුම්
st.set_page_config(page_title="Square Racer Game", page_icon="🏎️", layout="centered")

st.title("🏎️ Square Racer: Math Challenge")
st.write("Target එකේ තියෙන අංකය උඩින් කාර් එක පදවන්න!")

# වේගය පාලනය
speed_val = st.slider("වේගය (Speed):", min_value=1, max_value=10, value=4)

# --- GAME ENGINE (කාර් එකේ පින්තූරය නිවැරදි කර ඇත) ---
game_js = f"""
<div id="gameContainer" style="width:100%; height:550px; background:#222; position:relative; overflow:hidden; border:5px solid #444; cursor:none; border-radius: 15px;">
    <div id="roadLines" style="position:absolute; left:50%; width:2px; height:200%; top:-100%; border-left: 5px dashed rgba(255,255,255,0.3);"></div>
    
    <div id="car" style="position:absolute; bottom:30px; left:45%; width:60px; z-index:100;">
        <img src="https://raw.githubusercontent.com/isurukihanduwage8804/car-game-new/main/top-view-sports-car-260nw-2304283365-removebg-preview.png" 
             style="width:100%; filter: drop-shadow(0px 10px 5px rgba(0,0,0,0.5));"
             onerror="this.src='https://cdn-icons-png.flaticon.com/512/744/744465.png';">
    </div>
    
    <div id="ui" style="position:absolute; top:15px; left:15px; color:#0f0; font-family:monospace; font-size:20px; z-index:200; background:rgba(0,0,0,0.8); padding:10px; border-radius:10px; border:2px solid #0f0;">
        SCORE: <span id="score">0</span><br>
        TARGET: <span id="nextNum">1</span>
    </div>
</div>

<script>
    const container = document.getElementById('gameContainer');
    const car = document.getElementById('car');
    const scoreBoard = document.getElementById('score');
    const nextNumBoard = document.getElementById('nextNum');
    const roadLines = document.getElementById('roadLines');
    
    let score = 0;
    let gameSpeed = {speed_val};
    let roadPos = -100;

    // වර්ග සංඛ්‍යා 1 සිට 625 දක්වා
    const squares = [];
    for(let i=1; i<=25; i++) {{ squares.push(i*i); }}
    let squareIndex = 0;

    // ශබ්දය (Beep Sound)
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playBeep() {{
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.frequency.value = 1000;
        gain.gain.value = 0.05;
        osc.start();
        osc.stop(audioCtx.currentTime + 0.1);
    }}

    // පාර පහළට යන ඇනිමේෂන් එක
    function animateRoad() {{
        roadPos += gameSpeed * 1.5;
        if(roadPos > 0) roadPos = -100;
        roadLines.style.top = roadPos + "%";
        requestAnimationFrame(animateRoad);
    }}
    animateRoad();

    // අංක මැවීම (Spawn Numbers)
    function spawnNumber() {{
        if (squareIndex >= squares.length) squareIndex = 0;
        const currentTarget = squares[squareIndex];
        nextNumBoard.innerText = currentTarget;

        const el = document.createElement('div');
        el.innerText = currentTarget;
        el.style.position = 'absolute';
        el.style.top = '-60px';
        el.style.left = (Math.random() * 70 + 15) + '%';
        el.style.color = '#ffff00';
        el.style.fontSize = '35px';
        el.style.fontWeight = 'bold';
        el.style.textShadow = '2px 2px #000';
        container.appendChild(el);

        let topPos = -60;
        const moveInt = setInterval(() => {{
            topPos += gameSpeed;
            el.style.top = topPos + 'px';

            const carRect = car.getBoundingClientRect();
            const numRect = el.getBoundingClientRect();

            // කාර් එකේ ඉලක්කම වැදුණු විට
            if (numRect.top < carRect.bottom && numRect.bottom > carRect.top &&
                numRect.left < carRect.right && numRect.right > carRect.left) {{
                
                // වැදුණේ හරි ඉලක්කම නම් ලකුණු ලබා දීම
                if (el.innerText == nextNumBoard.innerText) {{
                    playBeep();
                    score += 10;
                    scoreBoard.innerText = score;
                    el.remove();
                    clearInterval(moveInt);
                    squareIndex++;
                }}
            }}

            if (topPos > 600) {{
                el.remove();
                clearInterval(moveInt);
            }}
        }}, 30);
    }}

    setInterval(spawnNumber, 2500 / (gameSpeed/2 + 1));

    // මවුස් එකෙන් කාර් එක පාලනය
    container.addEventListener('mousemove', (e) => {{
        let rect = container.getBoundingClientRect();
        let x = e.clientX - rect.left - 30;
        if(x > 10 && x < rect.width - 70) {{
            car.style.left = x + 'px';
        }}
    }});
</script>
"""

components.html(game_js, height=600)
