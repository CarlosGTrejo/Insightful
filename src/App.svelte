<!-- Sends audio file to backend for processing then displays the option to download it when it receives it back. -->
<script>
  let file;
  let socket;
  let audio_file;
  let elapsed_time;

  async function handleFileUpload(event) {
    file = event.target.files[0];

    if (!socket || socket.readyState !== WebSocket.OPEN) {
      socket = new WebSocket("ws://localhost:8000/ws");
    }

    socket.binaryType = "arraybuffer";

    socket.addEventListener("open", (event) => {
      socket.send(file);
    });
    // Count processing time after file is sent.
    const start_time = performance.now();

    socket.addEventListener("message", (event) => {
      audio_file = new Blob([event.data], { type: "audio/mpeg" });
      const end_time = performance.now();
      // Calculate processing time
      elapsed_time = Math.round(end_time - start_time);
    });
  }
</script>

<main>
  <input type="file" accept="audio/mpeg" on:change={handleFileUpload} />
  {#if audio_file}
    <p>Processing Time: {elapsed_time}ms</p>
    <a href={URL.createObjectURL(audio_file)} download="audio.mp3"
      >Download Processed Audio</a
    >
  {/if}
</main>
