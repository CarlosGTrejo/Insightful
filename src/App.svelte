<script>
  import {
    Header,
    HeaderUtilities,
    HeaderAction,
    HeaderGlobalAction,
    SkipToContent,
    FileUploader,
    SideNav,
    SideNavItems,
    SideNavLink,
    Content,
    Grid,
    Row,
    Column,
    Tile,
    Modal
  } from "carbon-components-svelte";
  import { onMount } from 'svelte';
  import Help from "carbon-icons-svelte/lib/Help.svelte";
  
  let url = ``;
  onMount(() => url = window.location.href);

  let open = true;
  let isSideNavOpen = false;
  let chapters = [];
  let title;

  let processed = false;
  let file;
  let socket;
  let elapsed_time; // Used to measure perf
  let start_time;  // Used to measure perf
  let summary;
  let transcript;
  let data;

  async function handleFileUpload(event) {
    file = event.detail[0];  // Get file from event

    // Send file if websocket is already open
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      if (url.includes('localhost')) {
        console.log('🧪 Development mode? Probably.')
        socket = new WebSocket("ws://localhost:8000/ws");
      } else {
        socket = new WebSocket("ws://localhost:8000/ws");  // TODO: Change this for production
      }


      // Send File
      socket.addEventListener("open", (event) => {
        start_time = performance.now();  // Start perf counter
        socket.send(file)  // Send file to server
        if (file.name === '!dev.mp3') {  // Used for testing purposes to avoid
          socket.send('dev/file')               // using up all of our deepgram credit
        } else {
          socket.send(file.type) // Send mimetype
        }
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
      data = JSON.parse(event.data);
      transcript = data.transcript;
      summary = data.summary;

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
  <HeaderUtilities>
    <HeaderAction bind:isOpen={open} icon={Help}>
    </HeaderAction>
  </HeaderUtilities>
</Header>

<Modal passiveModal bind:open modalHeading="Welcome to Insightful" on:open on:close>
  <p>
    Insightful is a tool for transcribing and summarizing audio files. Upload an audio 
    file to get started.
  </p>
  <p>Files may not be larger than 25 MB nor longer than 60 minutes.</p>
  <p>To view this window again, click the "Help" icon in the top-right of this page.</p>
</Modal>


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
