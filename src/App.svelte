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

  let url = ``;
  onMount(() => url = window.location.href);

  //let open = false;
  let isSideNavOpen = false;
  let chapters = [];

  let processed = false;
  let fileUploader;
  let file;
  let is_valid = true;
  let socket;
  let elapsed_time; // Used to measure perf
  let start_time;  // Used to measure perf

  let title;  // file name (not sure how to generate better title)
  let summary;  // audio summary
  let transcript;  // array of word and its timestamp
  let currentTime;  // audio element timestamp
  let data;  // Data received from the backend

  let currChapter = 0;

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
      summary = data.openai_summary ? data.openai_summary : (data.summary.map(dict => dict.summary)).join('\n\n');  // each summary is a dict: {summary: str, start_word: int, end_word: int}
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

<style lang="scss">
  @import '@carbon/type';

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
