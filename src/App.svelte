<script>
  import {
    Header,
    SkipToContent,
    FileUploader,
    SideNav,
    SideNavItems,
    SideNavLink,
  } from "carbon-components-svelte";

  let isSideNavOpen = false;
  let chapters
  let title
  //let chapters = ["FitnessGram","Pacer","Test"];
  //let title = "FitnessGram Pacer Test";

  let processed = false;
  let file;
  let socket;
  let transcript
  //let transcript = "The FitnessGram pacer test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly but gets faster each minute after you hear this signal bodeboop. A sing lap should be completed every time you hear this sound. ding Remember to run in a straight line and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark. Get ready!… Start. ding ";
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

<!-- Issues arose when main was styled as a whole. Each component is stylized inidividually as a result. -->
<!--<style>
  main {
    
  }
</style>
-->

<Header company="" platformName="Insightful" bind:isSideNavOpen>
  <svelte:fragment slot="skip-to-content">
    <SkipToContent />
  </svelte:fragment>
</Header>

<main>
  {#if !processed}
  <div style="display: grid; place-items: center; height: 100vh; padding: auto;">
    <FileUploader
      labelTitle="Upload file"
      buttonLabel="Add file"
      labelDescription="Only audio files are accepted."
      accept={["audio/*"]}
      on:change={handleFileUpload}
    />
  </div>
  {:else}
  <!-- TODO: Style transcript to display like in the Figma design and display "chapters" on the left side with times stamps (eg. use the variable "chapters" which will be an array that holds the chapter title and timestamp as a string, use simulated data if necessary for now) -->
  <!-- Chapters in the side navigation bar -->
    <SideNav bind:isOpen={isSideNavOpen}>
      <SideNavItems>
        {#each chapters as chapter}
          <SideNavLink text={chapter} />
        {/each}
      </SideNavItems>
    </SideNav>
  <!-- Transcript, as well as generated title -->
    <div style="display: grid; place-items: start left; color:#6f6f6f; padding-left:304px; padding-right:32vw; padding-top: 100px;">
      <p><strong>{title}</strong></p>
      <p>{transcript ? transcript: 'No transcript available'}</p>
    </div>
  {/if}
</main>
