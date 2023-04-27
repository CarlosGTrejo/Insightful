<script>
  import { Loading } from 'carbon-components-svelte';

  let file;
  let socket;
  let transcript;
  let elapsed_time;
  let loading = false;
  let start_time;
  let data;
  let summary;

  async function handleFileUpload(event) {
    file = event.target.files[0];
    loading = true;


    // Send File
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      socket = new WebSocket("ws://localhost:8000/ws");

      socket.addEventListener("open", (event) => {
        start_time = performance.now();  // Start perf counter
        socket.send(file)  // Send file to server
        if (file.name === '!dev') {  // Used for testing purposes to avoid
          socket.send('dev/file')               // using up all of our deepgram credit
        } else {
          socket.send(file.type) // Send mimetype
        }
      })

      // Error handling
      socket.addEventListener("error", (event) => {
        console.error(event)
      })
    } else {
      socket.send(file);  // Send file if socket is open already
    }


    // Receive data
    socket.addEventListener("message", (event) => {
      console.dir(event)
      data = JSON.parse(event.data);
      transcript = data.transcript;
      summary = data.summary;

      loading = false
      const end_time = performance.now();

      // Calculate processing time
      elapsed_time = Math.round(end_time - start_time);
      console.log(`%c ⏱️ Processing time: ${elapsed_time.toLocaleString("en-US")}ms`, 'background-color: yellow; color: black; font-weight: bold; font-size: 30px; font-family: "Ubuntu Mono", monospace, sans-serif')
    });
  }
</script>

<main>
  <input type="file" accept="audio/*" on:change={handleFileUpload} />
  {#if loading}
    <Loading />
  {:else}
    <p>{transcript ? transcript: 'No transcript available'}</p>
    <p>{summary ? summary: 'No summary available'}</p>
  {/if}
</main>
