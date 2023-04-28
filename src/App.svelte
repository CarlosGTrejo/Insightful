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
  import { onMount } from 'svelte';

  let url = ``;
  onMount(() => url = window.location.href);

  let isSideNavOpen = false;
  let chapters = [];

  let file;
  let socket;
  let elapsed_time; // Used to measure perf
  let start_time;  // Used to measure perf
  let processed = false;

  let title;  // file name (not sure how to generate better title)
  let summary;  // audio summary
  let transcript;  // array of word and its timestamp
  let currentTime;  // audio element timestamp
  let data;  // Data received from the backend

  let currChapter = 0;

  async function handleFileUpload(event) {
    file = event.detail[0];  // Get file from event
    title = file.name;

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
        if (file.name === '!dev.mp3') {  // Send custom mimetype to flag server to use development mode.
          socket.send('dev/file')
        } else {
          socket.send(file.type) // Send normal mimetype
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
      transcript = data.transcript;  // Contains words and their timestamp [['word', 0.24, 0.89], ...]
      summary = (data.summary.map(dict => dict.summary)).join('\n\n');  // each summary is a dict: {summary: str, start_word: int, end_word: int}
      chapters = data.summary.map(summary_dict => (
          {
            chapter: summary_dict.summary.slice(0,23).trim() + '...',
            start: transcript[summary_dict.start_word][1],
            end: transcript[summary_dict.end_word-1][2]
          }
        ))
      console.log(chapters)
      const end_time = performance.now();  // Stop perf counter

      // Calculate processing time and log to console
      elapsed_time = Math.round(end_time - start_time);
      console.log(`%c ⏱️ Processing time: ${elapsed_time.toLocaleString("en-US")}ms`, 'background-color: yellow; color: black; font-weight: bold; font-size: 30px; font-family: "Ubuntu Mono", monospace, sans-serif')
      processed = true;  // File is done being processed, set to true so that transcript shows up.
    });
  }

  function jump(timestamp) {
    return function (e) {
      currentTime = timestamp;
    }
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
    max-width: 100%;
  }
  audio {
    height: 2.5em;
    margin-top: 1em;
    min-width: 100%;
  }
  .highlight {
    background-color: white;
    color: black;
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
  <SideNav bind:isOpen={isSideNavOpen}>
    <SideNavItems>
      {#each chapters as obj}
        <SideNavLink text={obj.chapter} isSelected={obj.start <= currentTime && currentTime < obj.end} on:click={jump(obj.start)}/>
      {/each}
    </SideNavItems>
  </SideNav>
  <Content>
    <Grid>
      <Row>
        <!-- Transcript + audio player -->
        <Column sm={2} md={8} lg={10}>
          <h1>{title}</h1>
          <audio controls src="{URL.createObjectURL(file)}" bind:currentTime></audio>
          <p>
            {#each transcript as [word, start_ts, end_ts]}
              <span class:highlight="{start_ts <= currentTime && currentTime < end_ts}" on:click={jump(start_ts)}>{word} </span>
            {/each}
          </p>
        </Column>
        <Column sm={1} md={4} lg={5}>
          <Tile>
            <h1>Summary</h1>
            <p>{summary}</p>
          </Tile>
        </Column>
      </Row>
    </Grid>
  </Content>
{/if}
