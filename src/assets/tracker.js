let ws;
let reconnectionTimeout;

function sendUpdate() {
    const lifeTotals = {};
    document.querySelectorAll(".life-display").forEach((display) => {
        lifeTotals[display.closest("[data-player]").dataset.player] = Number(
            display.innerText
        );
    });
    console.log("Sending update:", lifeTotals);
    ws.send(JSON.stringify({ type: "update", data: lifeTotals }));
}

function createWebSocket() {
    const host = document.location.host.split(":")[0];
    ws = new WebSocket(`ws://${host}:8765`);
    ws.addEventListener("open", () => {
        const connectionIndicator = document.querySelector(".connection");
        connectionIndicator.querySelector(".connection-status").innerText =
            "Connected";
        connectionIndicator.querySelector(
            ".connection-light"
        ).style.backgroundColor = "#00f400";
        sendUpdate();
    });

    ws.addEventListener("close", () => {
        const connectionIndicator = document.querySelector(".connection");
        connectionIndicator.querySelector(".connection-status").innerText =
            "Disconnected";
        connectionIndicator.querySelector(
            ".connection-light"
        ).style.backgroundColor = "#f40000";
        // try to reconnect:
        clearTimeout(reconnectionTimeout);
        reconnectionTimeout = setTimeout(createWebSocket, 1000);
    });

    ws.addEventListener("error", (event) => {
        console.error("WebSocket error:", event);
        clearTimeout(reconnectionTimeout);
        reconnectionTimeout = setTimeout(createWebSocket, 1000);
    });
}

createWebSocket();

const floatingChangeTimeouts = {};

document.addEventListener("mousedown", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;

    if (btn.classList.contains("life-btn")) {
        const player = btn.closest("[data-player]");
        const playerNum = player.dataset.player;
        const increment = Number(btn.dataset.increment);
        const lifeDisplay = player.querySelector(".life-display");
        lifeDisplay.innerText = Number(lifeDisplay.innerText) + increment;

        const floatingChange = player.querySelector(
            `.floating-change[data-increment="${btn.dataset.increment}"]`
        );
        if (floatingChange.classList.contains("floating-change--hidden")) {
            floatingChange.innerText = increment.toString();
            floatingChange.classList.remove("floating-change--hidden");
        } else {
            floatingChange.innerText = (
                Number(floatingChange.innerText) + increment
            ).toString();
        }
        if (increment > 0) {
            floatingChange.innerText = `+${floatingChange.innerText}`;
        }
        const timeoutKey = `${playerNum}-${btn.dataset.increment}`;
        clearTimeout(floatingChangeTimeouts[timeoutKey]);
        floatingChangeTimeouts[timeoutKey] = setTimeout(() => {
            floatingChange.classList.add("floating-change--hidden");
        }, 3000);

        sendUpdate();
    }

    if (btn.classList.contains("reset-btn")) {
        if (!confirm("Reset both life totals?")) return;
        const lifeDisplays = document.querySelectorAll(".life-display");
        lifeDisplays.forEach((display) => {
            display.innerText = "20";
        });
        const floatingChanges = document.querySelectorAll(".floating-change");
        floatingChanges.forEach((change) => {
            change.innerText = "";
        });

        sendUpdate();
    }
});
