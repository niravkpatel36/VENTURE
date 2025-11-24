// musicgen.js
// Minimal client-side music generator & simple WAV export (via Tone.Recorder)
const MusicGen = (function(){
  let synths = [];
  let seq = null;
  let started = false;
  let recorder = null;
  let analyzer = null;
  let ctx = null;
  let canvasEl = null;

  // helper: mood -> parameters
  function moodToParams(moodText){
    const m = (moodText||'').toLowerCase();
    if (m.includes('chill') || m.includes('calm') || m.includes('ambient')) {
      return { bpm: 70, scale: 'minor', root: 'A4', instrument: 'pad' };
    }
    if (m.includes('happy') || m.includes('uplift')) {
      return { bpm: 110, scale: 'major', root: 'C4', instrument: 'synth' };
    }
    if (m.includes('drive') || m.includes('night')) {
      return { bpm: 100, scale: 'minor', root: 'D4', instrument: 'pluck' };
    }
    if (m.includes('epic') || m.includes('cinematic')) {
      return { bpm: 80, scale: 'minor', root: 'C3', instrument: 'pad' };
    }
    // default
    return { bpm: 90, scale: 'minor', root: 'A4', instrument: 'pad' };
  }

  // simple mode: generate a chord progression and a melody using scale degrees
  function generateSequence(params, bars){
    // map scale to intervals
    const major = [0,2,4,5,7,9,11];
    const minor = [0,2,3,5,7,8,10];
    const scale = params.scale === 'major' ? major : minor;
    const rootMidi = Tone.Frequency(params.root).toMidi(); // base
    // build notes for single bar
    const steps = [];
    for (let i=0;i<bars*4;i++){
      const degree = scale[Math.floor(Math.random()*scale.length)];
      const octaveShift = (Math.random() > .8) ? 12 : 0;
      const midi = rootMidi + degree + octaveShift - 12; // drop to range
      steps.push(Tone.Frequency(midi, "midi").toNote());
    }
    return steps;
  }

  // create synths
  function createSynth(type){
    if (type === 'pad'){
      return new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "sine" },
        envelope: { attack: 0.8, decay: 0.5, sustain: 0.6, release: 2 }
      }).toDestination();
    }
    if (type === 'pluck'){
      return new Tone.PluckSynth().toDestination();
    }
    if (type === 'synth'){
      return new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "triangle" },
        envelope: { attack: 0.02, decay: 0.2, sustain: 0.6, release: 1 }
      }).toDestination();
    }
    if (type === 'bass'){
      return new Tone.MonoSynth({
        oscillator: { type: "sawtooth" },
        filter: { Q: 2, type: "lowpass", rolloff: -12 },
        envelope: { attack: 0.02, decay: 0.3, sustain: 0.6, release: 0.5 }
      }).toDestination();
    }
    return new Tone.Synth().toDestination();
  }

  async function start(opts){
    if (started) return;
    // init Tone
    await Tone.start();
    const mood = opts.moodInput.value;
    const userParams = moodToParams(mood);
    const bpm = parseInt(opts.tempoInput.value,10) || userParams.bpm;
    const bars = parseInt(opts.lengthSelect.value,10) || 16;
    const instrument = opts.instrumentSelect.value || userParams.instrument;

    Tone.Transport.bpm.value = bpm;
    // create synth and connect analyzer & recorder
    const mainSynth = createSynth(instrument);
    synths = [mainSynth];

    // Analyzer for visuals
    const analyser = new Tone.Analyser("waveform", 256);
    mainSynth.connect(analyser);
    analyzer = analyser;

    // Recorder
    recorder = new Tone.Recorder();
    // route a master output copy for recording
    Tone.Destination.connect(recorder);

    // generate sequence
    const notes = generateSequence(userParams, bars);
    // Create part
    let i = 0;
    seq = new Tone.Loop((time) => {
      const note = notes[i % notes.length];
      mainSynth.triggerAttackRelease(note, "8n", time);
      i++;
    }, "8n").start(0);

    Tone.Transport.start();
    recorder.start();
    started = true;

    // start visuals
    if (opts.canvas) {
      canvasEl = opts.canvas;
      startVisuals(analyzer, canvasEl);
    }

    if (opts.statusEl) opts.statusEl.textContent = "Playing — mood: " + mood + " (" + bpm + " BPM)";
  }

  async function stop(opts){
    if (!started) return;
    Tone.Transport.stop();
    seq.stop();
    // stop recorder and download buffer
    if (recorder) {
      const recording = await recorder.stop();
      // For demo: create local download link when user chooses to download explicitly; but we can also auto-download
      if (opts && opts.onRecording) opts.onRecording(recording);
    }
    // cleanup
    synths.forEach(s => s.dispose && s.dispose());
    synths = [];
    started = false;
    if (opts && opts.statusEl) opts.statusEl.textContent = "Stopped";
    stopVisuals();
  }

  // simple visual wrapper that reads analyzer and draws circles
  let visRAF = null;
  let isVisualRunning = false;

  function startVisuals(analyser, canvas){
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;
    isVisualRunning = true;

    function frame(){
      if (!isVisualRunning) return;
      const values = analyser.getValue();
      ctx.clearRect(0,0,canvas.width,canvas.height);
      // darkened backdrop so text remains visible - but we draw transparent, caller may set body background
      const base = 'rgba(0,0,0,0)';
      ctx.fillStyle = base;
      ctx.fillRect(0,0,canvas.width,canvas.height);

      // draw pulsating orange orbs
      const len = Math.min(32, values.length);
      for (let i=0;i<len;i++){
        const v = Math.abs(values[i]) * 2; // scale
        const x = (i / len) * canvas.width;
        const y = canvas.height/2 + (values[(i+5)%values.length]*canvas.height/3);
        const radius = Math.max(2, Math.abs(v) * 40);
        ctx.beginPath();
        const g = ctx.createRadialGradient(x, y, 0, x, y, radius*2);
        g.addColorStop(0, "rgba(255,140,0,0.9)");
        g.addColorStop(0.5, "rgba(255,180,100,0.35)");
        g.addColorStop(1, "rgba(255,140,0,0)");
        ctx.fillStyle = g;
        ctx.arc(x, y, radius, 0, Math.PI*2);
        ctx.fill();
      }
      visRAF = requestAnimationFrame(frame);
    }
    visRAF = requestAnimationFrame(frame);
  }

  function stopVisuals(){
    isVisualRunning = false;
    if (visRAF) cancelAnimationFrame(visRAF);
  }

  // public API
  function init(opts){
    const options = Object.assign({
      moodInput: null, tempoInput: null, lengthSelect: null,
      instrumentSelect: null, generateBtn: null, stopBtn: null,
      downloadBtn: null, statusEl: null, canvas: null
    }, opts);

    options.generateBtn.addEventListener('click', async () => {
      await start(options);
    });

    options.stopBtn.addEventListener('click', async () => {
      await stop({
        onRecording: async (blob) => {
          // store last recording to download if user clicks download
          window.lastRecording = blob;
        },
        statusEl: options.statusEl
      });
    });

    options.downloadBtn.addEventListener('click', async () => {
      if (window.lastRecording) {
        const url = URL.createObjectURL(window.lastRecording);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'sargam-mix.wav';
        document.body.appendChild(a);
        a.click();
        a.remove();
      } else {
        options.statusEl.textContent = 'No recording available — press Stop to finalize a recording.';
      }
    });

    // hook touch-friendly behavior
  }

  return { init, start, stop };
})();
