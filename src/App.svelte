<script>
  import {
    Header,
    SkipToContent,
    FileUploader,
  } from "carbon-components-svelte";

  let isSideNavOpen = false;

  let processed = false;
  let file;
  let socket;
  let transcript;
  let elapsed_time;
  let start_time;

  async function handleFileUpload(event) {
    console.dir(event)
    file = event.detail[0];

    if (!socket || socket.readyState !== WebSocket.OPEN) {
      socket = new WebSocket("ws://localhost:8000/ws");

      socket.addEventListener("open", (event) => {
        start_time = performance.now();  // Start perf counter
        socket.send(file)  // Send file to server
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
      transcript = event.data;

      const end_time = performance.now();

      // Calculate processing time
      elapsed_time = Math.round(end_time - start_time);
      console.log(`%c ⏱️ Processing time: ${elapsed_time.toLocaleString("en-US")}ms`, 'background-color: yellow; color: black; font-weight: bold; font-size: 30px; font-family: "Ubuntu Mono", monospace, sans-serif')
      processed = true;
    });
  }
</script>

<style>
  main {
    display: grid;
    place-items: center;
    height: 100vh;
    padding: auto;
  }
</style>

<Header company="IBM" platformName="Carbon Svelte" bind:isSideNavOpen>
  <svelte:fragment slot="skip-to-content">
    <SkipToContent />
  </svelte:fragment>
</Header>

<main>
  {#if !processed}
    <FileUploader
      labelTitle="Upload file"
      buttonLabel="Add file"
      labelDescription="Only audio files are accepted."
      accept={["audio/*"]}
      on:change={handleFileUpload}
    />
  {:else}
  <!-- TODO: Style transcript to display like in the Figma design and display "chapters" on the left side with times stamps (eg. use the variable "chapters" which will be an array that holds the chapter title and timestamp as a string, use simulated data if necessary for now) -->
    <p>{transcript ? transcript: 'No transcript available'}</p>
  {/if}
</main>
