function renderButton(state) {
    const container = document.getElementById('button-container');
    if (state === 'off') {
        container.innerHTML = `<button class="led-btn green" onclick="setLed('on')">Sprinkle!</button>`;
    } else if (state === 'on') {
        container.innerHTML = `<button class="led-btn red" onclick="setLed('off')">Stop Sprinkling</button>`;
    }
}

function fetchStateAndRender() {
    fetch('/led')
        .then(response => response.json())
        .then(data => {
            renderButton(data.state);
        });
}

function setLed(state) {
    fetch('/led', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ state: state })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('status').innerText = data.status || data.error;
        fetchStateAndRender();
    })
    .catch(error => {
        document.getElementById('status').innerText = 'Error: ' + error;
    });
}

// On page load
fetchStateAndRender(); 