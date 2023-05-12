<script setup lang="ts">
defineProps({
  title: String
});
</script>

<template>
  <div class="end-screen">
    <div class="text">
      <h1> Das war {{ title }}</h1>
      <!-- <h1>The end</h1>
      <p>
        Drifter stands for many things: for a band, for a movie, for a ship, and for tourists who stagger through the
        world with a backpack. It stands for a driver with special skills and for a buoy floating aimlessly in shallow
        water. Drifter means many things, but mainly to travel to the edges of knowledge and never turn back.
      </p>
      <p>
        It is the first audioguide to dynamically cover 100% of the earth. It is currently in development, co-written
        by&nbsp;<em><a href="https://ralphtharayil.com/" target="_blank">Ralph Tharayil</a></em> and part of my augmented
        audio research. Sign up&nbsp;for the newsletter <a
          href="https://drifter.augmented.audio/"
          target="_blank"
        >here</a>.
      </p>
      <div class="block-image" title="Single Image">
        <div>
          <picture style="aspect-ratio: 1.74242 / 1;">
            <source
              media="(max-width: 400px)"
              srcset="https://cdn.sanity.io/images/29fiedpe/production/aafe73f1df498e3334d90be55f26906c42529760-2760x1584.png?w=400&amp;auto=format, https://cdn.sanity.io/images/29fiedpe/production/aafe73f1df498e3334d90be55f26906c42529760-2760x1584.png?w=800&amp;auto=format 2x"
            >
            <source
              media="(max-width: 799px)"
              srcset="https://cdn.sanity.io/images/29fiedpe/production/aafe73f1df498e3334d90be55f26906c42529760-2760x1584.png?w=800&amp;auto=format, https://cdn.sanity.io/images/29fiedpe/production/aafe73f1df498e3334d90be55f26906c42529760-2760x1584.png?w=1600&amp;auto=format 2x"
            >
            <source
              media="(max-width: 1200px)"
              srcset="https://cdn.sanity.io/images/29fiedpe/production/aafe73f1df498e3334d90be55f26906c42529760-2760x1584.png?w=1200&amp;auto=format, https://cdn.sanity.io/images/29fiedpe/production/aafe73f1df498e3334d90be55f26906c42529760-2760x1584.png?w=1600&amp;auto=format 2x"
            >
            <source
              media="(max-width: 1600px)"
              srcset="https://cdn.sanity.io/images/29fiedpe/production/aafe73f1df498e3334d90be55f26906c42529760-2760x1584.png?w=1600&amp;auto=format, https://cdn.sanity.io/images/29fiedpe/production/aafe73f1df498e3334d90be55f26906c42529760-2760x1584.png?w=2000&amp;auto=format 2x"
            >
            <source
              media="(min-width: 1601px)"
              srcset="https://cdn.sanity.io/images/29fiedpe/production/aafe73f1df498e3334d90be55f26906c42529760-2760x1584.png?w=2000&amp;auto=format, https://cdn.sanity.io/images/29fiedpe/production/aafe73f1df498e3334d90be55f26906c42529760-2760x1584.png?w=2500&amp;auto=format 2x"
            >
            <img
              src="https://cdn.sanity.io/images/29fiedpe/production/aafe73f1df498e3334d90be55f26906c42529760-2760x1584.png?w=800&amp;auto=format"
              loading="lazy" style="aspect-ratio: 1.74242 / 1;"
            >
          </picture>
        </div>
      </div>
      <p>
        Expected release of the first beta version will be around the summer of 2023. For more information on other
        augmented audio pieces, take a look at&nbsp;<a
          href="https://augmented.audio/"
          target="_blank"
        >augmented.audio</a>.
      </p>

      <div class="block-image" title="Single Image">
        <div>
          <picture style="aspect-ratio: 0.666667 / 1;">
            <source
              media="(max-width: 400px)"
              srcset="https://cdn.sanity.io/images/29fiedpe/production/d7a9525778e4f371c5910fb8a126f284f5d67856-1200x1800.jpg?w=400&amp;auto=format, https://cdn.sanity.io/images/29fiedpe/production/d7a9525778e4f371c5910fb8a126f284f5d67856-1200x1800.jpg?w=800&amp;auto=format 2x"
            >
            <source
              media="(max-width: 799px)"
              srcset="https://cdn.sanity.io/images/29fiedpe/production/d7a9525778e4f371c5910fb8a126f284f5d67856-1200x1800.jpg?w=800&amp;auto=format, https://cdn.sanity.io/images/29fiedpe/production/d7a9525778e4f371c5910fb8a126f284f5d67856-1200x1800.jpg?w=1600&amp;auto=format 2x"
            >
            <source
              media="(max-width: 1200px)"
              srcset="https://cdn.sanity.io/images/29fiedpe/production/d7a9525778e4f371c5910fb8a126f284f5d67856-1200x1800.jpg?w=1200&amp;auto=format, https://cdn.sanity.io/images/29fiedpe/production/d7a9525778e4f371c5910fb8a126f284f5d67856-1200x1800.jpg?w=1600&amp;auto=format 2x"
            >
            <source
              media="(max-width: 1600px)"
              srcset="https://cdn.sanity.io/images/29fiedpe/production/d7a9525778e4f371c5910fb8a126f284f5d67856-1200x1800.jpg?w=1600&amp;auto=format, https://cdn.sanity.io/images/29fiedpe/production/d7a9525778e4f371c5910fb8a126f284f5d67856-1200x1800.jpg?w=2000&amp;auto=format 2x"
            >
            <source
              media="(min-width: 1601px)"
              srcset="https://cdn.sanity.io/images/29fiedpe/production/d7a9525778e4f371c5910fb8a126f284f5d67856-1200x1800.jpg?w=2000&amp;auto=format, https://cdn.sanity.io/images/29fiedpe/production/d7a9525778e4f371c5910fb8a126f284f5d67856-1200x1800.jpg?w=2500&amp;auto=format 2x"
            >
            <img
              src="https://cdn.sanity.io/images/29fiedpe/production/d7a9525778e4f371c5910fb8a126f284f5d67856-1200x1800.jpg?w=800&amp;auto=format"
              loading="lazy" style="aspect-ratio: 0.666667 / 1;"
            >
          </picture>
        </div>
      </div>

      <p>
        Expected release of the first beta version will be around the summer of 2023. For more information on other
        augmented audio pieces, take a look at&nbsp;<a
          href="https://augmented.audio/"
          target="_blank"
        >augmented.audio</a>.
      </p> -->
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.end-screen {
  box-sizing: border-box;
  max-width: $desktopMaxWidthText;
  margin: 0 auto;

  img {
    width: 100%;
  }
}
</style>
