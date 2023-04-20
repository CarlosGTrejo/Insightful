<script>
  // UIShell (Time Frames/Chapters)
  import {
    Header,
    HeaderUtilities,
    HeaderGlobalAction,
    HeaderNav,
    HeaderNavItem,
    HeaderNavMenu,
    SideNav,
    SideNavItems,
    SideNavMenu,
    SideNavMenuItem,
    SideNavLink,
    SideNavDivider,
    SkipToContent,
    Content,
    Grid,
    Row,
    Column,
  } from "carbon-components-svelte";
  import { Help } from 'carbon-icons-svelte/lib/Help.svelte';

  import { Loading } from 'carbon-components-svelte';

  // Transcript
  import { TextArea } from "carbon-components-svelte";
  import { Button } from "carbon-components-svelte";

  // File Uploader
  import { FileUploader } from "carbon-components-svelte";

  // Tooltip (Resources)
  import { Tooltip } from "carbon-components-svelte";

  // Tile (Summary)
  import { Tile } from "carbon-components-svelte";

  // Search (Search Transcript)
  import { Modal } from "carbon-components-svelte";
  import { Search } from "carbon-components-svelte";
  


  let isSideNavOpen = false;
  let open = false;
  let readonly = true;

  let file;
  let socket;
  let transcript;
  let elapsed_time;
  let loading = false;
  let start_time;

  async function handleFileUpload(event) {
    file = event.target.files[0];
    loading = true;

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
  {/if}

  <!--UIShell (Time Frames/Chapters)-->
  <div>
    <Header company="Insightful" platformName="" bind:isSideNavOpen>
     <svelte:fragment slot="skip-to-content">
      <SkipToContent />
      </svelte:fragment>
      <HeaderUtilities>
        <HeaderGlobalAction aria-label="Help" icon={Help} />
      </HeaderUtilities>
    </Header> 

    <SideNav bind:isOpen={isSideNavOpen}>
      <SideNavItems>
       <SideNavLink text="chapter 1" />
       <SideNavLink text="chapter 2" />
       <SideNavLink text="chapter 3" />
      </SideNavItems>
    </SideNav>
  </div>

  <!--Transcript-->
  <div>
    <TextArea
     readonly
     labelText="Transcript"
     placeholder="The FitnessGram Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds."
    />
  </div>

  <!--File Uploader-->
  <div class = "fileUploader">
    <FileUploader
     multiple
     labelTitle="Upload a file"
     buttonLabel="Add files"
     labelDescription="Max file size is 25Mb. Supported file types are .flac and .mp3"
     accept={["audio/*"]}
     status="complete"
    />


    <FileUploaderItem bin:name="file" status="uploading" />
    <FileUploaderItem bin:name="file" status="complete" />
 
  </div>

  <!--Tile (Summary)-->
  <div class= "summary">
    <Tile>Summary</Tile>
  </div>

  <!--Tooltip (Resources)-->
  <div class= "resources">
    <Tooltip>
      <p>Learn More about Insightful.</p>
    </Tooltip>
  </div>

  <!--Transcript Search Bar-->
  <div class = "search-bar">
    <form action="https://www.google.com/search" method="get" class="search-bar">
     <Search size="lg" placeholder="Search Transcript" name="q"/>
    </form>
   
 
  </div>
</main>
