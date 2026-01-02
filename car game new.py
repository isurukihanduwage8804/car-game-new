import streamlit as st
import streamlit.components.v1 as components

# පේජ් එකේ සැකසුම්
st.set_page_config(page_title="Square Racer Game", page_icon="🏎️", layout="centered")

st.title("🏎️ Square Racer: Math Challenge")
st.write("වර්ග සංඛ්‍යාව හප්පන්න, එහි වර්ගමූලය (Square Root) රවුම තුළ දිස්වනු ඇත!")

# වේගය පාලනය
speed_val = st.slider("වේගය (Speed):", min_value=1, max_value=10, value=4)

# --- GAME ENGINE ---
game_js = f"""
<div id="gameContainer" style="width:100%; height:550px; background:#f4d03f; position:relative; overflow:hidden; border:15px solid #2ecc71; border-radius: 15px; outline: none;" tabindex="0">
    <div id="roadLines" style="position:absolute; left:50%; width:2px; height:200%; top:-100%; border-left: 5px dashed rgba(0,0,0,0.3);"></div>
    
    <div id="car" style="position:absolute; bottom:30px; left:45%; width:70px; z-index:100; transition: left 0.1s ease-out;">
        <img src="https://raw.githubusercontent.com/isurukihanduwage8804/car-game-new/main/car.png" 
             style="width:100%; filter: drop-shadow(0px 10px 5px rgba(0,0,0,0.4));"
             onerror="this.src='https://cdn-icons-png.flaticon.com/512/744/744465.png';">
    </div>
    
    <div id="rootDisplay" style="position:absolute; top:20px; left:10px; width:90px; height:90px; background:#fff; color:#e74c3c; border-radius:50%; border:5px solid #e74c3c; display:none; align-items:center; justify-content:center; font-size:35px; font-weight:bold; box-shadow: 0 4px 15px rgba(0,0,0,0.5); z-index:200; font-family: Arial;">
        <span id="rootVal"></span>
    </div>

    <div id="targetUI" style="position:absolute; top:20px; right:20px; background:rgba(0,0,0,0.8); color:#fff; padding:10px 20px; border-radius:10px; border:2px solid #fff; font-family:sans-serif; font-size:18px; z-index:200;">
        TARGET: <span id="nextNum" style="color:#0f0; font-weight:bold;">1</span>
    </div>
</div>

<script>
    const container = document.getElementById('gameContainer');
    const car = document.getElementById('car');
    const nextNumBoard = document.getElementById('nextNum');
    const rootDisplay = document.getElementById('rootDisplay');
    const rootText = document.getElementById('rootVal');
    
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

    document.addEventListener('keydown', (e) => {{
        if (e.key === "ArrowLeft" && carX > 8) {{ carX -= 7; }}
        else if (e.key === "ArrowRight" && carX < 82) {{ carX += 7; }}
        car.style.left = carX + "%";
    }});

    function animateRoad() {{
        roadPos += gameSpeed * 1.8;
        if(roadPos > 0) roadPos = -100;
        document.getElementById('roadLines').style.top = roadPos + "%";
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
        el.style.left = (Math.random() * 60 + 20) + '%';
        el.style.color = '#000';
        el.style.fontSize = '45px';
        el.style.fontWeight = '900';
        el.style.fontFamily = 'Arial Black';
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
                    
                    // වර්ගමූලය (ඉලක්කම පමණක්) රවුම ඇතුළේ පෙන්වීම
                    const val = Math.sqrt(parseInt(el.innerText));
                    rootText.innerText = val; 
                    rootDisplay.style.display = 'flex'; 
                    
                    el.remove();
                    clearInterval(moveInt);
                    squareIndex++;
                }}
            }}
            if (topPos > 600) {{ el.remove(); clearInterval(moveInt); }}
        }}, 30);
    }}

    setInterval(spawnNumber, 2800 / (gameSpeed/2 + 1));
    container.focus();
</script>
"""

components.html(game_js, height=600)
