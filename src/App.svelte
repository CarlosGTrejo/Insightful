<script>
  import {
    Header,
    SkipToContent,
    FileUploader,
    SideNav,
    SideNavItems,
    SideNavLink,
    Content,
    Grid,
    Row,
    Column,
    Tile
  } from "carbon-components-svelte";

  let isSideNavOpen = false;
  let chapters = [];
  let title;

  let processed = false;
  let file;
  let socket;
  let transcript;
  let elapsed_time; // Used to measure perf
  let start_time;  // Used to measure perf

  async function handleFileUpload(event) {
    file = event.detail[0];  // Get file from event

    if (!socket || socket.readyState !== WebSocket.OPEN) {  // Open up a socket if there isn't one open already, then send file
      socket = new WebSocket("ws://localhost:8000/ws");

      socket.addEventListener("open", (event) => {
        start_time = performance.now();  // Start perf counter
        socket.send(file)  // Send file to server
      })

      // Error handling (log errors to console)
      socket.addEventListener("error", (event) => {
        console.error(event)
      })
    } else {
      socket.send(file);  // Send file if a socket is already opened
    }

    // Receive data from backend
    socket.addEventListener("message", (event) => {
      console.dir(event)
      transcript = event.data;

      const end_time = performance.now();  // Stop perf counter

      // Calculate processing time and log to console
      elapsed_time = Math.round(end_time - start_time);
      console.log(`%c ⏱️ Processing time: ${elapsed_time.toLocaleString("en-US")}ms`, 'background-color: yellow; color: black; font-weight: bold; font-size: 30px; font-family: "Ubuntu Mono", monospace, sans-serif')
      processed = true;  // File is done being processed, set to true so that transcript shows up.
    });
  }
</script>

<!-- Issues arose when main was styled as a whole. Each component is stylized inidividually as a result. -->
<style lang="scss">
  @import '@carbon/type';

  .file-uploader-wrapper { // Used to center FileUpload component
    display: grid;
    place-items: center;
    height: 90vh;
  }

  h1 {
    @include type-style('heading-01');
    // color: #6F6F6F;
  }
  p {
    @include type-style('body-02');
    margin-top: 1em;
  }
  audio {
    height: 2.5em;
    margin-top: 1em;
    min-width: 100%;
  }

</style>


<Header company="" platformName="Insightful" bind:isSideNavOpen>
  <svelte:fragment slot="skip-to-content">
    <SkipToContent />
  </svelte:fragment>
</Header>


{#if !processed}
    <Content>
      <div class="file-uploader-wrapper">
        <FileUploader
          labelTitle="Upload file"
          buttonLabel="Add file"
          labelDescription="Only audio files are accepted."
          accept={["audio/*"]}
          on:change={handleFileUpload}
        />
      </div>
    </Content>
{:else}
<!-- Add chapters to the side bar -->
  <SideNav bind:isOpen={isSideNavOpen}>
    <SideNavItems>
      {#each chapters as chapter}
        <SideNavLink text={chapter} />
      {/each}
    </SideNavItems>
  </SideNav>
  <Content>
    <Grid>
      <Row>
        <!-- Transcript + audio player -->
        <Column sm={2} md={8} lg={10}>
          <h1>{title}</h1>
          <audio controls src="{URL.createObjectURL(file)}"></audio>
          <p>{transcript ? transcript: 'No transcript available'}</p>
        </Column>
        <Column sm={1} md={4} lg={5}>
          <Tile>
            <h1>Summary</h1>
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. At veniam, nesciunt nostrum qui quis provident veritatis minus deserunt voluptate sequi aperiam? Facere officia quam tenetur labore optio nam esse quae.</p>
          </Tile>
        </Column>
      </Row>
    </Grid>
  </Content>
{/if}
