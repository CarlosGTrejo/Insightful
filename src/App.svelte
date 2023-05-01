<script>
  import {
    Header,
    //HeaderUtilities,
    //HeaderAction,
    //HeaderGlobalAction,
    SkipToContent,
    FileUploader,
    FileUploaderItem,
    SideNav,
    SideNavItems,
    SideNavLink,
    Content,
    Grid,
    Row,
    Column,
    Tile
  } from "carbon-components-svelte";
  import { onMount } from 'svelte';
  //import Help from "carbon-icons-svelte/lib/Help.svelte";

  let url = ``;
  onMount(() => url = window.location.href);

  //let open = false;
  let isSideNavOpen = false;
  let chapters = [];
  let title;

  let processed = false;
  let fileUploader;
  let file;
  let is_valid = true;
  let socket;
  let elapsed_time; // Used to measure perf
  let start_time;  // Used to measure perf
  let summary;
  let transcript;
  let data;

  function timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async function handleFileUpload(event) {
    file = event.detail[0];  // Get file from event
    if (file.size > 50_000_000) {
      await Promise.all([timeout(500)]) // Add a small delay to update file validity
      fileUploader.clearFiles()
      is_valid = false;
      return
    }
    is_valid = true;
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
    //height: 50vh;
  }

  .landing-page-text {
    display: grid;
    place-items: center left;
    height: 50vh;
  }

  h4 {
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
  <!--<HeaderUtilities>
    <HeaderAction bind:isOpen={open} icon={Help}>
    </HeaderAction>
  </HeaderUtilities>-->
</Header>

<!--<Modal passiveModal bind:open modalHeading="Welcome to Insightful" on:open on:close>
  <p>Insightful is a tool for transcribing and summarizing audio files. Upload an audio file to get started.</p>
  <p>Files may not be larger than 25 MB nor longer than 60 minutes.</p>
  <p>To view this window again, click the "Help" icon in the top-right of this page.</p>
</Modal>-->


{#if !processed}
    <Content>
      <Grid>
        <Row padding>
            <Column sm={4} md={8} lg={10}>
              <h1>Welcome to Insightful</h1>
              <p>A productivity-boosting application that uses AI technology to help people focus on the key points of an audio recording. It works for a variety of scenarios, such as lectures, speeches, and business meetings, by providing a summary, a complete transcript of the recording and the ability for users to focus and follow along while listening. Upload an audio file to get started.</p>
              <p>Files may not be larger than 25 MB nor longer than 60 minutes.</p>
            </Column>

            <Column sm={2} md={4} lg={5}>
              <FileUploader
                bind:this={fileUploader}
                labelTitle="Upload file"
                buttonLabel="Add file"
                labelDescription="Max file size is 50Mb. Only common audio files are accepted."
                accept={["audio/*"]}
                on:add={handleFileUpload}
              />
              {#if !is_valid}
                <FileUploaderItem
                  invalid
                  name={file.name}
                  errorSubject="File size exceeds 50Mb limit"
                  errorBody="Please select a new file."
                  status="edit"
                  on:delete={(e) => {is_valid=true}}
                />
              {/if}
            </Column>
        </Row>
      </Grid>
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
            <h4>Summary</h4>
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. At veniam, nesciunt nostrum qui quis provident veritatis minus deserunt voluptate sequi aperiam? Facere officia quam tenetur labore optio nam esse quae.</p>
          </Tile>
        </Column>
      </Row>
    </Grid>
  </Content>
{/if}
