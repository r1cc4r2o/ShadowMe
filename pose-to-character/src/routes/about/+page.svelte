<script>
    import Navbar from '$lib/components/Navbar.svelte';
</script>

<Navbar showPlayPause={false}/>

<div class="p-10">
    <h1 class="text-2xl font-bold py-5">Authors</h1>
    <p class="py-2">
        This application was developed by:
    </p>
    <ul class="list-disc list-inside">
        <li class="py-2">
            Marco Garosi
            •
            <a href="https://www.github.com/marco-garosi" class="text-emerald-500">GitHub</a>
            •
            <a href="https://www.linkedin.com/in/marco-garosi/" class="text-emerald-500">LinkedIn</a>
            •
            <a href="https://www.marcogarosi.it" class="text-emerald-500">Website</a>
        </li>
        <li class="py-2">
            Riccardo Tedoldi
            •
            <a href="https://www.github.com/r1cc4r2o" class="text-emerald-500">GitHub</a>
            •
            <a href="#" class="text-emerald-500">LinkedIn</a>
        </li>
    </ul>
    <p class="py-2">
        We are two students at the University of Trento, pursuing a Master's Degree in "Artificial Intelligence Systems".
    </p>
    <p class="py-2">
        We worked on this project for the Computer Vision course, held by Prof. Nicola Conci and Dr. Giulia Martinelli.
    </p>
</div>