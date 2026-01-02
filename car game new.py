import streamlit as st
import streamlit.components.v1 as components

# පේජ් එකේ සැකසුම්
st.set_page_config(page_title="Square Racer Game", page_icon="🏎️", layout="centered")

st.title("🏎️ Square Racer: Math Challenge")
st.write("කහ පාට පාරේ තියෙන කළු පාට ඉලක්කම් උඩින් කාර් එක පදවන්න!")

# වේගය පාලනය
speed_val = st.slider("වේගය (Speed):", min_value=1, max_value=10, value=4)

# --- GAME ENGINE ---
game_js = f"""
<div id="gameContainer" style="width:100%; height:550px; background:#f4d03f; position:relative; overflow:hidden; border:10px solid #2ecc71; border-radius: 15px; outline: none;" tabindex="0">
    <div id="roadLines" style="position:absolute; left:50%; width:2px; height:200%; top:-100%; border-left: 5px dashed rgba(0,0,0,0.3);"></div>
    
    <div id="car" style="position:absolute; bottom:30px; left:45%; width:70px; z-index:100; transition: left 0.1s ease-out;">
        <img src="https://raw.githubusercontent.com/isurukihanduwage8804/car-game-new/main/car.png" 
             style="width:100%; filter: drop-shadow(0px 10px 5px rgba(0,0,0,0.4));"
             onerror="this.src='https://cdn-icons-png.flaticon.com/512/744/744465.png';">
    </div>
    
    <div id="ui" style="position:absolute; top:15px; left:25px; color:#fff; font-family:sans-serif; font-size:20px; z-index:200; background:rgba(0,0,0,0.7); padding:10px; border-radius:10px; border:2px solid #fff;">
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
    let carX = 45; 

    const squares = [];
    for(let i=1; i<=25; i++) {{ squares.push(i*i); }}
    let squareIndex = 0;

    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playBeep() {{
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.frequency.value = 1100;
        gain.gain.value = 0.05;
        osc.start();
        osc.stop(audioCtx.currentTime + 0.1);
    }}

    // Arrow Key Controls
    document.addEventListener('keydown', (e) => {{
        if (e.key === "ArrowLeft" && carX > 5) {{
            carX -= 6;
        }} else if (e.key === "ArrowRight" && carX < 85) {{
            carX += 6;
        }}
        car.style.left = carX + "%";
    }});

    function animateRoad() {{
        roadPos += gameSpeed * 1.8;
        if(roadPos > 0) roadPos = -100;
        roadLines.style.top = roadPos + "%";
        requestAnimationFrame(animateRoad);
    }}
    animateRoad();

    function spawnNumber() {{
        if (squareIndex >= squares.length) squareIndex = 0;
        const currentTarget = squares[squareIndex];
        nextNumBoard.innerText = currentTarget;

        const el = document.createElement('div');
        el.innerText = currentTarget;
        el.style.position = 'absolute';
        el.style.top = '-60px';
        el.style.left = (Math.random() * 70 + 15) + '%';
        
        el.style.color = '#000000'; 
        el.style.fontSize = '45px'; 
        el.style.fontWeight = '900'; 
        el.style.fontFamily = 'Arial Black, sans-serif';
        el.style.textShadow = '1px 1px 0px rgba(255,255,255,0.5)';
        
        container.appendChild(el);

        let topPos = -60;
        const moveInt = setInterval(() => {{
            topPos += gameSpeed;
            el.style.top = topPos + 'px';

            const carRect = car.getBoundingClientRect();
            const numRect = el.getBoundingClientRect();

            if (numRect.top < carRect.bottom && numRect.bottom > carRect.top &&
                numRect.left < carRect.right && numRect.right > carRect.left) {{
                
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

    setInterval(spawnNumber, 2800 / (gameSpeed/2 + 1));
    container.focus();
</script>
"""

components.html(game_js, height=600)
