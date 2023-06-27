<script lang="ts" setup>
import { ElCollapse, ElCollapseItem } from "element-plus";
import { ref } from "vue";
const activeName = ref("");
</script>

<template>
  <div class="content-wrapper general-padding">
    <h1>Ooops</h1>
    <div class="gps-header">
      <img
        src="/no-gps-icon.svg"
        alt="no gps icon"
      >
      <h3>Kein GPS verfügbar</h3>
    </div>

    <p>
      Dieses Hörstück wird dynamisch über deine GPS-Koordinaten generiert. Dazu
      benötigen wir deine Erlaubnis.
      <br>
      <br>
      Lade die Seite neu und erlaube Zugriff auf deine Position.
      <br>
      <br>

      Wenn du wieder auf diese Seite kommst, vergewissere dich, dass GPS in den
      <b>Einstellungen</b> aktiviert ist. Wie das geht, erfährst du hier:
    </p>

    <ElCollapse
      v-model="activeName"
      accordion
    >
      <ElCollapseItem
        title="Apple Geräte"
        name="1"
      >
        <div>
          <p>Ortungsdienste für deinen Browser einschalten:</p>
          <ol>
            <li>
              Gehe zu “Einstellungen” > “Datenschutz und Sicherheit” >
              “Ortungsdienste”.
            </li>
            <li>Vergewissere dich, dass die Ortungsdienste aktiviert sind.</li>
            <li>Scrolle nach unten zur gewünschten App.</li>
            <li>Tippe auf deinen Browser und wähle die Option: “Immer”</li>
          </ol>
        </div>
      </ElCollapseItem>
      <ElCollapseItem
        title="Android Geräte"
        name="2"
      >
        <div>
          <p>Ortungsdienste für deinen Browser einschalten:</p>
          <ol>
            <li>Öffnen Sie auf Ihrem Android-Gerät die Einstellungen</li>
            <li>Tippen Sie auf Standort App-Berechtigung.</li>
            <li>
              Tippen Sie auf die App, die Sie als Browser verwenden, z. B.
              Google Chrome
            </li>
            <li>Setzen Sie für diese App den Standortzugriff auf “Zulassen”</li>
          </ol>
        </div>
      </ElCollapseItem>
      <ElCollapseItem
        title="Desktop"
        name="3"
      >
        <div>
          <p>Ortungsdienste für deinen Browser einschalten:</p>
          <ol>
            <li>
              Öffnen Sie auf Ihrem Desktop-Gerät die Einstellungen des Browsers
            </li>
            <li>Suchen Sie nach Berechtigungen oder Privacy.</li>
            <li>
              Setzen Sie für diese Webseite den Standortzugriff auf “Zulassen”
            </li>
          </ol>
        </div>
      </ElCollapseItem>
    </ElCollapse>

    <p>
      Sollte es weiterhin Probleme geben, bitte schreibe uns an
      <a href="mailto:contact@gencaster.org?subject=Hello">contact@gencaster.org</a>.
    </p>
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/mixins.scss";
@import "@/assets/variables.scss";

.content-wrapper {
  max-width: $desktopMaxWidthText;
  max-width: $desktopMaxWidthText;
  padding-bottom: $playerBarHeight;
  margin: 0 auto;
}

h1 {
  text-align: center;
  margin-bottom: calc($mobilePadding * 2);
}

.gps-header {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background-color: $green-light;
  border: $lineThick solid $black;
  aspect-ratio: 3 / 2;
  max-width: 350px;
  border-radius: $borderRadius;
  gap: 10%;
  margin: 0 auto;
  margin-bottom: calc($mobilePadding * 3);

  @include onScreen("tablet-portrait-up") {
    margin-bottom: calc($mobilePadding * 6);
  }

  h3 {
    @include fontStyle("smallHeadline");
    font-weight: bold;
    margin: 0;
  }

  img {
    width: 35%;
  }
}
</style>
