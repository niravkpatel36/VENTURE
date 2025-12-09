document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("audio-visualizer");
  const ctx = canvas.getContext("2d");
  const audio = document.getElementById("ai-audio");
  const promptInput = document.getElementById("prompt");
  const btn = document.getElementById("generate-btn");
  const loading = document.getElementById("loading");

  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  let audioCtx, analyser, source, dataArray;

  // Draw visualizer loop
  function draw() {
    requestAnimationFrame(draw);
    if (!analyser) return;

    analyser.getByteFrequencyData(dataArray);
    ctx.fillStyle = "rgba(0, 0, 0, 0.15)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const barWidth = (canvas.width / dataArray.length) * 2.5;
    let x = 0;
    for (let i = 0; i < dataArray.length; i++) {
      const barHeight = dataArray[i] * 1.8;
      const hue = i / dataArray.length * 360;
      ctx.fillStyle = `hsl(${hue}, 100%, 60%)`;
      ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
      x += barWidth + 1;
    }
  }

  // Connect audio to visualizer
  function setupVisualizer() {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioCtx.createAnalyser();
    source = audioCtx.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(audioCtx.destination);
    analyser.fftSize = 256;
    dataArray = new Uint8Array(analyser.frequencyBinCount);
    draw();
  }

  // Fetch AI-generated track
  btn.addEventListener("click", async () => {
    const mood = promptInput.value.trim();
    if (!mood) return alert("Please enter a mood or prompt.");
    btn.disabled = true;
    loading.classList.remove("hidden");

    try {
      const response = await fetch("/ai/generate/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: JSON.stringify({ prompt: mood }),
      });

      const result = await response.json();
      if (result.audio_url) {
        audio.src = result.audio_url;
        audio.classList.remove("hidden");
        await audio.play();
        setupVisualizer();
      } else {
        alert("AI generation failed. Try again.");
      }
    } catch (err) {
      console.error(err);
      alert("Error generating track.");
    } finally {
      btn.disabled = false;
      loading.classList.add("hidden");
    }
  });
});
