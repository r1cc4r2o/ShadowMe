<script>
    import PlayPause from "$lib/components/PlayPause.svelte";

    export let showPlayPause = true;
    export let pause = false;
    let source = pause ? '/play.png' : '/pause.png';
</script>

<nav
    class="bg-emerald-100 text-emerald-600 border-gray-200 dark:bg-emerald-500 dark:text-emerald-950 fixed bottom-0 w-full"
>
    <div
        class="max-w-screen-xl flex flex-wrap items-center justify-center mx-auto p-4"
    >
        <a href="/" class="flex items-center mx-5" target="_self">
            <img
                src="/icon.png"
                class="h-8 mr-3"
                alt="Human in pose"
            />

            <span
                class="self-center text-2xl font-semibold hidden md:block"
            >
                ShadowMe
            </span>
        </a>

        <a href="/about" id="about-button" class="flex items-center mx-5" target="_self">
            <img
                src="/info.png"
                class="h-6 mr-3"
                alt="About"
            />
        </a>

        {#if showPlayPause}
            <span class="mx-5">
                <PlayPause src={source}/>
            </span>
        {/if}
    </div>
</nav>
